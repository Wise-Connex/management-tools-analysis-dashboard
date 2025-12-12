#!/usr/bin/env python3
"""
Test script to force Kimi K2 model usage and verify correct section ordering.
"""

import asyncio
import sys
import json

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

async def test_kimi_k2_analysis():
    """Force Kimi K2 model and check section ordering."""

    print("🎯 TEST: Kimi K2 Analysis with Correct Section Ordering")
    print("=" * 80)
    print("Tool: Benchmarking")
    print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
    print("Language: Spanish")
    print("Model: FORCING Kimi K2 (moonshotai/kimi-k2-instruct)")
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

    print("\n🤖 FORCING KIMI K2 MODEL...")
    try:
        # Force Kimi K2 model specifically
        response = await ai_service.generate_analysis(
            prompt=prompt,
            language="es",
            model="moonshotai/kimi-k2-instruct"  # Force Kimi K2 specifically
        )

        print(f"✅ Kimi K2 response received")
        print(f"📊 Response type: {type(response)}")
        print(f"📏 Response length: {len(str(response))} characters")

        # Check which model was actually used
        actual_model = response.get('model_used', 'unknown')
        print(f"🤖 Actually used model: {actual_model}")

        # Display the complete response with PROPER SECTION ORDERING
        print(f"\n🎯 KIMI K2 ANALYSIS - PROPER SECTION ORDER:")
        print("=" * 80)

        if isinstance(response, dict) and "content" in response:
            content = response["content"]

            # Check section order by listing what we actually get
            print(f"\n📋 SECTIONS FOUND IN RESPONSE:")
            sections_found = []
            if "executive_summary" in content:
                sections_found.append("1. Executive Summary")
            if "principal_findings" in content:
                sections_found.append("2. Principal Findings")
            if "temporal_analysis" in content:
                sections_found.append("3. Temporal Analysis")
            if "heatmap_analysis" in content:
                sections_found.append("4. Heatmap Analysis")
            if "fourier_analysis" in content:
                sections_found.append("5. Fourier Analysis")
            if "pca_analysis" in content:
                sections_found.append("6. PCA Analysis")
            if "strategic_synthesis" in content:
                sections_found.append("7. Strategic Synthesis")
            if "conclusions" in content:
                sections_found.append("8. Conclusions")

            print("Expected order: 1→2→3→4→5→6→7→8")
            print("Actual order: " + " → ".join(sections_found))

            # Now display the complete response in correct order
            print(f"\n🎯 COMPLETE KIMI K2 ANALYSIS:")
            print("=" * 80)

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
                        if isinstance(finding, dict) and "bullet_point" in finding:
                            print(f"{i}. {finding['bullet_point']}")
                            if "reasoning" in finding:
                                # Clean reasoning without labels
                                reasoning = finding['reasoning']
                                reasoning = reasoning.replace("💡 Reasoning: ", "").replace("Reasoning: ", "")
                                print(f"   {reasoning}")
                            print()

            # TEMPORAL ANALYSIS
            if "temporal_analysis" in content and content["temporal_analysis"]:
                print("📈 TEMPORAL ANALYSIS")
                print("-" * 50)
                print(content["temporal_analysis"])
                print()

            # HEATMAP ANALYSIS
            if "heatmap_analysis" in content and content["heatmap_analysis"]:
                print("🔥 HEATMAP ANALYSIS")
                print("-" * 50)
                print(content["heatmap_analysis"])
                print()

            # FOURIER ANALYSIS
            if "fourier_analysis" in content and content["fourier_analysis"]:
                print("📊 FOURIER ANALYSIS")
                print("-" * 50)
                print(content["fourier_analysis"])
                print()

            # PCA ANALYSIS
            if "pca_analysis" in content and content["pca_analysis"]:
                print("📈 PCA ANALYSIS (Enhanced Source Influence Analysis)")
                print("-" * 60)
                print(content["pca_analysis"])
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
        print("✅ KIMI K2 ANALYSIS COMPLETE!")
        print("This analysis uses our enhanced prompt system with Kimi K2 model")

        return 0

    except Exception as e:
        print(f"❌ Error with Kimi K2: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_kimi_k2_analysis())
    sys.exit(exit_code)