#!/usr/bin/env python3
"""
Live AI Generation Script - Actual Groq API Calls

This script implements actual live AI generation using the Groq API
with force_refresh=True to generate real AI content that will appear
in the Groq console.

Key features:
- Uses actual Groq API calls (not precomputed data)
- Forces regeneration with force_refresh=True
- Stores results in database for future use
- Verifies API calls appear in Groq console
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Configure logging to see API calls
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG level to see all API interactions
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Import required components
from dashboard_app.key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager

# Check for Groq API key - try environment first, then use hardcoded test key
groq_api_key: str = (
    os.getenv("GROQ_API_KEY")
    or "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"
)

if not os.getenv("GROQ_API_KEY"):
    logger.warning("⚠️  GROQ_API_KEY environment variable not found!")
    logger.warning("Using hardcoded test key for demonstration purposes...")
    logger.info(f"✅ Using test Groq API key: {groq_api_key[:10]}...")
else:
    logger.info(f"✅ Groq API key found in environment: {groq_api_key[:10]}...")


async def generate_live_ai_analysis():
    """Generate actual live AI analysis using Groq API."""

    logger.info("🚀 Starting live AI generation with actual Groq API calls...")

    # Initialize database manager
    db_manager = get_database_manager()
    logger.info("✅ Database manager initialized")

    # Initialize key findings service with actual API keys
    key_findings_service = KeyFindingsService(
        db_manager=db_manager,
        groq_api_key=groq_api_key,
        config={
            "max_retries": 3,
            "enable_pca_emphasis": True,
            "confidence_threshold": 0.7,
        },
    )
    logger.info("✅ Key findings service initialized with Groq API")

    # Test combinations to generate
    test_combinations = [
        {
            "tool_name": "Calidad Total",
            "selected_sources": ["Google Trends"],
            "language": "es",
            "description": "Single source - Calidad Total + Google Trends",
        },
        {
            "tool_name": "Calidad Total",
            "selected_sources": [
                "Google Trends",
                "Bain Satisfaction",
                "Google Books",
                "Crossref",
                "Bain Usability",
            ],
            "language": "es",
            "description": "Multi source - Calidad Total + All 5 sources",
        },
    ]

    results = []

    for i, combo in enumerate(test_combinations, 1):
        logger.info(f"\n🔄 Test {i}/{len(test_combinations)}: {combo['description']}")
        logger.info(f"   Tool: {combo['tool_name']}")
        logger.info(f"   Sources: {combo['selected_sources']}")
        logger.info(f"   Language: {combo['language']}")

        try:
            # Generate with force_refresh=True to force live AI generation
            logger.info("🤖 Calling generate_key_findings with force_refresh=True...")

            start_time = datetime.now()

            result = await key_findings_service.generate_key_findings(
                tool_name=combo["tool_name"],
                selected_sources=combo["selected_sources"],
                language=combo["language"],
                force_refresh=True,  # 🔥 This forces live AI generation!
                source_display_names=combo["selected_sources"],
            )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info(f"⏱️  Generation completed in {duration:.2f} seconds")

            if result["success"]:
                logger.info(f"✅ SUCCESS: Analysis generated successfully")
                logger.info(f"   Cache hit: {result.get('cache_hit', False)}")
                logger.info(f"   Response time: {result.get('response_time_ms', 0)}ms")
                logger.info(f"   Source: {result.get('source', 'unknown')}")

                data = result.get("data", {})
                logger.info(f"   Model used: {data.get('model_used', 'unknown')}")
                logger.info(f"   Data points: {data.get('data_points_analyzed', 0)}")
                logger.info(f"   Confidence: {data.get('confidence_score', 0):.2f}")

                # Log content preview
                exec_summary = data.get("executive_summary", "")[:200]
                logger.info(f"   Executive summary preview: {exec_summary}...")

                results.append(
                    {
                        "combination": combo,
                        "success": True,
                        "duration": duration,
                        "model_used": data.get("model_used", "unknown"),
                        "response_time_ms": result.get("response_time_ms", 0),
                        "confidence_score": data.get("confidence_score", 0),
                        "data_points_analyzed": data.get("data_points_analyzed", 0),
                        "cache_hit": result.get("cache_hit", False),
                        "source": result.get("source", "unknown"),
                    }
                )

            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"❌ FAILED: {error_msg}")
                results.append(
                    {
                        "combination": combo,
                        "success": False,
                        "error": error_msg,
                        "duration": duration,
                    }
                )

        except Exception as e:
            logger.error(f"❌ EXCEPTION: {str(e)}")
            results.append(
                {"combination": combo, "success": False, "error": str(e), "duration": 0}
            )

        # Small delay between tests
        await asyncio.sleep(2)

    # Summary
    logger.info(f"\n📊 Generation Summary:")
    successful = sum(1 for r in results if r["success"])
    total = len(results)

    logger.info(f"   Total combinations: {total}")
    logger.info(f"   Successful: {successful}")
    logger.info(f"   Failed: {total - successful}")

    for i, result in enumerate(results, 1):
        combo = result["combination"]
        if result["success"]:
            logger.info(
                f"   {i}. ✅ {combo['description']} - {result['model_used']} ({result['response_time_ms']}ms)"
            )
        else:
            logger.info(
                f"   {i}. ❌ {combo['description']} - {result.get('error', 'Unknown error')}"
            )

    logger.info(f"\n🎯 IMPORTANT: Check your Groq console at https://console.groq.com/")
    logger.info(f"   to verify that actual API calls were made during this execution.")
    logger.info(f"   The calls should appear in your usage dashboard.")

    return results


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("🚀 LIVE AI GENERATION SCRIPT - ACTUAL GROQ API CALLS")
    logger.info("=" * 80)
    logger.info(
        "This script will make REAL API calls to Groq that will appear in your console."
    )
    logger.info("Make sure you have a valid Groq API key set in your environment.")
    logger.info("")

    # Run the async function
    results = asyncio.run(generate_live_ai_analysis())

    logger.info("\n" + "=" * 80)
    logger.info("✅ Live AI generation completed!")
    logger.info("=" * 80)
