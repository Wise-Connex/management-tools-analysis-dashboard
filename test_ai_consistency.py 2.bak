#!/usr/bin/env python3
"""
Test script to verify AI query generation consistency across different tool-source combinations.
This will test the improved prompt engineering to ensure all 7 sections are generated consistently.
"""

import sys
import os
import asyncio
import json
from datetime import datetime
from pathlib import Path

# Add the dashboard_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

from key_findings.key_findings_service import get_key_findings_service
from database import get_database_manager
from config import get_config


async def test_ai_consistency():
    """Test AI query generation consistency across different tool-source combinations."""

    print("🧪 Testing AI Query Generation Consistency")
    print("=" * 60)

    # Test combinations - start with a few key ones
    test_combinations = [
        ("Calidad Total", ["Google Trends"], "es"),
        ("Benchmarking", ["Google Trends"], "es"),
        ("Six Sigma", ["Google Trends"], "es"),
        ("Calidad Total", ["Google Books"], "es"),
        ("Lean Manufacturing", ["Google Trends"], "es"),
    ]

    results = []

    config = get_config()
    db_manager = get_database_manager()
    key_findings_service = get_key_findings_service(
        db_manager=db_manager,
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
        config={
            "max_retries": 3,
            "enable_pca_emphasis": True,
            "confidence_threshold": 0.7,
        },
    )

    for tool_name, selected_sources, language in test_combinations:
        print(f"\n🔍 Testing: {tool_name} + {selected_sources[0]} ({language})")

        try:
            result = await key_findings_service.generate_key_findings(
                tool_name=tool_name,
                selected_sources=selected_sources,
                language=language,
                force_refresh=True,  # Force fresh generation
                source_display_names=selected_sources,
            )

            if result.get("success") and result.get("data"):
                data = result["data"]

                # Check all 7 sections
                expected_sections = [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "strategic_synthesis",
                    "conclusions",
                ]

                section_status = {}
                total_chars = 0

                for section in expected_sections:
                    content = data.get(section, "")
                    char_count = len(str(content))
                    is_present = char_count > 50  # Reasonable minimum

                    section_status[section] = {
                        "present": is_present,
                        "characters": char_count,
                        "preview": str(content)[:100] + "..." if content else "EMPTY",
                    }
                    total_chars += char_count

                all_present = all(
                    status["present"] for status in section_status.values()
                )

                test_result = {
                    "tool": tool_name,
                    "source": selected_sources[0],
                    "language": language,
                    "success": True,
                    "all_sections_present": all_present,
                    "sections": section_status,
                    "total_characters": total_chars,
                    "response_time": result.get("response_time_ms", 0),
                    "confidence_score": data.get("confidence_score", 0),
                    "model_used": data.get("model_used", "unknown"),
                }

                print(
                    f"   ✅ Success: {all_present} | {total_chars:,} chars | {result.get('response_time_ms', 0)}ms"
                )

                if not all_present:
                    missing = [
                        s
                        for s, status in section_status.items()
                        if not status["present"]
                    ]
                    print(f"   ⚠️  Missing sections: {', '.join(missing)}")

            else:
                test_result = {
                    "tool": tool_name,
                    "source": selected_sources[0],
                    "language": language,
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                }
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")

            results.append(test_result)

        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            results.append(
                {
                    "tool": tool_name,
                    "source": selected_sources[0],
                    "language": language,
                    "success": False,
                    "error": str(e),
                }
            )

    # Generate summary report
    print(f"\n📊 Test Summary")
    print("=" * 60)

    successful_tests = [r for r in results if r.get("success")]
    failed_tests = [r for r in results if not r.get("success")]
    complete_tests = [r for r in successful_tests if r.get("all_sections_present")]

    print(f"Total tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Complete (all 7 sections): {len(complete_tests)}")
    print(f"Success rate: {len(successful_tests) / len(results) * 100:.1f}%")
    print(f"Completeness rate: {len(complete_tests) / len(results) * 100:.1f}%")

    if successful_tests:
        avg_response_time = sum(
            r.get("response_time", 0) for r in successful_tests
        ) / len(successful_tests)
        avg_chars = sum(r.get("total_characters", 0) for r in successful_tests) / len(
            successful_tests
        )
        avg_confidence = sum(
            r.get("confidence_score", 0) for r in successful_tests
        ) / len(successful_tests)

        print(f"\nPerformance Metrics:")
        print(f"Average response time: {avg_response_time:.0f}ms")
        print(f"Average content length: {avg_chars:,.0f} characters")
        print(f"Average confidence: {avg_confidence:.2f}")

    # Save detailed results
    output_file = f"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/ai_analysis_exports/consistency_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    detailed_results = {
        "test_metadata": {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "success_rate": len(successful_tests) / len(results) * 100,
            "completeness_rate": len(complete_tests) / len(results) * 100,
        },
        "summary": {
            "successful": len(successful_tests),
            "failed": len(failed_tests),
            "complete": len(complete_tests),
        },
        "performance": {
            "avg_response_time": avg_response_time if successful_tests else 0,
            "avg_content_length": avg_chars if successful_tests else 0,
            "avg_confidence": avg_confidence if successful_tests else 0,
        },
        "results": results,
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(detailed_results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Detailed results saved to: {output_file}")

    # Return success if most tests passed
    success_rate = len(successful_tests) / len(results)
    completeness_rate = len(complete_tests) / len(results)

    if success_rate >= 0.8 and completeness_rate >= 0.7:
        print(f"\n🎉 Overall Result: SUCCESS")
        print(f"   Success rate: {success_rate * 100:.1f}% (target: 80%)")
        print(f"   Completeness rate: {completeness_rate * 100:.1f}% (target: 70%)")
        return True
    else:
        print(f"\n⚠️  Overall Result: NEEDS IMPROVEMENT")
        print(f"   Success rate: {success_rate * 100:.1f}% (target: 80%)")
        print(f"   Completeness rate: {completeness_rate * 100:.1f}% (target: 70%)")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_ai_consistency())
    sys.exit(0 if success else 1)
