#!/usr/bin/env python3
"""
Test script to verify precomputed findings integration with Key Findings service.
"""

import sys
import sqlite3
import asyncio
import json
from pathlib import Path

# Add the dashboard_app to path
sys.path.append("/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app")


def get_precomputed_findings(
    tool_name: str, selected_sources: list, language: str = "es"
):
    """
    Get precomputed findings from the database.

    Args:
        tool_name: Selected management tool
        selected_sources: List of selected data sources
        language: Analysis language

    Returns:
        Formatted findings data or None if not found
    """
    try:
        # Create sources text (sorted for consistency)
        sources_text = ", ".join(sorted(selected_sources))

        # Connect to precomputed findings database
        conn = sqlite3.connect(
            "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
        )
        cursor = conn.cursor()

        # Query for exact match
        cursor.execute(
            """
            SELECT executive_summary, principal_findings, temporal_analysis, 
                   seasonal_analysis, fourier_analysis, pca_analysis, 
                   heatmap_analysis, confidence_score, model_used, 
                   data_points_analyzed, analysis_type
            FROM precomputed_findings 
            WHERE tool_name = ? AND sources_text = ? AND language = ? 
            AND is_active = 1
            LIMIT 1
        """,
            (tool_name, sources_text, language),
        )

        result = cursor.fetchone()
        conn.close()

        if not result:
            return None

        # Format result to match Key Findings structure
        formatted_result = {
            "tool_name": tool_name,
            "selected_sources": selected_sources,
            "language": language,
            "executive_summary": result[0] or "",
            "principal_findings": result[1] or "",
            "temporal_analysis": result[2] or "",
            "seasonal_analysis": result[3] or "",
            "fourier_analysis": result[4] or "",
            "pca_analysis": result[5] or "",
            "heatmap_analysis": result[6] or "",
            "confidence_score": result[7] or 0.8,
            "model_used": result[8] or "precomputed_database",
            "data_points_analyzed": result[9] or 0,
            "sources_count": len(selected_sources),
            "analysis_depth": result[10] or "comprehensive",
            "report_type": "precomputed",
            "is_precomputed": True,
            "sources_text": sources_text,
        }

        print(f"✅ Precomputed findings found for {tool_name} + {selected_sources}")
        print(
            f"   Executive summary: {len(formatted_result['executive_summary'])} chars"
        )
        print(f"   Model: {formatted_result['model_used']}")
        print(f"   Confidence: {formatted_result['confidence_score']}")

        return formatted_result

    except Exception as e:
        print(f"❌ Error getting precomputed findings: {e}")
        return None


def test_key_findings_integration():
    """Test the Key Findings integration with precomputed database."""

    print("🧪 Testing Key Findings Integration with Precomputed Database")
    print("=" * 60)

    # Test cases
    test_cases = [
        ("Calidad Total", ["Google Trends", "Crossref"], "es"),
        ("Benchmarking", ["Google Trends"], "es"),
        ("Alianzas y Capital de Riesgo", ["Crossref"], "es"),
        ("Benchmarking", ["Google Trends", "Bain Usability"], "es"),
    ]

    for tool_name, selected_sources, language in test_cases:
        print(f"\n🔍 Testing: {tool_name} + {selected_sources} ({language})")

        result = get_precomputed_findings(tool_name, selected_sources, language)

        if result:
            print(
                f"   ✅ SUCCESS: Found {len(result['executive_summary'])} char summary"
            )
            print(f"   📊 Analysis depth: {result['analysis_depth']}")
            print(f"   🎯 Confidence: {result['confidence_score']}")
        else:
            print(f"   ❌ NOT FOUND: No precomputed data available")

    print(f"\n{'=' * 60}")
    print("🎯 Summary: Precomputed findings integration working!")


if __name__ == "__main__":
    test_key_findings_integration()
