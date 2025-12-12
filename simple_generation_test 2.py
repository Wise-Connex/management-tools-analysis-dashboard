#!/usr/bin/env python3
"""
Simple test for Calidad Total analysis generation
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.key_findings.key_findings_service import get_key_findings_service


async def generate_calidad_total_analyses():
    """Generate Calidad Total analyses for requested combinations."""
    print("🚀 Calidad Total Analysis Generation")
    print("=" * 60)

    try:
        # Initialize services
        db_manager = get_precomputed_db_manager()
        key_findings_service = get_key_findings_service()

        # Define combinations to generate
        combinations = [
            {
                "tool": "Calidad Total",
                "sources": ["Google Trends"],
                "language": "es",
                "description": "Single-source analysis",
            },
            {
                "tool": "Calidad Total",
                "sources": [
                    "Google Trends",
                    "Google Books",
                    "Bain Usability",
                    "Bain Satisfaction",
                    "Crossref",
                ],
                "language": "es",
                "description": "Multi-source (all 5 sources)",
            },
            {
                "tool": "Calidad Total",
                "sources": ["Google Books", "Bain Satisfaction"],
                "language": "es",
                "description": "Multi-source (2 specific sources)",
            },
        ]

        results = []

        for i, combo in enumerate(combinations, 1):
            print(
                f"\n{i}. {combo['description']}: {combo['tool']} + {combo['sources']} ({combo['language']})"
            )

            try:
                # Generate analysis
                start_time = time.time()
                result = await key_findings_service.generate_key_findings(
                    tool_name=combo["tool"],
                    selected_sources=combo["sources"],
                    language=combo["language"],
                    force_refresh=True,
                )
                generation_time = time.time() - start_time

                if result["success"]:
                    print(f"✅ Generated successfully in {generation_time:.2f}s")

                    # Store in database
                    storage_result = db_manager.store_precomputed_analysis(
                        combination_hash=db_manager.generate_combination_hash(
                            tool_name=combo["tool"],
                            selected_sources=combo["sources"],
                            language=combo["language"],
                        ),
                        tool_name=combo["tool"],
                        selected_sources=combo["sources"],
                        language=combo["language"],
                        analysis_data=result.get("data", {}),
                    )

                    if storage_result:
                        print(f"✅ Stored in database successfully!")
                        results.append(
                            {
                                "combination": combo,
                                "success": True,
                                "generation_time": generation_time,
                                "storage_success": True,
                            }
                        )
                    else:
                        print(f"⚠️ Generated but storage failed")
                        results.append(
                            {
                                "combination": combo,
                                "success": True,
                                "generation_time": generation_time,
                                "storage_success": False,
                            }
                        )
                else:
                    print(
                        f"❌ Generation failed: {result.get('error', 'Unknown error')}"
                    )
                    results.append(
                        {
                            "combination": combo,
                            "success": False,
                            "error": result.get("error", "Unknown error"),
                        }
                    )

            except Exception as e:
                print(f"❌ Error processing combination: {e}")
                results.append(
                    {"combination": combo, "success": False, "error": str(e)}
                )

        # Summary
        print(f"\n{'=' * 60}")
        print("📊 GENERATION SUMMARY")
        print(f"{'=' * 60}")

        successful = sum(1 for r in results if r["success"])
        total = len(results)

        print(f"Total combinations processed: {total}")
        print(f"Successful generations: {successful}")
        print(f"Success rate: {successful / total * 100:.1f}%")

        for i, result in enumerate(results, 1):
            combo = result["combination"]
            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"

            print(f"\n{i}. {combo['description']} - {status}")

            if result["success"]:
                if result.get("storage_success"):
                    print(f"   ✅ Generated and stored successfully")
                else:
                    print(f"   ⚠️ Generated but storage failed")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown error')}")

        print(
            f"\\n🎯 Overall Status: {'✅ ALL COMBINATIONS SUCCESSFUL' if successful == total else '⚠️ SOME COMBINATIONS FAILED'}"
        )

        return results

    except Exception as e:
        print(f"❌ Overall test failed: {e}")
        import traceback

        traceback.print_exc()
        return []


if __name__ == "__main__":
    asyncio.run(generate_calidad_total_analyses())
