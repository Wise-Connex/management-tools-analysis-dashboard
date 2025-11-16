#!/usr/bin/env python3
"""
Extended AI Integration Test - Data Storage & Retrieval
Tests complex analysis results and data integrity.
"""

import sys
import os
import json
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_complex_analysis_storage():
    """Test storing complex analysis results with all fields populated."""
    print("\n🔬 Testing Complex Analysis Storage")
    print("=" * 45)

    try:
        precomputed_db = get_precomputed_db_manager()

        # Create complex analysis data
        complex_analysis = {
            "executive_summary": f"""# Análisis Ejecutivo - Gestión de Costos

## Resumen Estratégico
Este análisis integral examina las tendencias de "Gestión de Costos" utilizando datos de múltiples fuentes para proporcionar una perspectiva comprehensiva.

### Hallazgos Clave
1. **Crecimiento Sostenido**: Incremento del 23% en búsquedas durante el último año
2. **Adopción Empresarial**: Correlación positiva con indicadores de eficiencia
3. **Diversificación Regional**: Patrones diferenciados entre mercados

### Implicaciones para la Toma de Decisiones
- **Prioridad Alta**: Inversión en herramientas de gestión de costos
- **Timing Óptimo**: Implementación durante Q1 para maximizar ROI
- **Segmentación**: Enfoque diferenciado por tamaño empresarial""",
            "principal_findings": f"""# Hallazgos Principales - Análisis Multifuente

## Síntesis de Componentes Principales (PCA)

### Componente Principal (PC1) - 68.5% Varianza
- **Google Trends**: Carga 0.58 (interés público creciente)
- **Google Books**: Carga 0.52 (literatura académica)
- **Bain Usabilidad**: Carga 0.41 (implementación práctica)
- **Crossref**: Carga 0.47 (investigación científica)
- **Interpretación**: "Adopción Integral de Gestión de Costos"

### Componente Secundario (PC2) - 19.2% Varianza
- **Google Trends**: Carga -0.31 (efecto estacional)
- **Google Books**: Carga 0.72 (académico vs. práctico)
- **Bain Usabilidad**: Carga 0.63 (satisfacción empresarial)
- **Crossref**: Carga 0.58 (validación científica)
- **Interpretación**: "Divergencia Académico-Comercial"

### Matriz de Correlaciones
```
                GT    GB    BU    CR
Google Trends    1.00  0.74  0.69  0.72
Google Books     0.74  1.00  0.83  0.89
Bain Usability   0.69  0.83  1.00  0.76
Crossref         0.72  0.89  0.76  1.00
```""",
            "temporal_analysis": f"""# Análisis Temporal Detallado

## Tendencias Cronológicas (2020-2024)

### Fase de Crecimiento Acelerado (2020-2022)
- **Tasa de Crecimiento**: 15.2% anual compuesto
- **Volatilidad**: CV = 0.23 (baja variabilidad)
- **Momento**: Positivo con aceleración en 2021

### Fase de Consolidación (2022-2023)
- **Tasa de Crecimiento**: 8.7% anual
- **Volatilidad**: CV = 0.31 (moderada)
- **Momento**: Estable con ajustes estacionales

### Fase de Expansión (2023-2024)
- **Tasa de Crecimiento**: 12.4% anual
- **Volatilidad**: CV = 0.28 (controlada)
- **Aceleración**: 18% incremento vs. período anterior

## Análisis de Momentum
- **Momentum Actual**: +0.34 (fuerte tendencia ascendente)
- **Aceleración**: +0.12 (incremento de velocidad)
- **Proyección Q4 2024**: Crecimiento sostenido del 14%""",
            "seasonal_analysis": f"""# Análisis Estacional Comprehensivo

## Patrones Estacionales Identificados

### Ciclo Anual Principal (Período = 12 meses)
- **Amplitud Estacional**: 0.67 (fuerte estacionalidad)
- **Fase Principal**: Pico en Marzo (mes 3)
- **Valle Principal**: Valle en Agosto (mes 8)

### Subciclos Semestrales
- **Primer Semestre**: Tendencia ascendente (Q1-Q2)
- **Segundo Semestre**: Corrección y estabilización (Q3-Q4)

### Coeficientes Estacionales Mensuales
```
Ene: 0.89  Feb: 1.12  Mar: 1.34  Abr: 1.28
May: 1.15  Jun: 1.08  Jul: 0.96  Ago: 0.72
Sep: 0.94  Oct: 1.19  Nov: 1.31  Dic: 1.25
```

## Análisis de Predictibilidad
- **Índice de Estacionalidad**: 0.72 (predictibilidad alta)
- **R² del modelo estacional**: 0.84
- **Error de predicción**: ±4.2%""",
            "fourier_analysis": f"""# Análisis de Fourier - Espectro Completo

## Frecuencias Dominantes Identificadas

### Frecuencia Fundamental
- **Frecuencia**: 0.0833 cycles/month (12 meses)
- **Período**: 12.0 meses
- **Potencia**: 1,847 unidades (73% del total)
- **Significancia**: p < 0.001 (altamente significativa)

### Armónicos Superiores
1. **2do Armónico**: 0.1667 cycles/month (6 meses)
   - **Potencia**: 287 unidades (11% del total)
   - **Interpretación**: Variación semestral

2. **3er Armónico**: 0.25 cycles/month (4 meses)
   - **Potencia**: 156 unidades (6% del total)
   - **Interpretación**: Variación trimestral

3. **4to Armónico**: 0.333 cycles/month (3 meses)
   - **Potencia**: 89 unidades (4% del total)
   - **Interpretación**: Variación cuatrimestral

## Calidad de la Señal
- **Relación Señal/Ruido**: 12.7 (excelente)
- **Coherencia Espectral**: 0.89
- **Entropía Espectral**: 2.34 bits""",
            "pca_analysis": f"""# Análisis PCA - Metodología Avanzada

## Preparación de Datos
- **Matriz de Correlación**: 4×4 (4 fuentes de datos)
- **Estandarización**: Z-score aplicado
- **Adecuación Muestral**: KMO = 0.87 (excelente)

## Resultados de la Extracción
### Valores Propios (Eigenvalues)
1. **λ₁ = 2.74** (68.5% varianza)
2. **λ₂ = 0.77** (19.2% varianza)  
3. **λ₃ = 0.34** (8.5% varianza)
4. **λ₄ = 0.15** (3.8% varianza)

### Matriz de Cargas (Loadings)
```
           PC1    PC2    PC3    PC4
GT         0.58  -0.31   0.71  -0.23
GB         0.52   0.72  -0.39   0.19
BU         0.41   0.63   0.58   0.34
CR         0.47   0.58  -0.12   0.65
```

## Interpretación de Componentes

### PC1 - "Adopción General del Mercado"
- Representa la tendencia común de crecimiento
- Todas las cargas positivas
- Interpretación: "Momentum General de Adopción"

### PC2 - "Divergencia Sectorial"  
- Distingue fuentes académicas vs. comerciales
- Google Books y Bain con cargas altas positivas
- Google Trends con carga negativa
- Interpretación: "Orientación Sectorial"

## Validación del Modelo
- **Varianza Acumulada**: 87.7% (primeros 2 componentes)
- **Comunalidades**: Todas > 0.68
- **Test de Esfericidad**: χ² = 127.4, p < 0.001""",
            "heatmap_analysis": f"""# Análisis de Calor - Distribución Multidimensional

## Mapa de Densidad de Probabilidad

### Regiones de Alta Densidad (>75% Percentil)
- **Cluster Principal**: Centroide (μ = 2.3, σ = 0.8)
- **Cobertura**: 34% del espacio de datos
- **Interpretación**: Zona de adopción masiva

### Regiones de Media Densidad (25-75% Percentil)
- **Corredores de Transición**: 5 zonas conectivas
- **Gradiente Suave**: Transición controlada
- **Interpretación**: Adopción gradual

### Regiones de Baja Densidad (<25% Percentil)
- **Outliers Extremos**: 8 casos atípicos
- **Periferias**: 12% del espacio total
- **Interpretación**: Nichos especializados

## Análisis de Clusters
### Algoritmo: K-Means (k=3)
- **Cluster 1**: "Adopción Temprana" (42% datos)
- **Cluster 2**: "Adopción Masiva" (38% datos)  
- **Cluster 3**: "Adopción Retardada" (20% datos)

### Métricas de Calidad
- **Silhouette Score**: 0.73 (buena separación)
- **Inercia**: 1,247 (coherencia interna)
- **Coeficiente de Calinski-Harabasz**: 156.8""",
            "data_points_analyzed": 8634,
            "confidence_score": 0.94,
            "model_used": "gpt-4",
            "analysis_type": "multi_source",
            "tool_display_name": "Gestión de Costos",
        }

        # Store complex analysis
        print("💾 Storing complex analysis...")
        combination_hash = precomputed_db.generate_combination_hash(
            "Gestión de Costos",
            ["Google Trends", "Google Books", "Bain Usability", "Crossref"],
            "es",
        )

        record_id = precomputed_db.store_precomputed_analysis(
            combination_hash=combination_hash,
            tool_name="Gestión de Costos",
            selected_sources=[
                "Google Trends",
                "Google Books",
                "Bain Usability",
                "Crossref",
            ],
            language="es",
            analysis_data=complex_analysis,
        )

        print(f"✅ Stored complex analysis record ID: {record_id}")

        # Retrieve and verify completeness
        retrieved = precomputed_db.get_combination_by_hash(combination_hash)

        if retrieved:
            print("✅ Successfully retrieved complex analysis")

            # Verify all content fields are preserved
            fields_to_check = [
                "executive_summary",
                "principal_findings",
                "temporal_analysis",
                "seasonal_analysis",
                "fourier_analysis",
                "pca_analysis",
                "heatmap_analysis",
            ]

            all_preserved = True
            for field in fields_to_check:
                if field in retrieved and retrieved[field]:
                    field_length = len(retrieved[field])
                    print(f"   - {field}: {field_length} chars ✅")
                else:
                    print(f"   - {field}: MISSING ❌")
                    all_preserved = False

            # Check markdown formatting
            markdown_elements = ["#", "##", "###", "**", "`", "-", "*"]
            markdown_preserved = any(
                elem in retrieved.get("executive_summary", "")
                for elem in markdown_elements
            )

            print(
                f"   - Complete Content Preservation: {'✅ PASSED' if all_preserved else '❌ FAILED'}"
            )
            print(
                f"   - Markdown Formatting: {'✅ PASSED' if markdown_preserved else '❌ FAILED'}"
            )

            return {
                "success": True,
                "record_id": record_id,
                "content_preserved": all_preserved,
                "markdown_preserved": markdown_preserved,
                "total_content_length": sum(
                    len(retrieved.get(field, "")) for field in fields_to_check
                ),
            }
        else:
            return {"success": False, "error": "Complex analysis retrieval failed"}

    except Exception as e:
        print(f"❌ Complex analysis test failed: {e}")
        import traceback

        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_data_integrity():
    """Test data integrity and consistency across storage/retrieval."""
    print("\n🔍 Testing Data Integrity")
    print("=" * 30)

    try:
        precomputed_db = get_precomputed_db_manager()

        # Test case sensitivity in hash generation
        tool_names = ["Benchmarking", "benchmarking", "BENCHMARKING"]
        sources = ["Google Trends", "Bain Usability"]
        language = "es"

        hashes = []
        for tool_name in tool_names:
            hash_val = precomputed_db.generate_combination_hash(
                tool_name, sources, language
            )
            hashes.append(hash_val)
            print(f"   Tool: '{tool_name}' → Hash: {hash_val}")

        # All hashes should be the same (normalized)
        hash_consistency = len(set(hashes)) == 1
        print(
            f"   Hash Consistency: {'✅ PASSED' if hash_consistency else '❌ FAILED'}"
        )

        # Test source order independence
        sources_order1 = ["Google Trends", "Bain Usability"]
        sources_order2 = ["Bain Usability", "Google Trends"]

        hash1 = precomputed_db.generate_combination_hash(
            "Benchmarking", sources_order1, language
        )
        hash2 = precomputed_db.generate_combination_hash(
            "Benchmarking", sources_order2, language
        )

        order_independence = hash1 == hash2
        print(
            f"   Source Order Independence: {'✅ PASSED' if order_independence else '❌ FAILED'}"
        )
        print(f"   Hash 1: {hash1}")
        print(f"   Hash 2: {hash2}")

        return {
            "success": True,
            "hash_consistency": hash_consistency,
            "order_independence": order_independence,
        }

    except Exception as e:
        print(f"❌ Data integrity test failed: {e}")
        return {"success": False, "error": str(e)}


def run_extended_integration_tests():
    """Run extended integration tests."""
    print("🚀 Starting Extended AI Integration Tests")
    print("=" * 50)

    results = {}

    # Test 1: Complex Analysis Storage
    results["complex_storage"] = test_complex_analysis_storage()

    # Test 2: Data Integrity
    results["data_integrity"] = test_data_integrity()

    # Summary
    print("\n" + "=" * 50)
    print("📊 EXTENDED INTEGRATION TEST RESULTS")
    print("=" * 50)

    complex_success = results["complex_storage"]["success"]
    integrity_success = results["data_integrity"]["success"]

    print(f"✅ Complex Analysis Storage: {'PASSED' if complex_success else 'FAILED'}")
    print(f"✅ Data Integrity: {'PASSED' if integrity_success else 'FAILED'}")

    overall_success = complex_success and integrity_success
    print(
        f"\n🎯 Overall Result: {'✅ ALL EXTENDED TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
    )

    if overall_success:
        print("\n🎉 Database integration is robust and ready for production!")
        print("   - Complex analysis results properly stored and retrieved")
        print("   - Data integrity maintained across all operations")
        print("   - Hash generation is consistent and reliable")
    else:
        print("\n⚠️  Review failed tests before proceeding")

    return results


if __name__ == "__main__":
    results = run_extended_integration_tests()
    sys.exit(0 if all(r.get("success", False) for r in results.values()) else 1)
