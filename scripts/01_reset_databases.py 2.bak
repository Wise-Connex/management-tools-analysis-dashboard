#!/usr/bin/env python3
"""
Database reset utility for key findings review implementation.
Clears both precomputed and runtime databases and reinitializes schemas.
"""

import sys
import os
import sqlite3
import logging
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/logs/database_reset.log"
        ),
        logging.StreamHandler(),
    ],
)

# Database paths
PRECOMPUTED_DB_PATH = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
RUNTIME_DB_PATH = (
    "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/key_findings.db"
)


def create_directories():
    """Ensure database directories exist."""
    Path(PRECOMPUTED_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(RUNTIME_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    logging.info("✅ Database directories created/verified")


def reset_precomputed_database():
    """Reset precomputed findings database."""
    try:
        # Remove existing database
        if os.path.exists(PRECOMPUTED_DB_PATH):
            os.remove(PRECOMPUTED_DB_PATH)
            logging.info("✅ Removed existing precomputed database")

        # Create new database with schema
        from database_implementation.precomputed_findings_db import (
            PrecomputedFindingsDBManager,
        )

        db_manager = PrecomputedFindingsDBManager(PRECOMPUTED_DB_PATH)
        db_manager.populate_reference_data()

        # Verify creation
        stats = db_manager.get_statistics()
        logging.info(f"✅ Precomputed database created: {stats}")

        return True

    except Exception as e:
        logging.error(f"❌ Failed to reset precomputed database: {e}")
        return False


def reset_runtime_database():
    """Reset runtime cache database."""
    try:
        # Remove existing database
        if os.path.exists(RUNTIME_DB_PATH):
            os.remove(RUNTIME_DB_PATH)
            logging.info("✅ Removed existing runtime database")

        # Create new database with basic schema
        conn = sqlite3.connect(RUNTIME_DB_PATH)
        cursor = conn.cursor()

        # Create key_findings_reports table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS key_findings_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_hash TEXT UNIQUE NOT NULL,
            tool_name TEXT NOT NULL,
            selected_sources TEXT NOT NULL,
            language TEXT DEFAULT 'es',
            executive_summary TEXT NOT NULL,
            principal_findings TEXT NOT NULL,
            strategic_synthesis TEXT,
            conclusions TEXT,
            heatmap_analysis TEXT,
            pca_analysis TEXT,
            temporal_analysis TEXT,
            seasonal_analysis TEXT,
            fourier_analysis TEXT,
            analysis_type TEXT NOT NULL,
            sources_count INTEGER NOT NULL,
            analysis_depth TEXT,
            model_used TEXT NOT NULL,
            api_latency_ms INTEGER NOT NULL,
            confidence_score REAL,
            data_points_analyzed INTEGER NOT NULL,
            generation_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cache_version TEXT DEFAULT '2.0',
            access_count INTEGER DEFAULT 0,
            last_accessed DATETIME,
            user_rating INTEGER,
            user_feedback TEXT,
            content_validation_status TEXT DEFAULT 'valid',
            validation_errors TEXT
        )
        """)

        # Create key_findings_history table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS key_findings_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            previous_version_id INTEGER,
            change_type TEXT NOT NULL,
            changed_fields TEXT,
            change_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            changed_by TEXT,
            FOREIGN KEY (report_id) REFERENCES key_findings_reports(id)
        )
        """)

        # Create model_performance table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER,
            api_latency_ms INTEGER,
            error_message TEXT,
            user_satisfaction INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create cache_statistics table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            cache_hits INTEGER DEFAULT 0,
            cache_misses INTEGER DEFAULT 0,
            total_requests INTEGER DEFAULT 0,
            hit_rate REAL DEFAULT 0.0,
            average_response_time_ms REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()

        logging.info("✅ Runtime database created successfully")
        return True

    except Exception as e:
        logging.error(f"❌ Failed to reset runtime database: {e}")
        return False


def verify_databases():
    """Verify both databases are properly initialized."""
    try:
        # Check precomputed database
        from database_implementation.precomputed_findings_db import (
            PrecomputedFindingsDBManager,
        )

        precomputed_db = PrecomputedFindingsDBManager(PRECOMPUTED_DB_PATH)
        precomputed_stats = precomputed_db.get_statistics()

        # Check runtime database with basic SQLite verification
        conn = sqlite3.connect(RUNTIME_DB_PATH)
        cursor = conn.cursor()

        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = [
            "key_findings_reports",
            "key_findings_history",
            "model_performance",
            "cache_statistics",
        ]
        missing_tables = [table for table in expected_tables if table not in tables]

        conn.close()

        if missing_tables:
            logging.error(f"❌ Runtime database missing tables: {missing_tables}")
            return False

        logging.info(f"✅ Precomputed database stats: {precomputed_stats}")
        logging.info(f"✅ Runtime database verified with tables: {tables}")

        return True

    except Exception as e:
        logging.error(f"❌ Database verification failed: {e}")
        return False


def main():
    """Main reset function."""
    logging.info("🚀 Starting database reset process")
    logging.info(f"Timestamp: {datetime.now()}")

    try:
        # Create directories
        create_directories()

        # Reset databases
        precomputed_success = reset_precomputed_database()
        runtime_success = reset_runtime_database()

        if precomputed_success and runtime_success:
            # Verify databases
            verification_success = verify_databases()

            if verification_success:
                logging.info("✅ Database reset completed successfully")
                return 0
            else:
                logging.error("❌ Database verification failed")
                return 1
        else:
            logging.error("❌ Database reset failed")
            return 1

    except Exception as e:
        logging.error(f"❌ Unexpected error during reset: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
