# Key Findings Section Requirements
## Content Structure for Single-Source vs Multi-Source Analysis

## 📊 **Section Requirements by Analysis Type**

### **Single-Source Analysis** (7 sections total)

| Section | Content Type | Database Field | Purpose |
|---------|-------------|----------------|---------|
| 1. Header | Metadata | `tool_name`, `selected_sources`, `model_used`, `data_points_analyzed` | Report identification and metadata |
| 2. Executive Summary | Narrative | `executive_summary` | High-level strategic insights |
| 3. Principal Findings | Combined Narrative | `principal_findings` | **COMBINED** temporal + seasonal + fourier + findings |
| 4. Strategic Synthesis | Narrative | `strategic_synthesis` | Strategic recommendations |
| 5. Conclusions | Narrative | `conclusions` | Final takeaways and next steps |
| 6. Statistical Summary | Metadata | `data_points_analyzed`, `confidence_score` | Data metrics and validation |
| 7. Metadata | Technical | `api_latency_ms`, `generation_timestamp` | Technical information |

**❌ EXCLUDED for Single-Source:**
- Heatmap Analysis (correlation analysis requires multiple sources)
- PCA Analysis (principal component analysis requires multiple sources)

---

### **Multi-Source Analysis** (8+ sections total)

| Section | Content Type | Database Field | Purpose |
|---------|-------------|----------------|---------|
| 1. Header | Metadata | `tool_name`, `selected_sources`, `model_used`, `data_points_analyzed` | Report identification and metadata |
| 2. Executive Summary | Narrative | `executive_summary` | High-level strategic insights |
| 3. Principal Findings | Narrative | `principal_findings` | Main findings and insights |
| 4. Heatmap Analysis | Visual Analysis | `heatmap_analysis` | **CORRELATION MATRIX** between sources |
| 5. PCA Analysis | Statistical | `pca_analysis` | **PRINCIPAL COMPONENT ANALYSIS** |
| 6. Strategic Synthesis | Narrative | `strategic_synthesis` | Strategic recommendations |
| 7. Conclusions | Narrative | `conclusions` | Final takeaways and next steps |
| 8. Statistical Summary | Metadata | `data_points_analyzed`, `confidence_score` | Data metrics and validation |
| 9. Metadata | Technical | `api_latency_ms`, `generation_timestamp` | Technical information |
| 10+ Optional | Individual Analysis | `temporal_analysis`, `seasonal_analysis`, `fourier_analysis` | Individual source analyses |

**✅ INCLUDED for Multi-Source:**
- Heatmap Analysis (correlation between multiple data sources)
- PCA Analysis (dimensionality reduction across sources)
- Individual temporal/seasonal/fourier analyses for each source

---

## 📝 **Content Organization Rules**

### **Single-Source Content Flow:**
```
AI Response: [executive_summary, temporal_analysis, seasonal_analysis, fourier_analysis, ...]
↓
Database Storage:
- executive_summary → executive_summary
- temporal_analysis → principal_findings (with section header)
- seasonal_analysis → principal_findings (with section header)
- fourier_analysis → principal_findings (with section header)
- strategic_synthesis → strategic_synthesis
- conclusions → conclusions
- pca_insights → "" (empty for single-source)
- heatmap_analysis → "" (empty for single-source)
```

### **Multi-Source Content Flow:**
```
AI Response: [executive_summary, principal_findings, heatmap_analysis, pca_analysis, ...]
↓
Database Storage:
- executive_summary → executive_summary
- principal_findings → principal_findings
- heatmap_analysis → heatmap_analysis
- pca_analysis → pca_analysis
- strategic_synthesis → strategic_synthesis
- conclusions → conclusions
- temporal_analysis → temporal_analysis (if available)
- seasonal_analysis → seasonal_analysis (if available)
- fourier_analysis → fourier_analysis (if available)
```

---

## 🎯 **Section Headers and Formatting**

### **Single-Source Principal Findings Structure:**
```
🔍 ANÁLISIS TEMPORAL
[Temporal analysis content]

📅 PATRONES ESTACIONALES
[Seasonal analysis content]

🌊 ANÁLISIS ESPECTRAL
[Fourier analysis content]

🎯 SÍNTESIS ESTRATÉGICA
[Strategic synthesis content]

📝 CONCLUSIONES
[Conclusions content]
```

### **Multi-Source Section Headers:**
```
📋 Resumen Ejecutivo
🔍 Hallazgos Principales
🔥 Análisis del Mapa de Calor (Multi-fuente)
📊 Análisis PCA (Multi-fuente)
🎯 Síntesis Estratégica
📝 Conclusiones
```

---

## 📏 **Content Length Guidelines**

### **Single-Source:**
- **Executive Summary**: 400-600 words
- **Principal Findings**: 2000-4000 words (combined narrative)
- **Strategic Synthesis**: 300-500 words
- **Conclusions**: 200-400 words
- **Total**: 3000-5000+ words

### **Multi-Source:**
- **Executive Summary**: 400-600 words
- **Principal Findings**: 1000-2000 words
- **Heatmap Analysis**: 300-800 words
- **PCA Analysis**: 400-800 words
- **Strategic Synthesis**: 300-500 words
- **Conclusions**: 200-400 words
- **Individual Analyses**: 200-500 words each
- **Total**: 3000-6000+ words

---

## 🔍 **Content Validation Rules**

### **Single-Source Validation:**
- ✅ `principal_findings` MUST have substantial content (>1000 chars)
- ✅ `pca_analysis` SHOULD be empty or very short (<50 chars)
- ✅ `heatmap_analysis` SHOULD be empty or very short (<50 chars)
- ✅ Individual analysis fields should be empty
- ✅ `data_points_analyzed` MUST be > 0
- ✅ `model_used` MUST NOT be 'unknown'

### **Multi-Source Validation:**
- ✅ `principal_findings` MUST have substantial content (>500 chars)
- ✅ `pca_analysis` SHOULD have substantial content (>300 chars)
- ✅ `heatmap_analysis` SHOULD have substantial content (>300 chars)
- ✅ Individual analysis fields MAY have content
- ✅ `sources_count` MUST be > 1
- ✅ `data_points_analyzed` MUST be > 0

---

## 🚨 **Error Handling**

### **Content Validation Status:**
- **'valid'**: All required fields have appropriate content
- **'partial'**: Some content missing but core analysis present
- **'invalid'**: Critical content missing or malformed

### **Placeholder Content Handling:**
- "No PCA analysis available" → Empty string for single-source
- "No heatmap analysis available" → Empty string for single-source
- Broken text patterns → Cleaned and normalized

---

## 📈 **Performance Metrics**

### **Content Quality Indicators:**
- Word count per section
- Content completeness score (0-100)
- Validation status
- User ratings and feedback
- Access patterns and usage

### **Technical Performance:**
- Response time from AI services
- Token usage and cost tracking
- Cache hit/miss ratios
- Error rates and retry patterns