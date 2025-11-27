#!/usr/bin/env python3
"""
Debug script to examine the complete Kimi K2 response structure.
"""

import asyncio
import sys
import json

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

async def debug_kimi_k2_response():
    """Debug the complete Kimi K2 response structure."""

    print("🔍 DEBUG: Complete Kimi K2 Response Structure")
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

    print("\n🤖 CALLING KIMI K2 MODEL...")
    try:
        # Force Kimi K2 model specifically
        response = await ai_service.generate_analysis(
            prompt=prompt,
            language="es",
            model="moonshotai/kimi-k2-instruct"
        )

        print(f"✅ Kimi K2 response received")
        print(f"📊 Response type: {type(response)}")
        print(f"📏 Response length: {len(str(response))} characters")

        # Check which model was actually used
        actual_model = response.get('model_used', 'unknown')
        print(f"🤖 Actually used model: {actual_model}")

        # Examine the complete raw response structure
        print(f"\n🔍 COMPLETE RAW RESPONSE STRUCTURE:")
        print("=" * 80)

        # Print the complete raw JSON
        print(json.dumps(response, indent=2, ensure_ascii=False))

        # Also check what's in the content
        if isinstance(response, dict) and "content" in response:
            content = response["content"]
            print(f"\n📋 CONTENT ANALYSIS:")
            print(f"Content type: {type(content)}")
            if isinstance(content, dict):
                print(f"Content keys: {list(content.keys())}")
                for key, value in content.items():
                    if isinstance(value, (str, int, float, bool)):
                        print(f"  {key}: {value}")
                    elif isinstance(value, list):
                        print(f"  {key}: [list with {len(value)} items]")
                    elif isinstance(value, dict):
                        print(f"  {key}: [dict with {len(value)} keys]")
                    else:
                        print(f"  {key}: {type(value)}")

        print("\n" + "=" * 80)
        print("✅ KIMI K2 RESPONSE ANALYSIS COMPLETE!")

        return 0

    except Exception as e:
        print(f"❌ Error with Kimi K2: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(debug_kimi_k2_response())
    sys.exit(exit_code)