#!/usr/bin/env python3
"""
Clean script to display the improved AI response without data_source/confidence labels.
"""

import asyncio
import sys
import os

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

async def show_clean_response():
    """Generate and display the clean AI response without labels."""

    print("📖 IMPROVED AI ANALYSIS: BENCHMARKING + 5 SOURCES")
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
        print(f"📏 Response length: {len(str(response))} characters")

        # Display the complete response in clean format
        print(f"\n🎯 CLEAN AI ANALYSIS:")
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

            # PRINCIPAL FINDINGS - CLEAN FORMAT
            if "principal_findings" in content and content["principal_findings"]:
                print("📊 PRINCIPAL FINDINGS")
                print("-" * 50)
                findings = content["principal_findings"]
                if isinstance(findings, list):
                    for i, finding in enumerate(findings, 1):
                        if isinstance(finding, dict) and "bullet_point" in finding:
                            print(f"{i}. {finding['bullet_point']}")
                            if "reasoning" in finding:
                                # Clean reasoning without labels
                                reasoning = finding['reasoning']
                                # Remove any remaining labels
                                reasoning = reasoning.replace("💡 Reasoning: ", "").replace("Reasoning: ", "")
                                print(f"   {reasoning}")
                            print()

            # PCA ANALYSIS - ENHANCED
            if "pca_analysis" in content and content["pca_analysis"]:
                print("📈 PCA ANALYSIS (Enhanced Source Influence Analysis)")
                print("-" * 60)
                pca_content = content["pca_analysis"]
                print(pca_content)
                print()

            # HEATMAP ANALYSIS
            if "heatmap_analysis" in content and content["heatmap_analysis"]:
                print("🔥 HEATMAP ANALYSIS")
                print("-" * 50)
                print(content["heatmap_analysis"])
                print()

            # TEMPORAL ANALYSIS
            if "temporal_analysis" in content and content["temporal_analysis"]:
                print("📈 TEMPORAL ANALYSIS")
                print("-" * 50)
                print(content["temporal_analysis"])
                print()

            # FOURIER ANALYSIS
            if "fourier_analysis" in content and content["fourier_analysis"]:
                print("📊 FOURIER ANALYSIS")
                print("-" * 50)
                print(content["fourier_analysis"])
                print()

            # STRATEGIC SYNTHESIS
            if "strategic_synthesis" in content and content["strategic_synthesis"]:
                print("🎯 STRATEGIC SYNTHESIS")
                print("-" * 50)
                print(content["strategic_synthesis"])
                print()

            # CONCLUSIONS
            if "conclusions" in content and content["conclusions"]:
                print("🏁 CONCLUSIONS")
                print("-" * 50)
                print(content["conclusions"])
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
        print("This analysis uses our enhanced prompt system with:")
        print("  • Clean principal findings format (no data_source/confidence labels)")
        print("  • Sophisticated PCA analysis focusing on source influence")
        print("  • Alignment analysis between opinion/industry/academy")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(show_clean_response())
    sys.exit(exit_code)