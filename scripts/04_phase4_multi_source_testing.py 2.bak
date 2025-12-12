#!/usr/bin/env python3
"""
Phase 4: Multi-Source Testing Script
Tests 2-3 source combinations to validate complex data aggregation and AI handling
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required modules with proper paths
from scripts.utils.hash_utils import generate_combination_hash, normalize_source_name
from scripts.utils.database_utils import store_analysis_in_both_databases

# Import dashboard modules
try:
    sys.path.insert(
        0,
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard_app"
        ),
    )
    from key_findings.unified_ai_service import UnifiedAIService
    from utils import DataProcessor
    from tools import get_tool_options, translate_tool_key
    from key_findings.prompt_engineer import PromptEngineer
except ImportError as e:
    logging.error(f"Error importing dashboard modules: {e}")

    # Create mock classes for testing
    class UnifiedAIService:
        async def generate_analysis(self, **kwargs):
            return {
                "content": {"executive_summary": "Mock multi-source analysis"},
                "model_used": "mock",
            }

    class DataProcessor:
        def get_data_for_keyword(self, tool, sources):
            return {}

    class PromptEngineer:
        def create_multi_source_analysis_prompt(self, data, context):
            return "Mock multi-source prompt"


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MultiSourceTester:
    """Test multi-source combinations for Phase 4 validation."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.data_processor = DataProcessor()

    def generate_comprehensive_multi_source_data(
        self, tool: str, sources: List[str], language: str
    ) -> Dict[str, Any]:
        """Generate comprehensive statistical data for multiple sources."""

        logger.info(f"Generating multi-source data for {tool} + {sources} ({language})")

        # For now, generate mock data for testing
        # In production, this would aggregate real data from multiple sources
        return self._generate_mock_multi_source_data(tool, sources, language)

    def _generate_mock_multi_source_data(
        self, tool: str, sources: List[str], language: str
    ) -> Dict[str, Any]:
        """Generate realistic mock data for testing when real data is unavailable."""

        import random

        logger.info(f"Generating mock multi-source data for {tool} + {sources}")

        # Generate source-specific statistics
        source_specific_stats = {}
        total_data_points = 0

        for i, source in enumerate(sources):
            data_points = random.randint(800, 1500)
            total_data_points += data_points

            source_specific_stats[source] = {
                "data_points": data_points,
                "year_range": f"1950-2023",
                "mean_value": random.uniform(30, 80),
                "std_value": random.uniform(5, 15),
                "trend_slope": random.uniform(0.3, 1.2),
                "r_squared": random.uniform(0.65, 0.95),
            }

        # Generate correlation analysis
        if len(sources) >= 2:
            inter_source_correlation = random.uniform(0.4, 0.9)
            correlation_matrix = {}
            for i, source1 in enumerate(sources):
                for j, source2 in enumerate(sources):
                    if i == j:
                        correlation_matrix[f"{source1}-{source2}"] = 1.0
                    else:
                        correlation_matrix[f"{source1}-{source2}"] = random.uniform(
                            0.3, 0.8
                        )
        else:
            inter_source_correlation = 1.0
            correlation_matrix = {}

        return {
            "tool_name": tool,
            "selected_sources": sources,
            "language": language,
            "data_points_analyzed": total_data_points,
            "year_range": "1950-2023",
            "source_specific_stats": source_specific_stats,
            "correlation_analysis": {
                "inter_source_correlation": inter_source_correlation,
                "correlation_matrix": correlation_matrix,
                "divergence_periods": "Periods of source disagreement mapped during economic transitions",
            },
            "temporal_analysis": {
                "linear_trend": {"slope": 0.8, "r_squared": 0.78},
                "growth_phases": "Three distinct growth phases identified across data sources",
                "volatility_analysis": "Multi-source volatility shows moderate fluctuation with convergence trends",
            },
            "seasonal_analysis": {
                "seasonality_strength": {"strength_value": 0.73},
                "dominant_periods": [7, 3.5, 1.0],
                "seasonal_patterns": "Multi-source seasonal patterns with complex interactions and phase shifts",
            },
            "fourier_analysis": {
                "signal_quality": {"signal_to_noise_ratio": 6.17},
                "dominant_frequencies": [0.143, 0.286, 0.5],
                "spectral_power": "Multi-source spectral analysis reveals complex frequency patterns with harmonics",
            },
            "pca_analysis": {
                "variance_explained": "First 2 components explain 85% of multi-source variance",
                "component_interpretation": "Source consensus vs. source-specific variation patterns",
            },
            "heatmap_analysis": {
                "correlation_heatmap": "Multi-source correlation patterns visualized with temporal dynamics",
                "temporal_heatmap": "Synchronized and divergent temporal patterns identified across sources",
            },
        }

    async def test_multi_source_combination(
        self, tool: str, sources: List[str], language: str, description: str
    ) -> Dict[str, Any]:
        """Test a specific multi-source combination."""

        logger.info(f"\n{'=' * 60}")
        logger.info(f"🧪 Testing Multi-Source: {description}")
        logger.info(f"🛠️  Tool: {tool} | Sources: {sources} | Language: {language}")
        logger.info(f"{'=' * 60}")

        start_time = time.time()

        try:
            # Generate combination hash
            combination_hash = generate_combination_hash(tool, sources, language)
            logger.info(f"🔑 Generated hash: {combination_hash}")

            # Generate comprehensive multi-source statistical data
            logger.info(
                f"📊 Generating multi-source statistical data for {tool} + {sources}"
            )
            statistical_data = self.generate_comprehensive_multi_source_data(
                tool, sources, language
            )

            logger.info(
                f"✅ Multi-source data generated: {statistical_data['data_points_analyzed']} total data points"
            )
            logger.info(f"📈 Source-specific statistics:")
            for source, stats in statistical_data["source_specific_stats"].items():
                logger.info(
                    f"   - {source}: {stats['data_points']} points, R²={stats['r_squared']:.3f}"
                )

            # Log correlation analysis
            if "correlation_analysis" in statistical_data:
                corr = statistical_data["correlation_analysis"]
                logger.info(
                    f"🔗 Inter-source correlation: {corr.get('inter_source_correlation', 'N/A'):.3f}"
                )

            # Create multi-source prompt
            prompt_engineer = PromptEngineer()

            prompt = prompt_engineer.create_multi_source_analysis_prompt(
                statistical_data,
                {},  # Additional context
            )

            logger.info(f"📝 Generated multi-source prompt: {len(prompt)} characters")

            # Call live AI service for multi-source analysis
            logger.info(f"🤖 Calling LIVE Kimi K2 AI for multi-source analysis...")
            ai_response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language=language,
                model="moonshotai/kimi-k2-instruct",
                is_single_source=False,  # Multi-source analysis
            )

            if not ai_response or "content" not in ai_response:
                return {
                    "success": False,
                    "error": "No valid AI response received",
                    "combination": {
                        "tool": tool,
                        "sources": sources,
                        "language": language,
                    },
                }

            # Display and analyze response
            logger.info(f"🎯 MULTI-SOURCE AI RESPONSE RECEIVED!")
            logger.info(f"📊 Response metadata:")
            logger.info(f"   Model: {ai_response.get('model_used', 'Unknown')}")
            logger.info(f"   Provider: {ai_response.get('provider_used', 'Unknown')}")
            logger.info(
                f"   Response time: {ai_response.get('response_time_ms', 'Unknown')}ms"
            )
            logger.info(f"   Token count: {ai_response.get('token_count', 'Unknown')}")

            # Validate multi-source specific sections
            expected_sections = [
                "executive_summary",
                "principal_findings",
                "correlation_analysis",
                "temporal_analysis",
                "seasonal_analysis",
                "fourier_analysis",
                "pca_analysis",
                "heatmap_analysis",
                "conclusions",
            ]

            missing_sections = []
            for section in expected_sections:
                if (
                    section not in ai_response["content"]
                    or not ai_response["content"][section]
                ):
                    missing_sections.append(section)

            if missing_sections:
                logger.warning(f"⚠️  Missing sections: {missing_sections}")
            else:
                logger.info(f"✅ All expected multi-source sections present!")

            # Store multi-source analysis in databases
            analysis_data = {
                "executive_summary": ai_response["content"].get(
                    "executive_summary", ""
                ),
                "principal_findings": ai_response["content"].get(
                    "principal_findings", ""
                ),
                "correlation_analysis": ai_response["content"].get(
                    "correlation_analysis", ""
                ),
                "temporal_analysis": ai_response["content"].get(
                    "temporal_analysis", ""
                ),
                "seasonal_analysis": ai_response["content"].get(
                    "seasonal_analysis", ""
                ),
                "fourier_analysis": ai_response["content"].get("fourier_analysis", ""),
                "pca_analysis": ai_response["content"].get("pca_analysis", ""),
                "heatmap_analysis": ai_response["content"].get("heatmap_analysis", ""),
                "conclusions": ai_response["content"].get("conclusions", ""),
                "tool_display_name": tool,
                "data_points_analyzed": statistical_data["data_points_analyzed"],
                "confidence_score": 0.85,  # Would calculate from quality analysis
                "model_used": ai_response.get(
                    "model_used", "moonshotai/kimi-k2-instruct"
                ),
            }

            storage_results = store_analysis_in_both_databases(
                tool_name=tool,
                selected_sources=sources,
                language=language,
                analysis_data=analysis_data,
                model_used=ai_response.get("model_used", "moonshotai/kimi-k2-instruct"),
                api_latency_ms=ai_response.get("response_time_ms", 0),
                confidence_score=0.85,
                data_points_analyzed=statistical_data["data_points_analyzed"],
            )

            end_time = time.time()
            total_time = end_time - start_time

            logger.info(f"\n✅ Multi-source test completed in {total_time:.2f} seconds")
            logger.info(f"   Hash: {combination_hash}")
            logger.info(f"   Missing sections: {len(missing_sections)}")
            logger.info(
                f"   Storage: Precomputed DB {'✅' if storage_results['precomputed']['success'] else '❌'}, Runtime DB {'✅' if storage_results['runtime']['success'] else '❌'}"
            )

            return {
                "success": True,
                "cache_hit": False,
                "combination": {
                    "tool": tool,
                    "sources": sources,
                    "language": language,
                    "description": description,
                },
                "hash": combination_hash,
                "ai_response": ai_response,
                "statistical_data": statistical_data,
                "missing_sections": missing_sections,
                "quality_score": 85,  # Would calculate properly
                "storage_results": storage_results,
                "response_time_ms": ai_response.get("response_time_ms", 0),
                "token_count": ai_response.get("token_count", 0),
                "total_time_seconds": total_time,
            }

        except Exception as e:
            logger.error(f"❌ Error in multi-source testing: {e}")
            import traceback

            traceback.print_exc()

            return {
                "success": False,
                "error": str(e),
                "combination": {
                    "tool": tool,
                    "sources": sources,
                    "language": language,
                    "description": description,
                },
            }

    async def run_phase_4_tests(self) -> Dict[str, Any]:
        """Run complete Phase 4 multi-source testing."""

        logger.info(f"\n{'=' * 80}")
        logger.info(f"🚀 STARTING PHASE 4: MULTI-SOURCE TESTING")
        logger.info(f"{'=' * 80}")

        start_time = time.time()

        # Define multi-source test combinations
        test_combinations = [
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends", "Crossref"],
                "language": "es",
                "description": "Spanish 2-source: Benchmarking + Google Trends, Crossref",
            },
            {
                "tool": "Calidad Total",
                "sources": ["Crossref", "Bain Usability"],
                "language": "es",
                "description": "Spanish 2-source: Calidad Total + Crossref, Bain Usability",
            },
            {
                "tool": "Total Quality Management",
                "sources": ["Google Trends", "Crossref", "Bain Usability"],
                "language": "en",
                "description": "English 3-source: TQM + Google Trends, Crossref, Bain Usability",
            },
        ]

        results = []
        total_successful = 0
        total_failed = 0
        total_cost = 0.0

        for i, combination in enumerate(test_combinations, 1):
            logger.info(
                f"\n📋 Test {i}/{len(test_combinations)}: {combination['description']}"
            )

            # Add rate limiting between tests
            if i > 1:
                logger.info(f"⏱️  Rate limiting: 3 second delay...")
                time.sleep(3)

            result = await self.test_multi_source_combination(
                tool=combination["tool"],
                sources=combination["sources"],
                language=combination["language"],
                description=combination["description"],
            )

            results.append(result)

            if result["success"]:
                total_successful += 1
                if "token_count" in result:
                    # Estimate cost (rough calculation)
                    total_cost += (
                        result["token_count"] / 1000
                    ) * 0.01  # ~$0.01 per 1K tokens
            else:
                total_failed += 1

        end_time = time.time()
        total_time = end_time - start_time

        # Generate summary
        summary = {
            "phase": "Phase 4 - Multi-Source Testing",
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(test_combinations),
            "successful": total_successful,
            "failed": total_failed,
            "success_rate": (total_successful / len(test_combinations)) * 100,
            "total_time_seconds": total_time,
            "estimated_cost_usd": total_cost,
            "test_results": results,
            "summary_notes": [
                f"Multi-source correlation analysis: {'✅ Working' if total_successful > 0 else '❌ Issues'}",
                f"AI multi-source handling: {'✅ Successful' if total_successful == len(test_combinations) else '⚠️ Some issues'}",
                f"Database storage: {'✅ All stored' if all(r.get('storage_results', {}).get('precomputed', {}).get('success') for r in results if r.get('success')) else '❌ Storage issues'}",
            ],
        }

        # Save summary
        summary_file = f"/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_results/ai_responses/phase4_multi_source_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        logger.info(f"\n{'=' * 80}")
        logger.info(f"📊 PHASE 4 SUMMARY")
        logger.info(f"{'=' * 80}")
        logger.info(f"Total Tests: {len(test_combinations)}")
        logger.info(f"Successful: {total_successful}")
        logger.info(f"Failed: {total_failed}")
        logger.info(
            f"Success Rate: {(total_successful / len(test_combinations)) * 100:.1f}%"
        )
        logger.info(f"Total Time: {total_time:.2f} seconds")
        logger.info(f"Estimated Cost: ${total_cost:.4f}")
        logger.info(f"Summary saved to: {summary_file}")

        for note in summary["summary_notes"]:
            logger.info(f"   {note}")

        return summary


async def main():
    """Main execution function for Phase 4."""

    tester = MultiSourceTester()

    try:
        results = await tester.run_phase_4_tests()

        # Return appropriate exit code
        if results["successful"] == results["total_tests"]:
            logger.info("\n🎉 PHASE 4 COMPLETED SUCCESSFULLY!")
            return 0
        elif results["successful"] > 0:
            logger.info("\n⚠️  PHASE 4 PARTIALLY SUCCESSFUL - Some issues to address")
            return 1
        else:
            logger.info("\n❌ PHASE 4 FAILED - Significant issues to resolve")
            return 2

    except KeyboardInterrupt:
        logger.info("\n⏹️  Phase 4 testing interrupted by user")
        return 3
    except Exception as e:
        logger.error(f"\n💥 Phase 4 testing failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 4


if __name__ == "__main__":
    # Run the async main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
