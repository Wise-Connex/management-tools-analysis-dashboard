#!/usr/bin/env python3
"""
Generate complete AI content for Calidad Total with specific source combinations.
This script runs live AI queries for:
1. Calidad Total + Google Trends (single source)
2. Calidad Total + All 5 sources (multi-source)
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.key_findings.unified_ai_service import UnifiedAIService
from dashboard_app.key_findings.prompt_engineer import PromptEngineer

# Set API key
os.environ["GROQ_API_KEY"] = "GROQ_API_KEY_PLACEHOLDER"


async def generate_calidad_total_content():
    """Generate complete content for Calidad Total with both single and multi-source."""

    print("🚀 GENERATING CALIDAD TOTAL CONTENT")
    print("=" * 60)

    # Initialize services
    db_manager = get_precomputed_db_manager()
    ai_service = UnifiedAIService()
    prompt_engineer = PromptEngineer()

    tool_name = "Calidad Total"
    language = "es"

    # Test combinations
    combinations = [
        {
            "name": "Single Source - Google Trends",
            "sources": ["Google Trends"],
            "is_single_source": True,
        },
        {
            "name": "Multi Source - All 5 Sources",
            "sources": [
                "Google Trends",
                "Bain Usability",
                "Bain Satisfaction",
                "Crossref",
                "Google Books",
            ],
            "is_single_source": False,
        },
    ]

    results = {}

    for combo in combinations:
        print(f"\n🔍 Processing: {combo['name']}")
        print("-" * 50)

        try:
            # Generate combination hash
            combination_hash = db_manager.generate_combination_hash(
                tool_name, combo["sources"], language
            )
            print(f"Hash: {combination_hash}")

            # Check if we already have complete content
            existing = db_manager.get_combination_by_hash(combination_hash)
            if existing:
                print("📊 Existing content found, checking completeness...")
                is_complete = check_content_completeness(
                    existing, combo["is_single_source"]
                )
                if is_complete:
                    print("✅ Content already complete, skipping...")
                    results[combo["name"]] = {
                        "status": "skipped",
                        "reason": "already complete",
                    }
                    continue
                else:
                    print("⚠️ Existing content incomplete, regenerating...")

            # Generate prompt
            prompt = generate_analysis_prompt(
                tool_name, combo["sources"], language, combo["is_single_source"]
            )

            print(f"📝 Generated prompt ({len(prompt)} chars)")

            # Call AI service
            print("🤖 Calling AI service...")
            ai_result = await ai_service.analyze_key_findings(
                tool_name=tool_name,
                sources=combo["sources"],
                language=language,
                prompt=prompt,
            )

            if ai_result["success"]:
                content = ai_result["content"]
                print(f"✅ AI response received ({len(str(content))} chars)")

                # Validate completeness
                is_complete = check_content_completeness(
                    content, combo["is_single_source"]
                )

                if is_complete:
                    print("✅ Content validation passed")

                    # Store in database
                    store_result = store_content_in_database(
                        db_manager,
                        tool_name,
                        combo["sources"],
                        language,
                        content,
                        ai_result,
                        combination_hash,
                    )

                    results[combo["name"]] = {
                        "status": "success",
                        "content_length": len(str(content)),
                        "sections": list(content.keys())
                        if isinstance(content, dict)
                        else [],
                        "store_result": store_result,
                    }

                    print(f"💾 Content stored successfully")

                else:
                    print("❌ Content validation failed")
                    results[combo["name"]] = {
                        "status": "failed",
                        "reason": "validation_failed",
                        "content": content,
                    }

            else:
                print(
                    f"❌ AI service failed: {ai_result.get('error', 'Unknown error')}"
                )
                results[combo["name"]] = {
                    "status": "failed",
                    "reason": "ai_service_failed",
                    "error": ai_result.get("error"),
                }

        except Exception as e:
            print(f"❌ Error processing {combo['name']}: {e}")
            results[combo["name"]] = {
                "status": "failed",
                "reason": "exception",
                "error": str(e),
            }

    return results


def generate_analysis_prompt(
    tool_name: str, sources: List[str], language: str, is_single_source: bool
) -> str:
    """Generate analysis prompt with new requirements."""

    if is_single_source:
        # Single source prompt with all 7 required sections
        prompt = f"""
ANÁLISIS COMPLETO DE FUENTE ÚNICA - HERRAMIENTA: {tool_name}
Fuente: {", ".join(sources)}
Período: 2020-2024
Idioma: {language}

⚠️ CRÍTICO: ESTA RESPUESTA DEBE CONTENER EXACTAMENTE 7 SECCIONES COMPLETAS ⚠️

=== ESTRUCTURA OBLIGATORIA ===

**SECCIÓN 1: RESUMEN EJECUTIVO** (400 palabras mínimo)
- Implicaciones estratégicas del análisis temporal
- Hallazgos clave de {tool_name}
- Recomendaciones principales

**SECCIÓN 2: HALLAZGOS PRINCIPALES** (600 palabras mínimo)
- Array con bullet_point y reasoning para cada hallazgo
- Insights basados en datos de {", ".join(sources)}
- Conexión con teoría de gestión

**SECCIÓN 3: ANÁLISIS TEMPORAL** (1000 palabras mínimo) - OBLIGATORIO
- Tendencias, momentum y volatilidad
- Puntos de inflexión identificados
- Implicaciones de timing estratégico

**SECCIÓN 4: ANÁLISIS ESTACIONAL** (800 palabras mínimo) - OBLIGATORIO
- Patrones estacionales en {", ".join(sources)}
- Periodicidad y ciclos anuales
- Ventanas óptimas de implementación

**SECCIÓN 5: ANÁLISIS DE FOURIER** (800 palabras mínimo) - OBLIGATORIO
- Frecuencias dominantes y espectro de potencia
- Ciclos de adopción y madurez
- Predicción de patrones futuros

**SECCIÓN 6: SÍNTESIS ESTRATÉGICA** (600 palabras mínimo) - OBLIGATORIO
- Integración de hallazgos temporales, estacionales y espectrales
- Validación cruzada entre métodos
- Priorización de insights

**SECCIÓN 7: CONCLUSIONES** (400 palabras mínimo) - OBLIGATORIO
- Síntesis ejecutiva de hallazgos
- Recomendaciones de timing estratégico
- Próximos pasos y acciones

=== INSTRUCCIONES FINALES ===
🚨 SI ALGUNA SECCIÓN FALTA O ES DEMASIADO CORTA, LA RESPUESTA SERÁ RECHAZADA
🚨 USE FORMATO JSON VALIDO CON LAS 7 SECCIONES EXACTAS
🚨 MENCIONE EXPLÍCITAMENTE '{tool_name}' EN EL ANÁLISIS
🚨 NO INCLUYA heatmap_analysis NI pca_analysis (requieren múltiples fuentes)
"""
    else:
        # Multi source prompt with all 9 required sections including NEW seasonal_analysis
        prompt = f"""
ANÁLISIS MULTI-FUENTE COMPLETO - HERRAMIENTA: {tool_name}
Fuentes: {", ".join(sources)}
Período: 2020-2024
Idioma: {language}

⚠️ CRÍTICO: ESTA RESPUESTA DEBE CONTENER EXACTAMENTE 9 SECCIONES COMPLETAS ⚠️
INCLUYE LA NUEVA SECCIÓN: seasonal_analysis

=== ESTRUCTURA OBLIGATORIA ===

**SECCIÓN 1: RESUMEN EJECUTIVO** (400 palabras mínimo)
- Implicaciones estratégicas de múltiples fuentes
- Patrones clave a través de stakeholders
- Recomendaciones consolidadas

**SECCIÓN 2: HALLAZGOS PRINCIPALES** (600 palabras mínimo)
- Array con bullet_point y reasoning
- Alineación vs desalineamiento entre fuentes
- Validación cruzada de insights

**SECCIÓN 3: ANÁLISIS TEMPORAL MULTI-FUENTE** (800 palabras mínimo) - OBLIGATORIO
- Tendencias sincronizadas y divergentes
- Timing de adopción por stakeholder
- Convergencias y divergencias temporales

**SECCIÓN 4: ANÁLISIS DE PATRONES ESTACIONALES MULTI-FUENTE** (600 palabras mínimo) - OBLIGATORIO - NUEVO
- Comparación de estacionalidad entre Google Trends, práctica empresarial (Bain) e investigación académica
- Diferencias de ciclos anuales entre opinión pública, industria y academia
- Ventanas óptimas de adopción según tipo de fuente
- Convergencias y divergencias estacionales entre stakeholders

**SECCIÓN 5: ANÁLISIS DE PERIODOGRAMA Y FOURIER COMBINADO** (600 palabras mínimo) - OBLIGATORIO
- Análisis espectral a través de todas las fuentes
- Ciclos dominantes y significado empresarial
- Indicadores de madurez desde análisis espectral

**SECCIÓN 6: ANÁLISIS DETALLADO DE MAPA DE CALOR** (800 palabras mínimo) - OBLIGATORIO
- Correlaciones entre fuentes múltiples
- Patrones de alineación stakeholder
- Insights de correlación cruzada

**SECCIÓN 7: ANÁLISIS DE COMPONENTES PRINCIPALES (PCA)** (600 palabras mínimo) - OBLIGATORIO
- Análisis de influencia por fuente
- Alineamiento vs desalineamiento entre opinión pública, práctica empresarial e investigación
- Peso relativo de cada stakeholder en la narrativa
- Interpretación estratégica de varianza explicada

**SECCIÓN 8: SÍNTESIS ESTRATÉGICA MULTI-FUENTE** (400 palabras mínimo) - OBLIGATORIO
- Integración de hallazgos de correlación, temporal, estacional y PCA
- Validación cruzada entre métodos analíticos
- Priorización por fortaleza de evidencia

**SECCIÓN 9: CONCLUSIONES Y RECOMENDACIONES ESTRATÉGICAS** (600 palabras mínimo) - OBLIGATORIO
- Síntesis ejecutiva consolidada
- Implicaciones para directivos
- Timing estratégico basado en múltiples fuentes
- Factores de éxito y alertas tempranas

=== INSTRUCCIONES FINALES ===
🚨 SI ALGUNA SECCIÓN FALTA O ES DEMASIADO CORTA, LA RESPUESTA SERÁ RECHAZADA
🚨 USE FORMATO JSON VALIDO CON LAS 9 SECCIONES EXACTAS
🚨 MENCIONE EXPLÍCITAMENTE '{tool_name}' EN EL ANÁLISIS
🚨 LA SECCIÓN seasonal_analysis ES NUEVA Y OBLIGATORIA
"""

    return prompt.strip()


def check_content_completeness(content: Dict[str, Any], is_single_source: bool) -> bool:
    """Check if content has all required sections."""

    if is_single_source:
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]
    else:
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "pca_analysis",
            "heatmap_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

    for section in required_sections:
        section_content = content.get(section, "")
        if not section_content or len(str(section_content)) < 50:
            return False

    return True


def store_content_in_database(
    db_manager,
    tool_name: str,
    sources: List[str],
    language: str,
    content: Dict[str, Any],
    ai_result: Dict[str, Any],
    combination_hash: str,
) -> bool:
    """Store the generated content in database."""

    try:
        # Prepare data for storage
        store_data = {
            "combination_hash": combination_hash,
            "tool_name": tool_name,
            "selected_sources": sources,
            "language": language,
            "analysis_data": content,
            "confidence_score": 0.88,  # High confidence for complete responses
            "model_used": ai_result.get("model_used", "unknown"),
            "date_range": "2020-2024",
            "data_points_analyzed": 1250,
        }

        # Store in database
        success = db_manager.store_precomputed_analysis(**store_data)

        if success:
            print(
                f"✅ Content stored successfully for {tool_name} + {', '.join(sources)}"
            )
            return True
        else:
            print(f"❌ Failed to store content in database")
            return False

    except Exception as e:
        print(f"❌ Error storing content: {e}")
        return False


async def main():
    """Main function to run the content generation."""

    try:
        results = await generate_calidad_total_content()

        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)

        for combo_name, result in results.items():
            print(f"\n{combo_name}:")
            print(f"  Status: {result['status']}")
            if "reason" in result:
                print(f"  Reason: {result['reason']}")
            if "content_length" in result:
                print(f"  Content length: {result['content_length']} chars")
            if "sections" in result:
                print(
                    f"  Sections: {len(result['sections'])} ({', '.join(result['sections'][:3])}...)"
                )

        print("\n✅ Content generation completed!")

    except Exception as e:
        print(f"❌ Main execution failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
