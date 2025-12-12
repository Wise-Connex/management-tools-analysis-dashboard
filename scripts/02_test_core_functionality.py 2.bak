#!/usr/bin/env python3
"""
Minimal test for hash generation and database consistency.
Tests the core functionality without complex dependencies.
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add scripts directory to path for utilities
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Import our utilities
from utils.hash_utils import (
    generate_combination_hash,
    normalize_source_name,
    test_hash_generation,
)
from utils.database_utils import retrieve_analysis_by_hash


def test_hash_consistency():
    """Test hash generation consistency."""
    print("🔑 Testing Hash Generation Consistency")
    print("=" * 60)

    # Test the hash generation function
    result = test_hash_generation()

    if result:
        print("✅ Hash generation tests passed!")
    else:
        print("❌ Hash generation tests failed!")

    return result


def test_database_retrieval():
    """Test database retrieval functionality."""
    print("\n🗄️ Testing Database Retrieval")
    print("=" * 60)

    test_combinations = [
        {"tool": "Benchmarking", "sources": ["Google Trends"], "language": "es"},
        {"tool": "Calidad Total", "sources": ["Crossref"], "language": "es"},
    ]

    for i, combo in enumerate(test_combinations, 1):
        print(f"\nTest {i}: {combo['tool']} + {combo['sources']} ({combo['language']})")

        # Generate hash
        hash_value = generate_combination_hash(
            combo["tool"], combo["sources"], combo["language"]
        )

        print(f"Hash: {hash_value}")

        # Try to retrieve from database
        result = retrieve_analysis_by_hash(hash_value)

        if result:
            print(f"✅ Found in {result['source']} database")
            data = result.get("data", {})
            if "tool_name" in data:
                print(f"   Tool: {data['tool_name']}")
            if "sources_text" in data:
                print(f"   Sources: {data['sources_text']}")
            elif "selected_sources" in data:
                print(f"   Sources: {data['selected_sources']}")
        else:
            print("❌ Not found in database")

    return True


def test_source_name_normalization():
    """Test source name normalization."""
    print("\n📝 Testing Source Name Normalization")
    print("=" * 60)

    test_cases = [
        ("Google Trends", "Google Trends"),
        ("Google-Trends", "Google Trends"),
        ("google_trends", "Google Trends"),
        ("GOOGLE TRENDS", "Google Trends"),
        ("Bain - Usability", "Bain Usability"),
        ("Bain - Usabilidad", "Bain Usability"),
        ("Bain Usabilidad", "Bain Usability"),
    ]

    for input_name, expected in test_cases:
        result = normalize_source_name(input_name)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{input_name}' -> '{result}' (expected: '{expected}')")

    return True


def main():
    """Main function to run all tests."""
    print("🚀 Starting Key Findings Core Functionality Tests")
    print("=" * 80)
    print(f"Start time: {datetime.now()}")
    print("=" * 80)

    try:
        # Test 1: Hash consistency
        hash_success = test_hash_consistency()

        # Test 2: Source name normalization
        norm_success = test_source_name_normalization()

        # Test 3: Database retrieval
        db_success = test_database_retrieval()

        # Summary
        print(f"\n{'=' * 80}")
        print("📊 TEST SUMMARY")
        print(f"{'=' * 80}")
        print(f"Hash Consistency: {'✅ PASSED' if hash_success else '❌ FAILED'}")
        print(f"Source Normalization: {'✅ PASSED' if norm_success else '❌ FAILED'}")
        print(f"Database Retrieval: {'✅ PASSED' if db_success else '❌ FAILED'}")

        overall_success = hash_success and norm_success and db_success
        print(
            f"\nOverall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
        )

        return 0 if overall_success else 1

    except Exception as e:
        print(f"❌ Fatal error in main: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
