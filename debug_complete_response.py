#!/usr/bin/env python3
"""
Debug script to capture and display the COMPLETE AI response without truncation.
"""

import asyncio
import sys
import os
import json

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

async def debug_complete_response():
    """Generate and display the complete AI response with full debugging."""

    print("🔍 DEBUG: COMPLETE AI RESPONSE CAPTURE")
    print("=" * 80)
    print("Tool: Benchmarking")
    print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
    print("Language: Spanish")
    print("=" * 80)

    # Initialize services
    ai_service = UnifiedAIService()
    prompt_engineer = PromptEngineer(language="es")

    # Prepare test data
    test_data = {
        "tool_name": "Benchmarking",
        "selected_sources": ["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],
        "language": "es",
        "date_range_start": "1950-01-01",
        "date_range_end": "2023-12-31",
        "data_points_analyzed": 888,
        "pca_insights": {
            "dominant_patterns": [{"component": 1, "loadings": {"Google Trends": 0.8, "Google Books": 0.7, "Bain Usability": 0.6, "Bain Satisfaction": 0.5, "Crossref": 0.9}}],
            "total_variance_explained": 78.5
        },
        "heatmap_analysis": {"correlation_matrix": "sample_correlation_data"}
    }

    print("\n📝 GENERATING PROMPT...")
    prompt = prompt_engineer.create_analysis_prompt(test_data, {})
    print(f"✅ Prompt created: {len(prompt)} characters")

    # Show the complete prompt structure
    print(f"\n📋 COMPLETE PROMPT STRUCTURE:")
    print("-" * 50)
    lines = prompt.split('\n')
    section_num = 0
    for i, line in enumerate(lines):
        if line.startswith('**SECCIÓN') or line.startswith('**SECTION'):
            section_num += 1
            print(f"{section_num}. {line}")
        elif 'CONCLUSIONES' in line or 'CONCLUSIONS' in line:
            section_num += 1
            print(f"{section_num}. {line} (NEW)")

    print("\n🤖 CALLING AI SERVICE...")
    try:
        response = await ai_service.generate_analysis(
            prompt=prompt,
            language="es"
        )

        print(f"✅ AI response received")
        print(f"📊 Response type: {type(response)}")
        print(f"📏 Response length: {len(str(response))} characters")

        # Check if response has content structure
        if isinstance(response, dict):
            print(f"\n🔍 RESPONSE KEYS: {list(response.keys())}")

            if 'content' in response:
                content = response['content']
                print(f"\n📋 CONTENT KEYS: {list(content.keys()) if isinstance(content, dict) else 'Not a dict'}")

                if isinstance(content, dict):
                    # Check each section
                    sections_to_check = [
                        'executive_summary', 'principal_findings',
                        'pca_insights', 'pca_analysis', 'heatmap_analysis',
                        'temporal_analysis', 'seasonal_analysis', 'fourier_analysis',
                        'conclusions', 'strategic_recommendations'
                    ]

                    print(f"\n🔍 SECTION ANALYSIS:")
                    for section in sections_to_check:
                        if section in content:
                            section_content = content[section]
                            if isinstance(section_content, str):
                                word_count = len(section_content.split())
                                char_count = len(section_content)
                                print(f"  ✅ {section}: {word_count} words, {char_count} chars")
                                if char_count < 100:
                                    print(f"     ⚠️  WARNING: Very short content")
                            elif isinstance(section_content, list):
                                item_count = len(section_content)
                                print(f"  ✅ {section}: {item_count} items")
                            else:
                                print(f"  ✅ {section}: {type(section_content)}")
                        else:
                            print(f"  ❌ {section}: Missing")

            # Show the complete raw response
            print(f"\n📝 COMPLETE RAW RESPONSE:")
            print("=" * 80)
            print(json.dumps(response, indent=2, ensure_ascii=False))
            print("=" * 80)

        else:
            print(f"\n📝 RAW RESPONSE:")
            print(str(response))

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(debug_complete_response())
    sys.exit(exit_code)