#!/usr/bin/env python3
"""
Debug exact database content extraction
"""

import sqlite3
import json
import sys

def debug_exact_content():
    """Debug exact content from database"""

    print("Debugging exact database content...")
    print("=" * 60)

    # Connect to precomputed database
    try:
        conn = sqlite3.connect('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db')
        cursor = conn.cursor()

        # Query for multi-source Benchmarking
        cursor.execute("""
            SELECT tool_name, sources_text, language, analysis_type,
                   executive_summary, principal_findings, pca_analysis, heatmap_analysis,
                   model_used, data_points_analyzed, confidence_score
            FROM precomputed_findings
            WHERE tool_name = 'Benchmarking'
            AND sources_text = 'Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref'
            AND language = 'es'
        """)

        result = cursor.fetchone()
        if result:
            tool_name, sources_text, language, analysis_type, executive_summary, principal_findings, pca_analysis, heatmap_analysis, model_used, data_points, confidence = result

            print(f"✓ Found result for {tool_name} ({analysis_type})")
            print(f"✓ Sources: {sources_text}")
            print(f"✓ Model: {model_used}")
            print(f"✓ Data points: {data_points}")
            print(f"✓ Confidence: {confidence}")

            print(f"\n✓ Executive Summary (first 100 chars):")
            print(f"   '{executive_summary[:100]}...'")

            print(f"\n✓ Principal Findings (first 100 chars):")
            print(f"   '{principal_findings[:100]}...'")

            print(f"\n✓ PCA Analysis (first 200 chars):")
            print(f"   '{pca_analysis[:200]}...'")
            print(f"   Length: {len(pca_analysis)} chars")

            print(f"\n✓ Heatmap Analysis (first 200 chars):")
            print(f"   '{heatmap_analysis[:200]}...'")
            print(f"   Length: {len(heatmap_analysis)} chars")

            # Check if content is actually empty or just whitespace
            pca_trimmed = pca_analysis.strip()
            heatmap_trimmed = heatmap_analysis.strip()

            print(f"\n✓ PCA trimmed length: {len(pca_trimmed)} chars")
            print(f"✓ Heatmap trimmed length: {len(heatmap_trimmed)} chars")

            # Check for common placeholder text
            if "No PCA analysis available" in pca_analysis:
                print("✗ FOUND: PCA contains 'No PCA analysis available'")
            if "No heatmap analysis available" in heatmap_analysis:
                print("✗ FOUND: Heatmap contains 'No heatmap analysis available'")

            # Check content type
            if pca_trimmed:
                print("✓ PCA has actual content - should display")
            else:
                print("✗ PCA is empty - will not display")

            if heatmap_trimmed:
                print("✓ Heatmap has actual content - should display")
            else:
                print("✗ Heatmap is empty - will not display")

        else:
            print("✗ No result found for multi-source Benchmarking")

        conn.close()

    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

    return True

if __name__ == "__main__":
    success = debug_exact_content()
    sys.exit(0 if success else 1)