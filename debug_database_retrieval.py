#!/usr/bin/env python3
"""
Debug database retrieval to see what's actually being fetched.
"""

import sqlite3
import json

def debug_database_retrieval():
    """Debug what's actually in the databases and being retrieved."""

    print("🔍 DEBUGGING DATABASE RETRIEVAL")
    print("=" * 70)

    # Check precomputed findings database
    print("\n1️⃣ Checking Precomputed Findings Database:")
    conn1 = sqlite3.connect('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db')
    cursor1 = conn1.cursor()

    cursor1.execute("""
        SELECT tool_name, sources_text, analysis_type,
               LENGTH(COALESCE(executive_summary, '')) as exec_len,
               LENGTH(COALESCE(principal_findings, '')) as findings_len,
               LENGTH(COALESCE(temporal_analysis, '')) as temporal_len,
               LENGTH(COALESCE(seasonal_analysis, '')) as seasonal_len,
               LENGTH(COALESCE(fourier_analysis, '')) as fourier_len,
               LENGTH(COALESCE(pca_analysis, '')) as pca_len,
               LENGTH(COALESCE(heatmap_analysis, '')) as heatmap_len,
               model_used, confidence_score, data_points_analyzed
        FROM precomputed_findings
        WHERE tool_name = 'Benchmarking' AND language = 'es'
        ORDER BY id DESC LIMIT 2
    """)

    precomputed_results = cursor1.fetchall()
    conn1.close()

    for i, result in enumerate(precomputed_results, 1):
        (tool_name, sources_text, analysis_type, exec_len, findings_len, temporal_len,
         seasonal_len, fourier_len, pca_len, heatmap_len, model_used, confidence_score, data_points) = result

        print(f"\n   Result {i}:")
        print(f"     Tool: {tool_name}")
        print(f"     Sources: {sources_text}")
        print(f"     Analysis Type: {analysis_type}")
        print(f"     Model Used: {model_used}")
        print(f"     Confidence Score: {confidence_score}")
        print(f"     Data Points Analyzed: {data_points}")
        print(f"     Content Lengths:")
        print(f"       Executive Summary: {exec_len} chars")
        print(f"       Principal Findings: {findings_len} chars")
        print(f"       Temporal Analysis: {temporal_len} chars")
        print(f"       Seasonal Analysis: {seasonal_len} chars")
        print(f"       Fourier Analysis: {fourier_len} chars")
        print(f"       PCA Analysis: {pca_len} chars")
        print(f"       Heatmap Analysis: {heatmap_len} chars")

    # Check main database
    print("\n2️⃣ Checking Main Key Findings Database:")
    conn2 = sqlite3.connect('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/key_findings.db')
    cursor2 = conn2.cursor()

    cursor2.execute("""
        SELECT tool_name, selected_sources, language, model_used,
               length(executive_summary) as exec_len, length(principal_findings) as findings_len,
               api_latency_ms, confidence_score, data_points_analyzed, generation_timestamp
        FROM key_findings_reports
        WHERE tool_name = 'Benchmarking'
        ORDER BY generation_timestamp DESC LIMIT 2
    """)

    main_results = cursor2.fetchall()
    conn2.close()

    for i, result in enumerate(main_results, 1):
        (tool_name, selected_sources, language, model_used, exec_len, findings_len,
         api_latency, confidence_score, data_points, generation_timestamp) = result

        sources_list = json.loads(selected_sources) if selected_sources else []

        print(f"\n   Result {i}:")
        print(f"     Tool: {tool_name}")
        print(f"     Sources: {sources_list}")
        print(f"     Language: {language}")
        print(f"     Model Used: {model_used}")
        print(f"     API Latency: {api_latency}ms")
        print(f"     Confidence Score: {confidence_score}")
        print(f"     Data Points: {data_points}")
        print(f"     Generated: {generation_timestamp}")
        print(f"     Content Lengths:")
        print(f"       Executive Summary: {exec_len} chars")
        print(f"       Principal Findings: {findings_len} chars")

    print("\n" + "=" * 70)
    print("🔍 Database Debug Complete!")
    print("=" * 70)

if __name__ == "__main__":
    debug_database_retrieval()