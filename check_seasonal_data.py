#!/usr/bin/env python3
"""
Check Seasonal Data Availability for AI

This script checks if we have meaningful seasonal data to pass to the AI
and verifies that it's being included in the prompt.
"""

import os
import sys
import asyncio
import logging
import json
from datetime import datetime

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Import required components
from dashboard_app.key_findings.data_aggregator import DataAggregator
from database import get_database_manager
from dashboard_app.fix_source_mapping import map_display_names_to_source_ids


async def check_seasonal_data():
    """Check if we have meaningful seasonal data and if it's being passed to AI."""

    logger.info("=" * 70)
    logger.info("🔍 CHECKING SEASONAL DATA AVAILABILITY")
    logger.info("=" * 70)

    # Configuration
    tool_name = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    # Initialize data aggregator
    data_aggregator = DataAggregator(get_database_manager(), None)

    logger.info(f"🧪 Testing data collection for:")
    logger.info(f"   Tool: {tool_name}")
    logger.info(f"   Sources: {selected_sources}")

    try:
        # Convert display names to source IDs
        selected_source_ids = map_display_names_to_source_ids(selected_sources)
        logger.info(f"   Source IDs: {selected_source_ids}")

        # Collect analysis data
        logger.info("\n📊 Collecting analysis data...")
        analysis_data = data_aggregator.collect_analysis_data(
            tool_name, selected_source_ids, language, selected_sources
        )

        if "error" in analysis_data:
            logger.error(f"❌ Data collection failed: {analysis_data['error']}")
            return False

        logger.info(f"✅ Data collection successful!")

        # Check single source insights
        single_source_insights = analysis_data.get("single_source_insights", {})

        if not single_source_insights:
            logger.error("❌ No single source insights found!")
            return False

        if "error" in single_source_insights:
            logger.error(
                f"❌ Single source insights error: {single_source_insights['error']}"
            )
            return False

        logger.info(f"✅ Single source insights found!")

        # Check seasonal patterns specifically
        seasonal_patterns = single_source_insights.get("seasonal_patterns", {})

        logger.info("\n🌊 SEASONAL PATTERNS ANALYSIS")
        logger.info("=" * 50)

        if not seasonal_patterns:
            logger.error("❌ NO seasonal patterns found in single source insights!")
            return False

        logger.info(f"✅ Seasonal patterns data found!")

        # Analyze the seasonal data content
        monthly_patterns = seasonal_patterns.get("monthly_patterns", {})
        quarterly_patterns = seasonal_patterns.get("quarterly_patterns", {})
        year_over_year = seasonal_patterns.get("year_over_year", {})
        seasonality_strength = seasonal_patterns.get("seasonality_strength", {})

        logger.info(f"\n📅 Monthly Patterns:")
        if monthly_patterns:
            monthly_means = monthly_patterns.get("monthly_means", {})
            peak_month = monthly_patterns.get("peak_month", "Unknown")
            low_month = monthly_patterns.get("low_month", "Unknown")
            peak_value = monthly_patterns.get("peak_value", 0)
            low_value = monthly_patterns.get("low_value", 0)

            logger.info(f"   Peak: Month {peak_month} = {peak_value:.1f}")
            logger.info(f"   Low: Month {low_month} = {low_value:.1f}")
            logger.info(f"   Data points: {len(monthly_means)} months")

            if len(monthly_means) > 0:
                logger.info(
                    f"   Sample monthly data: {list(monthly_means.items())[:3]}"
                )
            else:
                logger.warning("⚠️ Monthly means is empty!")
        else:
            logger.error("❌ No monthly patterns found!")

        logger.info(f"\n📊 Quarterly Patterns:")
        if quarterly_patterns:
            quarterly_means = quarterly_patterns.get("quarterly_means", {})
            logger.info(f"   Data points: {len(quarterly_means)} quarters")
            logger.info(f"   Quarterly data: {quarterly_means}")
        else:
            logger.error("❌ No quarterly patterns found!")

        logger.info(f"\n📈 Year over Year:")
        if year_over_year:
            yearly_means = year_over_year.get("yearly_means", {})
            growth_rate = year_over_year.get("average_growth_rate", 0)
            logger.info(f"   Years covered: {len(yearly_means)} years")
            logger.info(f"   Growth rate: {growth_rate:.2f}%")
            logger.info(f"   Sample years: {list(yearly_means.items())[:3]}")
        else:
            logger.error("❌ No year over year data found!")

        logger.info(f"\n💪 Seasonality Strength:")
        if seasonality_strength:
            strength_value = seasonality_strength.get("strength_value", 0)
            strength_level = seasonality_strength.get("strength_level", "unknown")
            logger.info(f"   Strength: {strength_value:.3f}")
            logger.info(f"   Level: {strength_level}")
        else:
            logger.error("❌ No seasonality strength found!")

        # Overall assessment
        logger.info(f"\n" + "=" * 50)
        logger.info(f"📋 SEASONAL DATA ASSESSMENT")
        logger.info("=" * 50)

        meaningful_data = True

        if not monthly_patterns or len(monthly_patterns.get("monthly_means", {})) < 6:
            logger.error("❌ Insufficient monthly data for meaningful analysis")
            meaningful_data = False

        if (
            not quarterly_patterns
            or len(quarterly_patterns.get("quarterly_means", {})) < 2
        ):
            logger.error("❌ Insufficient quarterly data for meaningful analysis")
            meaningful_data = False

        if seasonality_strength.get("strength_value", 0) < 0.05:
            logger.warning(
                "⚠️ Very weak seasonality - may not be interesting to analyze"
            )

        if meaningful_data:
            logger.info("✅ We have meaningful seasonal data for AI analysis!")

            # Show what seasonal data would look like in the prompt
            logger.info(f"\n📝 SEASONAL DATA FOR PROMPT:")
            logger.info("=" * 50)
            prompt_seasonal_data = f"""
SEASONAL PATTERNS DATA (for analysis):
- Monthly means: {json.dumps(monthly_patterns.get("monthly_means", {}), indent=2)}
- Peak month: {monthly_patterns.get("peak_month", "N/A")} ({monthly_patterns.get("peak_value", 0):.1f})
- Low month: {monthly_patterns.get("low_month", "N/A")} ({monthly_patterns.get("low_value", 0):.1f})
- Quarterly means: {json.dumps(quarterly_patterns.get("quarterly_means", {}), indent=2)}
- Yearly means: {json.dumps(year_over_year.get("yearly_means", {}), indent=2)}
- Seasonality strength: {seasonality_strength.get("strength_value", 0):.3f} ({seasonality_strength.get("strength_level", "unknown")})
"""
            logger.info(prompt_seasonal_data)

            return True
        else:
            logger.error("❌ Insufficient seasonal data for meaningful AI analysis")
            return False

    except Exception as e:
        logger.error(f"❌ Exception during seasonal data check: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(check_seasonal_data())

    if success:
        logger.info("\n🎉 SEASONAL DATA IS AVAILABLE!")
        logger.info("The issue is likely in the prompt, not the data.")
    else:
        logger.info("\n❌ SEASONAL DATA ISSUES FOUND!")
        logger.info("This explains why AI can't generate seasonal analysis.")
