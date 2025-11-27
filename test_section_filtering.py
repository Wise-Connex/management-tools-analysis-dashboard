#!/usr/bin/env python3
"""
Test section filtering for single vs multi-source analysis.
"""

import sys
import os
import json
import sqlite3

# Add the dashboard_app to the path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

# Test the modal component directly
from key_findings.modal_component import KeyFindingsModal
import dash
from dash import html

def test_section_filtering():
    """Test that sections are properly filtered based on analysis type."""

    print("🧪 Testing Section Filtering for Single vs Multi-Source")
    print("=" * 60)

    # Create a mock Dash app
    app = dash.Dash(__name__)

    # Create modal component
    modal = KeyFindingsModal(app, None)

    # Test data for single source
    single_source_data = {
        "tool_name": "Benchmarking",
        "selected_sources": ["Google Trends"],
        "language": "es",
        "executive_summary": "Single source executive summary",
        "principal_findings": "Single source principal findings",
        "pca_analysis": "Single source PCA analysis",
        "heatmap_analysis": "Single source heatmap analysis",
        "analysis_type": "single_source",
        "confidence_score": 0.85,
        "model_used": "test_model"
    }

    # Test data for multi-source
    multi_source_data = {
        "tool_name": "Benchmarking",
        "selected_sources": ["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],
        "language": "es",
        "executive_summary": "Multi-source executive summary",
        "principal_findings": "Multi-source principal findings",
        "pca_analysis": "Multi-source PCA analysis",
        "heatmap_analysis": "Multi-source heatmap analysis",
        "analysis_type": "multi_source",
        "confidence_score": 0.92,
        "model_used": "test_model"
    }

    print("\n1️⃣ Testing Single Source Analysis:")
    single_result = modal.create_findings_display(single_source_data, "es")

    # Count sections by looking for H4 elements (section headers)
    section_count = 0
    heatmap_found = False
    pca_found = False

    def count_sections(element):
        nonlocal section_count, heatmap_found, pca_found
        if hasattr(element, 'children'):
            if isinstance(element.children, list):
                for child in element.children:
                    count_sections(child)
            else:
                count_sections(element.children)

        # Check if this is an H4 element with section title
        if hasattr(element, 'id') and element.id == 'h4':
            if 'Análisis de Correlación' in str(element.children):
                heatmap_found = True
            elif 'Análisis de Componentes Principales' in str(element.children):
                pca_found = True
            section_count += 1

    count_sections(single_result)

    print(f"   Expected sections: 3 (Executive Summary, Principal Findings, Metadata)")
    print(f"   Heatmap section found: {heatmap_found} (should be False)")
    print(f"   PCA section found: {pca_found} (should be False)")

    print("\n2️⃣ Testing Multi-Source Analysis:")
    multi_result = modal.create_findings_display(multi_source_data, "es")

    # Reset counters
    section_count = 0
    heatmap_found = False
    pca_found = False

    count_sections(multi_result)

    print(f"   Expected sections: 5 (all sections including heatmap and PCA)")
    print(f"   Heatmap section found: {heatmap_found} (should be True)")
    print(f"   PCA section found: {pca_found} (should be True)")

    print("\n" + "=" * 60)
    print("✅ Section filtering test complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_section_filtering()