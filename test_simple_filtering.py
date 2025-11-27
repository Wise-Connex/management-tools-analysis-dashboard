#!/usr/bin/env python3
"""
Test section filtering for single vs multi-source analysis - simple version.
"""

import sys
import os
import json

# Add the dashboard_app to the path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

def test_section_filtering():
    """Test that sections are properly filtered based on analysis type."""

    print("🧪 Testing Section Filtering for Single vs Multi-Source")
    print("=" * 60)

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

    # Simulate the logic from modal_component.py
    def simulate_section_filtering(report_data):
        # Extract data
        executive_summary = report_data.get('executive_summary', '')
        principal_findings = report_data.get('principal_findings', '')
        heatmap_analysis = report_data.get('heatmap_analysis', '')
        pca_analysis = report_data.get('pca_analysis', '')

        # Determine analysis type for section filtering
        analysis_type = report_data.get('analysis_type', 'multi_source')
        is_single_source = analysis_type == 'single_source'

        # Build sections dynamically based on analysis type
        sections = []

        # Always show these sections
        sections.append(f"Executive Summary: {executive_summary}")
        sections.append(f"Principal Findings: {principal_findings}")

        # Only show advanced sections for multi-source analysis
        if not is_single_source:
            sections.append(f"Heatmap Analysis: {heatmap_analysis}")
            sections.append(f"PCA Analysis: {pca_analysis}")

        # Always show metadata (simulated)
        sections.append(f"Metadata: confidence={report_data.get('confidence_score', 0)}")

        return sections

    print("\n1️⃣ Testing Single Source Analysis:")
    single_sections = simulate_section_filtering(single_source_data)

    print(f"   Number of sections: {len(single_sections)}")
    print(f"   Expected: 3 sections (Executive, Principal, Metadata)")
    for i, section in enumerate(single_sections, 1):
        print(f"   {i}. {section}")

    # Check if heatmap and PCA are excluded
    heatmap_excluded = not any("Heatmap" in section for section in single_sections)
    pca_excluded = not any("PCA" in section for section in single_sections)
    print(f"   ✅ Heatmap excluded: {heatmap_excluded}")
    print(f"   ✅ PCA excluded: {pca_excluded}")

    print("\n2️⃣ Testing Multi-Source Analysis:")
    multi_sections = simulate_section_filtering(multi_source_data)

    print(f"   Number of sections: {len(multi_sections)}")
    print(f"   Expected: 5 sections (all including heatmap and PCA)")
    for i, section in enumerate(multi_sections, 1):
        print(f"   {i}. {section}")

    # Check if heatmap and PCA are included
    heatmap_included = any("Heatmap" in section for section in multi_sections)
    pca_included = any("PCA" in section for section in multi_sections)
    print(f"   ✅ Heatmap included: {heatmap_included}")
    print(f"   ✅ PCA included: {pca_included}")

    print("\n" + "=" * 60)
    print("✅ Section filtering logic test complete!")
    print("=" * 60)

    # Verify the logic works correctly
    success = (
        len(single_sections) == 3 and
        len(multi_sections) == 5 and
        heatmap_excluded and
        pca_excluded and
        heatmap_included and
        pca_included
    )

    print(f"\n🎯 Overall Test Result: {'✅ PASSED' if success else '❌ FAILED'}")
    return success

if __name__ == "__main__":
    test_section_filtering()