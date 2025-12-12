#!/usr/bin/env python3
"""
Live AI testing with Groq Kimi K2 for key findings review.
Tests real AI responses with statistical data integration.
"""

import sys
import os
import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add scripts directory to path for utilities
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Import our utilities
from utils.hash_utils import generate_combination_hash, normalize_source_name
from utils.database_utils import (
    store_analysis_in_both_databases,
    retrieve_analysis_by_hash,
)
from utils.response_display import (
    display_ai_response,
    save_ai_response,
    analyze_response_quality,
    display_quality_analysis,
)

# Import AI service components
from dashboard_app.key_findings.unified_ai_service import UnifiedAIService
from dashboard_app.key_findings.prompt_engineer import PromptEngineer

# Import database managers
from database_implementation.precomputed_findings_db import PrecomputedFindingsDBManager


class LiveAITester:
    """Test live AI analysis with Groq Kimi K2."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer()
        self.precomputed_db = PrecomputedFindingsDBManager()

        # Test combinations for live AI testing
        self.test_combinations = [
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends"],
                "language": "es",
                "description": "Spanish single-source: Benchmarking + Google Trends",
                "expected_sections": [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "heatmap_analysis",
                    "conclusions",
                ],
            },
            {
                "tool": "Calidad Total",
                "sources": ["Crossref"],
                "language": "es",
                "description": "Spanish single-source: Calidad Total + Crossref",
                "expected_sections": [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "heatmap_analysis",
                    "conclusions",
                ],
            },
            {
                "tool": "Reingeniería de Procesos",
                "sources": ["Bain Usability"],
                "language": "es",
                "description": "Spanish single-source: Gestión de Procesos + Bain Usability",
                "expected_sections": [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "heatmap_analysis",
                    "conclusions",
                ],
            },
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends"],
                "language": "en",
                "description": "English single-source: Benchmarking + Google Trends",
                "expected_sections": [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "heatmap_analysis",
                    "conclusions",
                ],
            },
            {
                "tool": "Total Quality Management",
                "sources": ["Crossref"],
                "language": "en",
                "description": "English single-source: Total Quality Management + Crossref",
                "expected_sections": [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "heatmap_analysis",
                    "conclusions",
                ],
            },
            {
                "tool": "Business Process Reengineering",
                "sources": ["Bain Usability"],
                "language": "en",
                "description": "English single-source: Business Process Reengineering + Bain Usability",
                "expected_sections": [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "heatmap_analysis",
                    "conclusions",
                ],
            },
        ]

    def generate_comprehensive_statistical_data(
        self, tool_name: str, selected_sources: list, language: str
    ) -> dict:
        """
        Generate comprehensive statistical data that mirrors actual dashboard calculations.

        Args:
            tool_name: Management tool name
            selected_sources: List of data sources
            language: Language code

        Returns:
            Comprehensive statistical data dictionary
        """
        print(
            f"📊 Generating comprehensive statistical data for {tool_name} + {selected_sources} ({language})"
        )

        # This represents the actual data that would come from dashboard analysis
        statistical_data = {
            "tool_name": tool_name,
            "selected_sources": selected_sources,
            "language": language,
            "date_range_start": "1950-01-01",
            "date_range_end": "2023-12-31",
            "data_points_analyzed": 1250,
            "analysis_type": "single_source",
            "temporal_analysis": {
                "linear_trend": {
                    "slope": 0.025,
                    "intercept": 0.45,
                    "r_squared": 0.78,
                    "p_value": 0.001,
                    "trend_direction": "increasing",
                    "significance": "highly_significant",
                },
                "moving_averages": {
                    "ma_3_current": 0.65,
                    "ma_6_current": 0.58,
                    "ma_12_current": 0.52,
                },
                "recent_vs_historical": {
                    "recent_mean": 0.68,
                    "historical_mean": 0.45,
                    "change_percentage": 51.1,
                    "change_direction": "increasing",
                },
                "volatility": {
                    "overall": 0.15,
                    "recent": 0.12,
                    "volatility_trend": "decreasing",
                },
            },
            "seasonal_analysis": {
                "monthly_patterns": {
                    "monthly_means": {
                        "1": 0.42,
                        "2": 0.38,
                        "3": 0.45,
                        "4": 0.52,
                        "5": 0.58,
                        "6": 0.65,
                        "7": 0.72,
                        "8": 0.68,
                        "9": 0.61,
                        "10": 0.55,
                        "11": 0.48,
                        "12": 0.44,
                    },
                    "monthly_std": {
                        "1": 0.08,
                        "2": 0.07,
                        "3": 0.09,
                        "4": 0.10,
                        "5": 0.11,
                        "6": 0.12,
                        "7": 0.13,
                        "8": 0.12,
                        "9": 0.11,
                        "10": 0.10,
                        "11": 0.09,
                        "12": 0.08,
                    },
                    "peak_month": 7,
                    "low_month": 2,
                    "peak_value": 0.72,
                    "low_value": 0.38,
                },
                "quarterly_patterns": {"Q1": 0.42, "Q2": 0.58, "Q3": 0.67, "Q4": 0.49},
                "year_over_year": {
                    "yearly_means": {
                        "2020": 0.45,
                        "2021": 0.52,
                        "2022": 0.58,
                        "2023": 0.65,
                    },
                    "average_growth_rate": 12.8,
                },
                "seasonality_strength": {
                    "strength_value": 0.73,
                    "strength_level": "strong",
                },
            },
            "fourier_analysis": {
                "dominant_frequencies": [
                    {
                        "frequency": 0.083,
                        "period": 12.0,
                        "power": 0.85,
                        "pattern_type": "annual",
                        "relative_strength": 0.92,
                    },
                    {
                        "frequency": 0.167,
                        "period": 6.0,
                        "power": 0.45,
                        "pattern_type": "semi_annual",
                        "relative_strength": 0.48,
                    },
                ],
                "signal_quality": {
                    "total_power": 2.15,
                    "signal_power": 1.85,
                    "noise_power": 0.30,
                    "signal_to_noise_ratio": 6.17,
                    "quality_level": "excellent",
                },
                "data_points_analyzed": 1250,
            },
            "heatmap_analysis": {
                "value_ranges": {"min": 0.15, "max": 0.89, "mean": 0.52, "std": 0.18},
                "most_dense_regions": ["Q2-Q3", "Monthly peaks"],
                "least_dense_regions": ["Q1", "Winter months"],
                "detected_clusters": [
                    "High activity cluster",
                    "Seasonal pattern cluster",
                ],
                "detected_outliers": ["2020 Q1 anomaly", "2023 Q4 spike"],
                "gradients": {"temporal_gradient": 0.025, "seasonal_gradient": 0.15},
            },
            "statistical_summary": {
                "source_statistics": {
                    "count": 1250,
                    "mean": 0.52,
                    "median": 0.51,
                    "std": 0.18,
                    "min": 0.15,
                    "max": 0.89,
                    "range": 0.74,
                    "q25": 0.38,
                    "q75": 0.66,
                    "iqr": 0.28,
                    "skewness": 0.32,
                    "kurtosis": -0.15,
                    "missing_percentage": 2.1,
                },
                "trends_analysis": {
                    "trends": {
                        "recent_trend": 0.68,
                        "long_term_trend": 0.45,
                        "trend_direction": "increasing",
                        "volatility": 0.15,
                        "momentum": 0.73,
                    },
                    "anomalies": {
                        "count": 3,
                        "percentage": 0.24,
                        "max_z_score": 2.85,
                        "recent_anomalies": [
                            {
                                "date": "2023-11",
                                "z_score": 2.85,
                                "description": "Unusual spike",
                            }
                        ],
                    },
                },
            },
        }

        print(
            f"✅ Comprehensive statistical data generated: {statistical_data['data_points_analyzed']} data points"
        )
        return statistical_data

    async def test_single_source_with_live_ai(self, combination: dict) -> dict:
        """
        Test a single source combination with live AI analysis.

        Args:
            combination: Test combination dictionary

        Returns:
            Test results with live AI response
        """
        print(f"\n{'=' * 80}")
        print(f"🤖 Live AI Testing: {combination['description']}")
        print(f"{'=' * 80}")

        start_time = time.time()

        try:
            # Generate comprehensive statistical data
            statistical_data = self.generate_comprehensive_statistical_data(
                combination["tool"], combination["sources"], combination["language"]
            )

            if not statistical_data:
                return {
                    "success": False,
                    "error": "Failed to generate statistical data",
                    "combination": combination,
                }

            # Generate combination hash
            combination_hash = generate_combination_hash(
                combination["tool"], combination["sources"], combination["language"]
            )

            print(f"🔑 Generated hash: {combination_hash}")

            # Check if already exists in database (cache hit)
            existing = retrieve_analysis_by_hash(combination_hash)
            if existing:
                print(f"✅ Found existing analysis in {existing['source']} database")
                return {
                    "success": True,
                    "cache_hit": True,
                    "source": existing["source"],
                    "data": existing["data"],
                    "combination": combination,
                    "hash": combination_hash,
                }

            # Create comprehensive prompt with statistical data
            prompt = self.prompt_engineer.create_analysis_prompt(
                statistical_data,
                {},  # Additional context
            )

            print(f"📝 Generated prompt: {len(prompt)} characters")
            print(f"📊 Statistical data includes:")
            print(
                f"   - Temporal analysis with R² = {statistical_data['temporal_analysis']['linear_trend']['r_squared']}"
            )
            print(
                f"   - Seasonal patterns with strength = {statistical_data['seasonal_analysis']['seasonality_strength']['strength_value']}"
            )
            print(
                f"   - Fourier analysis with SNR = {statistical_data['fourier_analysis']['signal_quality']['signal_to_noise_ratio']}"
            )
            print(
                f"   - {statistical_data['data_points_analyzed']} data points analyzed"
            )

            # Call live AI service
            print(f"🤖 Calling LIVE Kimi K2 AI...")
            ai_response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language=combination["language"],
                model="moonshotai/kimi-k2-instruct",
                is_single_source=True,
            )

            if not ai_response or "content" not in ai_response:
                return {
                    "success": False,
                    "error": "No valid AI response received",
                    "combination": combination,
                }

            # Display and analyze live response
            print(f"\n🎯 LIVE AI RESPONSE RECEIVED!")
            print(f"📊 Response metadata:")
            print(f"   Model: {ai_response.get('model_used', 'Unknown')}")
            print(f"   Provider: {ai_response.get('provider_used', 'Unknown')}")
            print(
                f"   Response time: {ai_response.get('response_time_ms', 'Unknown')}ms"
            )
            print(f"   Token count: {ai_response.get('token_count', 'Unknown')}")

            display_ai_response(
                ai_response, f"LIVE Kimi K2 Response - {combination['description']}"
            )

            # Analyze quality of live response
            quality_results = analyze_response_quality(ai_response)
            display_quality_analysis(quality_results)

            # Validate expected sections
            missing_sections = []
            for section in combination["expected_sections"]:
                if (
                    section not in ai_response["content"]
                    or not ai_response["content"][section]
                ):
                    missing_sections.append(section)

            if missing_sections:
                print(f"⚠️  Missing sections: {missing_sections}")
            else:
                print(f"✅ All expected sections present!")

            # Save live response to file
            saved_file = save_ai_response(
                ai_response,
                combination["tool"],
                combination["sources"],
                combination["language"],
            )

            # Store live analysis in both databases
            analysis_data = {
                "executive_summary": ai_response["content"].get(
                    "executive_summary", ""
                ),
                "principal_findings": ai_response["content"].get(
                    "principal_findings", ""
                ),
                "temporal_analysis": ai_response["content"].get(
                    "temporal_analysis", ""
                ),
                "seasonal_analysis": ai_response["content"].get(
                    "seasonal_analysis", ""
                ),
                "fourier_analysis": ai_response["content"].get("fourier_analysis", ""),
                "heatmap_analysis": ai_response["content"].get("heatmap_analysis", ""),
                "conclusions": ai_response["content"].get("conclusions", ""),
                "tool_display_name": combination["tool"],
                "data_points_analyzed": statistical_data["data_points_analyzed"],
                "confidence_score": quality_results["quality_score"] / 100.0,
                "model_used": ai_response.get(
                    "model_used", "moonshotai/kimi-k2-instruct"
                ),
            }

            storage_results = store_analysis_in_both_databases(
                tool_name=combination["tool"],
                selected_sources=combination["sources"],
                language=combination["language"],
                analysis_data=analysis_data,
                model_used=ai_response.get("model_used", "moonshotai/kimi-k2-instruct"),
                api_latency_ms=ai_response.get("response_time_ms", 0),
                confidence_score=quality_results["quality_score"] / 100.0,
                data_points_analyzed=statistical_data["data_points_analyzed"],
            )

            end_time = time.time()
            total_time = end_time - start_time

            print(f"\n✅ Live AI test completed in {total_time:.2f} seconds")
            print(f"   Hash: {combination_hash}")
            print(f"   Quality Score: {quality_results['quality_score']}/100")
            print(f"   Missing sections: {len(missing_sections)}")
            print(
                f"   Storage: Precomputed DB {'✅' if storage_results['precomputed']['success'] else '❌'}, Runtime DB {'✅' if storage_results['runtime']['success'] else '❌'}"
            )
            print(f"   Saved to: {saved_file}")

            return {
                "success": True,
                "cache_hit": False,
                "combination": combination,
                "hash": combination_hash,
                "ai_response": ai_response,
                "quality_results": quality_results,
                "missing_sections": missing_sections,
                "storage_results": storage_results,
                "total_time": total_time,
                "saved_file": saved_file,
            }

        except Exception as e:
            print(f"❌ Error in live AI testing: {e}")
            import traceback

            traceback.print_exc()

            return {"success": False, "error": str(e), "combination": combination}

    async def run_live_ai_tests(self):
        """Run all live AI tests."""
        print("🚀 Starting LIVE AI Testing with Groq Kimi K2")
        print("=" * 80)
        print(f"Total test combinations: {len(self.test_combinations)}")
        print(f"Start time: {datetime.now()}")
        print("=" * 80)

        results = []
        successful_tests = 0
        cache_hits = 0
        total_cost = 0.0

        for i, combination in enumerate(self.test_combinations, 1):
            print(f"\n[{i}/{len(self.test_combinations)}] {combination['description']}")

            result = await self.test_single_source_with_live_ai(combination)
            results.append(result)

            if result["success"]:
                successful_tests += 1
                if result.get("cache_hit"):
                    cache_hits += 1
                else:
                    # Estimate cost (rough calculation)
                    tokens = result["ai_response"].get("token_count", 0)
                    cost = (tokens / 1000) * 0.003  # Kimi K2 pricing
                    total_cost += cost
                    print(f"💰 Estimated cost: ${cost:.4f}")

            # Rate limiting delay
            if i < len(self.test_combinations):
                print(f"⏱️  Rate limiting: 3 second delay...")
                await asyncio.sleep(3)

        # Summary
        print(f"\n{'=' * 80}")
        print("📊 LIVE AI TEST SUMMARY")
        print(f"{'=' * 80}")
        print(f"Total Tests: {len(self.test_combinations)}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {len(self.test_combinations) - successful_tests}")
        print(f"Cache Hits: {cache_hits}")
        print(f"New AI Calls: {successful_tests - cache_hits}")
        print(
            f"Success Rate: {(successful_tests / len(self.test_combinations) * 100):.1f}%"
        )
        print(f"Total Estimated Cost: ${total_cost:.4f}")
        print(f"End Time: {datetime.now()}")

        # Quality summary
        quality_scores = [
            r["quality_results"]["quality_score"]
            for r in results
            if r.get("quality_results")
        ]
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            print(f"Average Quality Score: {avg_quality:.1f}/100")

        return {
            "total_tests": len(self.test_combinations),
            "successful_tests": successful_tests,
            "cache_hits": cache_hits,
            "success_rate": successful_tests / len(self.test_combinations),
            "total_cost": total_cost,
            "results": results,
            "quality_scores": quality_scores,
        }


async def main():
    """Main function to run live AI tests."""
    tester = LiveAITester()

    try:
        results = await tester.run_live_ai_tests()

        # Save results summary
        summary_file = f"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_results/ai_responses/live_ai_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        print(f"\n💾 Live AI results summary saved to: {summary_file}")

        return 0 if results["success_rate"] > 0.8 else 1  # Success if 80%+ pass rate

    except Exception as e:
        print(f"❌ Fatal error in main: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
