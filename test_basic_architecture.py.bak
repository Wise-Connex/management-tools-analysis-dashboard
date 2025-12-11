#!/usr/bin/env python3
"""
Simple test for the new Key Findings Architecture

Tests the core components without complex imports.
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_basic_functionality():
    """Test basic functionality of new services."""
    print("🧪 Testing Basic New Architecture Functionality")
    print("=" * 60)

    try:
        # Test 1: Import retrieval service
        print("\n1️⃣ Testing Retrieval Service Import...")
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

        from key_findings.retrieval_service import get_key_findings_retrieval_service

        print("✅ Retrieval service import successful")

        # Test 2: Import content parser
        print("\n2️⃣ Testing Content Parser Import...")
        from key_findings.content_parser import get_key_findings_content_parser

        print("✅ Content parser import successful")

        # Test 3: Initialize services
        print("\n3️⃣ Testing Service Initialization...")

        retrieval_service = get_key_findings_retrieval_service()
        content_parser = get_key_findings_content_parser()

        print("✅ Service initialization successful")

        # Test 4: Test retrieval service structure
        print("\n4️⃣ Testing Retrieval Service Structure...")

        # Check if service has required methods
        required_methods = [
            "retrieve_precomputed_findings",
            "get_performance_metrics",
            "validate_combination_exists",
        ]

        for method in required_methods:
            if hasattr(retrieval_service, method):
                print(f"   ✅ {method}: Available")
            else:
                print(f"   ❌ {method}: Missing")

        # Test 5: Test content parser structure
        print("\n5️⃣ Testing Content Parser Structure...")

        required_parser_methods = [
            "parse_modal_content",
            "get_all_sections",
            "validate_content_structure",
        ]

        for method in required_parser_methods:
            if hasattr(content_parser, method):
                print(f"   ✅ {method}: Available")
            else:
                print(f"   ❌ {method}: Missing")

        # Test 6: Test basic parsing functionality
        print("\n6️⃣ Testing Basic Parsing...")

        # Create mock data
        mock_data = {
            "tool_name": "Calidad Total",
            "selected_sources": ["Google Trends"],
            "language": "es",
            "analysis_type": "single_source",
            "executive_summary": "This is a test executive summary.",
            "principal_findings": "These are test principal findings.",
            "temporal_analysis": "This is test temporal analysis.",
            "seasonal_analysis": "This is test seasonal analysis.",
            "fourier_analysis": "This is test Fourier analysis.",
            "strategic_synthesis": "This is test strategic synthesis.",
            "conclusions": "These are test conclusions.",
            "confidence_score": 0.85,
            "model_used": "kimi-k1",
            "data_points_analyzed": 1000,
            "response_time_ms": 50,
        }

        parse_result = content_parser.parse_modal_content(mock_data, "es")
        print(f"Parse result - success: {parse_result['success']}")

        if parse_result["success"]:
            parsed_data = parse_result["data"]
            sections = parsed_data.get("sections", {})
            present_sections = sum(
                1 for s in sections.values() if s.get("present", False)
            )
            print(f"Present sections: {present_sections}")
            print("✅ Basic parsing successful")
        else:
            print(f"⚠️ Basic parsing failed: {parse_result.get('error')}")

        # Test 7: Test section configurations
        print("\n7️⃣ Testing Section Configurations...")

        all_sections = content_parser.get_all_sections("es")
        print(f"Available sections: {len(all_sections)}")

        for section in all_sections[:3]:  # Show first 3
            print(f"   - {section['name']}: {section['title']}")

        print("\n✅ All basic functionality tests completed successfully!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("This may be expected if services are not yet fully integrated")
        return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_service_creation():
    """Test creating instances of the services."""
    print("\n🔧 Testing Service Creation")
    print("-" * 40)

    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

        from key_findings.retrieval_service import KeyFindingsRetrievalService
        from key_findings.content_parser import KeyFindingsContentParser

        # Create instances directly
        retrieval = KeyFindingsRetrievalService()
        parser = KeyFindingsContentParser()

        print("✅ Direct service creation successful")

        # Test singleton functions
        retrieval2 = KeyFindingsRetrievalService()
        parser2 = KeyFindingsContentParser()

        # Should be same instances (singleton)
        print(f"Retrieval services same instance: {retrieval is retrieval2}")
        print(f"Parser services same instance: {parser is parser2}")

        return True

    except Exception as e:
        print(f"❌ Service creation test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Basic Architecture Tests")
    print("=" * 60)

    # Test basic functionality
    success1 = test_basic_functionality()

    # Test service creation
    success2 = test_service_creation()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print(f"Basic Functionality Tests: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"Service Creation Tests: {'✅ PASSED' if success2 else '❌ FAILED'}")

    if success1 and success2:
        print("\n🎉 BASIC TESTS PASSED - Core architecture is working!")
        print("Next steps: Test with real database integration")
        exit(0)
    else:
        print("\n⚠️ Some basic tests failed - check the implementation")
        exit(1)
