#!/usr/bin/env python3
"""
Kimi K2 Cost Analysis and Testing Script
Demonstrates the real cost structure for 1,302 combinations at $3/1M tokens.
"""

import json
import math
from datetime import datetime


def calculate_kimi_k2_costs():
    """Calculate costs for Kimi K2 batch processing."""

    print("💰 Kimi K2 Batch Processing Cost Analysis")
    print("=" * 60)
    print("📊 Pricing: $3 per 1,000,000 tokens ($0.003 per 1K tokens)")
    print("=" * 60)

    # Configuration
    pricing_per_million = 3.0  # USD
    pricing_per_1k = pricing_per_million / 1000  # $0.003 per 1K tokens

    # Batch processing parameters
    total_combinations = 1302
    languages = 2  # Spanish and English

    # Token estimates based on our testing
    token_scenarios = [
        {
            "name": "Conservative Estimate",
            "prompt_tokens": 800,
            "response_tokens": 2000,
            "total_per_analysis": 2800,
        },
        {
            "name": "Realistic Estimate",
            "prompt_tokens": 1000,
            "response_tokens": 3000,
            "total_per_analysis": 4000,
        },
        {
            "name": "High Estimate",
            "prompt_tokens": 1200,
            "response_tokens": 4000,
            "total_per_analysis": 5200,
        },
    ]

    print("\n🎯 Analysis Scenarios:")
    print("-" * 60)

    for scenario in token_scenarios:
        total_tokens = total_combinations * scenario["total_per_analysis"]
        cost = (total_tokens / 1000) * pricing_per_1k
        cost_per_hour = cost / 2  # Assume ~2 hours processing time

        print(f"\n📊 {scenario['name']}:")
        print(f"   - Tokens per analysis: {scenario['total_per_analysis']:,}")
        print(f"   - Prompt tokens: {scenario['prompt_tokens']:,}")
        print(f"   - Response tokens: {scenario['response_tokens']:,}")
        print(f"   - Total tokens: {total_tokens:,}")
        print(f"   - Total cost: ${cost:.2f}")
        print(f"   - Cost per hour: ${cost_per_hour:.2f}")
        print(f"   - Cost per combination: ${cost / total_combinations:.4f}")

    # Detailed breakdown by language
    print(f"\n🌍 Language Breakdown (Realistic Estimate):")
    print("-" * 60)

    realistic = token_scenarios[1]  # Realistic estimate
    tokens_per_language = total_combinations * realistic["total_per_analysis"] / 2
    cost_per_language = (tokens_per_language / 1000) * pricing_per_1k

    print(f"Spanish combinations: {total_combinations // 2:,}")
    print(f"   - Tokens: {tokens_per_language:,}")
    print(f"   - Cost: ${cost_per_language:.2f}")

    print(f"English combinations: {total_combinations // 2:,}")
    print(f"   - Tokens: {tokens_per_language:,}")
    print(f"   - Cost: ${cost_per_language:.2f}")

    print(f"Total cost: ${cost_per_language * 2:.2f}")

    # ROI Analysis
    print(f"\n💡 Return on Investment Analysis:")
    print("-" * 60)

    estimated_user_analyses_per_day = 50
    time_saved_per_analysis = 10  # seconds (vs 5-15s live AI)
    annual_user_analyses = estimated_user_analyses_per_day * 365

    annual_time_saved = annual_user_analyses * time_saved_per_analysis / 3600  # hours
    estimated_hourly_value = 50  # USD per hour of developer time

    annual_value = annual_time_saved * estimated_hourly_value

    realistic_cost = (
        total_combinations * realistic["total_per_analysis"] / 1000
    ) * pricing_per_1k
    roi = (
        (annual_value - realistic_cost) / realistic_cost * 100
        if realistic_cost > 0
        else 0
    )

    print(f"Annual user analyses: {annual_user_analyses:,}")
    print(f"Annual time saved: {annual_time_saved:.1f} hours")
    print(f"Annual value: ${annual_value:.2f}")
    print(f"Batch processing cost: ${realistic_cost:.2f}")
    print(f"ROI: {roi:.0f}%")

    return {
        "pricing_per_million": pricing_per_million,
        "total_combinations": total_combinations,
        "scenarios": token_scenarios,
        "realistic_cost": realistic_cost,
        "annual_roi": roi,
    }


def generate_test_combinations():
    """Generate test combinations for validation."""

    management_tools = [
        {"id": 1, "name": "Alianzas y Capital de Riesgo"},
        {"id": 2, "name": "Benchmarking"},
        {"id": 3, "name": "Calidad Total"},
    ]

    data_sources = [
        {"display_name": "Google Trends"},
        {"display_name": "Google Books"},
        {"display_name": "Bain Usability"},
    ]

    test_combinations = []

    for tool in management_tools[:2]:  # First 2 tools only
        for source in data_sources[:2]:  # First 2 sources only
            for language in ["es", "en"]:
                combination = {
                    "tool_name": tool["name"],
                    "selected_sources": [source["display_name"]],
                    "language": language,
                    "sources_count": 1,
                }
                test_combinations.append(combination)

    print(f"\n🧪 Generated {len(test_combinations)} test combinations:")
    print("-" * 60)

    for i, combo in enumerate(test_combinations, 1):
        print(
            f"{i:2d}. {combo['tool_name']} + {combo['selected_sources'][0]} ({combo['language']})"
        )

    # Test cost for these combinations
    realistic_tokens_per_analysis = 4000
    test_cost = (len(test_combinations) * realistic_tokens_per_analysis / 1000) * 0.003

    print(f"\n💸 Test Cost Estimate:")
    print(f"   - Combinations: {len(test_combinations)}")
    print(f"   - Tokens per analysis: {realistic_tokens_per_analysis:,}")
    print(
        f"   - Total tokens: {len(test_combinations) * realistic_tokens_per_analysis:,}"
    )
    print(f"   - Test cost: ${test_cost:.4f}")

    return test_combinations


def main():
    """Main execution function."""

    # Calculate costs
    cost_analysis = calculate_kimi_k2_costs()

    # Generate test combinations
    test_combinations = generate_test_combinations()

    # Summary
    print(f"\n🚀 EXECUTIVE SUMMARY:")
    print("=" * 60)
    print(f"✅ Batch processing 1,302 combinations with Kimi K2")
    print(f"💰 Total estimated cost: ${cost_analysis['realistic_cost']:.2f}")
    print(f"📊 Token usage: ~5.2M tokens")
    print(f"⏱️ Processing time: ~2-3 hours")
    print(f"💡 Annual ROI: {cost_analysis['annual_roi']:.0f}%")
    print(f"🧪 Test mode cost: ${(len(test_combinations) * 4000 / 1000) * 0.003:.4f}")

    print(f"\n🎯 RECOMMENDATION:")
    print("-" * 60)
    print("1. Start with test mode (8 combinations, ~$0.10)")
    print("2. Validate results and performance")
    print("3. Proceed with full batch if satisfied")
    print("4. Monitor costs and adjust if needed")

    return cost_analysis


if __name__ == "__main__":
    main()
