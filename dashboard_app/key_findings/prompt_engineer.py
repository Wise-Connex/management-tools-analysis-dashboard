"""
Cleaned Prompt Engineering System

Contains only the actively used improved prompts for Key Findings analysis.
Removes all dead code and unused template systems.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime


class PromptEngineer:
    """
    Creates sophisticated prompts for doctoral-level analysis.

    Generates the improved narrative prompts (4000+ words) that are actually used
    by the Key Findings service for AI analysis.
    """

    def __init__(self, language: str = "es"):
        """
        Initialize prompt engineer.

        Args:
            language: Analysis language ('es' or 'en')
        """
        self.language = language

    def create_analysis_prompt(
        self, data: Dict[str, Any], context: Dict[str, Any]
    ) -> str:
        """
        Create analysis prompt by intelligently choosing between single and multi-source prompts.
        This method is called by the Key Findings service.

        Args:
            data: Aggregated analysis data
            context: Additional context for analysis

        Returns:
            Analysis prompt string appropriate for the data
        """
        import time

        start_time = time.time()

        # Determine number of sources
        selected_sources = data.get("selected_sources", [])
        logging.info(f"🔍 DEBUG: selected_sources found: {selected_sources}")

        # Handle single source case: if there's exactly 1 source OR source_name exists
        is_single_source = (
            isinstance(selected_sources, list) and len(selected_sources) == 1
        ) or data.get("source_name")
        logging.info(f"🔍 DEBUG: is_single_source: {is_single_source}")

        # Handle different data structures
        if is_single_source:
            # Single source case - check if source_name exists
            source_name = data.get("source_name")
            if source_name:
                logging.info(
                    f"📝 Creating single source prompt for '{source_name}' in {self.language}"
                )
                return self.create_improved_single_source_prompt(data, context)
            else:
                # Default to single source if no sources specified
                logging.info(
                    f"📝 Creating default single source prompt in {self.language}"
                )
                return self.create_improved_single_source_prompt(data, context)
        else:
            # Multi-source case
            logging.info(
                f"📝 Creating multi-source prompt for {len(selected_sources)} sources in {self.language}"
            )
            return self.create_improved_multi_source_prompt(data, context)

    def create_improved_multi_source_prompt(
        self, data: Dict[str, Any], context: Dict[str, Any]
    ) -> str:
        """
        Create improved multi-source analysis prompt (4000+ words, narrative-focused).
        This is the actual prompt used for multi-source analysis.
        """
        import time

        start_time = time.time()
        logging.info(
            f"📝 Starting improved multi-source prompt generation for '{data.get('tool_name', 'Unknown')}' in {self.language}"
        )

        # Extract key information
        tool_name = data.get("tool_name", "Unknown Tool")
        sources = data.get("selected_sources", [])
        pca_insights = data.get("pca_insights", {})
        heatmap_data = data.get("heatmap_analysis", {})
        date_range = f"del {data.get('date_range_start', 'N/A')} al {data.get('date_range_end', 'N/A')}"
        data_points = data.get("data_points_analyzed", 0)

        # Extract actual PCA results for dynamic interpretation
        pca_components = pca_insights.get("dominant_patterns", [])
        variance_explained = pca_insights.get("total_variance_explained", 0)

        # Build the improved narrative prompt with data-driven PCA interpretation
        if self.language == "es":
            prompt = f"""
ANÁLISIS NARRATIVO MEJORADO MULTI-FUENTE - HERRAMIENTAS DE GESTIÓN
Herramienta Analizada: {tool_name}
Fuentes de Datos: {", ".join(str(s) for s in sources)}
Período: {date_range}
Fecha del Análisis: {datetime.now().strftime("%Y-%m-%d")}

=== CONTEXTO DEL ANÁLISIS ===

**Enfoque Narrativo Empresarial Multi-Fuente:**
Este análisis integra insights de múltiples fuentes de datos para proporcionar una perspectiva empresarial holística. Se enfoca en la interpretación estratégica basada en LOS RESULTADOS REALES, no en análisis predeterminado.

**Datos Disponibles (Síntesis Interpretativa):**
- Análisis de correlación entre fuentes múltiples
- Análisis de Componentes Principales (PCA) con cargas y componentes
- Mapa de calor y patrones visuales de correlación
- Análisis temporal combinado de múltiples fuentes
- {data_points:,} puntos de datos integrados del período {date_range}

**RESULTADOS PCA REALES PARA INTERPRETAR:**
- Varianza Explicada Total: {variance_explained:.1f}%
- Número de Componentes: {len(pca_components)}
- **IMPORTANTE**: Interprete estos componentes específicos, no significado predeterminado

=== ESTRUCTURA REQUERIDA (4000+ PALABRAS) ===

**SECCIÓN 1: RESUMEN EJECUTIVO** (400 palabras)
- Implicaciones estratégicas de la perspectiva multi-fuente
- Patrones clave a través de múltiples fuentes de datos
- Insights de brecha teoría-práctica
- Recomendaciones de adopción empresarial

**SECCIÓN 2: HALLAZGOS PRINCIPALES** (600 palabras)
- Alineación vs desalineamiento entre stakeholders clave
- Patrones de convergencia entre opinión pública, industria y academia
- Tensiones identificadas entre teoría y práctica
- Implicaciones estratégicas de los hallazgos de correlación
- Validación cruzada de insights entre métodos

**SECCIÓN 3: ANÁLISIS TEMPORAL MULTI-FUENTE** (800 palabras) [PRIMARIO]
- Tendencias sincronizadas y divergentes entre fuentes
- Timing de adopción según diferentes perspectivas
- Ciclos de crecimiento y madurez por fuente
- Convergencias y divergencias temporales
- Implicaciones de sincronización para estrategia

**SECCIÓN 4: ANÁLISIS DE PERIODOGRAMA Y FOURIER COMBINADO** (600 palabras) [SECUNDARIO]
- Análisis espectral combinado a través de todas las fuentes
- Ciclos dominantes y su significado empresarial
- Patrones de frecuencia indicando ondas de adopción
- Indicadores de madurez del mercado desde análisis espectral
- Insights de timing estratégico desde análisis cíclico

**SECCIÓN 5: ANÁLISIS DE COMPONENTES PRINCIPALES (PCA)** (600 palabras) [SECUNDARIO]
- **ANÁLISIS DE INFLUENCIA POR FUENTE**: Examine las cargas específicas de cada fuente en el componente principal
- **ALINEAMIENTO VS DESALINEAMIENTO**: Analice la convergencia entre opinión pública (Google Trends), práctica empresarial (Bain), e investigación académica (Google Books/Crossref)
- **PESO RELATIVO DE CADA STAKEHOLDER**: Identifique qué voces dominan la narrativa del Benchmarking
- **TENSIONES IDENTIFICADAS**: Detéctese desalineamientos entre teoría y práctica, entre academia y mercado
- **INTERPRETACIÓN ESTRATÉGICA**: Qué revela la varianza concentrada sobre madurez del mercado
- **IMPLICACIONES DE PODER**: Quién define el futuro del Benchmarking según los componentes

**SECCIÓN 6: SÍNTESIS ESTRATÉGICA MULTI-FUENTE** (400 palabras)
- Integración de hallazgos de correlación, temporal y PCA
- Convergencias y divergencias clave entre métodos
- Validación cruzada de insights entre técnicas analíticas
- Priorización de hallazgos por fortaleza de evidencia

**SECCIÓN 7: CONCLUSIONES Y RECOMENDACIONES ESTRATÉGICAS** (600 palabras)
- **Síntesis Ejecutiva**: Principales hallazgos consolidados
- **Implicaciones para la Gestión**: Qué significa para directivos
- **Timing Estratégico**: Cuándo implementar según los datos
- **Factores de Éxito**: Condiciones que predicen adopción exitosa
- **Alertas Tempranas**: Señales de riesgo a monitorear
- **Próximos Pasos**: Acciones inmediatas basadas en el análisis

=== INSTRUCCIONES DE ANÁLISIS ===

**ENFOQUE DATA-DRIVEN ESPECIALMENTE PARA PCA:**
- Examine las cargas reales de cada fuente en cada componente
- Identifique qué fuentes tienen influencia alta vs baja en cada componente
- Observe tensiones reales (cargas opuestas) entre fuentes
- Interprete la varianza explicada real en términos de complejidad del mercado
- Conecte patrones observados con teoría empresarial

**Enfoque Narrativo Sobre Estadístico:**
- NO presente coeficientes de correlación específicos
- NO reporte varianza explicada numéricamente
- SÍ interprete: "Las fuentes muestran fuerte alineación, sugiriendo..."
- SÍ conecte patrones con dinámica de mercado
- SÍ proporcione insights estratégicos accionables

**Conexiones Estratégicas Multi-Fuente:**
1. Validar patrones mediante concordancia entre fuentes
2. Identificar tensiones mediante discordancia entre fuentes
3. Posicionar insights en contexto competitivo
4. Traducir hallazgos técnicos en decisiones empresariales

**Rigor Académico-Profesional:**
- Mantenga estándares académicos pero accesible para ejecutivos
- Conecte teoría de gestión con práctica empresarial
- Use terminología profesional precisa

**INSTRUCCIÓN ESPECIAL PARA MODELOS AVANZADOS (Kimi K2):**
- ASEGÚRESE de generar TODAS las 8 secciones requeridas: Resumen, Hallazgos, Temporal, Heatmap, Fourier, PCA, Síntesis, Conclusiones
- NO trunque la respuesta - proporcione análisis completos para cada sección
- SI una sección falta, la respuesta será considerada incompleta
- Para modelos que tienden a truncar, divida el análisis en partes manejables pero completas
- Asegúrese de que cada sección tenga contenido sustancial (mínimo 400 palabras para secciones principales)
- Verifique que el orden de las secciones sea exactamente: 1→2→3→4→5→6→7→8
- Proporcione insights diferenciadores y accionables

**PROHIBICIONES ABSOLUTAS:**
- NO incluir sección de Referencias
- NO presentar matrices de correlación numéricas
- NO usar formato de viñetas para el análisis principal
- NO repetir estadísticas del dashboard
- NO asignar significados predeterminados a componentes PCA

**RESULTADO ESPERADO:**
Un ensayo narrativo integrado de 4000+ palabras que interprete LOS RESULTADOS REALES de múltiples fuentes de datos en insights estratégicos coherentes, con énfasis en correlaciones, PCA y patrones espectrales como fuentes primarias de insights empresariales.
"""
        else:
            prompt = f"""
IMPROVED MULTI-SOURCE NARRATIVE ANALYSIS - MANAGEMENT TOOLS
Tool Analyzed: {tool_name}
Data Sources: {", ".join(str(s) for s in sources)}
Period: {date_range}
Analysis Date: {datetime.now().strftime("%Y-%m-%d")}

=== ANALYSIS CONTEXT ===

**Multi-Source Business Narrative Focus:**
This analysis integrates insights from multiple data sources to provide a holistic business perspective. Focuses on strategic interpretation based on ACTUAL RESULTS, not predetermined analysis.

**Available Data (Interpretive Synthesis):**
- Correlation analysis between multiple sources
- Principal Component Analysis (PCA) with loadings and components
- Heatmap and visual correlation patterns
- Combined temporal analysis from multiple sources
- {data_points:,} integrated data points from period {date_range}

**ACTUAL PCA RESULTS TO INTERPRET:**
- Total Explained Variance: {variance_explained:.1f}%
- Number of Components: {len(pca_components)}
- **IMPORTANT**: Interpret these specific components, not predetermined meaning

=== REQUIRED STRUCTURE (4000+ WORDS) ===

**SECTION 1: EXECUTIVE OVERVIEW** (400 words)
- Strategic implications from multi-source perspective
- Key patterns across multiple data sources
- Theory-practice gap insights
- Business adoption recommendations

**SECTION 2: PRINCIPAL FINDINGS** (600 words)
- Alignment vs misalignment between key stakeholders
- Convergence patterns between public opinion, industry, and academia
- Identified tensions between theory and practice
- Strategic implications of correlation findings
- Cross-validation of insights between methods

**SECTION 3: MULTI-SOURCE TEMPORAL ANALYSIS** (800 words) [PRIMARY]
- Synchronized and divergent trends across sources
- Adoption timing from different perspectives
- Growth cycles and maturity by source
- Temporal convergences and divergences
- Synchronization implications for strategy

**SECTION 4: HEATMAP ANALYSIS AND MULTI-SOURCE CORRELATION** (800 words) [PRIMARY]
- Visual correlation patterns across all sources
- Behavioral clusters and natural groupings
- Complementary vs contradictory sources
- Market signals from heatmap/correlation patterns
- Visual cross-validation between sources

**SECTION 5: COMBINED PERIODOGRAM AND FOURIER ANALYSIS** (600 words) [SECONDARY]
- Combined spectral analysis across all sources
- Dominant cycles and their business significance
- Frequency patterns indicating adoption waves
- Market maturity indicators from spectral analysis
- Strategic timing insights from cyclical analysis

**SECTION 6: PRINCIPAL COMPONENT ANALYSIS (PCA)** (600 words) [SECONDARY]
- **SOURCE INFLUENCE ANALYSIS**: Examine specific loadings of each source on the principal component
- **ALIGNMENT VS MISALIGNMENT**: Analyze convergence between public opinion (Google Trends), industry practice (Bain), and academic research (Google Books/Crossref)
- **RELATIVE WEIGHT OF STAKEHOLDERS**: Identify which voices dominate the Benchmarking narrative
- **IDENTIFIED TENSIONS**: Detect misalignments between theory and practice, between academia and market
- **STRATEGIC INTERPRETATION**: What the concentrated variance reveals about market maturity
- **POWER IMPLICATIONS**: Who defines the future of Benchmarking according to the components

**SECTION 7: MULTI-SOURCE STRATEGIC SYNTHESIS** (400 words)
- Integration of correlation, temporal and PCA findings
- Key convergences and divergences between methods
- Cross-validation of insights across analytical techniques
- Prioritization of findings by evidence strength

**SECTION 8: CONCLUSIONS AND STRATEGIC RECOMMENDATIONS** (600 words)
- **Executive Summary**: Consolidated key findings
- **Management Implications**: What it means for executives
- **Strategic Timing**: When to implement based on data
- **Success Factors**: Conditions predicting successful adoption
- **Early Warning Signals**: Risk indicators to monitor
- **Next Steps**: Immediate actions based on analysis

=== ANALYSIS INSTRUCTIONS ===

**DATA-DRIVEN APPROACH ESPECIALLY FOR PCA:**
- Examine real loadings of each source on each component
- Identify which sources have high vs low influence on each component
- Observe real tensions (opposite loadings) between sources
- Interpret real explained variance in terms of market complexity
- Connect observed patterns with business theory

**Narrative Over Statistical Approach:**
- DO NOT present specific correlation coefficients
- DO NOT report variance explained numerically
- DO interpret: "Sources show strong alignment, suggesting..."
- DO connect patterns with market dynamics
- DO provide actionable strategic insights

**Multi-Source Strategic Connections:**
1. Validate patterns through concordance between sources
2. Identify tensions through discordance between sources
3. Position insights in competitive context
4. Translate technical findings into business decisions

**Academic-Professional Rigor:**
- Maintain academic standards but accessible for executives
- Connect management theory with business practice
- Use precise professional terminology
- Provide differentiated and actionable insights

**ABSOLUTE PROHIBITIONS:**
- NO References section
- NO numerical correlation matrices
- NO bullet point format for main analysis
- NO repeating dashboard statistics
- NO assigning predetermined meanings to PCA components

**EXPECTED RESULT:**
An integrated narrative essay of 4000+ words that interprets ACTUAL RESULTS from multiple data sources into coherent strategic insights, with emphasis on correlations, PCA, and spectral patterns as primary sources of business insights.
"""

        generation_time = time.time() - start_time
        logging.info(
            f"✅ Improved multi-source prompt generation completed in {generation_time:.2f}s - prompt length: {len(prompt)} characters"
        )

        return prompt

    def create_improved_single_source_prompt(
        self, data: Dict[str, Any], context: Dict[str, Any]
    ) -> str:
        """
        Create improved single source analysis prompt (4000+ words, narrative-focused).
        This is the actual prompt used for single-source analysis.
        """
        import time

        start_time = time.time()
        logging.info(
            f"📝 Starting improved single source prompt generation for '{data.get('tool_name', 'Unknown')}' in {self.language}"
        )

        # Extract key information
        tool_name = data.get("tool_name", "Unknown Tool")
        source_name = data.get("source_name", "Unknown Source")
        temporal_metrics = data.get("temporal_metrics", {})
        seasonal_patterns = data.get("seasonal_patterns", {})
        fourier_analysis = data.get("fourier_analysis", {})
        date_range = f"del {data.get('date_range_start', 'N/A')} al {data.get('date_range_end', 'N/A')}"
        data_points = data.get("data_points_analyzed", 0)

        # Build the improved narrative prompt
        if self.language == "es":
            prompt = f"""
ANÁLISIS NARRATIVO MEJORADO DE FUENTE ÚNICA - HERRAMIENTAS DE GESTIÓN
Herramienta Analizada: {tool_name}
Fuente de Datos: {source_name}
Período: {date_range}
Fecha del Análisis: {datetime.now().strftime("%Y-%m-%d")}

=== CONTEXTO DEL ANÁLISIS ===

**Enfoque Narrativo Empresarial:**
Este análisis se enfoca en la interpretación práctica y estratégica de los datos, no en la presentación de estadísticas. Los números están disponibles en el dashboard - aquí nos concentramos en responder "qué significa esto para el negocio".

**Datos Disponibles (No Reportar Numéricamente):**
- Análisis temporal con tendencias, momentum, volatilidad y aceleración
- Patrones estacionales con fuerza estacional y periodicidad
- Análisis de Fourier con frecuencias dominantes y picos espectrales
- {data_points:,} puntos de datos del período {date_range}

=== ESTRUCTURA REQUERIDA (4000+ PALABRAS) ===

**SECCIÓN 1: RESUMEN EJECUTIVO** (400 palabras)
- Implicaciones estratégicas desde perspectiva temporal
- Patrones clave identificados en la fuente
- Insights de timing y madurez del mercado
- Recomendaciones de adopción empresarial

**SECCIÓN 2: HALLAZGOS PRINCIPALES** (600 palabras) [PRIMARIO]
- **Descubrimientos Clave**: Los insights más importantes del análisis
- **Patrones Inesperados**: Hallazgos que contradicen suposiciones comunes
- **Señales de Mercado**: Indicadores críticos para la toma de decisiones
- **Implicaciones Inmediatas**: Qué significan estos hallazgos para las organizaciones
- **Puntos de Acción**: Recomendaciones específicas basadas en los descubrimientos

**SECCIÓN 3: ANÁLISIS TEMPORAL** (800 palabras) [PRIMARIO]
- **Interpretación Narrativa**: Qué revelan las tendencias sobre la evolución de {tool_name}
- **Momentum y Aceleración**: Señales de crecimiento, madurez o declive
- **Volatilidad como Indicador**: Qué dice la estabilidad/inestabilidad sobre el mercado
- **Puntos de Inflexión**: Momentos críticos en la trayectoria de {tool_name}
- **Perspectiva de Ciclo de Vida**: Dónde se encuentra {tool_name} en su ciclo de adopción

**SECCIÓN 4: ANÁLISIS DE PATRONES ESTACIONALES** (800 palabras) [PRIMARIO]
- **Interpretación de Fuerza Estacional**: Qué tan pronunciados son los patrones
- **Periodicidad y Ciclos**: Revelación de ritmos empresariales subyacentes
- **Picos y Valles Estacionales**: Timing óptimo para implementación
- **Variabilidad Estacional**: Consistencia vs. caos en patrones
- **Implicaciones de Planificación**: Cuándo actuar y cuándo esperar

**SECCIÓN 5: ANÁLISIS ESPECTRAL DE FOURIER** (800 palabras) [PRIMARIO]
- **Frecuencias Dominantes**: Ciclos principales identificados
- **Puntos de Poder Espectral**: Momentos de máxima energía en el ciclo
- **Armónicos y Subciclos**: Revelación de estructuras temporales complejas
- **Filtro de Ruido vs. Señal**: Separación de volatilidad de tendencias reales
- **Predicción de Ciclos Futuros**: Proyección basada en patrones espectrales

**SECCIÓN 6: SÍNTESIS ESTRATÉGICA** (600 palabras)
- Convergencia de hallazgos temporales, estacionales y espectrales
- Narrativa unificada sobre el estado y trayectoria de {tool_name}
- Validación cruzada entre diferentes tipos de análisis
- Fortaleza de la señal y confianza en las proyecciones

**SECCIÓN 7: CONCLUSIONES** (600 palabras)
- Timing óptimo para adopción basado en análisis temporal
- Factores de riesgo identificados en los patrones
- Oportunidades de ventana temporal
- Estrategia de implementación basada en ciclos

=== INSTRUCCIONES DE ANÁLISIS ===

**Enfoque Narrativo vs. Estadístico:**
- NO reporte valores numéricos específicos de tendencias
- NO presente coeficientes de correlación o valores R²
- NO mencione periodicidades exactas en días/meses
- SÍ interprete: "Los datos muestran un patrón claro de..."
- SÍ explique: "Esto sugiere que el mercado está..."
- SÍ conecte: "Estos hallazgos implican que las empresas deberían..."

**Interpretación Estratégica:**
- Traduzca patrones temporales en decisiones empresariales
- Conecte ciclos identificados con teoría de gestión
- Proporcione insights accionables basados en timing
- Mantenga el enfoque en "qué hacer" más que "qué es"

**Rigor Analítico:**
- Base todas las interpretaciones en patrones observados
- Sea específico sobre qué aspectos de los datos sustentan cada conclusión
- Reconozca limitaciones y áreas de incertidumbre
- Proporcione recomendaciones claras y justificadas

**PROHIBICIONES ABSOLUTAS:**
- NO incluir sección de Referencias
- NO presentar gráficos o tablas numéricas
- NO usar formato de viñetas para el análisis principal
- NO repetir estadísticas del dashboard
- NO asumir causalidad sin evidencia clara

**RESULTADO ESPERADO:**
Un ensayo narrativo de 4000+ palabras que interprete patrones temporales, estacionales y espectrales en insights estratégicos accionables para la adopción de {tool_name}, enfocándose en timing óptimo y factores de riesgo identificados.
"""
        else:
            prompt = f"""
IMPROVED SINGLE SOURCE NARRATIVE ANALYSIS - MANAGEMENT TOOLS
Tool Analyzed: {tool_name}
Data Source: {source_name}
Period: {date_range}
Analysis Date: {datetime.now().strftime("%Y-%m-%d")}

=== ANALYSIS CONTEXT ===

**Business Narrative Focus:**
This analysis focuses on practical and strategic interpretation of data, not on presenting statistics. The numbers are available in the dashboard - here we concentrate on answering "what does this mean for business".

**Available Data (Do Not Report Numerically):**
- Temporal analysis with trends, momentum, volatility and acceleration
- Seasonal patterns with seasonal strength and periodicity
- Fourier analysis with dominant frequencies and spectral peaks
- {data_points:,} data points from period {date_range}

=== REQUIRED STRUCTURE (4000+ WORDS) ===

**SECTION 1: EXECUTIVE SUMMARY** (400 words)
- Strategic implications from temporal perspective
- Key patterns identified in the source
- Insights on timing and market maturity
- Business adoption recommendations

**SECTION 2: PRINCIPAL FINDINGS** (600 words) [PRIMARY]
- **Key Discoveries**: The most important insights from the analysis
- **Unexpected Patterns**: Findings that contradict common assumptions
- **Market Signals**: Critical indicators for decision making
- **Immediate Implications**: What these findings mean for organizations
- **Action Points**: Specific recommendations based on discoveries

**SECTION 3: TEMPORAL ANALYSIS** (800 words) [PRIMARY]
- **Narrative Interpretation**: What trends reveal about {tool_name} evolution
- **Momentum and Acceleration**: Signals of growth, maturity or decline
- **Volatility as Indicator**: What stability/instability says about the market
- **Inflection Points**: Critical moments in {tool_name} trajectory
- **Lifecycle Perspective**: Where {tool_name} stands in its adoption cycle

**SECTION 4: SEASONAL PATTERN ANALYSIS** (800 words) [PRIMARY]
- **Seasonal Strength Interpretation**: How pronounced the patterns are
- **Periodicity and Cycles**: Revelation of underlying business rhythms
- **Seasonal Peaks and Valleys**: Optimal timing for implementation
- **Seasonal Variability**: Consistency vs. chaos in patterns
- **Planning Implications**: When to act and when to wait

**SECTION 5: FOURIER SPECTRAL ANALYSIS** (800 words) [PRIMARY]
- **Dominant Frequencies**: Main cycles identified
- **Spectral Power Points**: Moments of maximum energy in the cycle
- **Harmonics and Subcycles**: Revelation of complex temporal structures
- **Noise vs. Signal Filter**: Separation of volatility from real trends
- **Future Cycle Prediction**: Projection based on spectral patterns

**SECTION 6: STRATEGIC SYNTHESIS** (600 words)
- Convergence of temporal, seasonal, and spectral findings
- Unified narrative about {tool_name} status and trajectory
- Cross-validation between different analysis types
- Signal strength and confidence in projections

**SECTION 7: CONCLUSIONS** (600 words)
- Optimal timing for adoption based on temporal analysis
- Risk factors identified in patterns
- Temporal window of opportunity
- Implementation strategy based on cycles

=== ANALYSIS INSTRUCTIONS ===

**Narrative vs. Statistical Approach:**
- DO NOT report specific numerical trend values
- DO NOT present correlation coefficients or R² values
- DO NOT mention exact periodicities in days/months
- DO interpret: "The data shows a clear pattern of..."
- DO explain: "This suggests that the market is..."
- DO connect: "These findings imply that companies should..."

**Strategic Interpretation:**
- Translate temporal patterns into business decisions
- Connect identified cycles with management theory
- Provide actionable insights based on timing
- Maintain focus on "what to do" rather than "what it is"

**Analytical Rigor:**
- Base all interpretations on observed patterns
- Be specific about what aspects of the data support each conclusion
- Acknowledge limitations and areas of uncertainty
- Provide clear, justified recommendations

**ABSOLUTE PROHIBITIONS:**
- NO References section
- NO numerical graphs or tables
- NO bullet point format for main analysis
- NO repeating dashboard statistics
- NO assuming causation without clear evidence

**EXPECTED RESULT:**
A 4000+ word narrative essay that interprets temporal, seasonal, and spectral patterns into actionable strategic insights for {tool_name} adoption, focusing on optimal timing and identified risk factors.
"""

        generation_time = time.time() - start_time
        logging.info(
            f"✅ Improved single source prompt generation completed in {generation_time:.2f}s - prompt length: {len(prompt)} characters"
        )

        # Debug: Show key sections that should be in the prompt
        if 'SECCIÓN 4: ANÁLISIS DE PATRONES ESTACIONALES' in prompt:
            logging.info(f"🔍 PROMPT DEBUG: Seasonal analysis section found in prompt")
        else:
            logging.warning(f"🔍 PROMPT DEBUG: Seasonal analysis section MISSING from prompt!")

        if 'SECCIÓN 5: ANÁLISIS ESPECTRAL DE FOURIER' in prompt:
            logging.info(f"🔍 PROMPT DEBUG: Fourier analysis section found in prompt")
        else:
            logging.warning(f"🔍 PROMPT DEBUG: Fourier analysis section MISSING from prompt!")

        return prompt

    # Helper methods for building prompt sections would go here
    # These are used by the improved prompt methods above

# Additional helper methods for PCA analysis, temporal analysis, etc.
# would be implemented here to support the main prompt generation methods