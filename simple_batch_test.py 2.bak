#!/usr/bin/env python3
"""
Simple Batch Processing Test
Tests the pipeline with simulation mode only.
"""

import sys
import asyncio
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from database_implementation.phase3_precomputation_pipeline import (
    PrecomputationPipeline,
)


async def main():
    """Simple test of the batch processing pipeline."""
    print("🚀 Simple Batch Processing Test")
    print("=" * 50)

    # Initialize components
    db_manager = get_precomputed_db_manager()
    pipeline = PrecomputationPipeline(use_simulation=True)

    print("✅ Components initialized successfully")

    # Generate combinations
    print("\n🔢 Generating combinations...")
    combinations = pipeline.generate_all_combinations()

    print(f"📊 Generated {len(combinations)} combinations")
    print(f"🎯 Tools: 21, Sources: 31 combinations each, Languages: 2")

    # Test with a small sample first
    test_size = 5
    test_combinations = combinations[:test_size]

    print(f"\n🧪 Testing with {test_size} combinations:")

    start_time = time.time()
    success_count = 0

    for i, combination in enumerate(test_combinations, 1):
        print(
            f"  {i}. Processing: {combination['tool_name']} + {', '.join(combination['selected_sources'])} ({combination['language']})"
        )

        try:
            # Generate analysis using pipeline's simulation
            analysis_data = pipeline.simulate_ai_analysis(combination)

            # Store in database
            db_manager.store_precomputed_analysis(
                combination_hash=combination["combination_hash"],
                tool_name=combination["tool_name"],
                selected_sources=combination["selected_sources"],
                language=combination["language"],
                analysis_data=analysis_data,
            )

            success_count += 1
            print(f"     ✅ Stored successfully")

        except Exception as e:
            print(f"     ❌ Failed: {e}")

    elapsed_time = time.time() - start_time

    print(f"\n📈 Results:")
    print(f"   Processed: {success_count}/{test_size}")
    print(f"   Time: {elapsed_time:.2f} seconds")
    print(f"   Rate: {success_count / elapsed_time:.1f} combinations/second")

    # Test retrieval
    print(f"\n🔍 Testing retrieval...")
    test_combo = test_combinations[0]
    retrieved = db_manager.get_combination_by_hash(test_combo["combination_hash"])

    if retrieved:
        print(f"   ✅ Retrieved successfully: {retrieved['tool_name']}")
    else:
        print(f"   ❌ Retrieval failed")

    print(f"\n🎉 Test completed successfully!")
    return True


if __name__ == "__main__":
    asyncio.run(main())
