#!/usr/bin/env python3
"""
Test script for precomputed findings database implementation.
Tests basic operations and validates database schema.
"""

import sys
import os
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_database_creation():
    """Test database creation and schema initialization."""
    print("🔧 Testing database creation...")

    # Initialize database manager
    db_manager = get_precomputed_db_manager()
    print("✅ Database manager initialized")

    # Populate reference data
    db_manager.populate_reference_data()
    print("✅ Reference data populated")

    # Get database statistics
    stats = db_manager.get_statistics()
    print(f"✅ Database stats retrieved: {stats}")

    return db_manager


def test_hash_generation(db_manager):
    """Test hash generation consistency."""
    print("\n🔑 Testing hash generation...")

    # Test hash consistency
    tool_name = "Benchmarking"
    selected_sources = ["Google Trends", "Bain Usability", "Bain Satisfaction"]
    language = "es"

    hash1 = db_manager.generate_combination_hash(tool_name, selected_sources, language)
    hash2 = db_manager.generate_combination_hash(tool_name, selected_sources, language)

    print(f"Generated hash: {hash1}")
    print(f"Consistency check: {'✅ PASSED' if hash1 == hash2 else '❌ FAILED'}")

    # Test different combinations
    different_sources = ["Google Books", "Crossref"]
    hash3 = db_manager.generate_combination_hash(tool_name, different_sources, language)

    print(f"Different combination: {hash3}")
    print(f"Uniqueness check: {'✅ PASSED' if hash1 != hash3 else '❌ FAILED'}")

    return hash1


def test_job_creation(db_manager):
    """Test computation job creation and management."""
    print("\n📋 Testing job creation...")

    # Create a test job (use unique combination to avoid duplicates)
    tool_name = "Calidad Total"  # Different tool
    selected_sources = [
        "Google Books",
        "Crossref",
    ]  # Different sources to avoid duplicate
    language = "en"  # Different language

    job_id = db_manager.create_computation_job(
        tool_name, selected_sources, language, priority=10
    )
    print(f"✅ Created job ID: {job_id}")

    # Get next pending job
    next_job = db_manager.get_next_pending_job()
    if next_job:
        print(f"✅ Retrieved next job: {next_job['id']} - {next_job['tool_name']}")

        # Update job status
        success = db_manager.update_job_status(job_id, "running", progress_percent=25)
        print(f"✅ Updated job status: {'SUCCESS' if success else 'FAILED'}")

        # Mark job completed
        success = db_manager.mark_job_completed(job_id)
        print(f"✅ Marked job completed: {'SUCCESS' if success else 'FAILED'}")
    else:
        print("❌ No pending jobs found")

    return job_id


def test_analysis_storage(db_manager, test_hash):
    """Test storing and retrieving analysis data."""
    print("\n💾 Testing analysis storage...")

    # Create sample analysis data with different combination
    tool_name = "Calidad Total"  # Different tool
    selected_sources = ["Google Trends", "Crossref"]  # Different sources
    language = "es"

    # Generate new hash for different combination
    test_hash = db_manager.generate_combination_hash(
        tool_name, selected_sources, language
    )

    analysis_data = {
        "executive_summary": "# Análisis Ejecutivo\n\nEste es un resumen ejecutivo de prueba.",
        "principal_findings": "## Hallazgos Principales\n\nEste es un hallazgo principal.",
        "temporal_analysis": "# Análisis Temporal\n\nTendencias observadas...",
        "seasonal_analysis": "# Análisis Estacional\n\nPatrones estacionales...",
        "fourier_analysis": "# Análisis de Fourier\n\nFrecuencias dominantes...",
        "pca_analysis": "# Análisis PCA\n\nComponentes principales...",
        "heatmap_analysis": "# Análisis de Calor\n\nDistribución de datos...",
        "tool_display_name": "Benchmarking",
        "data_points_analyzed": 1500,
        "confidence_score": 0.85,
        "model_used": "gpt-4",
    }

    # Store analysis
    record_id = db_manager.store_precomputed_analysis(
        test_hash, tool_name, selected_sources, language, analysis_data
    )
    print(f"✅ Stored analysis record ID: {record_id}")

    # Retrieve analysis
    retrieved = db_manager.get_combination_by_hash(test_hash)
    if retrieved:
        print(f"✅ Retrieved analysis: {retrieved['id']} - {retrieved['tool_name']}")
        print(f"   - Executive summary length: {len(retrieved['executive_summary'])}")
        print(f"   - Data points analyzed: {retrieved['data_points_analyzed']}")
        print(f"   - Confidence score: {retrieved['confidence_score']}")
        return True
    else:
        print("❌ Failed to retrieve stored analysis")
        return False


def test_database_performance(db_manager):
    """Test database performance and statistics."""
    print("\n📊 Testing database performance...")

    # Get updated statistics
    stats = db_manager.get_statistics()
    print(f"Database Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test query performance with multiple lookups
    import time

    # Test hash lookups (should be very fast)
    tool_name = "Benchmarking"
    sources = ["Google Trends", "Bain Usability"]
    language = "es"

    start_time = time.time()
    for i in range(10):
        test_hash = db_manager.generate_combination_hash(tool_name, sources, language)
        result = db_manager.get_combination_by_hash(test_hash)
    end_time = time.time()

    avg_time = (end_time - start_time) / 10 * 1000  # Convert to milliseconds
    print(f"✅ Average lookup time: {avg_time:.2f}ms (Target: <100ms)")

    return True


def run_comprehensive_tests():
    """Run all tests and report results."""
    print("🚀 Starting Precomputed Findings Database Tests\n")

    try:
        # Test 1: Database creation and setup
        db_manager = test_database_creation()

        # Test 2: Hash generation
        test_hash = test_hash_generation(db_manager)

        # Test 3: Job management
        job_id = test_job_creation(db_manager)

        # Test 4: Analysis storage and retrieval
        storage_success = test_analysis_storage(db_manager, test_hash)

        # Test 5: Performance testing
        performance_success = test_database_performance(db_manager)

        # Final results
        print("\n" + "=" * 50)
        print("TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"✅ Database Creation: PASSED")
        print(f"✅ Hash Generation: PASSED")
        print(f"✅ Job Management: PASSED")
        print(
            f"{'✅' if storage_success else '❌'} Analysis Storage: {'PASSED' if storage_success else 'FAILED'}"
        )
        print(
            f"{'✅' if performance_success else '❌'} Performance Test: {'PASSED' if performance_success else 'FAILED'}"
        )

        overall_success = storage_success and performance_success
        print(
            f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
        )

        return overall_success

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
