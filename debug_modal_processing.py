#!/usr/bin/env python3
"""
Debug the modal component data processing step by step.
"""

import sys
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

def debug_modal_processing():
    """Debug modal component data processing."""

    print("🔍 DEBUGGING MODAL COMPONENT PROCESSING")
    print("=" * 70)

    # Simulate the data that would come from the database
    test_data_single = {
        'tool_name': 'Benchmarking',
        'selected_sources': ['Google Trends'],
        'language': 'es',
        'executive_summary': 'El análisis temporal integral de Benchmarking a través de Google Trends (1950-2023) revela un ciclo de vida maduro con patrones estacionales estables y ciclos espectrales bien definidos.',
        'principal_findings': '',
        'temporal_analysis': '',
        'seasonal_analysis': '',
        'fourier_analysis': '',
        'strategic_synthesis': '',
        'conclusions': '',
        'heatmap_analysis': '',
        'pca_analysis': '',
        'analysis_type': 'single_source',
        'confidence_score': 0.89,
        'model_used': 'gpt-4',
        'data_points_analyzed': 2847
    }

    test_data_multi = {
        'tool_name': 'Benchmarking',
        'selected_sources': ['Google Trends', 'Google Books', 'Bain Usability', 'Bain Satisfaction', 'Crossref'],
        'language': 'es',
        'executive_summary': 'El análisis multi-fuente del Benchmarking revela una desconexión crítica entre la percepción pública, la práctica empresarial y la investigación académica.',
        'principal_findings': 'Durante siete décadas, el Benchmarking ha evolucionado desde una herramienta operativa hasta un imperativo estratégico.',
        'temporal_analysis': '',
        'seasonal_analysis': '',
        'fourier_analysis': '',
        'strategic_synthesis': '',
        'conclusions': '',
        'heatmap_analysis': '',
        'pca_analysis': 'El análisis de componentes principales identifica tres fuerzas dominantes: la narrativa de mejora continua liderada por la industria.',
        'analysis_type': 'multi_source',
        'confidence_score': 0.92,
        'model_used': 'moonshotai/kimi-k2-instruct',
        'data_points_analyzed': 1247
    }

    # Import the modal component
    from key_findings.modal_component import KeyFindingsModal
    import dash

    # Create a minimal Dash app for testing
    app = dash.Dash(__name__)
    modal = KeyFindingsModal(app, None)

    print("\n1️⃣ Testing Single Source Modal Processing:")
    print(f"   Input analysis_type: {test_data_single['analysis_type']}")
    print(f"   Input model_used: {test_data_single['model_used']}")
    print(f"   Input data_points_analyzed: {test_data_single['data_points_analyzed']}")

    # Test the data extraction process
    executive_summary = modal._extract_text_content(test_data_single.get('executive_summary', ''))
    principal_findings = modal._extract_text_content(test_data_single.get('principal_findings', ''))
    temporal_analysis = modal._extract_text_content(test_data_single.get('temporal_analysis', ''))
    seasonal_analysis = modal._extract_text_content(test_data_single.get('seasonal_analysis', ''))
    fourier_analysis = modal._extract_text_content(test_data_single.get('fourier_analysis', ''))
    strategic_synthesis = modal._extract_text_content(test_data_single.get('strategic_synthesis', ''))
    conclusions = modal._extract_text_content(test_data_single.get('conclusions', ''))
    heatmap_analysis = modal._extract_text_content(test_data_single.get('heatmap_analysis', ''))
    pca_analysis = modal._extract_text_content(test_data_single.get('pca_analysis', ''))

    print(f"   Extracted Data:")
    print(f"     Executive Summary: {len(executive_summary)} chars")
    print(f"     Principal Findings: {len(principal_findings)} chars")
    print(f"     Temporal Analysis: {len(temporal_analysis)} chars")
    print(f"     Seasonal Analysis: {len(seasonal_analysis)} chars")
    print(f"     Fourier Analysis: {len(fourier_analysis)} chars")
    print(f"     Strategic Synthesis: {len(strategic_synthesis)} chars")
    print(f"     Conclusions: {len(conclusions)} chars")
    print(f"     Heatmap Analysis: {len(heatmap_analysis)} chars")
    print(f"     PCA Analysis: {len(pca_analysis)} chars")

    # Test section filtering logic
    analysis_type = test_data_single.get('analysis_type', 'multi_source')
    is_single_source = analysis_type == 'single_source'

    print(f"   Analysis Type: {analysis_type}")
    print(f"   Is Single Source: {is_single_source}")

    # Simulate section building
    sections = []

    if executive_summary:
        sections.append("Executive Summary")
    if principal_findings:
        sections.append("Principal Findings")
    if temporal_analysis:
        sections.append("Temporal Analysis")
    if fourier_analysis:
        sections.append("Fourier Analysis")
    if strategic_synthesis:
        sections.append("Strategic Synthesis")
    if conclusions:
        sections.append("Conclusions")

    # Single source specific sections
    if is_single_source:
        if seasonal_analysis:
            sections.append("Seasonal Analysis")
        if pca_analysis:
            sections.append("PCA Analysis")

    # Multi-source specific sections
    else:
        if heatmap_analysis:
            sections.append("Heatmap Analysis")
        if pca_analysis:
            sections.append("PCA Analysis")

    print(f"   Sections to display: {sections}")

    print("\n2️⃣ Testing Multi-Source Modal Processing:")
    print(f"   Input analysis_type: {test_data_multi['analysis_type']}")
    print(f"   Input model_used: {test_data_multi['model_used']}")
    print(f"   Input data_points_analyzed: {test_data_multi['data_points_analyzed']}")

    # Test metadata extraction
    metadata = modal._extract_metadata(test_data_multi)
    print(f"   Extracted Metadata:")
    for key, value in metadata.items():
        print(f"     {key}: {value}")

    print("\n3️⃣ Testing Content Extraction Issues:")

    # Test empty content handling
    empty_content = ""
    extracted_empty = modal._extract_text_content(empty_content)
    print(f"   Empty content extraction: '{extracted_empty}' (length: {len(extracted_empty)})")

    # Test None content handling
    none_content = None
    extracted_none = modal._extract_text_content(none_content)
    print(f"   None content extraction: '{extracted_none}' (length: {len(extracted_none)})")

    # Test JSON content handling
    json_content = '{"analysis": "test content", "data": "more content"}'
    extracted_json = modal._extract_text_content(json_content)
    print(f"   JSON content extraction: '{extracted_json[:50]}...' (length: {len(extracted_json)})")

    print("\n" + "=" * 70)
    print("🔍 Modal Processing Debug Complete!")
    print("=" * 70)

if __name__ == "__main__":
    debug_modal_processing()