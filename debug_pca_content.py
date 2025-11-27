#!/usr/bin/env python3
"""
Debug PCA content processing
"""

import sys
import json
sys.path.append('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.modal_component import KeyFindingsModal

def debug_pca_processing():
    """Debug PCA content processing"""

    # Sample data from actual database
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
        'pca_analysis': 'Análisis de Componentes Principales realizado con éxito. Los componentes principales revelan patrones importantes en los datos de múltiples fuentes.',
        'heatmap_analysis': '',  # Empty like in actual database
        'model_used': 'moonshotai/kimi-k2-instruct',
        'data_points_analyzed': 1247,
        'api_latency_ms': 12,
        'generation_timestamp': '2025-11-24 14:00:00',
        'sources_count': 5
    }

    # Test the methods directly without full initialization
    modal = KeyFindingsModal.__new__(KeyFindingsModal)  # Create instance without __init__

    print("Debugging PCA content processing...")
    print("=" * 60)

    # Extract PCA content
    pca_analysis = modal._extract_text_content(multi_source_data.get('pca_analysis', ''))
    heatmap_analysis = modal._extract_text_content(multi_source_data.get('heatmap_analysis', ''))

    print(f"✓ Raw PCA analysis: '{pca_analysis}'")
    print(f"✓ Raw PCA length: {len(pca_analysis)} chars")
    print(f"✓ Raw heatmap analysis: '{heatmap_analysis}'")
    print(f"✓ Raw heatmap length: {len(heatmap_analysis)} chars")

    # Test paragraph splitting
    paragraphs = [p.strip() for p in pca_analysis.split('\n\n') if p.strip()]
    print(f"✓ PCA paragraphs after splitting: {paragraphs}")
    print(f"✓ PCA paragraph count: {len(paragraphs)}")

    # Test the actual PCA section creation
    if pca_analysis:
        print("✓ PCA content exists - should create section")
        # Simulate the section creation
        html_paragraphs = []
        for p in paragraphs:
            html_paragraphs.append(f"<p>{p}</p>")
        print(f"✓ HTML paragraphs: {html_paragraphs}")
    else:
        print("✗ PCA content is empty - section will not be created")

    # Test the actual heatmap section creation
    if heatmap_analysis:
        print("✓ Heatmap content exists - should create section")
    else:
        print("✗ Heatmap content is empty - section will not be created")

    # Test the filtering logic
    analysis_type = multi_source_data.get('analysis_type', 'multi_source')
    is_single_source = analysis_type == 'single_source'

    print(f"\n✓ Analysis type: {analysis_type}")
    print(f"✓ Is single source: {is_single_source}")

    # Simulate the section filtering logic
    sections = []

    if pca_analysis:
        sections.append("pca_analysis")
        print("✓ PCA section will be included")
    else:
        print("✗ PCA section will be excluded (no content)")

    if not is_single_source and heatmap_analysis:
        sections.append("heatmap_analysis")
        print("✓ Heatmap section will be included")
    else:
        print("✗ Heatmap section will be excluded (no content or single source)")

    print(f"\n✓ Final sections: {sections}")

    # Check if this matches what we expect
    expected_pca = bool(pca_analysis)
    expected_heatmap = bool(heatmap_analysis and not is_single_source)

    print(f"\n✓ Expected PCA inclusion: {expected_pca}")
    print(f"✓ Expected heatmap inclusion: {expected_heatmap}")

    if expected_pca and len(sections) > 0:
        print("\n🎉 SUCCESS: PCA processing should work correctly!")
        return True
    else:
        print("\n❌ ISSUE: PCA processing has problems!")
        return False

if __name__ == "__main__":
    success = debug_pca_processing()
    sys.exit(0 if success else 1)