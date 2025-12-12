#!/usr/bin/env python3
"""
Fix Seasonal Analysis with Post-Processing

Since the AI model is not generating the seasonal_analysis section,
this script implements a post-processing solution that creates the
missing section by extracting seasonal content from other sections.
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


async def fix_seasonal_analysis_post_processing():
    """Fix missing seasonal_analysis using post-processing."""

    logger.info("=" * 70)
    logger.info("🔧 FIXING SEASONAL ANALYSIS - POST PROCESSING")
    logger.info("=" * 70)

    # Configuration
    tool_name = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    logger.info(f"🧪 Fixing analysis for:")
    logger.info(f"   Tool: {tool_name}")
    logger.info(f"   Sources: {selected_sources}")

    # Step 1: Generate fresh analysis
    logger.info("\nStep 1: Generating fresh analysis...")

    key_findings_service = KeyFindingsService(
        db_manager=get_database_manager(),
        groq_api_key="GROQ_API_KEY_PLACEHOLDER",
        config={
            "max_retries": 1,
            "enable_pca_emphasis": True,
            "confidence_threshold": 0.7,
        },
    )

    try:
        result = await key_findings_service.generate_key_findings(
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            force_refresh=True,
            source_display_names=selected_sources,
        )

        if not result["success"]:
            logger.error(
                f"❌ Live generation failed: {result.get('error', 'Unknown error')}"
            )
            return False

        logger.info(f"✅ Fresh analysis generated")

        # Step 2: Check if seasonal_analysis is missing
        data = result["data"]

        seasonal_content = data.get("seasonal_analysis", "")
        if seasonal_content and len(str(seasonal_content)) > 50:
            logger.info(
                f"✅ seasonal_analysis already present: {len(seasonal_content)} chars"
            )
            return True

        logger.info(
            f"❌ seasonal_analysis missing or empty - applying post-processing fix"
        )

        # Step 3: Get seasonal data for generation
        logger.info("\nStep 2: Collecting seasonal data for generation...")

        from dashboard_app.fix_source_mapping import map_display_names_to_source_ids
        from dashboard_app.key_findings.data_aggregator import DataAggregator

        data_aggregator = DataAggregator(get_database_manager(), None)
        selected_source_ids = map_display_names_to_source_ids(selected_sources)

        analysis_data = data_aggregator.collect_analysis_data(
            tool_name, selected_source_ids, language, selected_sources
        )

        if "error" in analysis_data:
            logger.error(f"❌ Data collection failed: {analysis_data['error']}")
            return False

        single_source_insights = analysis_data.get("single_source_insights", {})
        seasonal_patterns = single_source_insights.get("seasonal_patterns", {})

        if not seasonal_patterns:
            logger.error("❌ No seasonal patterns found in data")
            return False

        # Step 4: Generate seasonal_analysis content manually
        logger.info("\nStep 3: Generating seasonal_analysis content...")

        seasonal_analysis = generate_seasonal_analysis_content(
            tool_name=tool_name,
            source_name="Google Trends",
            seasonal_patterns=seasonal_patterns,
            language=language,
        )

        if not seasonal_analysis:
            logger.error("❌ Failed to generate seasonal analysis content")
            return False

        logger.info(f"✅ Generated seasonal_analysis: {len(seasonal_analysis)} chars")

        # Step 5: Add to the result and store
        logger.info("\nStep 4: Updating result with seasonal_analysis...")

        data["seasonal_analysis"] = seasonal_analysis

        # Verify all sections are now present
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

        logger.info("\nStep 5: Verifying all sections present...")

        all_present = True
        for section in required_sections:
            content = data.get(section, "")
            if content and len(str(content)) > 50:
                logger.info(f"   ✅ {section}: {len(str(content))} chars")
            else:
                logger.error(f"   ❌ {section}: {len(str(content))} chars (missing)")
                all_present = False

        if not all_present:
            logger.error("❌ Some sections still missing after post-processing")
            return False

        # Step 6: Store the fixed analysis
        logger.info("\nStep 6: Storing fixed analysis in database...")

        db_manager = get_precomputed_db_manager()
        combination_hash = db_manager.generate_combination_hash(
            tool_name=tool_name, selected_sources=selected_sources, language=language
        )

        # Map AI-generated sections to database schema fields
        # The database schema expects: executive_summary, principal_findings, temporal_analysis,
        # seasonal_analysis, fourier_analysis, pca_analysis, heatmap_analysis

        # Store strategic_synthesis and conclusions in pca_analysis and heatmap_analysis for now
        # (since this is single-source analysis, PCA/heatmap are less critical)
        pca_content = f"{data.get('pca_analysis', '')}\n\nSTRATEGIC SYNTHESIS:\n{data.get('strategic_synthesis', '')}"
        heatmap_content = f"{data.get('heatmap_analysis', '')}\n\nCONCLUSIONS:\n{data.get('conclusions', '')}"

        analysis_content = {
            "executive_summary": data.get("executive_summary", ""),
            "principal_findings": json.dumps(data.get("principal_findings", []))
            if data.get("principal_findings")
            else "[]",
            "temporal_analysis": data.get("temporal_analysis", ""),
            "seasonal_analysis": data.get("seasonal_analysis", ""),  # Fixed!
            "fourier_analysis": data.get("fourier_analysis", ""),
            "pca_analysis": pca_content,
            "heatmap_analysis": heatmap_content,
            "model_used": data.get("model_used", ""),
            "response_time_ms": int(result.get("response_time_ms", 0)),
            "confidence_score": float(data.get("confidence_score", 0.0)),
            "data_points_analyzed": int(data.get("data_points_analyzed", 0)),
            "analysis_type": "single_source",
            "generation_method": "live_ai_fixed_post_processing",
        }

        success = db_manager.store_precomputed_analysis(
            combination_hash=combination_hash,
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            analysis_data=analysis_content,
        )

        if success:
            logger.info(f"✅ Successfully stored fixed analysis")
            logger.info(f"   Hash: {combination_hash}")
            logger.info(f"   All 7 sections now present and verified")
            return True
        else:
            logger.error(f"❌ Failed to store fixed analysis")
            return False

    except Exception as e:
        logger.error(f"❌ Exception during post-processing: {str(e)}")
        return False


def generate_seasonal_analysis_content(
    tool_name, source_name, seasonal_patterns, language
):
    """Generate seasonal_analysis content based on the patterns."""

    try:
        if language == "es":
            monthly_patterns = seasonal_patterns.get("monthly_patterns", {})
            quarterly_patterns = seasonal_patterns.get("quarterly_patterns", {})
            year_over_year = seasonal_patterns.get("year_over_year", {})
            seasonality_strength = seasonal_patterns.get("seasonality_strength", {})

            peak_month = monthly_patterns.get("peak_month", "N/A")
            low_month = monthly_patterns.get("low_month", "N/A")
            peak_value = monthly_patterns.get("peak_value", 0)
            low_value = monthly_patterns.get("low_value", 0)
            strength_value = seasonality_strength.get("strength_value", 0)
            strength_level = seasonality_strength.get("strength_level", "unknown")

            # Create Spanish seasonal analysis
            seasonal_analysis = f"""📅 PATRONES ESTACIONALES

El análisis de patrones estacionales de {tool_name} en {source_name} revela una estructura temporal distintiva que proporciona insights críticos para el timing óptimo de implementación organizacional.

**Interpretación de Fuerza Estacional:**

El análisis cuantitativo revela una fuerza estacional de {strength_value:.3f}, clasificada como "{strength_level}", lo que indica que los patrones estacionales son {"sustancialmente significativos" if strength_value > 0.1 else "moderadamente presentes" if strength_value > 0.05 else "sutilmente detectables"}. Esta fuerza estacional sugiere que la adopción de {tool_name} no es uniforme a lo largo del año, sino que sigue ritmos predecibles relacionados con ciclos empresariales y de planificación organizacional.

**Periodicidad y Ciclos Identificados:**

Los datos mensuales muestran un patrón claro con el pico máximo ocurriendo en el mes {peak_month} ({peak_value:.1f} puntos) y el mínimo en el mes {low_month} ({low_value:.1f} puntos). Esta diferencia de {((peak_value - low_value) / peak_value * 100):.1f}% entre el pico y el valle estacional indica una variabilidad significativa que las organizaciones pueden aprovechar estratégicamente.

**Picos y Valles Estacionales:**

El análisis de picos estacionales revela que {tool_name} experimenta su mayor interés durante {peak_month}, lo cual probablemente coincide con períodos de planificación estratégica anual y establecimiento de objetivos empresariales. Por el contrario, el mínimo en {low_month} sugiere menor actividad corporativa, posiblemente relacionado con períodos vacacionales o de menor intensidad operacional.

**Variabilidad Estacional:**

La variabilidad estacional identificada indica {"alta consistencia" if strength_value > 0.15 else "consistencia moderada" if strength_value > 0.08 else "variabilidad significativa"} en los patrones temporales, lo que sugiere que las organizaciones han desarrollado comportamientos predecibles relacionados con la adopción de {tool_name} a lo largo del año.

**Implicaciones de Planificación:**

Estos hallazgos estacionales tienen implicaciones directas para la planificación estratégica. Las organizaciones que buscan implementar {tool_name} deben considerar el timing estacional para maximizar el impacto y la adopción. El período de {peak_month} ofrece la ventana óptima para lanzamientos y iniciativas de implementación, mientras que {low_month} puede ser ideal para evaluación y planificación de la siguiente fase.

**Recomendaciones de Timing:**

Basado en los patrones estacionales identificados, se recomienda:
1. Iniciar procesos de implementación durante {peak_month} para capitalizar el interés máximo
2. Realizar evaluaciones y ajustes durante {low_month} cuando la presión operacional es menor
3. Planificar actividades de formación y capacitación para coincidir con los períodos de mayor receptividad organizacional

Este análisis estacional proporciona una guía temporal precisa para maximizar la efectividad de la implementación de {tool_name} en contextos organizacionales."""

            return seasonal_analysis

        else:
            # English version (if needed)
            return "English seasonal analysis content would go here."

    except Exception as e:
        logger.error(f"Error generating seasonal analysis: {str(e)}")
        return None


if __name__ == "__main__":
    success = asyncio.run(fix_seasonal_analysis_post_processing())

    if success:
        logger.info("\n🎉 POST-PROCESSING FIX SUCCESSFUL!")
        logger.info("✅ seasonal_analysis section now present")
        logger.info("✅ All 7 sections verified")
        logger.info("✅ Fixed analysis stored in database")
    else:
        logger.info("\n❌ POST-PROCESSING FIX FAILED!")
        logger.info("Manual intervention required.")
