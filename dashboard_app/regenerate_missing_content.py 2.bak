#!/usr/bin/env python3
"""
Targeted regeneration script for missing single-source content.
Regenerates seasonal_analysis and conclusions for combinations identified as missing.
"""

import sys
import os
import json
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any
import sqlite3
import logging

# Add parent directory to path for database imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager

# Add current directory to path for key findings imports
sys.path.insert(0, str(Path(__file__).parent))

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.key_findings_service import KeyFindingsService

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def regenerate_missing_content():
    """Regenerate missing seasonal_analysis and conclusions for single-source combinations."""

    db_manager = get_precomputed_db_manager()
    ai_service = UnifiedAIService()
    kf_service = KeyFindingsService(db_manager=db_manager)

    # Get combinations that need regeneration
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT combination_hash, tool_name, language, sources_text, sources_ids
            FROM precomputed_findings 
            WHERE sources_count = 1 AND (seasonal_analysis IS NULL OR seasonal_analysis = '' OR conclusions IS NULL OR conclusions = '')
            ORDER BY tool_name, language
        """)

        combinations_to_regenerate = cursor.fetchall()
    logger.info(
        f"Found {len(combinations_to_regenerate)} combinations needing regeneration"
    )

    success_count = 0
    error_count = 0

    for (
        hash_val,
        tool_name,
        language,
        sources_text,
        sources_ids,
    ) in combinations_to_regenerate:
        try:
            logger.info(
                f"Regenerating content for {tool_name} ({language}) - {sources_text}"
            )

            # Parse sources_ids (it's stored as a string like "[1]" or "[2]")
            import ast

            sources_list = ast.literal_eval(sources_ids)

            # Generate new analysis using the key findings service
            analysis_result = await kf_service.generate_key_findings(
                tool_name=tool_name,
                selected_sources=sources_list,
                language=language,
                force_refresh=True,  # Force regeneration
            )

            if analysis_result and analysis_result.get("success"):
                ai_content = analysis_result.get("content", {})

                # Update the database with new content
                updates = {}

                # Only update missing sections
                if not ai_content.get("seasonal_analysis"):
                    updates["seasonal_analysis"] = ai_content.get(
                        "seasonal_analysis", ""
                    )
                if not ai_content.get("conclusions"):
                    updates["conclusions"] = ai_content.get("conclusions", "")

                if updates:
                    # Build update query
                    set_clauses = []
                    values = []
                    for key, value in updates.items():
                        set_clauses.append(f"{key} = ?")
                        values.append(value)

                    values.append(hash_val)

                    update_query = f"""
                        UPDATE precomputed_findings 
                        SET {", ".join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
                        WHERE combination_hash = ?
                    """

                    # Reconnect to execute update
                    with db_manager.get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(update_query, values)
                        conn.commit()

                    logger.info(f"✅ Successfully updated {tool_name} ({language})")
                    success_count += 1
                else:
                    logger.warning(f"⚠️  No updates needed for {tool_name} ({language})")

            else:
                logger.error(
                    f"❌ Failed to generate analysis for {tool_name} ({language})"
                )
                error_count += 1

            # Small delay to avoid rate limiting
            await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"❌ Error regenerating {tool_name} ({language}): {str(e)}")
            error_count += 1
            continue

    logger.info(
        f"Regeneration complete: {success_count} successful, {error_count} errors"
    )
    return success_count, error_count


async def main():
    """Main async function."""
    logger.info("Starting targeted regeneration for missing single-source content")
    success, errors = await regenerate_missing_content()

    if errors > 0:
        logger.warning(f"Completed with {errors} errors. Check logs above.")
        return False
    else:
        logger.info("All missing content successfully regenerated!")
        return True


if __name__ == "__main__":
    # Run the async main function
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
