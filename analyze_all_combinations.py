#!/usr/bin/env python3
"""
Database Analysis - Check all combinations for missing sections
"""

import os
import sys

# Add database implementation path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "database_implementation"))

try:
    from precomputed_findings_db import get_precomputed_db_manager

    print("✅ Successfully imported database manager")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def analyze_all_combinations():
    """Analyze all combinations in the database for missing sections."""
    print("🔍 Database Analysis - All Combinations Section Status")
    print("=" * 65)

    try:
        # Initialize database manager
        db_manager = get_precomputed_db_manager()

        # Get all records
        with db_manager.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, tool_name, sources_text, language, analysis_type,
                       LENGTH(executive_summary) as exec_len,
                       LENGTH(principal_findings) as principal_len,
                       LENGTH(temporal_analysis) as temporal_len,
                       LENGTH(seasonal_analysis) as seasonal_len,
                       LENGTH(fourier_analysis) as fourier_len,
                       LENGTH(strategic_synthesis) as strategic_len,
                       LENGTH(conclusions) as conclusions_len
                FROM precomputed_findings 
                WHERE is_active = 1
                ORDER BY tool_name, language, sources_text
            """)
            records = cursor.fetchall()

        print(f"📊 Total active combinations in database: {len(records)}")

        # Analyze each record
        complete_combinations = 0
        incomplete_combinations = 0
        single_source_complete = 0
        single_source_incomplete = 0

        required_sections = [
            "exec_len",
            "principal_len",
            "temporal_len",
            "seasonal_len",
            "fourier_len",
            "strategic_len",
            "conclusions_len",
        ]

        print(f"\n📋 Detailed Analysis:")
        print(
            f"{'ID':<4} {'Tool':<25} {'Sources':<20} {'Lang':<4} {'Type':<12} {'Complete':<8}"
        )
        print("-" * 85)

        for record in records:
            id_val, tool_name, sources, language, analysis_type = record[:5]
            lengths = record[5:]

            # Count sections with substantial content (>10 chars)
            sections_with_content = 0
            for length in lengths:
                if length and length > 10:
                    sections_with_content += 1

            is_complete = sections_with_content >= 6
            status = "✅ COMPLETE" if is_complete else "❌ INCOMPLETE"

            print(
                f"{id_val:<4} {tool_name[:24]:<25} {sources[:19]:<20} {language:<4} {analysis_type[:11]:<12} {status:<8}"
            )

            if is_complete:
                complete_combinations += 1
                if analysis_type == "single_source":
                    single_source_complete += 1
            else:
                incomplete_combinations += 1
                if analysis_type == "single_source":
                    single_source_incomplete += 1

        print(f"\n📊 Summary Statistics:")
        print(f"  Total combinations: {len(records)}")
        print(f"  Complete (6+ sections): {complete_combinations}")
        print(f"  Incomplete (<6 sections): {incomplete_combinations}")
        print(f"  Single-source complete: {single_source_complete}")
        print(f"  Single-source incomplete: {single_source_incomplete}")
        print(f"  Success rate: {(complete_combinations / len(records) * 100):.1f}%")
        print(
            f"  Single-source success rate: {(single_source_complete / (single_source_complete + single_source_incomplete) * 100):.1f}%"
        )

        # Identify which sections are missing most often
        print(f"\n🔍 Missing Section Analysis:")
        section_names = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

        for i, section in enumerate(section_names):
            missing_count = 0
            for record in records:
                length = record[5 + i]  # Offset for the first 5 fields
                if not length or length <= 10:
                    missing_count += 1
            print(
                f"  {section}: {missing_count}/{len(records)} missing ({missing_count / len(records) * 100:.1f}%)"
            )

    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    analyze_all_combinations()
