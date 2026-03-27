#!/usr/bin/env python3
"""
30-Combination Key Findings Batch Generator

This script generates 30 specific tool-source-language combinations using live AI queries
and stores them in the precomputed findings database.

Categories:
- Category 1: 10 single-source combinations
- Category 2: 10 two-source combinations
- Category 3: 10 multi-source combinations (3-5 sources)

Total estimated cost: ~$0.90
Total estimated time: ~22.5 minutes
"""

import os
import sys
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add dashboard_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Import required components
from key_findings.key_findings_service import get_key_findings_service
from key_findings.unified_ai_service import UnifiedAIService
from database_implementation.precomputed_findings_db import get_precomputed_db_manager

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class CombinationBatchGenerator:
    """Generates 30 specific combinations for testing the dashboard."""

    def __init__(self):
        self.db_manager = get_precomputed_db_manager()
        self.ai_service = UnifiedAIService(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.start_time = None
        self.results = {
            "total_combinations": 30,
            "successful": 0,
            "failed": 0,
            "cost_estimate": 0.0,
            "time_estimate": 0.0,
            "categories": {
                "single_source": {"total": 10, "completed": 0, "failed": 0},
                "multi_source_pairs": {"total": 10, "completed": 0, "failed": 0},
                "comprehensive": {"total": 10, "completed": 0, "failed": 0},
            },
            "details": [],
        }

    def get_combinations(self) -> List[Dict[str, Any]]:
        """Get the 30 specific combinations to generate."""

        # Category 1: Single-Source Foundation (10 combinations)
        single_source = [
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends"],
                "language": "es",
                "category": "single_source",
            },
            {
                "tool": "Competencias Centrales",
                "sources": ["Google Trends"],
                "language": "en",
                "category": "single_source",
            },
            {
                "tool": "Cuadro de Mando Integral",
                "sources": ["Google Books"],
                "language": "es",
                "category": "single_source",
            },
            {
                "tool": "Experiencia del Cliente",
                "sources": ["Bain Usability"],
                "language": "en",
                "category": "single_source",
            },
            {
                "tool": "Fusiones y Adquisiciones",
                "sources": ["Crossref"],
                "language": "es",
                "category": "single_source",
            },
            {
                "tool": "Gestión de Costos",
                "sources": ["Bain Satisfaction"],
                "language": "en",
                "category": "single_source",
            },
            {
                "tool": "Innovación Colaborativa",
                "sources": ["Google Trends"],
                "language": "es",
                "category": "single_source",
            },
            {
                "tool": "Lealtad del Cliente",
                "sources": ["Google Books"],
                "language": "en",
                "category": "single_source",
            },
            {
                "tool": "Outsourcing",
                "sources": ["Bain Usability"],
                "language": "es",
                "category": "single_source",
            },
            {
                "tool": "Planificación Estratégica",
                "sources": ["Crossref"],
                "language": "en",
                "category": "single_source",
            },
        ]

        # Category 2: Multi-Source Strategic Pairs (10 combinations)
        multi_source_pairs = [
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends", "Google Books"],
                "language": "es",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Competencias Centrales",
                "sources": ["Google Trends", "Bain Usability"],
                "language": "en",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Cuadro de Mando Integral",
                "sources": ["Google Books", "Crossref"],
                "language": "es",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Experiencia del Cliente",
                "sources": ["Bain Usability", "Bain Satisfaction"],
                "language": "en",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Gestión del Cambio",
                "sources": ["Google Trends", "Crossref"],
                "language": "es",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Innovación Colaborativa",
                "sources": ["Google Books", "Bain Usability"],
                "language": "en",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Lealtad del Cliente",
                "sources": ["Google Trends", "Bain Satisfaction"],
                "language": "es",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Optimización de Precios",
                "sources": ["Crossref", "Bain Usability"],
                "language": "en",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Reingeniería de Procesos",
                "sources": ["Google Books", "Crossref"],
                "language": "es",
                "category": "multi_source_pairs",
            },
            {
                "tool": "Segmentación de Clientes",
                "sources": ["Bain Usability", "Bain Satisfaction"],
                "language": "en",
                "category": "multi_source_pairs",
            },
        ]

        # Category 3: Comprehensive Multi-Source (10 combinations)
        comprehensive = [
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends", "Google Books", "Bain Usability"],
                "language": "es",
                "category": "comprehensive",
            },
            {
                "tool": "Competencias Centrales",
                "sources": [
                    "Google Trends",
                    "Google Books",
                    "Bain Usability",
                    "Crossref",
                    "Bain Satisfaction",
                ],
                "language": "en",
                "category": "comprehensive",
            },
            {
                "tool": "Experiencia del Cliente",
                "sources": ["Google Trends", "Bain Usability", "Bain Satisfaction"],
                "language": "es",
                "category": "comprehensive",
            },
            {
                "tool": "Gestión de la Cadena de Suministro",
                "sources": ["Google Books", "Crossref", "Bain Usability"],
                "language": "en",
                "category": "comprehensive",
            },
            {
                "tool": "Innovación Colaborativa",
                "sources": [
                    "Google Trends",
                    "Google Books",
                    "Bain Usability",
                    "Crossref",
                    "Bain Satisfaction",
                ],
                "language": "es",
                "category": "comprehensive",
            },
            {
                "tool": "Planificación Estratégica",
                "sources": ["Google Trends", "Google Books", "Crossref"],
                "language": "en",
                "category": "comprehensive",
            },
            {
                "tool": "Propósito y Visión",
                "sources": ["Google Trends", "Bain Usability", "Bain Satisfaction"],
                "language": "es",
                "category": "comprehensive",
            },
            {
                "tool": "Talento y Compromiso",
                "sources": [
                    "Google Trends",
                    "Google Books",
                    "Bain Usability",
                    "Crossref",
                    "Bain Satisfaction",
                ],
                "language": "en",
                "category": "comprehensive",
            },
            {
                "tool": "Alianzas y Capital de Riesgo",
                "sources": ["Google Books", "Crossref", "Bain Usability"],
                "language": "es",
                "category": "comprehensive",
            },
            {
                "tool": "Estrategias de Crecimiento",
                "sources": ["Google Trends", "Google Books", "Bain Satisfaction"],
                "language": "en",
                "category": "comprehensive",
            },
        ]

        return single_source + multi_source_pairs + comprehensive

    def generate_sources_text(self, sources: List[str]) -> str:
        """Generate the sources text for database storage."""
        if len(sources) == 5:
            return "All 5 Sources"
        else:
            return ", ".join(sources)

    def calculate_cost_estimate(self, num_sources: int, language: str) -> float:
        """Calculate cost estimate based on sources and language."""
        # Base costs per combination type
        base_costs = {
            1: 0.02,  # Single source
            2: 0.03,  # Two sources
            3: 0.035,  # Three sources
            4: 0.04,  # Four sources
            5: 0.05,  # Five sources
        }

        cost = base_costs.get(num_sources, 0.04)

        # Language adjustment (English slightly more expensive)
        if language == "en":
            cost *= 1.1

        return cost

    def calculate_time_estimate(self, num_sources: int) -> float:
        """Calculate time estimate in seconds."""
        time_per_source = 30  # 30 seconds per source

        # Multi-source combinations take longer
        if num_sources > 1:
            time_per_source *= 1.5

        return num_sources * time_per_source

    async def generate_single_combination(
        self, combination: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a single combination using live AI."""

        tool_name = combination["tool"]
        sources = combination["sources"]
        language = combination["language"]
        category = combination["category"]

        logger.info(f"🎯 Generating: {tool_name} + {len(sources)} sources ({language})")

        try:
            # Check if combination already exists
            sources_text = self.generate_sources_text(sources)
            hash_value = self.db_manager.generate_combination_hash(
                tool_name=tool_name, selected_sources=sources, language=language
            )

            existing = self.db_manager.get_combination_by_hash(hash_value)
            if existing:
                logger.info(
                    f"⚠️  Combination already exists: {tool_name} + {sources_text}"
                )
                return {
                    "success": True,
                    "already_exists": True,
                    "tool": tool_name,
                    "sources": sources,
                    "language": language,
                    "category": category,
                    "hash": hash_value,
                }

            # Initialize key findings service for this combination
            key_findings_service = get_key_findings_service(
                self.db_manager,
                os.getenv("GROQ_API_KEY", ""),
                os.getenv("OPENROUTER_API_KEY", ""),
                {},
            )

            # Generate the analysis using force_refresh to ensure live AI
            start_time = datetime.now()

            result = await key_findings_service.generate_key_findings(
                tool_name=tool_name,
                selected_sources=sources,
                language=language,
                force_refresh=True,  # Force live AI generation
            )

            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()

            # Calculate estimates
            cost_estimate = self.calculate_cost_estimate(len(sources), language)
            time_estimate = self.calculate_time_estimate(len(sources))

            logger.info(
                f"✅ Generated: {tool_name} in {generation_time:.1f}s (est: {time_estimate:.1f}s)"
            )

            return {
                "success": True,
                "tool": tool_name,
                "sources": sources,
                "sources_text": sources_text,
                "language": language,
                "category": category,
                "hash": hash_value,
                "generation_time": generation_time,
                "cost_estimate": cost_estimate,
                "time_estimate": time_estimate,
                "timestamp": start_time.isoformat(),
            }

        except Exception as e:
            logger.error(f"❌ Failed to generate {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
                "sources": sources,
                "language": language,
                "category": category,
                "hash": hash_value if "hash_value" in locals() else None,
            }

    async def generate_all_combinations(self):
        """Generate all 30 combinations."""

        logger.info("🚀 Starting 30-Combination Batch Generation")
        logger.info("=" * 60)

        self.start_time = datetime.now()
        combinations = self.get_combinations()

        total_cost = 0.0
        total_time = 0.0

        for i, combination in enumerate(combinations, 1):
            logger.info(f"\n📊 Processing combination {i}/30")
            logger.info(f"   Category: {combination['category']}")
            logger.info(f"   Tool: {combination['tool']}")
            logger.info(
                f"   Sources: {len(combination['sources'])} ({combination['sources']})"
            )
            logger.info(f"   Language: {combination['language']}")

            # Generate the combination
            result = await self.generate_single_combination(combination)

            # Update results
            self.results["details"].append(result)

            if result["success"]:
                self.results["successful"] += 1
                self.results["categories"][combination["category"]]["completed"] += 1
                total_cost += result.get("cost_estimate", 0.03)
                total_time += result.get("generation_time", 30)
            else:
                self.results["failed"] += 1
                self.results["categories"][combination["category"]]["failed"] += 1

            # Progress update
            progress = (i / 30) * 100
            logger.info(
                f"   Progress: {i}/30 ({progress:.1f}%) | Success: {self.results['successful']} | Failed: {self.results['failed']}"
            )

        # Final statistics
        self.results["cost_estimate"] = round(total_cost, 2)
        self.results["time_estimate"] = round(total_time / 60, 1)  # Convert to minutes
        self.results["actual_time"] = round(
            (datetime.now() - self.start_time).total_seconds() / 60, 1
        )

        self.print_final_summary()
        self.save_results()

    def print_final_summary(self):
        """Print the final generation summary."""

        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds() / 60

        logger.info("\n" + "=" * 80)
        logger.info("🎯 30-COMBINATION GENERATION COMPLETE")
        logger.info("=" * 80)

        logger.info(f"📊 SUMMARY STATISTICS:")
        logger.info(f"   Total combinations: {self.results['total_combinations']}")
        logger.info(f"   Successful: {self.results['successful']}")
        logger.info(f"   Failed: {self.results['failed']}")
        logger.info(f"   Success rate: {(self.results['successful'] / 30) * 100:.1f}%")

        logger.info(f"\n💰 COST & TIME:")
        logger.info(f"   Estimated cost: ${self.results['cost_estimate']:.2f}")
        logger.info(f"   Estimated time: {self.results['time_estimate']:.1f} minutes")
        logger.info(f"   Actual time: {total_duration:.1f} minutes")

        logger.info(f"\n📋 CATEGORY BREAKDOWN:")
        for category, data in self.results["categories"].items():
            success_rate = (
                (data["completed"] / data["total"]) * 100 if data["total"] > 0 else 0
            )
            logger.info(
                f"   {category.replace('_', ' ').title()}: {data['completed']}/{data['total']} ({success_rate:.1f}%)"
            )

        logger.info(f"\n🎯 DATABASE IMPACT:")
        logger.info(
            f"   Database coverage: {self.results['successful']}/30 new combinations"
        )
        logger.info(
            f"   Total combinations in DB: {3 + self.results['successful']} (was 3)"
        )
        logger.info(
            f"   Coverage increase: {((3 + self.results['successful']) / 1302) * 100:.3f}%"
        )

        logger.info("=" * 80)

    def save_results(self):
        """Save generation results to file."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"30_combination_generation_results_{timestamp}.json"

        # Add metadata
        self.results["generation_started"] = self.start_time.isoformat()
        self.results["generation_completed"] = datetime.now().isoformat()
        self.results["duration_minutes"] = round(
            (datetime.now() - self.start_time).total_seconds() / 60, 1
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Results saved to: {filename}")


async def main():
    """Main execution function."""

    print("🚀 30-Combination Key Findings Batch Generator")
    print("=" * 60)

    # Verify API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "GROQ_API_KEY_PLACEHOLDER":
        print("❌ GROQ_API_KEY not configured or invalid")
        print("   Please ensure GROQ_API_KEY is set in your .env file")
        return

    print(f"✅ API Key configured: {api_key[:20]}...")

    # Initialize and run generator
    generator = CombinationBatchGenerator()
    await generator.generate_all_combinations()


if __name__ == "__main__":
    asyncio.run(main())
