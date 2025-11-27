#!/usr/bin/env python3
"""
Debug JSON extraction of PCA content
"""

import json

def debug_json_extraction():
    """Debug JSON extraction of PCA content"""

    # Actual PCA content from database
    pca_json_content = '{"analysis": {"dominant_patterns": [{"component": 1, "loadings": {"Google Trends": 0.8, "Google Books": 0.7, "Bain Usability": 0.6, "Bain Satisfaction": 0.5, "Crossref": 0.9}}], "total_variance_explained": 0.75}}'

    print("Debugging JSON extraction of PCA content...")
    print("=" * 60)

    print(f"✓ Raw JSON content: {pca_json_content}")
    print(f"✓ JSON content length: {len(pca_json_content)} chars")

    # Simulate the extraction method
    def extract_text_content(content):
        """Simulate the _extract_text_content method"""
        if isinstance(content, str):
            # Check if it's JSON formatted
            if content.strip().startswith('{') and content.strip().endswith('}'):
                try:
                    json_data = json.loads(content)
                    if isinstance(json_data, dict):
                        # Look for common text fields - prioritize heatmap_analysis for new structure
                        for field in ['executive_summary', 'principal_findings', 'heatmap_analysis', 'pca_analysis', 'bullet_point', 'analysis']:
                            if field in json_data and isinstance(json_data[field], str):
                                return json_data[field]
                except:
                    pass
            return content
        elif isinstance(content, dict):
            # Extract from dictionary - prioritize heatmap_analysis for new structure
            for field in ['executive_summary', 'principal_findings', 'heatmap_analysis', 'pca_analysis', 'bullet_point', 'analysis']:
                if field in content and isinstance(content[field], str):
                    return content[field]

        return str(content) if content else ''

    # Test extraction
    extracted_content = extract_text_content(pca_json_content)
    print(f"✓ Extracted content: '{extracted_content}'")
    print(f"✓ Extracted content length: {len(extracted_content)} chars")

    # Test if it's empty
    if extracted_content:
        print("✓ Content was successfully extracted")
    else:
        print("✗ Content extraction failed - result is empty")

    # Let's manually parse and see what happens
    try:
        json_data = json.loads(pca_json_content)
        print(f"✓ Parsed JSON: {json_data}")
        print(f"✓ JSON type: {type(json_data)}")

        # Check the fields the extraction method looks for
        fields_to_check = ['executive_summary', 'principal_findings', 'heatmap_analysis', 'pca_analysis', 'bullet_point', 'analysis']

        for field in fields_to_check:
            if field in json_data:
                field_content = json_data[field]
                print(f"✓ Field '{field}' found: {field_content} (type: {type(field_content)})")
                if isinstance(field_content, str):
                    print(f"  → This field would be extracted!")
                    print(f"  → Extracted value: '{field_content}'")
                else:
                    print(f"  → This field would NOT be extracted (not a string)")
            else:
                print(f"✗ Field '{field}' not found")

    except Exception as e:
        print(f"✗ JSON parsing failed: {e}")

    # The issue is clear: 'analysis' contains an object, not a string
    # The extraction method only extracts STRING values, not objects

    print("\n" + "="*60)
    print("ISSUE IDENTIFIED:")
    print("The PCA content in database is stored as JSON with nested objects.")
    print("The extraction method only extracts STRING values from JSON.")
    print("Since 'analysis' contains an object (not a string), nothing is extracted.")
    print("This results in empty content, causing 'No PCA analysis available' message.")

    return len(extracted_content) > 0

if __name__ == "__main__":
    success = debug_json_extraction()
    sys.exit(0 if success else 1)