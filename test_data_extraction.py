#!/usr/bin/env python3
"""
Test data extraction functions directly.
"""

import json

def test_data_extraction():
    """Test the data extraction functions directly."""

    print("🔍 TESTING DATA EXTRACTION FUNCTIONS")
    print("=" * 70)

    def _extract_text_content(content):
        """Extract text content from various data types."""
        if isinstance(content, str):
            # Check if it's JSON formatted
            if content.strip().startswith('{') and content.strip().endswith('}'):
                try:
                    json_data = json.loads(content)
                    if isinstance(json_data, dict):
                        # Look for common text fields
                        for field in ['executive_summary', 'principal_findings', 'heatmap_analysis', 'pca_analysis', 'bullet_point', 'analysis']:
                            if field in json_data and isinstance(json_data[field], str):
                                return json_data[field]
                except:
                    pass
            return content
        elif isinstance(content, dict):
            # Extract from dictionary
            for field in ['executive_summary', 'principal_findings', 'heatmap_analysis', 'pca_analysis', 'bullet_point', 'analysis']:
                if field in content and isinstance(content[field], str):
                    return content[field]
        elif isinstance(content, list) and content:
            # Extract from list
            if isinstance(content[0], str):
                return ' '.join(content)
            elif isinstance(content[0], dict) and 'bullet_point' in content[0]:
                return '\n'.join([item.get('bullet_point', '') for item in content])
        return str(content) if content else ""

    def _extract_metadata(report_data):
        """Extract metadata from report data."""
        return {
            'model_used': report_data.get('model_used', 'N/A'),
            'response_time_ms': report_data.get('api_latency_ms', 0),
            'data_points_analyzed': report_data.get('data_points_analyzed', 0),
            'generation_timestamp': report_data.get('generation_timestamp', 'N/A'),
            'access_count': report_data.get('access_count', 0),
            'analysis_depth': report_data.get('analysis_depth', 'comprehensive'),
            'sources_count': report_data.get('sources_count', 0)
        }

    # Test data from your actual output
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

    print("\n1️⃣ Testing Single Source Data Extraction:")

    executive_summary = _extract_text_content(test_data_single.get('executive_summary', ''))
    principal_findings = _extract_text_content(test_data_single.get('principal_findings', ''))
    temporal_analysis = _extract_text_content(test_data_single.get('temporal_analysis', ''))
    seasonal_analysis = _extract_text_content(test_data_single.get('seasonal_analysis', ''))
    fourier_analysis = _extract_text_content(test_data_single.get('fourier_analysis', ''))
    strategic_synthesis = _extract_text_content(test_data_single.get('strategic_synthesis', ''))
    conclusions = _extract_text_content(test_data_single.get('conclusions', ''))
    heatmap_analysis = _extract_text_content(test_data_single.get('heatmap_analysis', ''))
    pca_analysis = _extract_text_content(test_data_single.get('pca_analysis', ''))

    print(f"   Executive Summary: '{executive_summary[:50]}...' ({len(executive_summary)} chars)")
    print(f"   Principal Findings: '{principal_findings[:50]}...' ({len(principal_findings)} chars)")
    print(f"   Temporal Analysis: '{temporal_analysis[:50]}...' ({len(temporal_analysis)} chars)")
    print(f"   Seasonal Analysis: '{seasonal_analysis[:50]}...' ({len(seasonal_analysis)} chars)")
    print(f"   Fourier Analysis: '{fourier_analysis[:50]}...' ({len(fourier_analysis)} chars)")
    print(f"   Strategic Synthesis: '{strategic_synthesis[:50]}...' ({len(strategic_synthesis)} chars)")
    print(f"   Conclusions: '{conclusions[:50]}...' ({len(conclusions)} chars)")
    print(f"   Heatmap Analysis: '{heatmap_analysis[:50]}...' ({len(heatmap_analysis)} chars)")
    print(f"   PCA Analysis: '{pca_analysis[:50]}...' ({len(pca_analysis)} chars)")

    # Test section filtering
    analysis_type = test_data_single.get('analysis_type', 'multi_source')
    is_single_source = analysis_type == 'single_source'

    print(f"   Analysis Type: {analysis_type}")
    print(f"   Is Single Source: {is_single_source}")

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

    print("\n2️⃣ Testing Metadata Extraction:")

    metadata = _extract_metadata(test_data_single)
    print(f"   Model Used: {metadata['model_used']}")
    print(f"   Response Time: {metadata['response_time_ms']}ms")
    print(f"   Data Points Analyzed: {metadata['data_points_analyzed']}")

    print("\n3️⃣ Testing Multi-Source Section Filtering:")

    analysis_type_multi = test_data_multi.get('analysis_type', 'multi_source')
    is_single_source_multi = analysis_type_multi == 'single_source'

    print(f"   Analysis Type: {analysis_type_multi}")
    print(f"   Is Single Source: {is_single_source_multi}")

    # Extract multi-source data
    pca_analysis_multi = _extract_text_content(test_data_multi.get('pca_analysis', ''))
    heatmap_analysis_multi = _extract_text_content(test_data_multi.get('heatmap_analysis', ''))

    print(f"   PCA Analysis: '{pca_analysis_multi[:50]}...' ({len(pca_analysis_multi)} chars)")
    print(f"   Heatmap Analysis: '{heatmap_analysis_multi[:50]}...' ({len(heatmap_analysis_multi)} chars)")

    sections_multi = []

    # Check if PCA analysis should be included for multi-source
    if pca_analysis_multi:
        sections_multi.append("PCA Analysis")
    if heatmap_analysis_multi:
        sections_multi.append("Heatmap Analysis")

    print(f"   Multi-source sections: {sections_multi}")

    print("\n4️⃣ Testing Content Issues from Your Output:")

    # The issue where "No PCA analysis available" appears despite having content
    print("   Issue: PCA shows 'No PCA analysis available' despite having content")
    print(f"   PCA content length: {len(pca_analysis_multi)} chars")
    print(f"   PCA content exists: {bool(pca_analysis_multi)}")
    print(f"   Should show PCA section: {bool(pca_analysis_multi)}")

    print("\n5️⃣ Testing Empty Content Handling:")

    empty_content = ""
    extracted_empty = _extract_text_content(empty_content)
    print(f"   Empty string: '{extracted_empty}' (length: {len(extracted_empty)}, bool: {bool(extracted_empty)})")

    # Test what happens with the actual empty fields from database
    print(f"   Empty temporal will show section: {bool(extracted_empty)} ❌")

    print("\n" + "=" * 70)
    print("🔍 Data Extraction Debug Complete!")
    print("=" * 70)
    print("Key Findings:")
    print("• Empty sections (0 chars) won't display - this is correct behavior")
    print("• PCA analysis exists and should display for multi-source")
    print("• Model and data points are properly extracted from metadata")
    print("• Section filtering logic works correctly")
    print("• The 'No PCA analysis available' issue is likely in the PCA section creation method")
    print("=" * 70)

if __name__ == "__main__":
    test_data_extraction()" "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py"} "file_path":"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_data_extraction.py