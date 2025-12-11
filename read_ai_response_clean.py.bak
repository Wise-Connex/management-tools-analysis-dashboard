#!/usr/bin/env python3
"""
Clean script to display the complete AI response for Benchmarking + 5 sources.
"""

import asyncio
import sys
import os

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

async def read_complete_ai_response():
    """Generate and display the complete AI response."""

    print("📖 COMPLETE AI ANALYSIS: BENCHMARKING + 5 SOURCES")
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

    print("\n🤖 CALLING AI SERVICE...")
    try:
        response = await ai_service.generate_analysis(
            prompt=prompt,
            language="es"
        )

        print(f"✅ AI response received")
        print(f"📊 Response type: {type(response)}")
        print(f"📏 Response length: {len(str(response))} characters\n")

        # Display the complete response in clean format
        print("🎯 COMPLETE AI ANALYSIS:")
        print("=" * 80)
        print()

        if isinstance(response, dict) and "content" in response:
            content = response["content"]

            # EXECUTIVE SUMMARY
            if "executive_summary" in content and content["executive_summary"]:
                print("📋 EXECUTIVE SUMMARY")
                print("-" * 50)
                print(content["executive_summary"])
                print()

            # PRINCIPAL FINDINGS
            if "principal_findings" in content and content["principal_findings"]:
                print("📊 PRINCIPAL FINDINGS")
                print("-" * 50)
                findings = content["principal_findings"]
                if isinstance(findings, list):
                    for i, finding in enumerate(findings, 1):
                        print(f"\n{i}. {finding['bullet_point']}")
                        if "reasoning" in finding:
                            print(f"   💡 Reasoning: {finding['reasoning']}")
                        if "data_source" in finding:
                            print(f"   📊 Data Source: {finding['data_source']}")
                        if "confidence" in finding:
                            print(f"   🎯 Confidence: {finding['confidence']}")
                print()

            # PCA ANALYSIS
            if "pca_insights" in content and content["pca_insights"]:
                print("📈 PCA ANALYSIS (Multi-Source Principal Component Analysis)")
                print("-" * 50)
                pca_data = content["pca_insights"]

                if "component_dominance" in pca_data:
                    print(f"\n🏆 Component Dominance:")
                    print(pca_data["component_dominance"])

                if "source_loadings" in pca_data:
                    print(f"\n📊 Source Loadings:")
                    print(pca_data["source_loadings"])

                if "market_tension" in pca_data:
                    print(f"\n⚖️ Market Tension:")
                    print(pca_data["market_tension"])

                if "strategic_implications" in pca_data:
                    print(f"\n🎯 Strategic Implications:")
                    print(pca_data["strategic_implications"])
                print()

            # HEATMAP ANALYSIS
            if "heatmap_analysis" in content and content["heatmap_analysis"]:
                print("🔥 HEATMAP ANALYSIS (Correlation Analysis)")
                print("-" * 50)
                print(content["heatmap_analysis"])
                print()

            # TECHNICAL METADATA
            print("🔧 TECHNICAL INFORMATION")
            print("-" * 50)
            print(f"Model Used: {response.get('model_used', 'unknown')}")
            print(f"Provider: {response.get('provider_used', 'unknown')}")
            print(f"Response Time: {response.get('response_time_ms', 'unknown')}ms")
            print(f"Token Count: {response.get('token_count', 'unknown')}")
            print(f"Language: {response.get('language', 'unknown')}")
            print(f"Total Findings: {len(content.get('principal_findings', []))}")

        else:
            print("📝 RAW RESPONSE:")
            print(str(response))

        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE!")
        print("This analysis used our cleaned 4000+ word narrative prompt system")
        print("integrating data from all 5 sources into a comprehensive business analysis.")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(read_complete_ai_response())
    sys.exit(exit_code)