#!/usr/bin/env python3
"""
Debug script to trace scenario hash generation and database lookup.
"""

import sys
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.key_findings_service import KeyFindingsService
from key_findings.database_manager import KeyFindingsDBManager
import hashlib
import json

class HashDebugger:
    """Debug scenario hash generation and database lookup."""

    def debug_hash_generation(self):
        """Debug the hash generation process."""

        print("🔍 Debugging Scenario Hash Generation")
        print("=" * 60)

        # Initialize services
        db_manager = KeyFindingsDBManager('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/database.db')
        kf_service = KeyFindingsService(db_manager=db_manager)

        # Test data that should match our database
        test_cases = [
            {
                "tool_name": "Benchmarking",
                "selected_sources": ["Google Trends"],
                "language": "es",
                "date_range_start": "1950-01-01",
                "date_range_end": "2023-12-31",
                "expected_hash": "single_source_test_001"
            },
            {
                "tool_name": "Benchmarking",
                "selected_sources": ["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],
                "language": "es",
                "date_range_start": "1950-01-01",
                "date_range_end": "2023-12-31",
                "expected_hash": "multi_source_test_001"
            }
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"\\n🧪 Test Case {i}:")
            print(f"  Tool: {test_case['tool_name']}")
            print(f"  Sources: {test_case['selected_sources']}")
            print(f"  Language: {test_case['language']}")
            print(f"  Expected Hash: {test_case['expected_hash']}")

            # Generate the scenario hash manually
            data_dict = {
                "tool_name": test_case['tool_name'],
                "selected_sources": test_case['selected_sources'],
                "language": test_case['language'],
                "date_range_start": test_case['date_range_start'],
                "date_range_end": test_case['date_range_end']
            }

            # Sort sources for consistent hashing
            data_dict['selected_sources'] = sorted(data_dict['selected_sources'])

            # Create hash
            data_string = json.dumps(data_dict, sort_keys=True)
            scenario_hash = hashlib.sha256(data_string.encode()).hexdigest()

            print(f"  Generated Hash: {scenario_hash}")
            print(f"  Expected Hash:  {test_case['expected_hash']}")
            print(f"  Match: {'✅ YES' if scenario_hash == test_case['expected_hash'] else '❌ NO'}")

            # Check if this hash exists in database
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM key_findings_reports WHERE scenario_hash = ?", (scenario_hash,))
            count = cursor.fetchone()[0]

            print(f"  In Database: {'✅ EXISTS' if count > 0 else '❌ NOT FOUND'}")

            if count > 0:
                cursor.execute("SELECT id, tool_name, selected_sources FROM key_findings_reports WHERE scenario_hash = ?", (scenario_hash,))
                result = cursor.fetchone()
                if result:
                    id, tool_name, sources = result
                    sources_list = eval(sources) if sources else []
                    print(f"  Database ID: {id}")
                    print(f"  Database Tool: {tool_name}")
                    print(f"  Database Sources: {sources_list}")

        # Also check what hashes are actually in the database
        print("\\n\\n📊 All Hashes in Database:")
        cursor.execute("SELECT id, scenario_hash, tool_name, selected_sources FROM key_findings_reports ORDER BY id")
        all_reports = cursor.fetchall()

        for report in all_reports:
            id, scenario_hash, tool_name, sources = report
            sources_list = eval(sources) if sources else []
            print(f"\\n  ID {id}: {scenario_hash[:16]}...")
            print(f"    Tool: {tool_name}")
            print(f"    Sources: {sources_list}")

        print("\\n" + "=" * 60)
        print("🔍 Hash Generation Debug Complete!")

if __name__ == "__main__":
    debugger = HashDebugger()
    debugger.debug_hash_generation()

print("\\n" + "="*60)
print("🔍 Hash Generation Debug Complete!")
print("="*60)
print("This will help identify:")
print("• Whether hash generation matches our test data")
print("• What hashes are actually in the database")
print("• Where the mismatch might be occurring")
print("="*60)