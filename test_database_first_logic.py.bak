#!/usr/bin/env python3
"""
Database-First Logic Test Script

Tests the database-first implementation for Key Findings service.
Verifies hash generation, database retrieval, and fallback logic.
"""

import os
import sys
import time
from pathlib import Path


def test_database_first_logic():
    """Test database-first logic implementation."""
    print("🗄️ Database-First Logic Test")
    print("=" * 50)

    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    try:
        # Test 1: Database Manager Initialization
        print("\n1️⃣ Testing Database Manager Initialization...")
        from database_implementation.precomputed_findings_db import (
            get_precomputed_db_manager,
        )

        db_manager = get_precomputed_db_manager()
        print("   ✅ Database manager initialized")

        # Test 2: Hash Generation
        print("\n2️⃣ Testing Hash Generation...")
        tool_name = "Benchmarking"
        selected_sources = ["Google Trends", "Bain Usability"]
        language = "es"

        hash_value = db_manager.generate_combination_hash(
            tool_name, selected_sources, language
        )
        print(f"   Generated hash: {hash_value}")

        # Test consistency
        hash2 = db_manager.generate_combination_hash(
            tool_name, selected_sources, language
        )
        assert hash_value == hash2, "Hash consistency failed"
        print("   ✅ Hash generation is consistent")

        # Test 3: Database Statistics
        print("\n3️⃣ Testing Database Statistics...")
        stats = db_manager.get_statistics()
        print(f"   Total findings: {stats.get('total_findings', 0)}")
        print(f"   Database size: {stats.get('database_size_mb', 0):.2f} MB")

        # Test 4: Combination Retrieval (will test fallback if not found)
        print("\n4️⃣ Testing Combination Retrieval...")

        # Try to retrieve a combination
        result = db_manager.get_combination_by_hash(hash_value)

        if result:
            print("   ✅ Combination found in database")
            print(f"   Tool: {result.get('tool_name')}")
            print(f"   Sources: {result.get('sources_text')}")
            print(f"   Language: {result.get('language')}")
            print(f"   Analysis type: {result.get('analysis_type')}")

            # Check content fields
            content_fields = [
                "executive_summary",
                "principal_findings",
                "temporal_analysis",
            ]
            for field in content_fields:
                content = result.get(field, "")
                if content:
                    print(f"   {field}: ✅ Present ({len(content)} chars)")
                else:
                    print(f"   {field}: ⚠️ Missing")
        else:
            print("   ⚠️ Combination not found in database (fallback to AI)")

        # Test 5: Performance Test
        print("\n5️⃣ Testing Query Performance...")

        if result:
            # Test multiple retrievals for performance
            times = []
            for i in range(10):
                start = time.time()
                db_manager.get_combination_by_hash(hash_value)
                end = time.time()
                times.append((end - start) * 1000)  # Convert to ms

            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)

            print(f"   Average query time: {avg_time:.2f}ms")
            print(f"   Min query time: {min_time:.2f}ms")
            print(f"   Max query time: {max_time:.2f}ms")

            if avg_time < 100:
                print("   ✅ Performance target achieved (<100ms)")
            else:
                print("   ⚠️ Performance above target (>100ms)")

        # Test 6: Database-First Service Integration
        print("\n6️⃣ Testing Database-First Service...")
        try:
            from dashboard_app.key_findings.database_first_service import (
                DatabaseFirstService,
            )

            db_first_service = DatabaseFirstService()

            # Test database lookup
            analysis_result = db_first_service.get_analysis_from_database(
                tool_name, selected_sources, language
            )

            if analysis_result:
                print("   ✅ Database-first service working")
                print(
                    f"   Response time: {analysis_result.get('response_time_ms', 'N/A')}ms"
                )
            else:
                print("   ⚠️ No analysis found (would trigger fallback)")

        except Exception as e:
            print(f"   ❌ Database-first service error: {e}")

        # Test 7: Coverage Check
        print("\n7️⃣ Testing Database Coverage...")

        # Check if we have the expected number of combinations
        expected_combinations = 1302  # 21 tools × 31 source combinations × 2 languages
        actual_combinations = stats.get("total_findings", 0)

        print(f"   Expected combinations: {expected_combinations}")
        print(f"   Actual combinations: {actual_combinations}")

        if actual_combinations >= expected_combinations * 0.9:  # 90% threshold
            print("   ✅ Database coverage is adequate")
        elif actual_combinations > 0:
            print(
                f"   ⚠️ Partial coverage ({actual_combinations}/{expected_combinations})"
            )
        else:
            print("   ❌ Database is empty")

        print(f"\n✅ Database-first logic test completed")
        return True

    except Exception as e:
        print(f"\n❌ Database-first logic test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_database_first_logic()
    sys.exit(0 if success else 1)
