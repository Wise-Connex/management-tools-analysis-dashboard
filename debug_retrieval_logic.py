#!/usr/bin/env python3
"""
Debug the actual retrieval logic step by step.
"""

import sys
import sqlite3
import json

# Add dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

def debug_retrieval_logic():
    """Debug the step-by-step retrieval process."""

    print("🔍 DEBUGGING RETRIEVAL LOGIC STEP-BY-STEP")
    print("=" * 70)

    # Test the hash generation and retrieval process
    from key_findings.database_manager import KeyFindingsDBManager

    db_manager = KeyFindingsDBManager('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/key_findings.db')

    print("\n1️⃣ Testing Single Source Hash Generation:")

    # Test single source
    tool_name = "Benchmarking"
    selected_sources = ["Google Trends"]
    language = "es"

    print(f"   Input: tool='{tool_name}', sources={selected_sources}, lang='{language}'")

    scenario_hash = db_manager.generate_scenario_hash(tool_name, selected_sources, language)
    print(f"   Generated Hash: {scenario_hash}")

    # Check if this hash exists in main database
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM key_findings_reports WHERE scenario_hash = ?", (scenario_hash,))
        count = cursor.fetchone()[0]
        print(f"   In Main DB: {'EXISTS' if count > 0 else 'NOT FOUND'}")

        if count > 0:
            cursor.execute("""
                SELECT executive_summary, principal_findings, pca_insights,
                       model_used, api_latency_ms, confidence_score, data_points_analyzed
                FROM key_findings_reports
                WHERE scenario_hash = ?
            """, (scenario_hash,))
            result = cursor.fetchone()
            if result:
                exec_sum, findings, pca_insights, model_used, api_latency, confidence, data_points = result
                print(f"   Retrieved Data:")
                print(f"     Model Used: {model_used}")
                print(f"     API Latency: {api_latency}ms")
                print(f"     Confidence Score: {confidence}")
                print(f"     Data Points: {data_points}")
                print(f"     Executive Summary Length: {len(exec_sum or '')} chars")
                print(f"     Principal Findings Length: {len(findings or '')} chars")
                print(f"     PCA Insights: {pca_insights[:100]}..." if pca_insights else "None")

    print("\n2️⃣ Testing Multi-Source Hash Generation:")

    # Test multi-source
    selected_sources_multi = ["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"]

    print(f"   Input: tool='{tool_name}', sources={selected_sources_multi}, lang='{language}'")

    scenario_hash_multi = db_manager.generate_scenario_hash(tool_name, selected_sources_multi, language)
    print(f"   Generated Hash: {scenario_hash_multi}")

    # Check if this hash exists in main database
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM key_findings_reports WHERE scenario_hash = ?", (scenario_hash_multi,))
        count = cursor.fetchone()[0]
        print(f"   In Main DB: {'EXISTS' if count > 0 else 'NOT FOUND'}")

        if count > 0:
            cursor.execute("""
                SELECT executive_summary, principal_findings, pca_insights,
                       model_used, api_latency_ms, confidence_score, data_points_analyzed
                FROM key_findings_reports
                WHERE scenario_hash = ?
            """, (scenario_hash_multi,))
            result = cursor.fetchone()
            if result:
                exec_sum, findings, pca_insights, model_used, api_latency, confidence, data_points = result
                print(f"   Retrieved Data:")
                print(f"     Model Used: {model_used}")
                print(f"     API Latency: {api_latency}ms")
                print(f"     Confidence Score: {confidence}")
                print(f"     Data Points: {data_points}")
                print(f"     Executive Summary Length: {len(exec_sum or '')} chars")
                print(f"     Principal Findings Length: {len(findings or '')} chars")
                print(f"     PCA Insights: {pca_insights[:100]}..." if pca_insights else "None")

    print("\n3️⃣ Testing Precomputed Findings Retrieval:")

    # Test precomputed findings service directly
    from key_findings.key_findings_service import KeyFindingsService

    kf_service = KeyFindingsService(db_manager=db_manager)

    # Test single source precomputed retrieval
    print(f"   Testing precomputed retrieval for single source...")

    # Manually test the _get_precomputed_findings method
    precomputed_result = kf_service._get_precomputed_findings(tool_name, selected_sources, language)

    if precomputed_result:
        print(f"   ✅ Precomputed findings found!")
        print(f"   Data keys: {list(precomputed_result.keys())}")
        for key, value in precomputed_result.items():
            if isinstance(value, str):
                print(f"     {key}: {len(value)} chars")
            else:
                print(f"     {key}: {value}")
    else:
        print(f"   ❌ No precomputed findings found")

    print("\n4️⃣ Testing Multi-Source Precomputed Retrieval:")

    precomputed_result_multi = kf_service._get_precomputed_findings(tool_name, selected_sources_multi, language)

    if precomputed_result_multi:
        print(f"   ✅ Precomputed findings found!")
        print(f"   Data keys: {list(precomputed_result_multi.keys())}")
        for key, value in precomputed_result_multi.items():
            if isinstance(value, str):
                print(f"     {key}: {len(value)} chars")
            else:
                print(f"     {key}: {value}")
    else:
        print(f"   ❌ No precomputed findings found")

    print("\n" + "=" * 70)
    print("🔍 Retrieval Logic Debug Complete!")
    print("=" * 70)

if __name__ == "__main__":
    debug_retrieval_logic()