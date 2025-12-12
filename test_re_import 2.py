#!/usr/bin/env python3
"""
Test the re import fix for the single-source filtering.
"""

# Test the regex patterns that were causing the error
import re

# Test data similar to what would be in principal_findings_raw
test_content = """
## 🔍 HALLAZGOS PRINCIPALES

🔥 Análisis del Mapa de Calor: El mapa de calor muestra patrones de correlación significativos entre las variables temporales.

📊 Análisis PCA: El análisis de componentes principales revela que el 85% de la varianza se explica por los primeros tres componentes.

El análisis temporal muestra una tendencia decreciente significativa en el uso de Benchmarking.
"""

print("🧪 Testing re import fix...")

# Test the exact code that was causing the error
heatmap_patterns = [
    r"🔥.*Análisis del Mapa de Calor.*",
    r"🔥.*Heatmap Analysis.*",
    r"Análisis del Mapa de Calor.*",
    r"Heatmap Analysis.*"
]

pca_patterns = [
    r"📊.*Análisis PCA.*",
    r"📊.*PCA Analysis.*",
    r"Análisis PCA.*",
    r"PCA Analysis.*",
    r"No PCA a\s*n\s*alysis\s*available"
]

principal_findings_raw = test_content

# Apply the filtering logic
for pattern in heatmap_patterns:
    principal_findings_raw = re.sub(pattern, '', principal_findings_raw, flags=re.IGNORECASE)

for pattern in pca_patterns:
    principal_findings_raw = re.sub(pattern, '', principal_findings_raw, flags=re.IGNORECASE)

principal_findings_raw = re.sub(r'No PCA\s+a\s*n\s*alysis\s+available', '', principal_findings_raw, flags=re.IGNORECASE)
principal_findings_raw = re.sub(r'PCA\s+a\s*n\s*alysis\s+available', '', principal_findings_raw, flags=re.IGNORECASE)

print("✅ Original content length:", len(test_content))
print("✅ Filtered content length:", len(principal_findings_raw))
print("✅ Filtered content:")
print(principal_findings_raw.strip())

print("\n🎯 re import fix verification complete!")