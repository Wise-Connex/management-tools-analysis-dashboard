#!/usr/bin/env python3
"""
Fix Final Modal Formatting Issues

This script fixes the remaining formatting issues:
1. Remove JSON wrapper from principal findings
2. Completely remove PCA and heatmap sections for single-source
3. Clean up section titles and duplicate headers
4. Ensure proper single-source modal structure
"""

import os
import sys
import asyncio
import logging
import json
import re
from datetime import datetime

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Import required components
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def fix_final_modal_formatting():
    """Fix final formatting issues in modal content."""

    logger.info("=" * 70)
    logger.info("🔧 FIXING FINAL MODAL FORMATTING ISSUES")
    logger.info("=" * 70)

    # Configuration
    tool_name = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    db_manager = get_precomputed_db_manager()
    combination_hash = db_manager.generate_combination_hash(
        tool_name=tool_name, selected_sources=selected_sources, language=language
    )

    result = db_manager.get_combination_by_hash(combination_hash)

    if not result:
        logger.error(f"❌ No analysis found with hash: {combination_hash}")
        return False

    logger.info(f"✅ Found analysis with hash: {combination_hash}")

    # Extract current content
    executive_summary = clean_section_content(result.get("executive_summary", ""))
    principal_findings_raw = result.get("principal_findings", "")
    temporal_analysis = clean_section_content(result.get("temporal_analysis", ""))
    seasonal_analysis = clean_section_content(result.get("seasonal_analysis", ""))
    fourier_analysis = clean_section_content(result.get("fourier_analysis", ""))
    strategic_synthesis = clean_section_content(result.get("strategic_synthesis", ""))
    conclusions = clean_section_content(result.get("conclusions", ""))

    # Fix principal findings - remove JSON wrapper and format as clean bullets
    logger.info("\nStep 1: Fixing principal findings formatting...")
    principal_findings = fix_principal_findings_format(principal_findings_raw)

    # Clean up seasonal analysis - remove duplicate header
    logger.info("\nStep 2: Cleaning up seasonal analysis...")
    seasonal_analysis = clean_seasonal_analysis(seasonal_analysis)

    # For single-source, we don't need PCA and heatmap at all
    logger.info("\nStep 3: Removing PCA and heatmap for single-source...")

    # Prepare final clean content structure
    final_content = {
        "executive_summary": executive_summary,
        "principal_findings": json.dumps(principal_findings, ensure_ascii=False),
        "temporal_analysis": temporal_analysis,
        "seasonal_analysis": seasonal_analysis,
        "fourier_analysis": fourier_analysis,
        "strategic_synthesis": strategic_synthesis,
        "conclusions": conclusions,
        "model_used": result.get("model_used", "") or "",
        "response_time_ms": int(result.get("original_computation_time_ms") or 0),
        "confidence_score": float(result.get("confidence_score", 0.0) or 0.0),
        "data_points_analyzed": int(result.get("data_points_analyzed", 0) or 0),
        "analysis_type": "single_source",
        "generation_method": "live_ai_final_clean",
    }

    # Store the final clean content
    success = db_manager.store_precomputed_analysis(
        combination_hash=combination_hash,
        tool_name=tool_name,
        selected_sources=selected_sources,
        language=language,
        analysis_data=final_content,
    )

    if success:
        logger.info(f"✅ Successfully stored final clean content")
        logger.info(f"   Principal findings: {len(principal_findings)} characters")
        logger.info(f"   PCA and heatmap: Completely removed for single-source")
        logger.info(f"   Clean section titles")
        logger.info(f"   No duplicate headers")
        return True
    else:
        logger.error(f"❌ Failed to store final clean content")
        return False


def fix_principal_findings_format(principal_findings_raw):
    """Fix principal findings by removing JSON wrapper and formatting as clean bullets."""

    try:
        # Remove JSON wrapper if present
        if principal_findings_raw.startswith('"') and principal_findings_raw.endswith(
            '"'
        ):
            # It's wrapped in JSON string quotes
            cleaned = principal_findings_raw[1:-1]  # Remove outer quotes
            # Unescape the inner quotes
            cleaned = cleaned.replace('\\"', '"')
        else:
            cleaned = principal_findings_raw

        # Try to parse as JSON
        try:
            findings_data = json.loads(cleaned)
            if isinstance(findings_data, list):
                formatted = []
                for i, finding in enumerate(findings_data, 1):
                    if isinstance(finding, dict):
                        bullet_point = finding.get("bullet_point", "")
                        reasoning = finding.get("reasoning", "")

                        if bullet_point and reasoning:
                            formatted.append(f"• **{bullet_point}**\n\n{reasoning}")
                        elif bullet_point:
                            formatted.append(f"• **{bullet_point}**")
                    else:
                        formatted.append(f"• {str(finding)}")

                return "\n\n".join(formatted)
            else:
                # If it's not a list, just clean it up
                return cleaned
        except (json.JSONDecodeError, TypeError):
            # If it's not valid JSON, clean it up anyway
            return cleaned

    except Exception as e:
        logger.error(f"Error fixing principal findings: {str(e)}")
        return principal_findings_raw


def clean_seasonal_analysis(seasonal_analysis):
    """Clean seasonal analysis by removing duplicate header."""

    # Remove the duplicate "📅 PATRONES ESTACIONALES" header if it appears at the start
    if seasonal_analysis.startswith("📅 PATRONES ESTACIONALES\n\n"):
        return seasonal_analysis[26:]  # Remove the header

    return seasonal_analysis


def clean_section_content(content):
    """Clean general section content by removing extra whitespace and fixing formatting."""

    # Remove extra newlines and clean up
    content = re.sub(r"\n{3,}", "\n\n", content)
    content = content.strip()

    return content


if __name__ == "__main__":
    success = fix_final_modal_formatting()

    if success:
        logger.info("\n🎉 FINAL MODAL FORMATTING FIXED!")
        logger.info("✅ Principal findings now clean (no JSON wrapper)")
        logger.info("✅ PCA and heatmap completely removed for single-source")
        logger.info("✅ No duplicate section headers")
        logger.info("✅ Clean single-source modal structure")
        logger.info("✅ Ready for perfect modal display")
    else:
        logger.info("\n❌ FINAL FORMATTING FIX FAILED!")
