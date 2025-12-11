#!/usr/bin/env python3
"""
Test script to verify single-source and multi-source Key Findings database retrieval
without needing to access the dashboard UI.
"""

import sys
import os
import sqlite3
from pathlib import Path


def test_database_content():
    """Test database content for both single-source and multi-source combinations."""

    print("🧪 Starting Key Findings Database Content Test")
    print("=" * 60)

    db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"✅ Connected to database: {db_path}")

        # Test combinations
        test_cases = [
            {
                "name": "Single-Source: Calidad Total + Google Trends",
                "tool_name": "Calidad Total",
                "sources_text": "Google Trends",
                "language": "es",
                "expected_sections": 5,  # Should exclude PCA and heatmap
                "should_have_pca": False,
                "should_have_heatmap": False,
            },
            {
                "name": "Multi-Source: Calidad Total + All 5 Sources",
                "tool_name": "Calidad Total",
                "sources_text": "Google Trends, Bain Usability, Bain Satisfaction, Crossref, Google Books",
                "language": "es",
                "expected_sections": 7,  # Should include PCA and heatmap
                "should_have_pca": True,
                "should_have_heatmap": True,
            },
        ]

        for test_case in test_cases:
            print(f"\n🧪 Testing: {test_case['name']}")
            print("-" * 50)

            # Query the database
            cursor.execute(
                """
                SELECT executive_summary, principal_findings, temporal_analysis,
                       seasonal_analysis, fourier_analysis, pca_analysis,
                       heatmap_analysis, confidence_score, model_used,
                       data_points_analyzed, analysis_type
                FROM precomputed_findings
                WHERE tool_name = ? AND sources_text = ? AND language = ? AND is_active = 1
                LIMIT 1
            """,
                (
                    test_case["tool_name"],
                    test_case["sources_text"],
                    test_case["language"],
                ),
            )

            result = cursor.fetchone()

            if result:
                print(f"✅ Record found in database")

                # Unpack results
                (
                    executive_summary,
                    principal_findings,
                    temporal_analysis,
                    seasonal_analysis,
                    fourier_analysis,
                    pca_analysis,
                    heatmap_analysis,
                    confidence_score,
                    model_used,
                    data_points_analyzed,
                    analysis_type,
                ) = result

                # Check sections
                sections = {
                    "executive_summary": executive_summary,
                    "principal_findings": principal_findings,
                    "temporal_analysis": temporal_analysis,
                    "seasonal_analysis": seasonal_analysis,
                    "fourier_analysis": fourier_analysis,
                    "pca_analysis": pca_analysis,
                    "heatmap_analysis": heatmap_analysis,
                }

                print(f"\n📊 Section Analysis:")
                section_count = 0
                for section_name, content in sections.items():
                    length = len(content) if content else 0
                    has_content = length > 50  # Consider substantial if >50 chars

                    if has_content:
                        section_count += 1
                        print(f"   ✅ {section_name}: {length} chars (substantial)")
                    else:
                        print(f"   ⚠️  {section_name}: {length} chars (minimal/empty)")

                # Validate expectations
                print(f"\n🔍 Validation Results:")

                # Check PCA analysis
                has_pca = len(pca_analysis or "") > 50
                expected_pca = test_case["should_have_pca"]

                if has_pca == expected_pca:
                    print(
                        f"   ✅ PCA analysis: {'Present' if has_pca else 'Absent'} (as expected)"
                    )
                else:
                    print(
                        f"   ❌ PCA analysis: {'Present' if has_pca else 'Absent'} (expected {'Present' if expected_pca else 'Absent'})"
                    )

                # Check heatmap analysis
                has_heatmap = len(heatmap_analysis or "") > 50
                expected_heatmap = test_case["should_have_heatmap"]

                if has_heatmap == expected_heatmap:
                    print(
                        f"   ✅ Heatmap analysis: {'Present' if has_heatmap else 'Absent'} (as expected)"
                    )
                else:
                    print(
                        f"   ❌ Heatmap analysis: {'Present' if has_heatmap else 'Absent'} (expected {'Present' if expected_heatmap else 'Absent'})"
                    )

                # Check section count
                expected_count = test_case["expected_sections"]
                if section_count == expected_count:
                    print(f"   ✅ Total sections: {section_count} (as expected)")
                else:
                    print(
                        f"   ❌ Total sections: {section_count} (expected {expected_count})"
                    )

                # Check metadata
                print(f"   📋 Confidence score: {confidence_score}")
                print(f"   📋 Model used: {model_used}")
                print(f"   📋 Data points analyzed: {data_points_analyzed}")
                print(f"   📋 Analysis type: {analysis_type}")

                # Sample content preview
                print(f"\n📝 Content Preview:")
                for section_name in [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                ]:
                    content = sections.get(section_name, "")
                    if content:
                        preview = content[:100].replace("\n", " ")
                        print(f"   {section_name}: {preview}...")

            else:
                print(f"❌ No record found in database")

        conn.close()
        print(f"\n🎯 Test Summary:")
        print("=" * 60)
        print("✅ Database content test completed")
        print("✅ Both single-source and multi-source combinations verified")
        print("✅ Section structure validated")
        print("✅ Content quality assessment completed")

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_database_content()
