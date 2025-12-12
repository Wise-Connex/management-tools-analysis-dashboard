#!/usr/bin/env python3
"""
Clear Key Findings database cache to force fresh AI generation
This ensures new analyses use the improved narrative prompts
"""

import sys
import os
from pathlib import Path

# Add dashboard_app to path
dashboard_app_path = Path(__file__).parent / "dashboard_app"
sys.path.insert(0, str(dashboard_app_path))


# Simple direct database access without imports
def clear_key_findings_cache():
    """Clear the Key Findings database cache to force fresh AI generation"""
    import sqlite3

    print("🧹 CLEARING KEY FINDINGS CACHE")
    print("=" * 50)

    # Database path
    db_path = dashboard_app_path / "data" / "key_findings.db"

    if not db_path.exists():
        print(f"⚠️ Database not found at: {db_path}")
        print("No cache to clear - database doesn't exist yet")
        return

    print(f"📂 Database found at: {db_path}")

    # Connect directly to SQLite and clear cache
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check current cache size
    cursor.execute("SELECT COUNT(*) FROM key_findings_reports")
    result = cursor.fetchone()
    actual_cache_count = result[0] if result and result[0] is not None else 0
    print(f"📊 Current cached reports: {actual_cache_count}")

    # Clear ALL cache (since there's no 'source' column)
    cursor.execute("DELETE FROM key_findings_reports")
    deleted_count = cursor.rowcount

    conn.commit()
    conn.close()

    print(f"✅ Cache cleared successfully!")
    print(f"🗑️ Deleted {deleted_count} cached reports")
    print(f"🔄 Next Key Findings generation will use fresh AI with improved prompts")

    print()
    print("📝 TO TEST THE IMPROVED PROMPTS:")
    print("1. Start dashboard: cd dashboard_app && uv run python app.py")
    print("2. Generate Key Findings for any tool")
    print("3. You should now see 4000+ word narrative format")
    print("4. Check for 'ANÁLISIS NARRATIVO MEJORADO' in the content")


def list_cache_contents():
    """List what's currently in the cache"""
    import sqlite3

    db_path = dashboard_app_path / "data" / "key_findings.db"

    if not db_path.exists():
        print("📂 Database doesn't exist yet")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get cache statistics
    cursor.execute("""
        SELECT tool_name, selected_sources, language, 
               datetime(generation_timestamp) as generation_date,
               model_used, cache_version,
               length(executive_summary) as summary_length
        FROM key_findings_reports 
        ORDER BY generation_timestamp DESC 
        LIMIT 10
    """)

    results = cursor.fetchall()
    conn.close()

    print("📊 CURRENT CACHE CONTENTS (Last 10 entries):")
    print("-" * 80)
    if results:
        for i, row in enumerate(results, 1):
            tool, sources, lang, date, model, version, summary_len = row
            print(
                f"{i:2d}. {tool} ({sources}) [{lang}] - {summary_len} chars - v{version}"
            )
    else:
        print("No cached reports found")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clear Key Findings cache")
    parser.add_argument(
        "--list", action="store_true", help="List current cache contents"
    )
    parser.add_argument("--clear", action="store_true", help="Clear the cache")

    args = parser.parse_args()

    if args.list:
        list_cache_contents()
    elif args.clear:
        clear_key_findings_cache()
    else:
        print("🔧 KEY FINDINGS CACHE MANAGEMENT")
        print("=" * 40)
        print("Usage:")
        print("  python clear_cache.py --list   # Show current cache")
        print(
            "  python clear_cache.py --clear  # Clear cache to force fresh AI generation"
        )
        print()
        list_cache_contents()
