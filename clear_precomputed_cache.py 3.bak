#!/usr/bin/env python3
"""
Clear the precomputed findings database cache
"""

import sqlite3
import os

def clear_precomputed_cache():
    """Clear the precomputed findings cache"""

    db_path = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db'

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get count before clearing
        cursor.execute("SELECT COUNT(*) FROM precomputed_findings")
        count_before = cursor.fetchone()[0]

        # Clear all entries
        cursor.execute("DELETE FROM precomputed_findings")

        # Reset the auto-increment counter (optional)
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='precomputed_findings'")

        conn.commit()

        # Verify clearing
        cursor.execute("SELECT COUNT(*) FROM precomputed_findings")
        count_after = cursor.fetchone()[0]

        conn.close()

        print(f"🧹 PRECOMPUTED FINDINGS CACHE CLEARED")
        print("=" * 50)
        print(f"✅ Entries before: {count_before}")
        print(f"✅ Entries after: {count_after}")
        print(f"🗑️ Deleted entries: {count_before - count_after}")
        print("\n🔄 Next Key Findings generation will create fresh precomputed data")
        print("✅ This will use the updated modal component with all fixes")

        return True

    except Exception as e:
        print(f"❌ Error clearing precomputed cache: {e}")
        return False

if __name__ == "__main__":
    success = clear_precomputed_cache()
    exit(0 if success else 1)