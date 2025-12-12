#!/usr/bin/env python3
"""
Test the JSON extraction fix for PCA content
"""

import json
import sys
sys.path.append('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.modal_component import KeyFindingsModal

def test_json_extraction_fix():
    """Test the JSON extraction fix for PCA content"""

    # Actual PCA content from database
    pca_json_content = '{"analysis": {"dominant_patterns": [{"component": 1, "loadings": {"Google Trends": 0.8, "Google Books": 0.7, "Bain Usability": 0.6, "Bain Satisfaction": 0.5, "Crossref": 0.9}}], "total_variance_explained": 0.75}}'

    # Test the methods directly without full initialization
    modal = KeyFindingsModal.__new__(KeyFindingsModal)  # Create instance without __init__

    print("Testing JSON extraction fix for PCA content...")
    print("=" * 60)

    print(f"✓ Raw JSON content: {pca_json_content[:100]}...")
    print(f"✓ JSON content length: {len(pca_json_content)} chars")

    # Test extraction
    extracted_content = modal._extract_text_content(pca_json_content)
    print(f"✓ Extracted content: '{extracted_content}'")
    print(f"✓ Extracted content length: {len(extracted_content)} chars")

    # Test if it's empty
    if extracted_content:
        print("✓ Content was successfully extracted")
        print("✓ Content is now in narrative format, not raw JSON!")
    else:
        print("✗ Content extraction failed - result is empty")
        return False

    # Test the JSON to narrative conversion directly
    print("\n" + "="*40)
    print("Testing JSON to narrative conversion...")

    json_data = json.loads(pca_json_content)
    narrative_content = modal._convert_json_to_narrative(json_data)
    print(f"✓ Narrative content: '{narrative_content}'")
    print(f"✓ Narrative content length: {len(narrative_content)} chars")

    # Test paragraph splitting (as used in PCA section creation)
    paragraphs = [p.strip() for p in narrative_content.split('\n\n') if p.strip()]
    print(f"✓ Paragraphs after splitting: {len(paragraphs)}")
    for i, para in enumerate(paragraphs, 1):
        print(f"  Paragraph {i}: {para[:80]}...")

    # Test with empty content
    empty_json = '{"analysis": {}}'
    empty_extracted = modal._extract_text_content(empty_json)
    print(f"\n✓ Empty JSON extraction: '{empty_extracted}'")

    if len(extracted_content) > 0 and "Componentes Principales" in extracted_content:
        print("\n🎉 SUCCESS: JSON extraction fix is working correctly!")
        print("✓ PCA content will now display as narrative instead of 'No PCA analysis available'")
        return True
    else:
        print("\n❌ FAILURE: JSON extraction fix is not working properly!")
        return False

if __name__ == "__main__":
    success = test_json_extraction_fix()
    sys.exit(0 if success else 1)