#!/usr/bin/env python3
"""
Store Live AI Results in Database

This script takes the live AI-generated content and stores it in the
precomputed_findings database for future use.
"""

import os
import sys
import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Import required components
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def store_live_ai_result(
    tool_name: str,
    selected_sources: List[str],
    language: str,
    analysis_data: Dict[str, Any],
    model_used: str,
    response_time_ms: int,
    confidence_score: float,
    data_points_analyzed: int,
) -> bool:
    """
    Store live AI-generated analysis in the precomputed findings database.

    Args:
        tool_name: Management tool name
        selected_sources: List of data sources
        language: Analysis language
        analysis_data: Complete analysis content
        model_used: AI model that generated the content
        response_time_ms: API response time in milliseconds
        confidence_score: Analysis confidence score
        data_points_analyzed: Number of data points analyzed

    Returns:
        True if storage was successful, False otherwise
    """
    try:
        # Get database manager
        db_manager = get_precomputed_db_manager()
        logger.info(f"✅ Database manager initialized")

        # Generate combination hash
        combination_hash = db_manager.generate_combination_hash(
            tool_name=tool_name, selected_sources=selected_sources, language=language
        )
        logger.info(f"🔑 Generated combination hash: {combination_hash}")

        # Prepare analysis data for storage - serialize complex objects
        analysis_content = {
            "executive_summary": analysis_data.get("executive_summary", ""),
            "principal_findings": json.dumps(
                analysis_data.get("principal_findings", [])
            ),
            "temporal_analysis": analysis_data.get("temporal_analysis", ""),
            "seasonal_analysis": analysis_data.get("seasonal_analysis", ""),
            "fourier_analysis": analysis_data.get("fourier_analysis", ""),
            "strategic_synthesis": analysis_data.get("strategic_synthesis", ""),
            "conclusions": analysis_data.get("conclusions", ""),
            "heatmap_analysis": analysis_data.get("heatmap_analysis", ""),
            "pca_analysis": analysis_data.get("pca_analysis", ""),
            "pca_insights": json.dumps(analysis_data.get("pca_insights", {})),
            "model_used": model_used,
            "response_time_ms": response_time_ms,
            "confidence_score": confidence_score,
            "data_points_analyzed": data_points_analyzed,
            "sources_count": len(selected_sources),
            "analysis_type": "single_source"
            if len(selected_sources) == 1
            else "multi_source",
            "generation_method": "live_ai",
            "generated_at": datetime.now().isoformat(),
        }

        # Store in database
        success = db_manager.store_precomputed_analysis(
            combination_hash=combination_hash,
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            analysis_data=analysis_content,
        )

        if success:
            logger.info(
                f"✅ Successfully stored live AI analysis for {tool_name} + {len(selected_sources)} sources"
            )
            logger.info(f"   Combination hash: {combination_hash}")
            logger.info(f"   Model used: {model_used}")
            logger.info(f"   Response time: {response_time_ms}ms")
            logger.info(f"   Confidence score: {confidence_score:.2f}")
            return True
        else:
            logger.error(f"❌ Failed to store analysis in database")
            return False

    except Exception as e:
        logger.error(f"❌ Error storing live AI result: {str(e)}")
        return False


def main():
    """Main function to demonstrate storing live AI results."""

    logger.info("=" * 60)
    logger.info("🗄️  STORE LIVE AI RESULTS IN DATABASE")
    logger.info("=" * 60)

    # Example data from the successful single-source generation
    example_analysis = {
        "tool_name": "Calidad Total",
        "selected_sources": ["Google Trends"],
        "language": "es",
        "analysis_data": {
            "executive_summary": "El análisis longitudinal de Calidad Total en Google Trends (2004-2023) revela un paradigma en transición: de metodología estandarizada a filosofía adaptativa. La tendencia temporal muestra una consolidación inicial (2004-2010) con picos de 75.7 puntos, seguida de un declive progresivo hasta mínimos de 5.3 puntos en 2019, y una recuperación moderada post-pandemia hasta 14.2 puntos en 2023. Este patrón sugiere que Calidad Total ha evolucionado desde una herramienta de moda hacia una disciplina madura con aplicaciones específicas.",
            "principal_findings": [
                {
                    "bullet_point": "Calidad Total muestra una tendencia decreciente significativa con pendiente de -0.21 y R²=0.59",
                    "reasoning": "El análisis temporal revela una disminución consistente de 34.1% entre el período histórico (2004-2013) y reciente (2014-2023), indicando un cambio fundamental en la percepción y adopción de esta herramienta de gestión.",
                },
                {
                    "bullet_point": "Patrones estacionales identifican Q1 como período de mayor interés con 24.7 puntos promedio",
                    "reasoning": "El análisis estacional muestra que marzo representa el pico máximo de búsquedas (27.4 puntos), mientras que agosto registra el mínimo (14.4 puntos), sugiriendo correlación con ciclos presupuestarios y de planificación anual.",
                },
                {
                    "bullet_point": "Análisis espectral detecta frecuencia dominante de 120 meses con alta significancia",
                    "reasoning": "El análisis de Fourier identifica un ciclo principal de 10 años con potencia espectral de 4781.5, indicando patrones de adopción a largo plazo que podrían relacionarse con ciclos económicos o tecnológicos.",
                },
                {
                    "bullet_point": "Recuperación post-pandemia sugiere adaptación a nuevas realidades organizacionales",
                    "reasoning": "El incremento del 49.3% entre 2019 (5.3 puntos) y 2023 (14.2 puntos) indica que Calidad Total ha encontrado nuevas aplicaciones en contextos de transformación digital y resiliencia organizacional.",
                },
                {
                    "bullet_point": "Volatilidad creciente refleja contexto de incertidumbre y búsqueda de estabilidad",
                    "reasoning": "El aumento de volatilidad del 35.7% en el período reciente sugiere que las organizaciones experimentan con Calidad Total como respuesta a entornos empresariales cada vez más dinámicos e impredecibles.",
                },
            ],
            "temporal_analysis": "El análisis temporal de Calidad Total en Google Trends revela un patrón de adopción que sigue la curva de difusión tecnológica clásica. La fase de introducción (2004-2007) muestra niveles elevados de interés inicial, con puntuaciones promedio de 51.2 puntos, reflejando la novedad y expectativa generada por esta metodología. Durante la fase de crecimiento (2008-2012), se observa una consolidación con valores promedio de 25.8 puntos, indicando adopción sistemática por parte de organizaciones early-adopters. La fase de madurez (2013-2019) presenta un declive progresivo hasta mínimos de 5.3 puntos, característico de herramientas que se vuelven commodity. Finalmente, la fase de renovación (2020-2023) muestra una recuperación hasta 14.2 puntos, sugiriendo una reinvención de la metodología para contextos contemporáneos.",
            "seasonal_analysis": "Los patrones estacionales de Calidad Total revelan una fuerte correlación con los ciclos naturales del año empresarial. El primer trimestre (Q1) registra el mayor interés con 24.7 puntos promedio, coincidiendo con períodos de planificación estratégica y establecimiento de objetivos anuales. El segundo trimestre (Q2) mantiene niveles significativos con 23.5 puntos, alineado con implementación de iniciativas. El tercer trimestre (Q3) muestra el mínimo anual con 16.1 puntos, correspondiente a períodos vacacionales y menor actividad corporativa. El cuarto trimestre (Q4) recupera a 20.5 puntos, asociado a evaluaciones de fin de año y preparación para el siguiente ciclo. Esta estacionalidad sugiere que Calidad Total se utiliza principalmente como herramienta de planificación y evaluación más que de operación continua.",
            "fourier_analysis": "El análisis espectral de Fourier identifica frecuencias dominantes que revelan los ciclos subyacentes en la adopción de Calidad Total. La frecuencia más significativa (0.0083 ciclos/mes) corresponde a un período de 120 meses (10 años), con potencia espectral de 4781.5, indicando un ciclo de adopción a largo plazo posiblemente relacionado con transformaciones tecnológicas o económicas. La segunda frecuencia (0.0125 ciclos/mes) con período de 80 meses y potencia de 1827.6 sugiere un ciclo intermedio que podría relacionarse con ciclos de inversión empresarial. La tercera frecuencia (0.0167 ciclos/mes) con período de 60 meses y potencia de 1536.3 indica un ciclo quinquenal que puede corresponder a ciclos de planificación estratégica corporativa. Estos hallazgos sugieren que la adopción de Calidad Total responde a múltiples ritmos temporales superpuestos.",
            "strategic_synthesis": "La síntesis estratégica de los análisis temporal, estacional y espectral revela que Calidad Total ha evolucionado desde una herramienta de moda hacia una disciplina contextual y estratégica. Los patrones temporales muestran una madurez de la metodología que ha encontrado su nicho en contextos específicos de mejora continua. La estacionalidad identifica ventanas óptimas de implementación que las organizaciones pueden aprovechar para maximizar la adopción. Los ciclos espectrales sugieren que la herramienta responde a fuerzas macroeconómicas y tecnológicas más amplias. Esta comprensión integral permite a las organizaciones anticipar tendencias y planificar la implementación de Calidad Total en momentos de máximo impacto estratégico.",
            "conclusions": "El análisis integral de Calidad Total en Google Trends (2004-2023) concluye que esta herramienta de gestión ha completado su ciclo de adopción masiva y ha encontrado su lugar como disciplina especializada. La tendencia decreciente no indica obsolescencia, sino madurez y especialización. Las organizaciones deben considerar Calidad Total no como solución universal, sino como metodología contextual aplicable en situaciones específicas de mejora de procesos. Las ventanas óptimas de implementación coinciden con ciclos de planificación anual, particularmente en Q1. La recuperación post-pandemia sugiere nuevas aplicaciones en contextos de transformación digital. El ciclo de 10 años identificado indica que la herramienta puede experimentar renovaciones periódicas que las organizaciones deben monitorear para mantenerse competitivas.",
        },
        "model_used": "moonshotai/kimi-k2-instruct",
        "response_time_ms": 15201,
        "confidence_score": 0.92,
        "data_points_analyzed": 240,
    }

    # Store the result
    success = store_live_ai_result(**example_analysis)

    if success:
        logger.info("\n✅ Live AI result successfully stored in database!")
        logger.info(
            "This content will now be available for fast retrieval without API calls."
        )
    else:
        logger.info("\n❌ Failed to store live AI result in database.")

    return success


if __name__ == "__main__":
    main()
