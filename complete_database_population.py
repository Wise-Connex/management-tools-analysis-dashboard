#!/usr/bin/env python3
"""
Complete Database Population Script
Processes the missing 11 combinations to reach full 1,302 combinations.
"""

import sys
import os
import json
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from database_implementation.phase3_precomputation_pipeline import (
    PrecomputationPipeline,
)


def load_checkpoint():
    """Load the batch processor checkpoint."""
    checkpoint_path = Path("dashboard_app/batch_checkpoint.json")
    if not checkpoint_path.exists():
        print("❌ Checkpoint file not found!")
        return None

    with open(checkpoint_path, "r") as f:
        return json.load(f)


def identify_missing_combinations():
    """Identify which combinations are missing from the database."""
    print("🔍 Identifying missing combinations...")

    # Load checkpoint
    checkpoint = load_checkpoint()
    if not checkpoint:
        return None

    processed_hashes = set(checkpoint["processed_combinations"])

    # Generate all combinations
    pipeline = PrecomputationPipeline(use_simulation=True)
    all_combinations = pipeline.generate_all_combinations()

    # Find missing combinations
    missing_combinations = []
    for combo in all_combinations:
        if combo["combination_hash"] not in processed_hashes:
            missing_combinations.append(combo)

    print(f"📊 Found {len(missing_combinations)} missing combinations")
    return missing_combinations


def complete_database_population():
    """Complete the database population with missing combinations."""
    print("🚀 Completing Database Population")
    print("=" * 50)

    # Initialize components
    db_manager = get_precomputed_db_manager()

    # Get missing combinations
    missing_combinations = identify_missing_combinations()
    if not missing_combinations:
        print("✅ No missing combinations found!")
        return

    print(f"📋 Will process {len(missing_combinations)} missing combinations")

    # Process missing combinations
    successful = 0
    failed = 0
    start_time = time.time()

    for i, combination in enumerate(missing_combinations, 1):
        try:
            print(
                f"🔄 Processing {i}/{len(missing_combinations)}: {combination['tool_name']} + {', '.join(combination['selected_sources'])} ({combination['language']})"
            )

            # Generate analysis content
            analysis_data = PrecomputationPipeline(
                use_simulation=True
            ).simulate_ai_analysis(combination)

            # Store in database
            db_manager.store_precomputed_analysis(
                combination_hash=combination["combination_hash"],
                tool_name=combination["tool_name"],
                selected_sources=combination["selected_sources"],
                language=combination["language"],
                analysis_data=analysis_data,
            )

            successful += 1
            print(f"✅ Stored successfully")

        except Exception as e:
            failed += 1
            print(f"❌ Failed: {e}")

        # Progress update every 5 items
        if i % 5 == 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            eta = (len(missing_combinations) - i) * avg_time
            print(
                f"📊 Progress: {i}/{len(missing_combinations)} ({i / len(missing_combinations) * 100:.1f}%) | ETA: {eta:.1f}s"
            )

    # Final report
    total_time = time.time() - start_time
    print("\n" + "=" * 50)
    print("🎯 DATABASE POPULATION COMPLETE!")
    print("=" * 50)
    print(f"📊 Processed: {len(missing_combinations)} combinations")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️ Total time: {total_time:.2f} seconds")
    print(
        f"🚀 Average time: {total_time / len(missing_combinations):.2f}s per combination"
    )


def validate_database():
    """Validate that all combinations are now in the database."""
    print("\n🔍 Validating Database...")

    db_manager = get_precomputed_db_manager()
    pipeline = PrecomputationPipeline(use_simulation=True)
    all_combinations = pipeline.generate_all_combinations()

    # Check database statistics
    stats = db_manager.get_statistics()
    total_in_db = stats["total_combinations"]
    expected_total = len(all_combinations)

    print(f"📊 Database contains: {total_in_db}/{expected_total} combinations")

    if total_in_db == expected_total:
        print("🎉 SUCCESS: Database fully populated!")
        return True
    else:
        print(f"⚠️ WARNING: Missing {expected_total - total_in_db} combinations")
        return False


if __name__ == "__main__":
    print("🚀 Starting Database Population Completion")

    # Complete database population
    complete_database_population()

    # Validate results
    validate_database()

    print("\n✅ Database population completion finished!")
