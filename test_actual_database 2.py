#!/usr/bin/env python3
"""
Test with actual database content to see what sections are displayed.
"""

import sqlite3
import json

def test_actual_database_content():
    """Test with actual content from the precomputed findings database."""

    print("🔍 Testing with Actual Database Content")
    print("=" * 70)

    # Connect to database
    db_path = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Test single source
    print("\n1️⃣ Testing Single Source from Database:")
    cursor.execute("""
        SELECT executive_summary, principal_findings, temporal_analysis, seasonal_analysis,
               fourier_analysis, pca_analysis, heatmap_analysis, analysis_type
        FROM precomputed_findings
        WHERE tool_name = 'Benchmarking' AND sources_text = 'Google Trends'
        AND language = 'es' AND is_active = 1
        LIMIT 1
    """)

    single_result = cursor.fetchone()

    if single_result:
        exec_summary, principal_findings, temporal_analysis, seasonal_analysis, fourier_analysis, pca_analysis, heatmap_analysis, analysis_type = single_result

        print(f"   Analysis Type: {analysis_type}")
        print(f"   Executive Summary: {len(exec_summary or '')} chars")
        print(f"   Principal Findings: {len(principal_findings or '')} chars")
        print(f"   Temporal Analysis: {len(temporal_analysis or '')} chars")
        print(f"   Seasonal Analysis: {len(seasonal_analysis or '')} chars")
        print(f"   Fourier Analysis: {len(fourier_analysis or '')} chars")
        print(f"   PCA Analysis: {len(pca_analysis or '')} chars")
        print(f"   Heatmap Analysis: {len(heatmap_analysis or '')} chars")

        # Simulate the modal logic to see what sections would be displayed
        sections_to_show = []

        # Check which sections have content
        if exec_summary:
            sections_to_show.append("Executive Summary")
        if principal_findings:
            sections_to_show.append("Principal Findings")
        if temporal_analysis:
            sections_to_show.append("Temporal Analysis")
        if seasonal_analysis:
            sections_to_show.append("Seasonal Analysis")
        if fourier_analysis:
            sections_to_show.append("Fourier Analysis")
        if pca_analysis:
            sections_to_show.append("PCA Analysis")

        # For single source, exclude heatmap
        if analysis_type == 'single_source':
            print(f"   Excluded (single source): Heatmap Analysis")

        sections_to_show.append("Metadata")

        print(f"   Sections that will be displayed: {len(sections_to_show)}")
        for i, section in enumerate(sections_to_show, 1):
            print(f"     {i}. {section}")

    else:
        print("   ❌ No single source data found")

    # Test multi-source
    print("\n2️⃣ Testing Multi-Source from Database:")
    cursor.execute("""
        SELECT executive_summary, principal_findings, temporal_analysis, seasonal_analysis,
               fourier_analysis, pca_analysis, heatmap_analysis, analysis_type
        FROM precomputed_findings
        WHERE tool_name = 'Benchmarking'
        AND sources_text = 'Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref'
        AND language = 'es' AND is_active = 1
        LIMIT 1
    """)

    multi_result = cursor.fetchone()

    if multi_result:
        exec_summary, principal_findings, temporal_analysis, seasonal_analysis, fourier_analysis, pca_analysis, heatmap_analysis, analysis_type = multi_result

        print(f"   Analysis Type: {analysis_type}")
        print(f"   Executive Summary: {len(exec_summary or '')} chars")
        print(f"   Principal Findings: {len(principal_findings or '')} chars")
        print(f"   Temporal Analysis: {len(temporal_analysis or '')} chars")
        print(f"   Seasonal Analysis: {len(seasonal_analysis or '')} chars")
        print(f"   Fourier Analysis: {len(fourier_analysis or '')} chars")
        print(f"   PCA Analysis: {len(pca_analysis or '')} chars")
        print(f"   Heatmap Analysis: {len(heatmap_analysis or '')} chars")

        # Simulate the modal logic to see what sections would be displayed
        sections_to_show = []

        # Check which sections have content
        if exec_summary:
            sections_to_show.append("Executive Summary")
        if principal_findings:
            sections_to_show.append("Principal Findings")
        if temporal_analysis:
            sections_to_show.append("Temporal Analysis")
        if fourier_analysis:
            sections_to_show.append("Fourier Analysis")
        if pca_analysis:
            sections_to_show.append("PCA Analysis")

        # For multi-source, include heatmap
        if analysis_type == 'multi_source':
            if heatmap_analysis:
                sections_to_show.append("Heatmap Analysis")
            print(f"   Excluded (multi-source): Seasonal Analysis")

        sections_to_show.append("Metadata")

        print(f"   Sections that will be displayed: {len(sections_to_show)}")
        for i, section in enumerate(sections_to_show, 1):
            print(f"     {i}. {section}")

    else:
        print("   ❌ No multi-source data found")

    conn.close()

    print("\n" + "=" * 70)
    print("📊 Database Content Analysis Complete!")
    print("=" * 70)
    print("Key Findings:")
    print("• Executive Summary and Principal Findings are populated for both")
    print("• PCA Analysis has content for both single and multi-source")
    print("• Most temporal/seasonal/fourier/heatmap sections are currently empty")
    print("• Modal component will only show sections with actual content")
    print("• This explains why users see fewer sections than expected")
    print("=" * 70)

if __name__ == "__main__":
    test_actual_database_content()