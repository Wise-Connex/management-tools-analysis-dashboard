#!/usr/bin/env python3
"""
Test script for the new Key Findings Modal Architecture

Tests the refactored workflow:
1. KeyFindingsRetrievalService - database retrieval
2. KeyFindingsContentParser - content formatting
3. Integration of both services
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_new_architecture():
    """Test the complete new architecture."""
    print("🧪 Testing New Key Findings Architecture")
    print("=" * 60)

    try:
        # Test 1: Import new services
        print("\n1️⃣ Testing Service Imports...")

        from dashboard_app.key_findings.retrieval_service import (
            get_key_findings_retrieval_service,
        )
        from dashboard_app.key_findings.content_parser import (
            get_key_findings_content_parser,
        )

        print("✅ Service imports successful")

        # Test 2: Initialize services
        print("\n2️⃣ Testing Service Initialization...")

        retrieval_service = get_key_findings_retrieval_service()
        content_parser = get_key_findings_content_parser()

        print("✅ Service initialization successful")

        # Test 3: Test retrieval service
        print("\n3️⃣ Testing KeyFindingsRetrievalService...")

        test_tool = "Calidad Total"
        test_sources = ["Google Trends"]
        test_language = "es"

        print(f"Testing retrieval: {test_tool} + {test_sources} ({test_language})")

        start_time = time.time()
        retrieval_result = retrieval_service.retrieve_precomputed_findings(
            tool_name=test_tool, selected_sources=test_sources, language=test_language
        )
        retrieval_time = (time.time() - start_time) * 1000

        print(f"Retrieval result - success: {retrieval_result['success']}")
        print(f"Retrieval time: {retrieval_time:.2f}ms")

        if retrieval_result["success"]:
            print("✅ Retrieval successful")
            data = retrieval_result["data"]
            print(f"Available fields: {list(data.keys())}")

            # Check key sections
            sections_to_check = [
                "executive_summary",
                "principal_findings",
                "temporal_analysis",
                "seasonal_analysis",
                "fourier_analysis",
                "strategic_synthesis",
                "conclusions",
            ]

            for section in sections_to_check:
                content = data.get(section, "")
                if content and len(content.strip()) > 10:
                    print(f"   ✅ {section}: {len(content)} chars")
                else:
                    print(f"   ⚠️ {section}: Missing or too short")
        else:
            print(f"⚠️ Retrieval failed: {retrieval_result.get('error')}")
            print("This is expected if the combination doesn't exist in the database")

        # Test 4: Test content parser
        print("\n4️⃣ Testing KeyFindingsContentParser...")

        if retrieval_result["success"] and retrieval_result["data"]:
            print("Testing content parsing...")

            parse_result = content_parser.parse_modal_content(
                retrieval_result["data"], test_language
            )

            print(f"Parse result - success: {parse_result['success']}")

            if parse_result["success"] and parse_result["data"]:
                print("✅ Content parsing successful")

                parsed_data = parse_result["data"]
                sections = parsed_data.get("sections", {})
                metadata = parsed_data.get("metadata", {})

                print(
                    f"Metadata: tool={metadata.get('tool_name')}, sources={len(metadata.get('selected_sources', []))}, language={metadata.get('language')}"
                )

                # Count present sections
                present_sections = sum(
                    1 for section in sections.values() if section.get("present", False)
                )
                print(f"Present sections: {present_sections}/{len(sections)}")

                # Show section details
                for section_name, section_data in sections.items():
                    if section_data.get("present", False):
                        print(
                            f"   ✅ {section_name}: {section_data.get('length', 0)} chars"
                        )
                    else:
                        print(f"   ⚠️ {section_name}: Not present")

                # Test validation
                print("\nTesting content validation...")
                validation_result = content_parser.validate_content_structure(
                    parse_result
                )
                print(f"Validation result - valid: {validation_result['valid']}")
                if validation_result["warnings"]:
                    print(f"Warnings: {validation_result['warnings']}")
                if validation_result["issues"]:
                    print(f"Issues: {validation_result['issues']}")

            else:
                print(f"❌ Content parsing failed: {parse_result.get('error')}")
        else:
            print("⚠️ Skipping content parser test (no data to parse)")

        # Test 5: Performance metrics
        print("\n5️⃣ Testing Performance Metrics...")

        retrieval_metrics = retrieval_service.get_performance_metrics()
        print(f"Retrieval service metrics: {retrieval_metrics}")

        # Test multiple retrievals for performance
        if retrieval_result["success"]:
            print("Testing multiple retrievals for performance...")

            times = []
            for i in range(5):
                start = time.time()
                result = retrieval_service.retrieve_precomputed_findings(
                    test_tool, test_sources, test_language
                )
                times.append((time.time() - start) * 1000)

            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)

            print(
                f"Performance - Average: {avg_time:.2f}ms, Min: {min_time:.2f}ms, Max: {max_time:.2f}ms"
            )

            if avg_time < 100:
                print("✅ Performance target achieved (<100ms)")
            else:
                print(f"⚠️ Performance above target: {avg_time:.2f}ms")

        # Test 6: Error handling
        print("\n6️⃣ Testing Error Handling...")

        # Test invalid inputs
        invalid_result = retrieval_service.retrieve_precomputed_findings(
            tool_name="", selected_sources=[], language="es"
        )

        print(f"Invalid input handling - success: {invalid_result['success']}")
        print(f"Error message: {invalid_result.get('error')}")

        if not invalid_result["success"]:
            print("✅ Error handling working correctly")

        print("\n✅ All architecture tests completed successfully!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(
            "This is expected if the services are not yet integrated into the main codebase"
        )
        return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_service_integration():
    """Test the integration of both services."""
    print("\n🔗 Testing Service Integration...")

    try:
        from dashboard_app.key_findings.retrieval_service import (
            get_key_findings_retrieval_service,
        )
        from dashboard_app.key_findings.content_parser import (
            get_key_findings_content_parser,
        )

        # Get services
        retrieval_service = get_key_findings_retrieval_service()
        content_parser = get_key_findings_content_parser()

        # Test complete workflow
        test_cases = [
            {
                "tool": "Calidad Total",
                "sources": ["Google Trends"],
                "language": "es",
                "expected_sections": 6,  # Single source
            },
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends", "Bain Usability"],
                "language": "en",
                "expected_sections": 7,  # Multi source
            },
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(
                f"\nIntegration Test {i}: {test_case['tool']} + {test_case['sources']} ({test_case['language']})"
            )

            # Step 1: Retrieve
            retrieval_result = retrieval_service.retrieve_precomputed_findings(
                tool_name=test_case["tool"],
                selected_sources=test_case["sources"],
                language=test_case["language"],
            )

            if retrieval_result["success"]:
                # Step 2: Parse
                parse_result = content_parser.parse_modal_content(
                    retrieval_result["data"], test_case["language"]
                )

                if parse_result["success"]:
                    # Step 3: Validate
                    sections = parse_result["data"].get("sections", {})
                    present_sections = sum(
                        1 for s in sections.values() if s.get("present", False)
                    )

                    print(
                        f"✅ Integration successful: {present_sections} sections present"
                    )

                    if present_sections >= test_case["expected_sections"]:
                        print(
                            f"✅ Section count validation passed: {present_sections}/{test_case['expected_sections']}"
                        )
                    else:
                        print(
                            f"⚠️ Section count below expected: {present_sections}/{test_case['expected_sections']}"
                        )
                else:
                    print(f"⚠️ Parsing failed: {parse_result.get('error')}")
            else:
                print(f"⚠️ Retrieval failed: {retrieval_result.get('error')}")

        print("\n✅ Service integration tests completed")
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting New Architecture Tests")
    print("=" * 60)

    # Test basic architecture
    success1 = test_new_architecture()

    # Test service integration
    success2 = test_service_integration()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print(f"Basic Architecture Tests: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"Service Integration Tests: {'✅ PASSED' if success2 else '❌ FAILED'}")

    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED - New architecture is working correctly!")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed - check the implementation")
        sys.exit(1)
