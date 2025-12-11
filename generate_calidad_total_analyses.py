#!/usr/bin/env python3
"""
Generate AI queries for Calidad Total combinations and store in database

Generates comprehensive AI analyses for:
1. Calidad Total + Google Trends (single-source)
2. Calidad Total + All 5 sources (multi-source)
3. Calidad Total + Google Books, Bain Satisfaction (multi-source)
"""

import asyncio
import json
import time
import logging
import sys
from typing import Dict, List, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "dashboard_app"))

# Import required modules
from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.key_findings.key_findings_service import get_key_findings_service
from dashboard_app.key_findings.unified_ai_service import get_unified_ai_service


class CalidadTotalAnalysisGenerator:
    """Generator for Calidad Total AI analyses with multiple source combinations."""

    def __init__(self):
        """Initialize the generator with required services."""
        self.db_manager = get_precomputed_db_manager()
        self.key_findings_service = get_key_findings_service()

        # All available sources
        self.all_sources = [
            "Google Trends",
            "Google Books",
            "Bain Usability",
            "Bain Satisfaction",
            "Crossref",
        ]

        # Source mappings for database storage
        self.source_mapping = {
            "Google Trends": 1,
            "Google Books": 2,
            "Bain Usability": 3,
            "Crossref": 4,
            "Bain Satisfaction": 5,
        }

    async def generate_single_source_analysis(
        self, tool_name: str, source: str, language: str
    ) -> Dict[str, Any]:
        """Generate single-source analysis for Calidad Total."""
        logger.info(
            f"🎯 Generating single-source analysis: {tool_name} + {source} ({language})"
        )

        try:
            # Generate analysis using the AI service
            result = await self.key_findings_service.generate_key_findings(
                tool_name=tool_name,
                selected_sources=[source],
                language=language,
                force_refresh=True,  # Force fresh generation
            )

            if result["success"]:
                logger.info(f"✅ Single-source analysis generated successfully")
                return result
            else:
                logger.error(
                    f"❌ Failed to generate single-source analysis: {result.get('error')}"
                )
                return result

        except Exception as e:
            logger.error(f"❌ Error generating single-source analysis: {e}")
            return {"success": False, "error": f"Generation failed: {str(e)}"}

    async def generate_multi_source_analysis(
        self, tool_name: str, sources: List[str], language: str
    ) -> Dict[str, Any]:
        """Generate multi-source analysis for Calidad Total."""
        logger.info(
            f"🎯 Generating multi-source analysis: {tool_name} + {len(sources)} sources ({language})"
        )

        try:
            # Generate analysis using the AI service
            result = await self.key_findings_service.generate_key_findings(
                tool_name=tool_name,
                selected_sources=sources,
                language=language,
                force_refresh=True,  # Force fresh generation
            )

            if result["success"]:
                logger.info(f"✅ Multi-source analysis generated successfully")
                return result
            else:
                logger.error(
                    f"❌ Failed to generate multi-source analysis: {result.get('error')}"
                )
                return result

        except Exception as e:
            logger.error(f"❌ Error generating multi-source analysis: {e}")
            return {"success": False, "error": f"Generation failed: {str(e)}"}

    def store_analysis_in_database(
        self, result: Dict[str, Any], tool_name: str, sources: List[str], language: str
    ) -> bool:
        """Store the generated analysis in the precomputed database."""
        try:
            if not result["success"]:
                logger.warning(f"⚠️ Skipping database storage due to generation failure")
                return False

            logger.info(
                f"🗄️ Storing analysis in database: {tool_name} + {len(sources)} sources ({language})"
            )

            # Extract the analysis data
            analysis_data = result.get("data", {})

            # Generate combination hash
            combination_hash = self.db_manager.generate_combination_hash(
                tool_name=tool_name, selected_sources=sources, language=language
            )

            # Prepare data for storage
            storage_data = {
                "executive_summary": analysis_data.get("executive_summary", ""),
                "principal_findings": analysis_data.get("principal_findings", ""),
                "temporal_analysis": analysis_data.get("temporal_analysis", ""),
                "seasonal_analysis": analysis_data.get("seasonal_analysis", ""),
                "fourier_analysis": analysis_data.get("fourier_analysis", ""),
                "strategic_synthesis": analysis_data.get("strategic_synthesis", ""),
                "conclusions": analysis_data.get("conclusions", ""),
                "pca_analysis": analysis_data.get("pca_analysis", ""),
                "heatmap_analysis": analysis_data.get("heatmap_analysis", ""),
                "analysis_type": "single_source"
                if len(sources) == 1
                else "multi_source",
                "confidence_score": analysis_data.get("confidence_score", 0.0),
                "model_used": analysis_data.get("model_used", "unknown"),
                "data_points_analyzed": analysis_data.get("data_points_analyzed", 0),
            }

            # Store in database
            result = self.db_manager.store_precomputed_analysis(
                combination_hash=combination_hash,
                tool_name=tool_name,
                selected_sources=sources,
                language=language,
                analysis_data=storage_data,
            )

            if result:
                logger.info(f"✅ Successfully stored analysis in database")
                return True
            else:
                logger.error(f"❌ Failed to store analysis in database")
                return False

        except Exception as e:
            logger.error(f"❌ Error storing analysis in database: {e}")
            return False

    async def generate_all_combinations(self):
        """Generate all requested Calidad Total combinations."""
        logger.info("🚀 Starting generation of all Calidad Total combinations")

        combinations = [
            {
                "tool": "Calidad Total",
                "sources": ["Google Trends"],
                "language": "es",
                "type": "single-source",
            },
            {
                "tool": "Calidad Total",
                "sources": [
                    "Google Trends",
                    "Google Books",
                    "Bain Usability",
                    "Bain Satisfaction",
                    "Crossref",
                ],
                "language": "es",
                "type": "multi-source (all 5)",
            },
            {
                "tool": "Calidad Total",
                "sources": ["Google Books", "Bain Satisfaction"],
                "language": "es",
                "type": "multi-source (2 specific)",
            },
        ]

        results = []

        for i, combo in enumerate(combinations, 1):
            logger.info(f"\\n{'=' * 60}")
            logger.info(
                f"Processing combination {i}/{len(combinations)}: {combo['tool']} + {combo['type']} ({combo['language']})"
            )
            logger.info(f"{'=' * 60}")

            start_time = time.time()

            # Generate analysis
            if len(combo["sources"]) == 1:
                result = await self.generate_single_source_analysis(
                    tool_name=combo["tool"],
                    source=combo["sources"][0],
                    language=combo["language"],
                )
            else:
                result = await self.generate_multi_source_analysis(
                    tool_name=combo["tool"],
                    sources=combo["sources"],
                    language=combo["language"],
                )

            generation_time = time.time() - start_time

            if result["success"]:
                logger.info(
                    f"✅ Analysis generated successfully in {generation_time:.2f}s"
                )

                # Store in database
                storage_result = self.store_analysis_in_database(
                    result=result,
                    tool_name=combo["tool"],
                    sources=combo["sources"],
                    language=combo["language"],
                )

                results.append(
                    {
                        "combination": combo,
                        "success": True,
                        "generation_time": generation_time,
                        "storage_success": storage_result,
                        "data": result.get("data", {}),
                    }
                )
            else:
                logger.error(f"❌ Failed to generate analysis")
                results.append(
                    {
                        "combination": combo,
                        "success": False,
                        "generation_time": generation_time,
                        "error": result.get("error", "Unknown error"),
                    }
                )

        return results

    def print_summary(self, results: List[Dict[str, Any]]):
        """Print a summary of the generation results."""
        print("\n" + "=" * 70)
        print("📊 GENERATION SUMMARY")
        print("=" * 70)

        successful = sum(1 for r in results if r["success"])
        total = len(results)

        print(f"Total combinations processed: {total}")
        print(f"Successful generations: {successful}")
        print(f"Success rate: {successful / total * 100:.1f}%")

        for i, result in enumerate(results, 1):
            combo = result["combination"]
            status = "✅ SUCCESS" if result["success"] else "❌ FAILED"

            print(
                f"\n{i}. {combo['tool']} + {combo['type']} ({combo['language']}) - {status}"
            )

            if result["success"]:
                print(f"   Generation time: {result['generation_time']:.2f}s")
                print(
                    f"   Storage success: {'✅' if result['storage_success'] else '❌'}"
                )

                # Show content summary
                data = result.get("data", {})
                sections = [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "strategic_synthesis",
                    "conclusions",
                ]
                present_sections = sum(
                    1
                    for section in sections
                    if data.get(section)
                    and len(str(data.get(section, "")).strip()) > 10
                )
                print(f"   Present sections: {present_sections}/{len(sections)}")
                print(f"   Confidence score: {data.get('confidence_score', 0):.2f}")
                print(f"   Data points: {data.get('data_points_analyzed', 0)}")
            else:
                print(f"   Error: {result.get('error', 'Unknown error')}")

        print(
            f"\\n🎯 Overall Status: {'✅ ALL COMBINATIONS SUCCESSFUL' if successful == total else '⚠️ SOME COMBINATIONS FAILED'}"
        )


async def main():
    """Main execution function."""
    print("🚀 Calidad Total Analysis Generation - Starting")
    print("=" * 70)

    generator = CalidadTotalAnalysisGenerator()

    # Generate all combinations
    results = await generator.generate_all_combinations()

    # Print summary
    generator.print_summary(results)

    print("\\n✅ Calidad Total Analysis Generation - Complete!")


if __name__ == "__main__":
    asyncio.run(main())
