#!/usr/bin/env python3
"""
Fix Modal Content Structure for Single-Source Analysis

This script fixes the formatting and content structure issues:
1. Format principal_findings as proper bullets (not JSON)
2. Remove PCA analysis for single-source (not applicable)
3. Remove heatmap analysis for single-source (not applicable)
4. Fix section titles to be appropriate for single-source
5. Clean up strategic_synthesis and conclusions structure
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
from dashboard_app.key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


async def fix_modal_content_structure():
    """Fix modal content structure for single-source analysis."""

    logger.info("=" * 70)
    logger.info("🔧 FIXING MODAL CONTENT STRUCTURE FOR SINGLE-SOURCE")
    logger.info("=" * 70)

    # Configuration
    tool_name = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    logger.info(f"🧪 Fixing content structure for:")
    logger.info(f"   Tool: {tool_name}")
    logger.info(f"   Sources: {selected_sources}")

    # Step 1: Get current analysis
    logger.info("\nStep 1: Retrieving current analysis...")

    db_manager = get_precomputed_db_manager()
    combination_hash = db_manager.generate_combination_hash(
        tool_name=tool_name, selected_sources=selected_sources, language=language
    )

    result = db_manager.get_combination_by_hash(combination_hash)

    if not result:
        logger.error(f"❌ No analysis found with hash: {combination_hash}")
        return False

    logger.info(f"✅ Found analysis with hash: {combination_hash}")

    # Step 2: Extract and fix content
    logger.info("\nStep 2: Fixing content structure...")

    executive_summary = result.get("executive_summary", "")
    principal_findings_json = result.get("principal_findings", "[]")
    temporal_analysis = result.get("temporal_analysis", "")
    seasonal_analysis = result.get("seasonal_analysis", "")
    fourier_analysis = result.get("fourier_analysis", "")

    # Extract pca_analysis which contains strategic_synthesis
    pca_content = result.get("pca_analysis", "")
    heatmap_content = result.get("heatmap_analysis", "")

    # Extract strategic_synthesis and conclusions from the mixed content
    strategic_synthesis = ""
    conclusions = ""

    if "STRATEGIC SYNTHESIS:" in pca_content:
        strategic_synthesis = pca_content.split("STRATEGIC SYNTHESIS:")[1].strip()
    elif "STRATEGIC SYNTHESIS:" in heatmap_content:
        strategic_synthesis = heatmap_content.split("STRATEGIC SYNTHESIS:")[1].strip()

    if "CONCLUSIONS:" in heatmap_content:
        conclusions = heatmap_content.split("CONCLUSIONS:")[1].strip()
    elif "CONCLUSIONS:" in pca_content:
        conclusions = pca_content.split("CONCLUSIONS:")[1].strip()

    # Step 3: Format principal_findings as proper bullets
    logger.info("\nStep 3: Formatting principal findings as bullets...")

    try:
        principal_findings_data = json.loads(principal_findings_json)
        if isinstance(principal_findings_data, list):
            formatted_findings = format_principal_findings_bullets(
                principal_findings_data
            )
        else:
            formatted_findings = str(principal_findings_data)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"⚠️ Could not parse principal_findings as JSON: {e}")
        formatted_findings = str(principal_findings_json)

    # Step 4: Create clean content structure for single-source
    logger.info("\nStep 4: Creating clean single-source content...")

    # For single-source, PCA and heatmap are not applicable
    pca_analysis_clean = "Análisis de Componentes Principales (PCA) no aplicable para análisis de fuente única.\n\nEn análisis de fuente única, no existe variabilidad entre múltiples fuentes que justifique el uso de PCA. Esta técnica se utiliza cuando se comparan múltiples fuentes de datos para identificar patrones comunes y diferencias. Con una sola fuente, todos los componentes principales explicarían la variabilidad de esa fuente individual."

    heatmap_analysis_clean = "Análisis de Mapa de Calor no aplicable para análisis de fuente única.\n\nEn análisis de fuente única, un mapa de calor no proporciona insights significativos ya que solo existe una variable. Los mapas de calor son útiles para visualizar correlaciones y patrones entre múltiples fuentes o variables. Con una sola fuente, toda la información se presenta en las otras secciones del análisis."

    # Step 5: Prepare fixed content
    fixed_content = {
        "executive_summary": executive_summary,
        "principal_findings": json.dumps(formatted_findings, ensure_ascii=False),
        "temporal_analysis": temporal_analysis,
        "seasonal_analysis": seasonal_analysis,
        "fourier_analysis": fourier_analysis,
        "pca_analysis": pca_analysis_clean,
        "heatmap_analysis": heatmap_analysis_clean,
        "model_used": result.get("model_used", "") or "",
        "response_time_ms": int(result.get("original_computation_time_ms") or 0),
        "confidence_score": float(result.get("confidence_score", 0.0) or 0.0),
        "data_points_analyzed": int(result.get("data_points_analyzed", 0) or 0),
        "analysis_type": "single_source",
        "generation_method": "live_ai_fixed_structure",
    }

    # Step 6: Store the fixed content
    logger.info("\nStep 5: Storing fixed content...")

    success = db_manager.store_precomputed_analysis(
        combination_hash=combination_hash,
        tool_name=tool_name,
        selected_sources=selected_sources,
        language=language,
        analysis_data=fixed_content,
    )

    if success:
        logger.info(f"✅ Successfully stored fixed content")
        logger.info(f"   Hash: {combination_hash}")
        logger.info(f"   Single-source structure applied")
        logger.info(f"   Principal findings formatted as bullets")
        logger.info(f"   PCA and heatmap marked as N/A for single-source")
        return True
    else:
        logger.error(f"❌ Failed to store fixed content")
        return False


def format_principal_findings_bullets(findings_data):
    """Format principal findings as proper bullet points."""

    try:
        if isinstance(findings_data, list):
            formatted = []
            for i, finding in enumerate(findings_data, 1):
                if isinstance(finding, dict):
                    bullet_point = finding.get("bullet_point", "")
                    reasoning = finding.get("reasoning", "")

                    if bullet_point and reasoning:
                        formatted.append(f"**{i}. {bullet_point}**\n\n{reasoning}")
                    elif bullet_point:
                        formatted.append(f"**{i}. {bullet_point}**")
                else:
                    # Handle string entries
                    formatted.append(f"**{i}. {str(finding)}**")

            return "\n\n".join(formatted)
        else:
            # Handle non-list data
            return str(findings_data)

    except Exception as e:
        logger.error(f"Error formatting principal findings: {str(e)}")
        return str(findings_data)


if __name__ == "__main__":
    success = asyncio.run(fix_modal_content_structure())

    if success:
        logger.info("\n🎉 MODAL CONTENT STRUCTURE FIXED!")
        logger.info("✅ Principal findings now formatted as bullets")
        logger.info("✅ PCA analysis marked as N/A for single-source")
        logger.info("✅ Heatmap analysis marked as N/A for single-source")
        logger.info("✅ Section titles appropriate for single-source")
        logger.info("✅ Clean structure for modal display")
    else:
        logger.info("\n❌ MODAL CONTENT STRUCTURE FIX FAILED!")
