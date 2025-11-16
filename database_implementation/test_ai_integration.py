#!/usr/bin/env python3
"""
AI Integration Test Script
Tests integration between existing AI analysis logic and new precomputed findings database.
"""

import sys
import os
import json
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "dashboard_app"))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_ai_integration_single_source():
    """Test AI integration for single source analysis."""
    print("\n🧪 Testing AI Integration - Single Source Analysis")
    print("=" * 50)

    try:
        # Initialize services (simplified for testing)
        precomputed_db = get_precomputed_db_manager()

        # For testing, we'll simulate the AI analysis since we may not have API keys
        print("📋 Simulating single source analysis...")

        # Test combination
        tool_name = "Benchmarking"
        selected_sources = ["Google Trends"]  # Single source
        language = "es"

        # Generate hash for this combination
        combination_hash = precomputed_db.generate_combination_hash(
            tool_name, selected_sources, language
        )
        print(f"🔑 Generated hash: {combination_hash}")

        # Simulate AI analysis results (in real implementation, this would call the AI service)
        simulated_ai_result = {
            "executive_summary": f"""# Análisis Ejecutivo - {tool_name}

## Resumen General
Este análisis examina las tendencias de búsqueda para "{tool_name}" utilizando datos de Google Trends. 

## Hallazgos Principales
- **Tendencia General**: Crecimiento sostenido en el interés de búsqueda
- **Patrón Estacional**: Picos identificados durante ciertos períodos del año
- **Volatilidad**: Nivel moderado de variación en las búsquedas

## Implicaciones Estratégicas
Los resultados sugieren una creciente adopción de herramientas de {tool_name} en el mercado español.""",
            "temporal_analysis": f"""# Análisis Temporal - {tool_name}

## Tendencias Observadas
El análisis temporal revela un **crecimiento positivo** en las búsquedas relacionadas con {tool_name}. La tendencia muestra:

- **Tendencia Lineal**: Pendiente positiva de 0.15 puntos por mes
- **Volatilidad**: Desviación estándar de 2.3 puntos
- **Momento**: Aceleración del 12% en los últimos 6 meses

## Volatilidad y Estabilidad
Los datos muestran un nivel de volatilidad **moderado** con períodos de estabilidad seguidos de aumentos significativos.""",
            "seasonal_analysis": f"""# Análisis Estacional - {tool_name}

## Patrones Estacionales Identificados
Se detectaron **patrones estacionales claros** en las búsquedas de {tool_name}:

- **Temporada Alta**: Marzo-Mayo y Septiembre-Noviembre
- **Temporada Baja**: Junio-Agosto y Diciembre-Febrero
- **Fuerza Estacional**: 0.68 (fuerte estacionalidad)

## Periodicidad
La periodicidad principal es **anual** con algunos componentes semestrales menores.""",
            "fourier_analysis": f"""# Análisis de Fourier - {tool_name}

## Frecuencias Dominantes
El análisis espectral identifica las siguientes frecuencias principales:

1. **Frecuencia Principal**: 0.083 cycles/month (período: 12 meses)
   - **Potencia**: 85% de la señal total
   - **Significancia**: Altamente significativa

2. **Frecuencia Secundaria**: 0.167 cycles/month (período: 6 meses)
   - **Potencia**: 12% de la señal total
   - **Significancia**: Moderadamente significativa

## Calidad de la Señal
- **Relación Señal/Ruido**: 8.2 (excelente)
- **Potencia Total**: 1,247 unidades
- **Potencia de Ruido**: 152 unidades""",
            "heatmap_analysis": f"""# Análisis de Calor - {tool_name}

## Distribución de Datos
El análisis de densidad revela patrones claros en los datos de {tool_name}:

- **Regiones de Alta Densidad**: Concentración en valores medios-altos
- **Regiones de Baja Densidad**: Valores extremos (muy bajos y muy altos)
- **Gradientes**: Transiciones suaves entre regiones de densidad

## Clusters Identificados
Se detectaron **2 clusters principales**:
1. Cluster Principal: 67% de los datos (tendencia creciente)
2. Cluster Secundario: 23% de los datos (variación estacional)

## Outliers
- **Valores Atípicos**: 3 puntos outlier detectados
- **Impacto**: Mínimo en el análisis general""",
            "data_points_analyzed": 2847,
            "confidence_score": 0.89,
            "model_used": "gpt-4",
            "analysis_type": "single_source",
            "tool_display_name": tool_name,
        }

        # Store the analysis in database
        print("💾 Storing analysis in database...")
        record_id = precomputed_db.store_precomputed_analysis(
            combination_hash=combination_hash,
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            analysis_data=simulated_ai_result,
        )
        print(f"✅ Stored analysis record ID: {record_id}")

        # Retrieve the analysis
        print("🔍 Retrieving analysis from database...")
        retrieved_analysis = precomputed_db.get_combination_by_hash(combination_hash)

        if retrieved_analysis:
            print("✅ Successfully retrieved analysis")
            print(f"   - Record ID: {retrieved_analysis['id']}")
            print(f"   - Tool: {retrieved_analysis['tool_name']}")
            print(f"   - Analysis Type: {retrieved_analysis['analysis_type']}")
            print(f"   - Confidence: {retrieved_analysis['confidence_score']}")
            print(
                f"   - Executive Summary Length: {len(retrieved_analysis['executive_summary'])}"
            )

            # Verify content preservation
            content_preserved = (
                retrieved_analysis["executive_summary"]
                == simulated_ai_result["executive_summary"]
                and retrieved_analysis["temporal_analysis"]
                == simulated_ai_result["temporal_analysis"]
                and retrieved_analysis["seasonal_analysis"]
                == simulated_ai_result["seasonal_analysis"]
                and retrieved_analysis["fourier_analysis"]
                == simulated_ai_result["fourier_analysis"]
                and retrieved_analysis["heatmap_analysis"]
                == simulated_ai_result["heatmap_analysis"]
            )

            print(
                f"   - Content Preservation: {'✅ PASSED' if content_preserved else '❌ FAILED'}"
            )

            # Test markdown formatting
            markdown_preserved = (
                "#" in retrieved_analysis["executive_summary"]
                and "##" in retrieved_analysis["temporal_analysis"]
                and "**" in retrieved_analysis["seasonal_analysis"]
            )
            print(
                f"   - Markdown Formatting: {'✅ PASSED' if markdown_preserved else '❌ FAILED'}"
            )

            return {
                "success": True,
                "record_id": record_id,
                "content_preserved": content_preserved,
                "markdown_preserved": markdown_preserved,
                "retrieved_data": retrieved_analysis,
            }
        else:
            print("❌ Failed to retrieve analysis")
            return {"success": False, "error": "Retrieval failed"}

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_ai_integration_multi_source():
    """Test AI integration for multi-source analysis."""
    print("\n🧪 Testing AI Integration - Multi Source Analysis")
    print("=" * 50)

    try:
        # Initialize database manager
        precomputed_db = get_precomputed_db_manager()

        # Test combination (multiple sources)
        tool_name = "Calidad Total"
        selected_sources = [
            "Google Trends",
            "Google Books",
            "Bain Usability",
        ]  # Multiple sources
        language = "es"

        # Generate hash for this combination
        combination_hash = precomputed_db.generate_combination_hash(
            tool_name, selected_sources, language
        )
        print(f"🔑 Generated hash: {combination_hash}")

        # Simulate multi-source AI analysis results
        simulated_multi_source_result = {
            "executive_summary": f"""# Análisis Ejecutivo - {tool_name}
## Análisis Multifuente Integrado

Este análisis combina datos de **3 fuentes** para proporcionar una visión comprehensiva de {tool_name}:

### Fuentes Analizadas
- **Google Trends**: Tendencias de búsqueda y interés público
- **Google Books**: Publicaciones académicas y literatura
- **Bain Usabilidad**: Datos de uso y adopción empresarial

### Hallazgos Principales Integrados
La convergencia de datos de múltiples fuentes revela patrones consistentes sobre {tool_name}:

1. **Consenso Intersource**: Las tres fuentes confirman el crecimiento
2. **Diferencias Temporales**: Bain muestra adopción más temprana
3. **Validación Cruzada**: Correlación del 0.87 entre fuentes

### Implicaciones Estratégicas
El análisis multifuente valida las tendencias identificadas y proporciona mayor confianza en las proyecciones.""",
            "principal_findings": f"""# Hallazgos Principales - Análisis PCA

## Análisis de Componentes Principales
El análisis PCA sobre las **3 fuentes** revela:

### Componente Principal (PC1) - 72% de la Varianza
- **Carga Factor Google Trends**: 0.45
- **Carga Factor Google Books**: 0.52  
- **Carga Factor Bain Usability**: 0.38
- **Interpretación**: "Adopción General del Mercado"

### Componente Secundario (PC2) - 18% de la Varianza
- **Carga Factor Google Trends**: -0.23
- **Carga Factor Google Books**: 0.67
- **Carga Factor Bain Usability**: -0.12
- **Interpretación**: "Interés Académico vs. Comercial"

### Correlaciones Intersource
- **Google Trends ↔ Google Books**: r = 0.73 (fuerte)
- **Google Trends ↔ Bain Usability**: r = 0.68 (fuerte)
- **Google Books ↔ Bain Usability**: r = 0.81 (muy fuerte)""",
            "pca_analysis": f"""# Análisis PCA Detallado - {tool_name}

## Metodología y Resultados
Se aplicó análisis de componentes principales a la matriz de correlación de las 3 fuentes de datos.

### Varianza Explicada
- **PC1**: 72.3% (Adopción General)
- **PC2**: 18.1% (Divergencia Académica-Comercial)
- **PC3**: 9.6% (Ruido residual)

### Interpretación de Componentes
1. **PC1 - "Adopción General"**: 
   - Representa la tendencia común de crecimiento en todas las fuentes
   - Fuerte loading positivo en Google Books (0.52)
   - Indica que el interés académico lidera la adopción

2. **PC2 - "Divergencia Temporal"**:
   - Distingue entre fuentes con diferentes ritmos de adopción
   - Bain muestra adopción más temprana que Google Trends
   - Sugiere diferentes ciclos de adopción por fuente

### Validez del Modelo
- **KMO**: 0.82 (excelente adecuación muestral)
- **Test de Esfericidad de Bartlett**: p < 0.001 (significativo)
- **Comunalidades**: Todas > 0.65 (buena extracción)""",
            "heatmap_analysis": f"""# Análisis de Correlación - Matriz de Calor

## Matriz de Correlaciones Intersource
```
                    GT    GB    BU
Google Trends     1.00  0.73  0.68
Google Books      0.73  1.00  0.81  
Bain Usability    0.68  0.81  1.00
```

## Patrones de Correlación
- **Correlación Más Fuerte**: Google Books ↔ Bain Usability (0.81)
- **Patrón Temporal**: Todas las correlaciones son positivas y significativas
- **Consistencia**: No se detectaron correlaciones negativas

## Análisis de Clusters
Se identificaron **2 clusters principales**:
1. **Cluster Académico-Comercial**: Google Books + Bain Usability
2. **Cluster de Tendencias**: Google Trends (más independiente)

## Outliers y Anomalías
- **Puntos Outlier**: 2 casos con correlaciones atípicas
- **Anomalías Temporales**: Períodos de divergencia en Q2 2023""",
            "data_points_analyzed": 4521,
            "confidence_score": 0.92,
            "model_used": "gpt-4",
            "analysis_type": "multi_source",
            "tool_display_name": tool_name,
        }

        # Store the multi-source analysis
        print("💾 Storing multi-source analysis in database...")
        record_id = precomputed_db.store_precomputed_analysis(
            combination_hash=combination_hash,
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            analysis_data=simulated_multi_source_result,
        )
        print(f"✅ Stored multi-source analysis record ID: {record_id}")

        # Retrieve and verify
        print("🔍 Retrieving multi-source analysis...")
        retrieved_analysis = precomputed_db.get_combination_by_hash(combination_hash)

        if retrieved_analysis:
            print("✅ Successfully retrieved multi-source analysis")
            print(f"   - Analysis Type: {retrieved_analysis['analysis_type']}")
            print(
                f"   - Principal Findings Length: {len(retrieved_analysis['principal_findings'])}"
            )
            print(
                f"   - PCA Analysis Length: {len(retrieved_analysis['pca_analysis'])}"
            )

            # Verify multi-source specific content
            multi_source_content = (
                "principal_findings" in retrieved_analysis
                and retrieved_analysis["principal_findings"]
                and "pca_analysis" in retrieved_analysis
                and retrieved_analysis["pca_analysis"]
                and retrieved_analysis["analysis_type"] == "multi_source"
            )

            print(
                f"   - Multi-source Content: {'✅ PASSED' if multi_source_content else '❌ FAILED'}"
            )

            return {
                "success": True,
                "record_id": record_id,
                "multi_source_content": multi_source_content,
                "analysis_type": retrieved_analysis["analysis_type"],
            }
        else:
            return {"success": False, "error": "Multi-source retrieval failed"}

    except Exception as e:
        print(f"❌ Multi-source test failed: {e}")
        return {"success": False, "error": str(e)}


def test_performance_comparison():
    """Test performance: AI generation vs database retrieval."""
    print("\n⚡ Performance Comparison Test")
    print("=" * 40)

    try:
        precomputed_db = get_precomputed_db_manager()

        # Test parameters
        tool_name = "Benchmarking"
        selected_sources = ["Google Trends", "Bain Usability"]
        language = "es"

        # Test database lookup speed
        print("🗄️ Testing database lookup performance...")
        combination_hash = precomputed_db.generate_combination_hash(
            tool_name, selected_sources, language
        )

        start_time = time.time()
        for i in range(100):
            result = precomputed_db.get_combination_by_hash(combination_hash)
        end_time = time.time()

        db_avg_time = ((end_time - start_time) / 100) * 1000  # Convert to milliseconds
        print(f"✅ Database lookup average: {db_avg_time:.2f}ms (100 iterations)")

        # Estimate AI generation time (this would be much slower in reality)
        estimated_ai_time = 8500  # Estimated 8.5 seconds for AI generation
        print(f"📊 Estimated AI generation time: {estimated_ai_time}ms")

        speed_improvement = estimated_ai_time / db_avg_time
        print(f"🚀 Speed improvement: {speed_improvement:.0f}x faster")
        print(f"🎯 Performance target: <100ms (achieved: {db_avg_time:.2f}ms)")

        return {
            "db_avg_time": db_avg_time,
            "estimated_ai_time": estimated_ai_time,
            "speed_improvement": speed_improvement,
            "target_met": db_avg_time < 100,
        }

    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return {"success": False, "error": str(e)}


def run_ai_integration_tests():
    """Run complete AI integration test suite."""
    print("🚀 Starting AI Integration Tests - Phase 2")
    print("=" * 60)

    results = {}

    # Test 1: Single Source Analysis
    results["single_source"] = test_ai_integration_single_source()

    # Test 2: Multi-Source Analysis
    results["multi_source"] = test_ai_integration_multi_source()

    # Test 3: Performance Comparison
    results["performance"] = test_performance_comparison()

    # Summary
    print("\n" + "=" * 60)
    print("🎯 AI INTEGRATION TEST RESULTS SUMMARY")
    print("=" * 60)

    single_success = results["single_source"]["success"]
    multi_success = results["multi_source"]["success"]
    perf_target_met = results["performance"].get("target_met", False)

    print(f"✅ Single Source Analysis: {'PASSED' if single_success else 'FAILED'}")
    print(f"✅ Multi-Source Analysis: {'PASSED' if multi_success else 'FAILED'}")
    print(f"✅ Performance Test: {'PASSED' if perf_target_met else 'FAILED'}")

    overall_success = single_success and multi_success and perf_target_met
    print(
        f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
    )

    if overall_success:
        print("\n🎉 AI Integration is ready for Phase 3: Full Precomputation Pipeline!")
    else:
        print("\n⚠️  Review failed tests before proceeding to Phase 3")

    return results


if __name__ == "__main__":
    results = run_ai_integration_tests()
    sys.exit(0 if all(r.get("success", False) for r in results.values()) else 1)
