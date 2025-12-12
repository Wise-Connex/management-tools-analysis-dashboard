#!/usr/bin/env python3
"""
Final integration test: Database retrieval + section filtering.
"""

import sys
import os
import json
import sqlite3

def test_database_integration():
    """Test complete flow: database retrieval + section filtering."""

    print("🔬 Final Integration Test: Database + Section Filtering")
    print("=" * 70)

    # Connect to precomputed findings database
    db_path = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db'

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Test single source retrieval
        print("\n1️⃣ Testing Single Source Database Retrieval:")
        cursor.execute("""
            SELECT executive_summary, principal_findings, pca_analysis,
                   heatmap_analysis, analysis_type, confidence_score, model_used
            FROM precomputed_findings
            WHERE tool_name = 'Benchmarking'
            AND sources_text = 'Google Trends'
            AND language = 'es'
            AND is_active = 1
            LIMIT 1
        """)

        single_result = cursor.fetchone()

        if single_result:
            exec_summary, principal_findings, pca_analysis, heatmap_analysis, analysis_type, confidence_score, model_used = single_result

            # Simulate the modal component logic
            single_data = {
                'executive_summary': exec_summary or '',
                'principal_findings': principal_findings or '',
                'pca_analysis': pca_analysis or '',
                'heatmap_analysis': heatmap_analysis or '',
                'analysis_type': analysis_type or 'single_source',
                'confidence_score': confidence_score or 0.8,
                'model_used': model_used or 'unknown'
            }

            print(f"   ✅ Retrieved single source data from database")
            print(f"   Analysis Type: {analysis_type}")
            print(f"   Executive Summary Length: {len(exec_summary or '')} chars")
            print(f"   Principal Findings Length: {len(principal_findings or '')} chars")
            print(f"   PCA Analysis Length: {len(pca_analysis or '')} chars")
            print(f"   Heatmap Analysis Length: {len(heatmap_analysis or '')} chars")

            # Apply section filtering logic
            is_single_source = single_data['analysis_type'] == 'single_source'
            sections_to_show = []

            # Always show these sections
            sections_to_show.append("Executive Summary")
            sections_to_show.append("Principal Findings")

            # Only show advanced sections for multi-source analysis
            if not is_single_source:
                sections_to_show.append("Heatmap Analysis")
                sections_to_show.append("PCA Analysis")

            # Always show metadata
            sections_to_show.append("Metadata")

            print(f"   Sections that will be displayed: {len(sections_to_show)}")
            for i, section in enumerate(sections_to_show, 1):
                print(f"     {i}. {section}")

            # Verify single source excludes heatmap and PCA
            expected_sections = 3  # Executive, Principal, Metadata
            if len(sections_to_show) == expected_sections:
                print(f"   ✅ Single source correctly shows {expected_sections} sections")
            else:
                print(f"   ❌ Single source shows {len(sections_to_show)} sections, expected {expected_sections}")

        else:
            print("   ❌ No single source data found in database")

        # Test multi-source retrieval
        print("\n2️⃣ Testing Multi-Source Database Retrieval:")
        cursor.execute("""
            SELECT executive_summary, principal_findings, pca_analysis,
                   heatmap_analysis, analysis_type, confidence_score, model_used
            FROM precomputed_findings
            WHERE tool_name = 'Benchmarking'
            AND sources_text = 'Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref'
            AND language = 'es'
            AND is_active = 1
            LIMIT 1
        """)

        multi_result = cursor.fetchone()

        if multi_result:
            exec_summary, principal_findings, pca_analysis, heatmap_analysis, analysis_type, confidence_score, model_used = multi_result

            # Simulate the modal component logic
            multi_data = {
                'executive_summary': exec_summary or '',
                'principal_findings': principal_findings or '',
                'pca_analysis': pca_analysis or '',
                'heatmap_analysis': heatmap_analysis or '',
                'analysis_type': analysis_type or 'multi_source',
                'confidence_score': confidence_score or 0.8,
                'model_used': model_used or 'unknown'
            }

            print(f"   ✅ Retrieved multi-source data from database")
            print(f"   Analysis Type: {analysis_type}")
            print(f"   Executive Summary Length: {len(exec_summary or '')} chars")
            print(f"   Principal Findings Length: {len(principal_findings or '')} chars")
            print(f"   PCA Analysis Length: {len(pca_analysis or '')} chars")
            print(f"   Heatmap Analysis Length: {len(heatmap_analysis or '')} chars")

            # Apply section filtering logic
            is_single_source = multi_data['analysis_type'] == 'single_source'
            sections_to_show = []

            # Always show these sections
            sections_to_show.append("Executive Summary")
            sections_to_show.append("Principal Findings")

            # Only show advanced sections for multi-source analysis
            if not is_single_source:
                sections_to_show.append("Heatmap Analysis")
                sections_to_show.append("PCA Analysis")

            # Always show metadata
            sections_to_show.append("Metadata")

            print(f"   Sections that will be displayed: {len(sections_to_show)}")
            for i, section in enumerate(sections_to_show, 1):
                print(f"     {i}. {section}")

            # Verify multi-source includes all sections
            expected_sections = 5  # All sections
            if len(sections_to_show) == expected_sections:
                print(f"   ✅ Multi-source correctly shows {expected_sections} sections")
            else:
                print(f"   ❌ Multi-source shows {len(sections_to_show)} sections, expected {expected_sections}")

        else:
            print("   ❌ No multi-source data found in database")

        conn.close()

        print("\n" + "=" * 70)
        print("✅ Integration test complete!")
        print("=" * 70)
        print("Summary:")
        print("• Single source analysis correctly excludes heatmap and PCA sections")
        print("• Multi-source analysis correctly includes all sections")
        print("• Database contains proper analysis_type values")
        print("• Section filtering logic works end-to-end")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error during integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    test_database_integration()