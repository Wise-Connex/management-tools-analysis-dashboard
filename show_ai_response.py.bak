#!/usr/bin/env python3
"""
Simple script to show the AI response for Benchmarking with 5 sources.
"""

import asyncio
import sys
import os
import json

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

async def show_ai_response():
    """Generate and show the AI response for Benchmarking with 5 sources."""

    print("🎯 AI Response for Benchmarking + 5 Sources")
    print("=" * 70)
    print("Tool: Benchmarking")
    print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
    print("Language: Spanish")
    print("=" * 70)

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

    print("\n1. 📝 GENERATING 4869-CHARACTER PROMPT...")
    prompt = prompt_engineer.create_analysis_prompt(test_data, {})

    print(f"✅ Prompt generated: {len(prompt)} characters")
    print(f"📝 Prompt starts with: {prompt[:100]}...")

    print("\n2. 🤖 CALLING AI SERVICE...")
    try:
        response = await ai_service.generate_analysis(
            prompt=prompt,
            language="es"
        )

        print(f"✅ AI response received: {type(response)}")
        print(f"📊 Response length: {len(str(response))} characters")

        print("\n3. 📋 COMPLETE AI ANALYSIS:")
        print("=" * 70)

        if isinstance(response, dict):
            # Show the complete structured response
            print("🎯 STRUCTURED AI RESPONSE:")
            print(json.dumps(response, indent=2, ensure_ascii=False))

            print("\n" + "=" * 70)
            print("🔍 KEY INSIGHTS EXTRACTED:")
            print("=" * 70)

            # Executive Summary
            if "executive_summary" in response and response["executive_summary"]:
                print("\n📄 EXECUTIVE SUMMARY:")
                print(response["executive_summary"])

            # Principal Findings
            if "principal_findings" in response and response["principal_findings"]:
                print("\n📊 PRINCIPAL FINDINGS:")
                findings = response["principal_findings"]
                if isinstance(findings, list):
                    for i, finding in enumerate(findings, 1):
                        if isinstance(finding, dict) and "bullet_point" in finding:
                            print(f"   {i}. {finding['bullet_point']}")
                        elif isinstance(finding, str):
                            print(f"   {i}. {finding}")

            # PCA Analysis
            if "pca_insights" in response and response["pca_insights"]:
                print("\n📈 PCA ANALYSIS:")
                pca_data = response["pca_insights"]
                if isinstance(pca_data, dict):
                    for key, value in pca_data.items():
                        print(f"   {key}: {value}")

            print("\n" + "=" * 70)
            print("✅ ANALYSIS COMPLETE!")
            print(f"   • Model used: {response.get('model_used', 'unknown')}")
            print(f"   • Response time: {response.get('response_time_ms', 'unknown')}ms")
            print(f"   • Token count: {response.get('token_count', 'unknown')}")
            print(f"   • Total findings: {len(response.get('principal_findings', []))}")

        else:
            print("📝 RAW RESPONSE:")
            print(str(response))

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(show_ai_response())
    sys.exit(exit_code)