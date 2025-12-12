#!/usr/bin/env python3
"""
Live AI Generation for Calidad Total Combinations using Groq API

Generates actual AI analyses using the Groq API for:
1. Calidad Total + Google Trends (single-source)
2. Calidad Total + All 5 sources (multi-source)
3. Calidad Total + Google Books, Bain Satisfaction (multi-source)

This will make actual API calls to Groq and generate fresh AI content.
"""

import asyncio
import os
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Set up Groq API key
os.environ["GROQ_API_KEY"] = "GROQ_API_KEY_PLACEHOLDER"


async def generate_live_ai_calidad_total():
    """Generate live AI analyses for Calidad Total combinations using Groq API."""

    # Import required modules
    from database_implementation.precomputed_findings_db import (
        get_precomputed_db_manager,
    )
    from dashboard_app.key_findings.key_findings_service import get_key_findings_service

    print("🚀 Live AI Generation for Calidad Total Combinations")
    print("=" * 60)
    print("🎯 This will make ACTUAL API calls to Groq!")

    # Initialize services
    db_manager = get_precomputed_db_manager()
    key_findings_service = get_key_findings_service()

    # Define combinations to generate
    combinations = [
        {
            "tool": "Calidad Total",
            "sources": ["Google Trends"],
            "language": "es",
            "description": "Single-source with Google Trends",
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
            "description": "Multi-source with all 5 sources",
        },
        {
            "tool": "Calidad Total",
            "sources": ["Google Books", "Bain Satisfaction"],
            "language": "es",
            "description": "Multi-source with Google Books and Bain Satisfaction",
        },
    ]

    results = []

    for i, combo in enumerate(combinations, 1):
        print(
            f"\n{i}. {combo['description']}: {combo['tool']} + {combo['sources']} ({combo['language']})"
        )
        print("🎯 This will make ACTUAL API calls to Groq!")

        try:
            start_time = time.time()

            # Generate live AI analysis using actual AI service
            result = await key_findings_service.generate_key_findings(
                tool_name=combo["tool"],
                selected_sources=combo["sources"],
                language=combo["language"],
                force_refresh=True,  # Force fresh AI generation
            )

            generation_time = time.time() - start_time

            if result["success"]:
                print(f"✅ Live AI generation successful in {generation_time:.2f}s")

                # Store the live AI-generated content
                combination_hash = db_manager.generate_combination_hash(
                    tool_name=combo["tool"],
                    selected_sources=combo["sources"],
                    language=combo["language"],
                )

                storage_result = db_manager.store_precomputed_analysis(
                    combination_hash=combination_hash,
                    tool_name=combo["tool"],
                    selected_sources=combo["sources"],
                    language=combo["language"],
                    analysis_data=result.get("data", {}),
                )

                if storage_result:
                    print(f"✅ Successfully stored LIVE AI-generated analysis!")
                    results.append(
                        {"success": True, "generation_time": generation_time}
                    )
                else:
                    print(f"❌ Failed to store analysis")
                    results.append({"success": False, "error": "Storage failed"})

            else:
                print(
                    f"❌ Live AI generation failed: {result.get('error', 'Unknown error')}"
                )
                results.append(
                    {"success": False, "error": result.get("error", "Unknown error")}
                )

        except Exception as e:
            print(f"❌ Error in live AI generation: {e}")
            results.append({"success": False, "error": str(e)})

    print("\\nFinal database state:")
    final_stats = db_manager.get_statistics()
    print(f"  Total findings: {final_stats.get('total_findings', 0)}")

    print("✅ Live AI generation completed!")


if __name__ == "__main__":
    asyncio.run(generate_live_ai_calidad_total())
