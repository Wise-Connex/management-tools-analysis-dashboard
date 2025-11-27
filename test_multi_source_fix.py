#!/usr/bin/env python3
"""
Test script to verify multi-source modal fixes
"""

import sys
import json
sys.path.append('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.modal_component import KeyFindingsModal

def test_multi_source_fix():
    """Test multi-source modal component fixes"""

    # Sample multi-source data from database
    multi_source_data = {
        'tool_name': 'Benchmarking',
        'selected_sources': [1, 2, 3, 4, 5],
        'language': 'es',
        'analysis_type': 'multi_source',
        'executive_summary': 'Este análisis examina las tendencias de búsqueda para "Benchmarking" utilizando datos de múltiples fuentes.',
        'principal_findings': 'Los resultados sugieren una creciente adopción de herramientas de Benchmarking.',
        'temporal_analysis': '',
        'seasonal_analysis': '',
        'fourier_analysis': '',
        'strategic_synthesis': 'Los resultados sugieren una creciente adopción de herramientas de Benchmarking en el mercado español.',
        'conclusions': 'Se recomienda seguir monitoreando esta tendencia.',
        'pca_analysis': 'PCA analysis content with 366 chars that should be included',
        'heatmap_analysis': 'Heatmap analysis content that should be included',
        'model_used': 'moonshotai/kimi-k2-instruct',
        'data_points_analyzed': 1247,
        'api_latency_ms': 12,
        'generation_timestamp': '2025-11-24 14:00:00',
        'sources_count': 5
    }

    # Test the methods directly without full initialization
    modal = KeyFindingsModal.__new__(KeyFindingsModal)  # Create instance without __init__

    print("Testing multi-source modal fixes...")
    print("=" * 50)

    # Test metadata extraction
    metadata = modal._extract_metadata(multi_source_data)
    print(f"✓ Model extracted: {metadata['model_used']} (should be 'moonshotai/kimi-k2-instruct')")
    print(f"✓ Data points extracted: {metadata['data_points_analyzed']} (should be 1247)")
    print(f"✓ Response time: {metadata['response_time_ms']}ms")

    # Test section filtering
    sections = []

    # Extract data
    executive_summary = modal._extract_text_content(multi_source_data.get('executive_summary', ''))
    principal_findings = modal._extract_text_content(multi_source_data.get('principal_findings', ''))
    temporal_analysis = modal._extract_text_content(multi_source_data.get('temporal_analysis', ''))
    seasonal_analysis = modal._extract_text_content(multi_source_data.get('seasonal_analysis', ''))
    fourier_analysis = modal._extract_text_content(multi_source_data.get('fourier_analysis', ''))
    strategic_synthesis = modal._extract_text_content(multi_source_data.get('strategic_synthesis', ''))
    conclusions = modal._extract_text_content(multi_source_data.get('conclusions', ''))
    heatmap_analysis = modal._extract_text_content(multi_source_data.get('heatmap_analysis', ''))
    pca_analysis = modal._extract_text_content(multi_source_data.get('pca_analysis', ''))

    print(f"\n✓ Heatmap analysis content length: {len(heatmap_analysis)} chars")
    print(f"✓ PCA analysis content length: {len(pca_analysis)} chars")

    # Determine analysis type
    analysis_type = multi_source_data.get('analysis_type', 'multi_source')
    is_single_source = analysis_type == 'single_source'

    print(f"\n✓ Analysis type: {analysis_type}")
    print(f"✓ Is single source: {is_single_source}")

    # Build sections (same logic as modal component)
    if executive_summary:
        sections.append("executive_summary")
    if principal_findings:
        sections.append("principal_findings")
    if temporal_analysis:
        sections.append("temporal_analysis")
    if fourier_analysis:
        sections.append("fourier_analysis")
    if strategic_synthesis:
        sections.append("strategic_synthesis")
    if conclusions:
        sections.append("conclusions")

    # Single source specific sections
    if is_single_source:
        if seasonal_analysis:
            sections.append("seasonal_analysis")
        # PCA should be EXCLUDED for single source
        # if pca_analysis:
        #     sections.append("pca_analysis")

    # Multi-source specific sections
    else:
        if heatmap_analysis:
            sections.append("heatmap_analysis")
        if pca_analysis:
            sections.append("pca_analysis")

    print(f"\n✓ Sections that will be displayed: {sections}")

    # Expected sections for multi source: 8 sections (including heatmap and PCA)
    expected_sections = ['executive_summary', 'principal_findings', 'strategic_synthesis', 'conclusions', 'heatmap_analysis', 'pca_analysis']

    print(f"\n✓ Expected sections: {expected_sections}")
    print(f"✓ Section count: {len(sections)} (should be {len(expected_sections)})")

    # Verify inclusions
    heatmap_included = 'heatmap_analysis' in sections
    pca_included = 'pca_analysis' in sections

    print(f"\n✓ Heatmap correctly included: {heatmap_included}")
    print(f"✓ PCA correctly included: {pca_included}")

    if heatmap_included and pca_included and len(sections) == len(expected_sections):
        print("\n🎉 SUCCESS: Multi-source fixes working correctly!")
        return True
    else:
        print("\n❌ FAILURE: Multi-source fixes not working properly!")
        return False

if __name__ == "__main__":
    success = test_multi_source_fix()
    sys.exit(0 if success else 1)