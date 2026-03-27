#!/usr/bin/env python3
"""
Update database schema to add missing columns for strategic_synthesis and conclusions
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


def update_database_schema():
    """Update the database schema to add missing columns."""
    print("🔧 Updating Database Schema - Adding Missing Columns")
    print("=" * 55)

    try:
        # Initialize database manager
        db_manager = get_precomputed_db_manager()

        # Add missing columns to the precomputed_findings table
        with db_manager.get_connection() as conn:
            print("📝 Adding strategic_synthesis column...")
            try:
                conn.execute(
                    "ALTER TABLE precomputed_findings ADD COLUMN strategic_synthesis TEXT"
                )
                print("✅ strategic_synthesis column added successfully")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("ℹ️ strategic_synthesis column already exists")
                else:
                    print(f"❌ Error adding strategic_synthesis column: {e}")

            print("📝 Adding conclusions column...")
            try:
                conn.execute(
                    "ALTER TABLE precomputed_findings ADD COLUMN conclusions TEXT"
                )
                print("✅ conclusions column added successfully")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("ℹ️ conclusions column already exists")
                else:
                    print(f"❌ Error adding conclusions column: {e}")

            # Commit the changes
            conn.commit()
            print("✅ Schema update completed")

            # Verify the new columns exist
            print("\n🔍 Verifying schema update...")
            cursor = conn.execute("PRAGMA table_info(precomputed_findings)")
            columns = cursor.fetchall()

            required_columns = ["strategic_synthesis", "conclusions"]
            found_columns = [col[1] for col in columns]

            print(f"📊 Current columns in precomputed_findings table:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")

            for req_col in required_columns:
                if req_col in found_columns:
                    print(f"✅ {req_col}: Found")
                else:
                    print(f"❌ {req_col}: Missing")

        print(f"\n🎯 Schema update completed successfully!")

    except Exception as e:
        print(f"❌ Schema update error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    update_database_schema()
