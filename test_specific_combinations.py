#!/usr/bin/env python3
"""
Simple script to generate Calidad Total content for specific source combinations.
Runs the mandatory live AI query for both single and multi-source scenarios.
"""

import os
import sys
import asyncio
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set API key
os.environ["GROQ_API_KEY"] = "GROQ_API_KEY_PLACEHOLDER"

from mandatory_live_ai_query import send_mandatory_live_ai_query
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


async def generate_specific_combinations():
    """Generate content for specific Calidad Total combinations."""

    print("🚀 GENERATING CALIDAD TOTAL CONTENT - SPECIFIC COMBINATIONS")
    print("=" * 70)

    # Initialize database manager
    db_manager = get_precomputed_db_manager()

    # Define the combinations we want to test
    combinations = [
        {
            "name": "Calidad Total + Google Trends (Single Source)",
            "tool": "Calidad Total",
            "sources": ["Google Trends"],
            "language": "es",
            "expected_sections": 7,  # Single source: 7 sections
        },
        {
            "name": "Calidad Total + All 5 Sources (Multi Source)",
            "tool": "Calidad Total",
            "sources": [
                "Google Trends",
                "Bain Usability",
                "Bain Satisfaction",
                "Crossref",
                "Google Books",
            ],
            "language": "es",
            "expected_sections": 9,  # Multi source: 9 sections (including NEW seasonal_analysis)
        },
    ]

    results = {}

    for combo in combinations:
        print(f"\n🔍 Processing: {combo['name']}")
        print("-" * 60)

        try:
            # Generate combination hash to check existing content
            combination_hash = db_manager.generate_combination_hash(
                combo["tool"], combo["sources"], combo["language"]
            )
            print(f"Combination Hash: {combination_hash}")

            # Check existing content
            existing = db_manager.get_combination_by_hash(combination_hash)
            if existing:
                print("📊 Existing content found, analyzing...")
                completeness = analyze_content_completeness(
                    existing, combo["expected_sections"]
                )
                print(
                    f"Current completeness: {completeness['complete_sections']}/{completeness['total_sections']} sections"
                )

                if completeness["is_complete"]:
                    print("✅ Content already complete, skipping generation")
                    results[combo["name"]] = {
                        "status": "skipped",
                        "reason": "already_complete",
                    }
                    continue
                else:
                    print(f"⚠️ Content incomplete, regenerating...")
                    print(
                        f"Missing sections: {', '.join(completeness['missing_sections'])}"
                    )
            else:
                print("❌ No existing content found, generating new...")

            # Run the mandatory live AI query
            print(f"🤖 Running mandatory live AI query...")
            print(f"Tool: {combo['tool']}")
            print(f"Sources: {', '.join(combo['sources'])}")
            print(f"Language: {combo['language']}")

            # Modify the global variables in the mandatory query module
            import mandatory_live_ai_query as mq

            mq.TOOL_NAME = combo["tool"]
            mq.SELECTED_SOURCES = combo["sources"]
            mq.LANGUAGE = combo["language"]

            # Run the query
            success = await send_mandatory_live_ai_query()

            if success:
                print("✅ Live AI query completed successfully")

                # Verify the new content
                new_content = db_manager.get_combination_by_hash(combination_hash)
                if new_content:
                    completeness = analyze_content_completeness(
                        new_content, combo["expected_sections"]
                    )
                    print(
                        f"New content completeness: {completeness['complete_sections']}/{completeness['total_sections']} sections"
                    )

                    if completeness["is_complete"]:
                        print("🎉 NEW CONTENT IS COMPLETE!")
                        results[combo["name"]] = {
                            "status": "success",
                            "sections_complete": completeness["complete_sections"],
                            "total_sections": completeness["total_sections"],
                            "content_length": sum(
                                len(str(new_content.get(section, "")))
                                for section in completeness["all_sections"]
                            ),
                        }
                    else:
                        print("⚠️ New content still incomplete")
                        results[combo["name"]] = {
                            "status": "partial_success",
                            "sections_complete": completeness["complete_sections"],
                            "total_sections": completeness["total_sections"],
                            "missing_sections": completeness["missing_sections"],
                        }
                else:
                    print("❌ No content found after generation")
                    results[combo["name"]] = {
                        "status": "failed",
                        "reason": "no_content_after_generation",
                    }
            else:
                print("❌ Live AI query failed")
                results[combo["name"]] = {
                    "status": "failed",
                    "reason": "ai_query_failed",
                }

        except Exception as e:
            print(f"❌ Error processing {combo['name']}: {e}")
            results[combo["name"]] = {
                "status": "failed",
                "reason": "exception",
                "error": str(e),
            }

    return results


def analyze_content_completeness(content: dict, expected_sections: int) -> dict:
    """Analyze content completeness based on new validation requirements."""

    if expected_sections == 7:  # Single source
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]
    else:  # Multi source (9 sections)
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "pca_analysis",
            "heatmap_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

    complete_sections = 0
    missing_sections = []
    section_details = {}

    for section in required_sections:
        section_content = content.get(section, "")
        has_content = bool(section_content and len(str(section_content)) > 50)

        section_details[section] = {
            "present": has_content,
            "length": len(str(section_content)) if section_content else 0,
        }

        if has_content:
            complete_sections += 1
        else:
            missing_sections.append(section)

    return {
        "is_complete": complete_sections == len(required_sections),
        "complete_sections": complete_sections,
        "total_sections": len(required_sections),
        "missing_sections": missing_sections,
        "section_details": section_details,
        "all_sections": required_sections,
    }


async def main():
    """Main function to run the specific combinations."""

    try:
        results = await generate_specific_combinations()

        print("\n" + "=" * 70)
        print("📊 FINAL RESULTS")
        print("=" * 70)

        for combo_name, result in results.items():
            print(f"\n{combo_name}:")
            print(f"  Status: {result['status']}")

            if result["status"] == "success":
                print(
                    f"  ✅ Complete sections: {result['sections_complete']}/{result['total_sections']}"
                )
                print(f"  📊 Content length: {result['content_length']} chars")
            elif result["status"] == "partial_success":
                print(
                    f"  ⚠️ Complete sections: {result['sections_complete']}/{result['total_sections']}"
                )
                print(f"  ❌ Missing: {', '.join(result['missing_sections'])}")
            else:
                print(f"  ❌ Reason: {result['reason']}")
                if "error" in result:
                    print(f"  🔍 Error: {result['error']}")

        # Summary
        successful = sum(1 for r in results.values() if r["status"] == "success")
        total = len(results)

        print(f"\n📈 SUMMARY: {successful}/{total} combinations successfully completed")

        if successful == total:
            print("🎉 ALL COMBINATIONS COMPLETE - READY FOR BATCH PROCESSING!")
        else:
            print("⚠️ Some combinations need attention before batch processing")

    except Exception as e:
        print(f"❌ Main execution failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
