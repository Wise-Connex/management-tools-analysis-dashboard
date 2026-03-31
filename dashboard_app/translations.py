# Bilingual Translation System for Management Tools Analysis Dashboard
# Supports Spanish (es) and English (en) languages

TRANSLATIONS = {
    "es": {
        # UI Labels and Buttons
        "select_tool": "Seleccione una Herramienta:",
        "select_sources": "Seleccione las Fuentes de Datos:",
        "select_source": "Seleccione una Fuente:",
        "select_all": "Seleccionar Todo",
        "show_table": "Mostrar Tabla",
        "hide_table": "Ocultar Tabla",
        "credits": "Créditos",
        "data_table": "Tabla de Datos",
        "data_table_title": "Tabla de Datos",
        "performance_monitor": "Monitor de Rendimiento del Sistema",
        "key_findings": "Hallazgos Principales",
        # Placeholders
        "select_management_tool": "Seleccione una Herramienta Gerencial",
        # Section Headers
        "temporal_analysis_2d": "Análisis Temporal 2D",
        "mean_analysis": "Análisis de Medias",
        "mean_analysis_title": "Análisis de Medias",
        "temporal_analysis_3d": "Análisis Temporal 3D",
        "seasonal_analysis": "Análisis Estacional",
        "fourier_analysis": "Análisis de Fourier (Periodograma)",
        "correlation_heatmap": "Mapa de Calor (Correlación)",
        "regression_analysis": "Análisis de Regresión",
        "pca_analysis": "Análisis PCA (Cargas y Componentes)",
        # Key Findings Modal Sections
        "temporal_analysis": "Análisis Temporal",
        "strategic_synthesis": "Síntesis Estratégica",
        "conclusions": "Conclusiones",
        # Date Range Labels
        "date_range": "Rango de Fechas:",
        "custom_range": "Rango Personalizado:",
        # 3D Analysis
        "data_frequency": "Frecuencia de Datos:",
        "monthly": "Mensual",
        "annual": "Anual",
        "chart_axes": "Ejes del Gráfico:",
        "y_axis": "Eje Y",
        "z_axis": "Eje Z",
        # Seasonal Analysis
        "original_series": "Serie Original",
        "trend": "Tendencia",
        "seasonal": "Estacional",
        "residuals": "Residuos",
        # Fourier Analysis
        "fourier_analysis_periodogram": "Análisis de Fourier - Periodograma",
        "magnitude": "Magnitud",
        "period_months": "Período (meses)",
        "significance_threshold": "Umbral Significancia (95%)",
        "significant_components": "Componentes Significativos",
        "non_significant_components": "Componentes No Significativos",
        "quarterly": "Trimestral (3m)",
        "semiannual": "Semestral (6m)",
        "annual": "Anual (12m)",
        # Dropdown Placeholders
        "select_source_for_analysis": "Seleccione fuente para cargar análisis",
        "select_y_axis": "Eje Y",
        "select_z_axis": "Eje Z",
        # Data Frequency
        "data_frequency": "Frecuencia de Datos:",
        "monthly": "Mensual",
        "annual": "Anual",
        # Chart Elements
        "date": "Fecha",
        "value": "Valor",
        "contribution_relative": "Contribución Relativa (%)",
        "absolute_value": "Valor Absoluto",
        "relative_absolute": "Relativo (100% = {max_value:.2f}) + Absoluto",
        "data_sources": "Fuentes de Datos",
        "correlation": "Correlación",
        "regression_equations": "Haga clic en el mapa de calor para ver las ecuaciones de regresión",
        "click_heatmap": "Haga clic en el mapa de calor para seleccionar variables para regresión",
        "invalid_selection": "Seleccione dos variables diferentes para el análisis de regresión",
        "cannot_regress_same": "No se puede hacer regresión de {var} contra sí mismo.",
        "select_different_vars": "Seleccione dos variables diferentes en el mapa de calor.",
        "correlation_heatmap_title": "Mapa de Calor de Correlación",
        "heatmap_instructions": "Haga clic en las celdas del mapa de calor para ver los valores de correlación. Los colores más intensos indican correlaciones más fuertes.",
        "regression_instructions": "Seleccione dos variables diferentes haciendo clic en el mapa de calor para ver el análisis de regresión y las ecuaciones polinomiales.",
        "temporal_3d_title": "Análisis Temporal 3D: {y_axis} vs {z_axis} ({frequency})",
        "temporal_3d_error": "Error en el análisis temporal 3D",
        "seasonal_title": "Análisis Estacional: {source}",
        "fourier_title": "Análisis de Fourier - Periodograma: {source}",
        "regression_title": "Análisis de Regresión Polinomial: {y_var} vs {x_var}",
        "regression_error": "Error en el análisis de regresión",
        "variables_not_found": "Variables no encontradas: {x_var} vs {y_var}",
        "pca_title": "Análisis PCA (Cargas y Componentes)",
        "pca_insights": "Insights del Análisis PCA",
        "pca_analysis_unavailable": "Análisis PCA no disponible",
        # Performance Monitor
        "database_info": "Información de Base de Datos",
        "total_records": "Total de Registros:",
        "unique_keywords": "Palabras Clave Únicas:",
        "data_sources_count": "Fuentes de Datos:",
        "current_query": "Consulta Actual",
        "records_in_use": "Registros en Uso:",
        "selected_sources": "Fuentes Seleccionadas:",
        "temporal_range": "Rango Temporal:",
        "tool": "Herramienta:",
        "performance_metrics": "Métricas de Rendimiento",
        "database_statistics": "Estadísticas de Base de Datos",
        "system_performance": "Rendimiento del Sistema",
        "analysis_type": "Tipo de Análisis:",
        "language_label": "Idioma:",
        "dashboard_label": "Dashboard:",
        "dashboard_name": "Herramientas de Análisis Gerencial",
        "multi_source": "Multi-Fuente",
        "single_source": "Fuente Única",
        "performance_info": "Las métricas de rendimiento se actualizan en tiempo real según los parámetros de análisis actuales.",
        "cache_entries": "Entradas en Cache:",
        "cache_usage": "Uso de Cache:",
        "cache_efficiency": "Eficiencia de Cache:",
        "data_points_total": "Puntos de Datos Totales:",
        "load_time": "Tiempo de Carga:",
        "query_efficiency": "Eficiencia de Consultas:",
        "memory_usage": "Uso de Memoria:",
        "compression": "Compresión:",
        "active_optimizations": "Optimizaciones Activas",
        "preprocessed_data": "✅ Datos pre-procesados en base de datos",
        "optimized_indexes": "✅ Índices optimizados para velocidad",
        "smart_cache": "✅ Caché inteligente de resultados",
        "lazy_loading": "✅ Lazy loading para análisis complejos",
        "auto_graph_optimization": "✅ Optimización automática de gráficos",
        # Modal
        "source_notes": "Notas de la Fuente",
        "close": "Cerrar",
        "no_notes": "No hay notas disponibles",
        # Error Messages
        "no_data_available": "No hay datos disponibles para la herramienta '{keyword}' con las fuentes seleccionadas.",
        "please_select_tool_and_sources": "Por favor, seleccione una Herramienta y al menos una Fuente de Datos.",
        "no_sources_selected": "Seleccione una herramienta para ver las fuentes disponibles",
        "no_doi_available": "No hay DOI disponible para esta herramienta",
        # Chart Labels
        "period_months": "Período (meses)",
        "magnitude": "Magnitud",
        "significance_threshold": "Umbral Significancia (95%)",
        "significant_components": "Componentes Significativos",
        "non_significant_components": "Componentes No Significativos",
        "quarterly": "Trimestral (3m)",
        "semiannual": "Semestral (6m)",
        "annual": "Anual (12m)",
        # Navigation
        "temporal_2d_nav": "Temporal 2D",
        "mean_analysis_nav": "Análisis Medias",
        "temporal_3d_nav": "Temporal 3D",
        "seasonal_nav": "Estacional",
        "fourier_nav": "Fourier",
        "correlation_nav": "Correlación",
        "regression_nav": "Regresión",
        "pca_nav": "PCA",
        "data_table_nav": "Tabla de Datos",
        "performance_nav": "Rendimiento",
        # Header
        "doctoral_research_focus": "Base analítica para la Investigación Doctoral",
        "ontological_dichotomy": 'Dicotomía ontológica en las "Modas Gerenciales"',
        "management_tools": "Herramientas gerenciales: Dinámicas temporales contingentes y antinomias policontextuales",
        "principal_investigator": "Investigador Principal",
        "academic_tutor": "Tutora Académica",
        "solidum_consulting": "Solidum Consulting",
        "developer": "Desarrollador",
        "ulac": "ULAC",
        # Credits
        "dashboard_analysis": "Dashboard de Análisis de",
        "management_tools_lower": "Herramientas Gerenciales",
        "developed_with": "Desarrollado con Python, Plotly y Dash",
        "by": "por:",
        "tutor": "Tutora Académica:",
        "license": "Licencia Dashboard: CC BY-NC 4.0",
        "harvard_dataverse": "Harvard Dataverse: Data de la Investigación",
        "harvard_title": "Datos en el prestigioso repositorio de la Universidad de Harvard",
        "nlm_publication": "Publicación en la National Library of Medicine",
        "nlm_title": "Datos en la Biblioteca Nacional de Medicina de EE.UU.",
        "zenodo_publication": "Publicación en el Repositorio CERN - Zenodo",
        "zenodo_title": "138 Informes Técnicos en el Repositorio Europeo Zenodo, del Conseil Européen pour la Recherche Nucléaire.",
        "openaire_visibility": "Visibilidad Europea en OpenAire",
        "openaire_title": "Informes y Datos indexados en el Portal Europeo de Ciencia Abierta OpenAire",
        "github_reports": "Informes y Documentación Técnica en GitHub",
        "github_title": "Documentación técnica y científica de herramientas gerenciales en GitHub",
        # Citation Modal
        "how_to_cite": "Cómo Citar",
        "cite_this_dashboard": "Cómo Citar este Dashboard",
        "to_ensure_academic_integrity": "Para asegurar la integridad académica y facilitar la referenciación, por favor utilice el siguiente formato de cita según el estilo requerido por su institución o publicación. Puede copiar el formato de su elección directamente.",
        "apa_7": "APA 7 (Asociación Americana de Psicología)",
        "chicago": "Chicago (17.ª ed., autor-fecha)",
        "mla": "MLA (9.ª ed.)",
        "oscola": "OSCOLA (Jurídico)",
        "vancouver": "Vancouver (Medicina/Salud)",
        "ieee": "IEEE (Ingeniería/Tecnología)",
        "download_ris": "Descargar RIS",
        "copy_citation": "Copiar Cita",
        "download_english_ris": "Descargar RIS (Inglés)",
        "download_spanish_ris": "Descargar RIS (Español)",
        "citation_copied": "Cita copiada al portapapeles",
        "ris_downloaded": "Archivo RIS descargado",
        "accessed_date": "12 de octubre de 2025",
        "accessed_format": "Consultado el 12 de octubre de 2025",
        "cited_format": "accedido el 12 de octubre de 2025",
        "download_ris_files": "Descargar archivos RIS",
        "ris_note": "Los archivos RIS son compatibles con la mayoría de los gestores de referencias bibliográficas como EndNote, Zotero, Mendeley, etc.",
        # Sidebar affiliations
        "university": "Universidad Latinoamericana y del Caribe (ULAC)",
        "postgraduate_coordination": "Coordinación General de Postgrado",
        "doctoral_program": "Doctorado en Ciencias Gerenciales",
        # Source Notes Modal
        "source": "Fuente:",
        "doi": "DOI:",
        "dashboard_url": "https://management-tools-analysis.com",
        # DOI and Links
        "ic_report_doi": "DOI del Informe IC:",
        # Regression
        "linear": "Lineal",
        "quadratic": "Cuadrática",
        "cubic": "Cúbica",
        "quartic": "Cuártica",
        "r_squared": "R²",
        "data_points": "Puntos de Datos",
        # Source names for display
        "bain_satisfaction": "Bain - Satisfacción",
        "bain_usability": "Bain - Usabilidad",
        "bain_satisfaction_db": "Bain - Satisfacción",
        "bain_usability_db": "Bain - Usabilidad",
        # PCA
        "loadings": "Cargas de Componentes",
        "explained_variance": "Varianza Explicada",
        "cumulative_variance": "Varianza Acumulativa (%)",
        "inverse_relationship": "Relación Inversa",
        # Fourier
        "select_source_fourier": "Seleccione una fuente de datos para ver el análisis de Fourier",
        # General
        "available": "disponibles",
        "none": "Ninguna",
        "healthy": "saludable",
        "unhealthy": "no saludable",
        "connected": "conectado",
        "unavailable": "no disponible",
        "version": "Versión",
        "service": "Servicio",
        "database": "Base de Datos",
        "less_than_half_second": "< 0.5 segundos",
        "high": "Alta",
        "optimized": "Optimizado",
        "average_compression": "85% promedio",
        # Key Findings Modal - Spanish
        "export_pdf_button": "Exportar PDF",
        "key_findings_modal_title": "🧠 Hallazgos Principales",
        "generating_analysis": "Generando análisis...",
        "may_take_30_seconds": "Esto puede tomar hasta 30 segundos...",
        "analyzing_multisource_data": "Analizando datos multi-fuente con énfasis en PCA...",
        "estimated_time_15_30_seconds": "Tiempo estimado: 15-30 segundos",
        "data_collected": "Datos recopilados",
        "pca_analysis_in_progress": "Análisis PCA en progreso...",
        "generating_ai_insights": "Generando insights con IA",
        "creating_executive_summary": "Creando resumen ejecutivo",
        "analysis_not_available": "Análisis No Disponible",
        "generated_by": "Generado por",
        "time": "Tiempo",
        "section_prefix_executive_summary": "📋 RESUMEN EJECUTIVO",
        "section_prefix_principal_findings": "🔍 HALLAZGOS PRINCIPALES",
        "section_prefix_temporal_analysis": "🔍 ANÁLISIS TEMPORAL",
        "section_prefix_seasonal_analysis": "📅 PATRONES ESTACIONALES",
        "section_prefix_fourier_analysis": "🌊 ANÁLISIS ESPECTRAL",
        "section_prefix_strategic_synthesis": "🎯 SÍNTESIS ESTRATÉGICA",
        "section_prefix_conclusions": "📝 CONCLUSIONES",
        "statistical_summary": "Resumen Estadístico",
        "data_analyzed": "Datos analizados",
        "data_points": "puntos",
        "time_range": "Rango temporal",
        "section_integrates_analyses": "Esta sección integra análisis de componentes principales, patrones temporales y correlaciones",
        "detailed_pca_analysis": "Análisis detallado de componentes principales",
        "paragraphs": "párrafos",
        "select_tool_and_sources": "Seleccione una herramienta y fuentes de datos para generar Key Findings.",
        "doctoral_analysis_will_provide": "El análisis doctoral proporcionará insights basados en:",
        "principal_component_analysis": "Análisis de Componentes Principales (PCA)",
        "temporal_trends_patterns": "Tendencias temporales y patrones",
        "correlations_between_sources": "Correlaciones entre fuentes de datos",
        "actionable_executive_insights": "Insights ejecutivos accionables",
        "analysis_information": "Información del Análisis",
        "ai_model": "Modelo IA:",
        "response_time": "Tiempo de Respuesta:",
        "data_points": "Puntos de Datos:",
        "generation_date": "Fecha de Generación:",
        "previous_accesses": "Accesos Previos:",
        "depth": "Profundidad:",
        "executive_summary": "Resumen Ejecutivo",
        "principal_findings": "Hallazgos Principales",
        "heatmap_analysis": "Análisis del Mapa de Calor",
        # Time Range Buttons
        "all": "Todo",
        "20_years": "20 años",
        "15_years": "15 años",
        "10_years": "10 años",
        "5_years": "5 años",
    },
    "en": {
        # UI Labels and Buttons
        "select_tool": "Select a Tool:",
        "select_sources": "Select Data Sources:",
        "select_source": "Select a Source:",
        "select_all": "Select All",
        "show_table": "Show Table",
        "hide_table": "Hide Table",
        "credits": "Credits",
        "data_table": "Data Table",
        "data_table_title": "Data Table",
        "performance_monitor": "System Performance Monitor",
        "key_findings": "Key Findings",
        # Placeholders
        "select_management_tool": "Select a Management Tool",
        # Section Headers
        "temporal_analysis_2d": "Temporal Analysis 2D",
        "mean_analysis": "Mean Analysis",
        "mean_analysis_title": "Mean Analysis",
        "temporal_analysis_3d": "Temporal Analysis 3D",
        "seasonal_analysis": "Seasonal Analysis",
        "fourier_analysis": "Fourier Analysis (Periodogram)",
        "correlation_heatmap": "Correlation Heatmap",
        "regression_analysis": "Regression Analysis",
        "pca_analysis": "PCA Analysis (Loadings and Components)",
        # Key Findings Modal Sections
        "temporal_analysis": "Temporal Analysis",
        "strategic_synthesis": "Strategic Synthesis",
        "conclusions": "Conclusions",
        # Time Range Buttons
        "all": "All",
        "20_years": "20 years",
        "15_years": "15 years",
        "10_years": "10 years",
        "5_years": "5 years",
        # Date Range Labels
        "date_range": "Date Range:",
        "custom_range": "Custom Range:",
        # 3D Analysis
        "data_frequency": "Data Frequency:",
        "monthly": "Monthly",
        "annual": "Annual",
        "chart_axes": "Chart Axes:",
        "y_axis": "Y Axis",
        "z_axis": "Z Axis",
        # Seasonal Analysis
        "original_series": "Original Series",
        "trend": "Trend",
        "seasonal": "Seasonal",
        "residuals": "Residuals",
        # Fourier Analysis
        "fourier_analysis_periodogram": "Fourier Analysis - Periodogram",
        "magnitude": "Magnitude",
        "period_months": "Period (months)",
        "significance_threshold": "Significance Threshold (95%)",
        "significant_components": "Significant Components",
        "non_significant_components": "Non-Significant Components",
        "quarterly": "Quarterly (3m)",
        "semiannual": "Semiannual (6m)",
        "annual": "Annual (12m)",
        # Dropdown Placeholders
        "select_source_for_analysis": "Select source to load analysis",
        "select_y_axis": "Y Axis",
        "select_z_axis": "Z Axis",
        # Data Frequency
        "data_frequency": "Data Frequency:",
        "monthly": "Monthly",
        "annual": "Annual",
        # Chart Elements
        "date": "Date",
        "value": "Value",
        "contribution_relative": "Relative Contribution (%)",
        "absolute_value": "Absolute Value",
        "relative_absolute": "Relative (100% = {max_value:.2f}) + Absolute",
        "data_sources": "Data Sources",
        "correlation": "Correlation",
        "regression_equations": "Click on the heatmap to see regression equations",
        "click_heatmap": "Click on the heatmap to select variables for regression",
        "invalid_selection": "Select two different variables for regression analysis",
        "cannot_regress_same": "Cannot regress {var} against itself.",
        "select_different_vars": "Select two different variables on the heatmap.",
        "correlation_heatmap_title": "Correlation Heatmap",
        "heatmap_instructions": "Click on heatmap cells to see correlation values. More intense colors indicate stronger correlations.",
        "regression_instructions": "Select two different variables by clicking on the heatmap to see regression analysis and polynomial equations.",
        "temporal_3d_title": "Temporal 3D Analysis: {y_axis} vs {z_axis} ({frequency})",
        "temporal_3d_error": "Error in 3D temporal analysis",
        "seasonal_title": "Seasonal Analysis: {source}",
        "fourier_title": "Fourier Analysis - Periodogram: {source}",
        "regression_title": "Polynomial Regression Analysis: {y_var} vs {x_var}",
        "regression_error": "Error in regression analysis",
        "variables_not_found": "Variables not found: {x_var} vs {y_var}",
        "pca_title": "PCA Analysis (Loadings and Components)",
        "pca_insights": "PCA Analysis Insights",
        "pca_analysis_unavailable": "PCA Analysis Unavailable",
        # Performance Monitor
        "database_info": "Database Information",
        "total_records": "Total Records:",
        "unique_keywords": "Unique Keywords:",
        "data_sources_count": "Data Sources:",
        "current_query": "Current Query",
        "records_in_use": "Records in Use:",
        "selected_sources": "Selected Sources:",
        "temporal_range": "Temporal Range:",
        "tool": "Tool:",
        "performance_metrics": "Performance Metrics",
        "database_statistics": "Database Statistics",
        "system_performance": "System Performance",
        "analysis_type": "Analysis Type:",
        "language_label": "Language:",
        "dashboard_name": "Management Tools Analysis",
        "dashboard_label": "Dashboard:",
        "multi_source": "Multi-Source",
        "single_source": "Single Source",
        "performance_info": "Performance metrics updated in real-time based on current analysis parameters.",
        "cache_entries": "Cache Entries:",
        "cache_usage": "Cache Usage:",
        "cache_efficiency": "Cache Efficiency:",
        "data_points_total": "Total Data Points:",
        "load_time": "Load Time:",
        "query_efficiency": "Query Efficiency:",
        "memory_usage": "Memory Usage:",
        "compression": "Compression:",
        "active_optimizations": "Active Optimizations",
        "preprocessed_data": "✅ Pre-processed data in database",
        "optimized_indexes": "✅ Optimized indexes for speed",
        "smart_cache": "✅ Smart result caching",
        "lazy_loading": "✅ Lazy loading for complex analyses",
        "auto_graph_optimization": "✅ Automatic graph optimization",
        # Modal
        "source_notes": "Source Notes",
        "close": "Close",
        "no_notes": "No notes available",
        # Error Messages
        "no_data_available": "No data available for tool '{keyword}' with selected sources.",
        "please_select_tool_and_sources": "Please select a Tool and at least one Data Source.",
        "no_sources_selected": "Select a tool to view available sources",
        "no_doi_available": "No DOI available for this tool",
        # Chart Labels
        "period_months": "Period (months)",
        "magnitude": "Magnitude",
        "significance_threshold": "Significance Threshold (95%)",
        "significant_components": "Significant Components",
        "non_significant_components": "Non-Significant Components",
        "quarterly": "Quarterly (3m)",
        "semiannual": "Semiannual (6m)",
        "annual": "Annual (12m)",
        # Navigation
        "temporal_2d_nav": "Temporal 2D",
        "mean_analysis_nav": "Mean Analysis",
        "temporal_3d_nav": "Temporal 3D",
        "seasonal_nav": "Seasonal",
        "fourier_nav": "Fourier",
        "correlation_nav": "Correlation",
        "regression_nav": "Regression",
        "pca_nav": "PCA",
        "data_table_nav": "Data Table",
        "performance_nav": "Performance",
        # Header
        "doctoral_research_focus": "Analytical basis for Doctoral Research",
        "ontological_dichotomy": 'Ontological dichotomy in "Management Fads"',
        "management_tools": "Management tools: Contingent temporal dynamics and policontextual antinomies",
        "principal_investigator": "Principal Researcher",
        "academic_tutor": "Academic Tutor",
        "solidum_consulting": "Solidum Consulting",
        "developer": "Developer",
        "ulac": "ULAC",
        # Credits
        "dashboard_analysis": "Analysis Dashboard of",
        "management_tools_lower": "Management Tools",
        "developed_with": "Developed with Python, Plotly and Dash",
        "by": "by:",
        "tutor": "Academic Tutor:",
        "license": "Dashboard License: CC BY-NC 4.0",
        "harvard_dataverse": "Harvard Dataverse: Research Data",
        "harvard_title": "Data in Harvard University's prestigious repository",
        "nlm_publication": "Publication in the National Library of Medicine",
        "nlm_title": "Data in the U.S. National Library of Medicine",
        "zenodo_publication": "Publication in the CERN Zenodo Repository",
        "zenodo_title": "138 Technical Reports in the European Zenodo Repository, from the Conseil Européen pour la Recherche Nucléaire.",
        "openaire_visibility": "European Visibility in OpenAire",
        "openaire_title": "Reports and Data indexed in the European Open Science Portal OpenAire",
        "github_reports": "Reports and Technical Documentation on GitHub",
        "github_title": "Technical and scientific documentation of management tools on GitHub",
        # Citation Modal
        "how_to_cite": "How to Cite",
        "cite_this_dashboard": "How to Cite this Dashboard",
        "to_ensure_academic_integrity": "To ensure academic integrity and facilitate referencing, please use the appropriate citation format below as required by your institution or publication. You can copy your preferred format directly.",
        "apa_7": "APA 7 (American Psychological Association)",
        "chicago": "Chicago (17th ed., author-date)",
        "mla": "MLA (9th ed.)",
        "oscola": "OSCOLA (Legal)",
        "vancouver": "Vancouver (Medicine/Health)",
        "ieee": "IEEE (Engineering/Tech)",
        "download_ris": "Download RIS",
        "copy_citation": "Copy Citation",
        "download_english_ris": "Download RIS (English)",
        "download_spanish_ris": "Download RIS (Spanish)",
        "citation_copied": "Citation copied to clipboard",
        "ris_downloaded": "RIS file downloaded",
        "accessed_date": "October 12, 2025",
        "accessed_format": "Accessed October 12, 2025",
        "cited_format": "accessed 12 October 2025",
        "download_ris_files": "Download RIS files",
        "ris_note": "RIS files are compatible with most reference management software such as EndNote, Zotero, Mendeley, etc.",
        # Sidebar affiliations
        "university": "Latin American and Caribbean University (ULAC)",
        "postgraduate_coordination": "General Postgraduate Coordination",
        "doctoral_program": "Doctorate in Management Sciences",
        # Header credits
        "developer": "Developer",
        # Source Notes Modal
        "source": "Source:",
        "doi": "DOI:",
        "dashboard_url": "https://management-tools-analysis.com",
        # DOI and Links
        "ic_report_doi": "IC Report DOI:",
        # Regression
        "linear": "Linear",
        "quadratic": "Quadratic",
        "cubic": "Cubic",
        "quartic": "Quartic",
        "r_squared": "R²",
        "data_points": "Data Points",
        # PCA
        "loadings": "Component Loadings",
        "explained_variance": "Explained Variance",
        "cumulative_variance": "Cumulative Variance (%)",
        "inverse_relationship": "Inverse Relationship",
        # Fourier
        "select_source_fourier": "Select a data source to view the Fourier analysis",
        # General
        "available": "available",
        "none": "None",
        "healthy": "healthy",
        "unhealthy": "unhealthy",
        "connected": "connected",
        "unavailable": "unavailable",
        "version": "Version",
        "service": "Service",
        "database": "Database",
        "less_than_half_second": "< 0.5 seconds",
        "high": "High",
        "optimized": "Optimized",
        "average_compression": "85% average",
        # Key Findings Modal - English
        "export_pdf_button": "Export PDF",
        "key_findings_modal_title": "🧠 Principal Findings",
        "generating_analysis": "Generating analysis...",
        "may_take_30_seconds": "This may take up to 30 seconds...",
        "analyzing_multisource_data": "Analyzing multi-source data with emphasis on PCA...",
        "estimated_time_15_30_seconds": "Estimated time: 15-30 seconds",
        "data_collected": "Data collected",
        "pca_analysis_in_progress": "PCA analysis in progress...",
        "generating_ai_insights": "Generating AI insights",
        "creating_executive_summary": "Creating executive summary",
        "analysis_not_available": "Analysis Not Available",
        "generated_by": "Generated by",
        "time": "Time",
        "section_prefix_executive_summary": "📋 EXECUTIVE SUMMARY",
        "section_prefix_principal_findings": "🔍 PRINCIPAL FINDINGS",
        "section_prefix_temporal_analysis": "🔍 TEMPORAL ANALYSIS",
        "section_prefix_seasonal_analysis": "📅 SEASONAL PATTERNS",
        "section_prefix_fourier_analysis": "🌊 SPECTRAL ANALYSIS",
        "section_prefix_strategic_synthesis": "🎯 STRATEGIC SYNTHESIS",
        "section_prefix_conclusions": "📝 CONCLUSIONS",
        "statistical_summary": "Statistical Summary",
        "data_analyzed": "Data analyzed",
        "data_points": "points",
        "time_range": "Time range",
        "section_integrates_analyses": "This section integrates principal component analysis, temporal patterns and correlations",
        "detailed_pca_analysis": "Detailed principal component analysis",
        "paragraphs": "paragraphs",
        "select_tool_and_sources": "Select a tool and data sources to generate Key Findings.",
        "doctoral_analysis_will_provide": "The doctoral analysis will provide insights based on:",
        "principal_component_analysis": "Principal Component Analysis (PCA)",
        "temporal_trends_patterns": "Temporal trends and patterns",
        "correlations_between_sources": "Correlations between data sources",
        "actionable_executive_insights": "Actionable executive insights",
        "analysis_information": "Analysis Information",
        "ai_model": "AI Model:",
        "response_time": "Response Time:",
        "data_points": "Data Points:",
        "generation_date": "Generation Date:",
        "previous_accesses": "Previous Accesses:",
        "depth": "Depth:",
        "executive_summary": "Executive Summary",
        "principal_findings": "Key Findings",
        "heatmap_analysis": "Heatmap Analysis",
    },
}

# Tool name translations (Spanish to English)
TOOL_TRANSLATIONS = {
    "es": {
        "Alianzas y Capital de Riesgo": "Alianzas y Capital de Riesgo",
        "Benchmarking": "Benchmarking",
        "Calidad Total": "Calidad Total",
        "Competencias Centrales": "Competencias Centrales",
        "Cuadro de Mando Integral": "Cuadro de Mando Integral",
        "Estrategias de Crecimiento": "Estrategias de Crecimiento",
        "Experiencia del Cliente": "Experiencia del Cliente",
        "Fusiones y Adquisiciones": "Fusiones y Adquisiciones",
        "Gestión de Costos": "Gestión de Costos",
        "Gestión de la Cadena de Suministro": "Gestión de la Cadena de Suministro",
        "Gestión del Cambio": "Gestión del Cambio",
        "Gestión del Conocimiento": "Gestión del Conocimiento",
        "Innovación Colaborativa": "Innovación Colaborativa",
        "Lealtad del Cliente": "Lealtad del Cliente",
        "Optimización de Precios": "Optimización de Precios",
        "Outsourcing": "Outsourcing",
        "Planificación Estratégica": "Planificación Estratégica",
        "Planificación de Escenarios": "Planificación de Escenarios",
        "Presupuesto Base Cero": "Presupuesto Base Cero",
        "Propósito y Visión": "Propósito y Visión",
        "Reingeniería de Procesos": "Reingeniería de Procesos",
        "Segmentación de Clientes": "Segmentación de Clientes",
        "Talento y Compromiso": "Talento y Compromiso",
    },
    "en": {
        "Alianzas y Capital de Riesgo": "Alliances and Venture Capital",
        "Benchmarking": "Benchmarking",
        "Calidad Total": "Total Quality",
        "Competencias Centrales": "Core Competencies",
        "Cuadro de Mando Integral": "Balanced Scorecard",
        "Estrategias de Crecimiento": "Growth Strategies",
        "Experiencia del Cliente": "Customer Experience",
        "Fusiones y Adquisiciones": "Mergers and Acquisitions",
        "Gestión de Costos": "Cost Management",
        "Gestión de la Cadena de Suministro": "Supply Chain Management",
        "Gestión del Cambio": "Change Management",
        "Gestión del Conocimiento": "Knowledge Management",
        "Innovación Colaborativa": "Collaborative Innovation",
        "Lealtad del Cliente": "Customer Loyalty",
        "Optimización de Precios": "Price Optimization",
        "Outsourcing": "Outsourcing",
        "Planificación Estratégica": "Strategic Planning",
        "Planificación de Escenarios": "Scenario Planning",
        "Presupuesto Base Cero": "Zero-Based Budgeting",
        "Propósito y Visión": "Purpose and Vision",
        "Reingeniería de Procesos": "Business Process Reengineering",
        "Segmentación de Clientes": "Customer Segmentation",
        "Talento y Compromiso": "Talent and Commitment",
    },
}


def get_text(key, language="es", **kwargs):
    """
    Get translated text for a given key and language.

    Args:
        key (str): Translation key
        language (str): Language code ('es' or 'en')
        **kwargs: Format string arguments

    Returns:
        str: Translated text
    """
    if language not in TRANSLATIONS:
        language = "es"  # Fallback to Spanish

    translation = TRANSLATIONS[language].get(key, key)  # Fallback to key if not found

    if kwargs:
        try:
            translation = translation.format(**kwargs)
        except (KeyError, ValueError):
            pass  # Return unformatted if formatting fails

    return translation


def get_tool_name(tool_key, language="es"):
    """
    Get translated tool name.

    Args:
        tool_key (str): Original tool name key
        language (str): Language code ('es' or 'en')

    Returns:
        str: Translated tool name
    """
    if language not in TOOL_TRANSLATIONS:
        language = "es"

    return TOOL_TRANSLATIONS[language].get(tool_key, tool_key)


def get_available_languages():
    """Get list of available language codes."""
    return list(TRANSLATIONS.keys())


def get_language_name(language_code):
    """Get human-readable language name."""
    names = {"es": "Español", "en": "English"}
    return names.get(language_code, language_code)


def translate_database_content(text, language="es"):
    """
    Translate database content that contains Spanish text.
    This handles common patterns found in the database notes.

    Args:
        text (str): The text from database to translate
        language (str): Target language code

    Returns:
        str: Translated text
    """
    if not text or language == "es":
        return text

    # Common translation patterns for database content
    translations = {
        # Source notes patterns
        "Descriptores lógicos:": "Logical Descriptors:",
        "Parámetros de búsqueda:": "Search Parameters:",
        "Parámetros de Insumos:": "Input Parameters:",
        "cobertura global": "global coverage",
        "marco temporal": "temporal framework",
        "categorización amplia": "broad categorization",
        "tipo de búsqueda": "search type",
        "Índice Relativo:": "Relative Index:",
        "Los datos se normalizan en un índice relativo": "Data is normalized into a relative index",
        "mediante la fórmula:": "using the formula:",
        "Índice relativo = (Volumen de búsqueda del término / Volumen total de búsquedas) x 100": "Relative Index = (Search volume of the term / Total search volume) x 100",
        "mitigando sesgos por heterogeneidad en volúmenes de búsqueda entre regiones y periodos.": "mitigating biases due to heterogeneity in search volumes between regions and periods.",
        "Metodología:": "Methodology:",
        "La métrica es comparativa, no absoluta,": "The metric is comparative, not absolute,",
        "basada en muestreo probabilístico,": "based on probabilistic sampling,",
        "lo que introduce variabilidad estadística.": "which introduces statistical variability.",
        "La interpretación se centra en tendencias de interés relativo,": "The interpretation focuses on relative interest trends,",
        "no en recuentos absolutos.": "not on absolute counts.",
        "Disponibilidad de datos (desde 2004)": "Data availability (since 2004)",
        "permite análisis diacrónico contextualizado en evolución digital": "allows contextualized diachronic analysis in digital evolution",
        "y patrones de búsqueda.": "and search patterns.",
        "Perfil de Usuarios:": "User Profile:",
        "Refleja interés público,": "Reflects public interest,",
        "popularidad de búsqueda": "search popularity",
        "y tendencias emergentes en tiempo real": "and emerging trends in real time",
        "en un perfil de usuarios heterogéneos:": "in a heterogeneous user profile:",
        "investigadores,": "researchers,",
        "periodistas,": "journalists,",
        "profesionales del marketing,": "marketing professionals,",
        "empresarios": "entrepreneurs",
        "y usuarios generales.": "and general users.",
        "Limitaciones:": "Limitations:",
        "No hay correlación directa entre interés en búsquedas": "There is no direct correlation between search interest",
        "e implementación efectiva en organizaciones.": "and effective implementation in organizations.",
        "La evolución terminológica puede afectar": "Terminological evolution may affect",
        "la coherencia longitudinal": "longitudinal coherence",
        # Bain Survey specific translations
        "Extracción de datos:": "Data Extraction:",
        "Encuesta de Herramientas Gerenciales de Bain & Company (Darrell Rigby)": "Bain & Company Management Tools Survey (Darrell Rigby)",
        "perfil de encuestados:": "respondent profile:",
        "CEOs (Directores Ejecutivos)": "CEOs (Chief Executive Officers)",
        "CFOs (Directores Financieros)": "CFOs (Chief Financial Officers)",
        "COOs (Directores de Operaciones)": "COOs (Chief Operating Officers)",
        "y otros líderes senior": "and other senior leaders",
        "Encuesta online": "Online survey",
        "cuestionarios estructurados": "structured questionnaires",
        "muestreo probabilístico y estratificado": "probabilistic and stratified sampling",
        "análisis estadístico": "statistical analysis",
        "Año/#Encuestados:": "Year/#Respondents:",
        "Índice de Satisfacción:": "Satisfaction Index:",
        "La métrica se calcula como:": "The metric is calculated as:",
        "Índice de Satisfacción = Promedio de las puntuaciones de satisfacción reportadas por ejecutivos (escala 0-5)": "Satisfaction Index = Average of satisfaction scores reported by executives (scale 0-5)",
        "Refleja la percepción promedio de los ejecutivos sobre la utilidad e impacto de la herramienta en su ecosistema gerencial": "Reflects the average perception of executives about the utility and impact of the tool in their management ecosystem",
        "donde una puntuación más alta indica mayor satisfacción": "where a higher score indicates greater satisfaction",
        "Directivos de alto nivel": "Senior executives",
        "consultores estratégicos": "strategic consultants",
        "profesionales de la gestión": "management professionals",
        "interesados en la implementación y adopción de": "interested in the implementation and adoption of",
        "metodologías de gestión": "management methodologies",
        "con un enfoque en la practicidad y el uso real en el campo empresarial": "with a focus on practicality and real use in the business field",
        "buscando insights sobre las tendencias de la práctica gerencial": "seeking insights on management practice trends",
        "Además,": "Additionally,",
        "especialistas en": "specialists in",
        "que buscan": "who seek",
        "El índice de satisfacción es subjetivo": "The satisfaction index is subjective",
        "y puede estar influenciado por el sesgo de deseabilidad social y autoinforme": "and may be influenced by social desirability bias and self-report",
        "la interpretación puede variar entre los encuestados": "interpretation may vary among respondents",
        "la terminología puede haber evolucionado y afectar la consistencia longitudinal": "terminology may have evolved and affect longitudinal consistency",
        "y la métrica no mide resultados objetivos ni impacto real": "and the metric does not measure objective results or real impact",
        "Fuente:": "Source:",
        # Bain Usability specific translations
        "Indicador de Usabilidad:": "Usability Indicator:",
        "Indicador de Usabilidad = (Número de ejecutivos que reportan uso de la herramienta en el año de la encuesta / Número total de ejecutivos encuestados en ese año) × 100": "Usability Indicator = (Number of executives reporting use of the tool in the survey year / Total number of executives surveyed in that year) × 100",
        "Refleja el porcentaje de ejecutivos que indicaron haber utilizado la herramienta de gestión en su organización durante el periodo previo al año de la encuesta": "Reflects the percentage of executives who indicated having used the management tool in their organization during the period prior to the survey year",
        "La variabilidad en el tamaño de la muestra entre los años puede afectar la comparabilidad": "Variability in sample size between years may affect comparability",
        "el sesgo de selección y autoinforme puede influir en las respuestas": "selection and self-report bias may influence responses",
        "y la medición del uso es un indicador relativo, no absoluto, de la efectividad": "and usage measurement is a relative, not absolute, indicator of effectiveness",
        # Crossref specific translations
        "campos de búsqueda:": "search fields:",
        '"Título" y "Resumen (Abstract)"': '"Title" and "Abstract"',
        "La métrica es el número de resultados que coinciden con los descriptores en los metadatos de CrossRef": "The metric is the number of results matching the descriptors in CrossRef metadata",
        "Refleja el volumen de publicaciones académicas (artículos, libros, conferencias, etc.) indexadas": "Reflects the volume of indexed academic publications (articles, books, conferences, etc.)",
        "La búsqueda en metadatos de CrossRef usa operadores booleanos": "CrossRef metadata search uses Boolean operators",
        "Interpretación centrada en el volumen de publicaciones": "Interpretation focused on publication volume",
        "Proporciona una medida cuantitativa del interés académico y las investigaciones publicadas": "Provides a quantitative measure of academic interest and published research",
        "Refleja el interés académico a través de publicaciones revisadas por pares y arbitradas, e indexadas": "Reflects academic interest through peer-reviewed and arbitrated indexed publications",
        "Usuarios típicos:": "Typical users:",
        "estudiantes": "students",
        "Dependencia de la exhaustividad y precisión de la indexación de CrossRef": "Dependence on the completeness and accuracy of CrossRef indexing",
        "Solo refleja volumen, no calidad, relevancia, impacto o citaciones": "Only reflects volume, not quality, relevance, impact or citations",
        "Descriptores lógicos pueden introducir sesgos": "Logical descriptors may introduce biases",
        "Cobertura limitada: no incluye todas las publicaciones académicas, solo su indexado": "Limited coverage: does not include all academic publications, only their indexing",
        "Proporciona DOI (Digital Object Identifier) y metadatos básicos": "Provides DOI (Digital Object Identifier) and basic metadata",
        "excluyendo datos bibliométricos adicionales": "excluding additional bibliometric data",
        # General patterns
        "benchmarking": "benchmarking",
        "+": "+",
        "web": "web",
        "01/2004-01/2025": "01/2004-01/2025",
        "2004": "2004",
        "2025": "2025",
        "1950": "1950",
        "95%": "95%",
        "N/A": "N/A",
        # Database source names (translated)
        "bain_usabilidad_translated": "Bain - Usability",
        "bain_satisfacción_translated": "Bain - Satisfaction",
    }

    # First apply general translations
    translated_text = text
    for spanish, english in translations.items():
        translated_text = translated_text.replace(spanish, english)

    # Then apply management tool specific translations
    translated_text = translate_management_tool_notes(translated_text, language)

    return translated_text


def translate_management_tool_notes(text, language="es"):
    """
    Translate management tool specific notes that contain Spanish text.
    This handles tool-specific terminology found in the database notes.

    Args:
        text (str): The text from database to translate
        language (str): Target language code

    Returns:
        str: Translated text
    """
    if not text or language == "es":
        return text

    # Management tool specific translations
    tool_translations = {
        # Tool names
        "Reingeniería de Procesos": "Business Process Reengineering",
        "Gestión de la Cadena de Suministro": "Supply Chain Management",
        "Planificación de Escenarios": "Scenario Planning",
        "Planificación Estratégica": "Strategic Planning",
        "Experiencia del Cliente": "Customer Experience Management",
        "Calidad Total": "Total Quality Management",
        "Propósito y Visión": "Mission and Vision",
        "Benchmarking": "Benchmarking",
        "Competencias Centrales": "Core Competencies",
        "Cuadro de Mando Integral": "Balanced Scorecard",
        "Alianzas y Capital de Riesgo": "Strategic Alliances and Venture Capital",
        "Outsourcing": "Outsourcing",
        "Segmentación de Clientes": "Customer Segmentation",
        "Fusiones y Adquisiciones": "Mergers and Acquisitions",
        "Gestión de Costos": "Cost Management",
        "Presupuesto Base Cero": "Zero-Based Budgeting",
        "Estrategias de Crecimiento": "Growth Strategies",
        "Gestión del Conocimiento": "Knowledge Management",
        "Gestión del Cambio": "Change Management",
        "Optimización de Precios": "Price Optimization",
        "Lealtad del Cliente": "Customer Loyalty",
        "Innovación Colaborativa": "Collaborative Innovation",
        "Talento y Compromiso": "Talent and Engagement",
        # Common phrases in tool descriptions
        "REINGENIERÍA DE PROCESOS:": "BUSINESS PROCESS REENGINEERING:",
        "GESTIÓN DE LA CADENA DE SUMINISTRO:": "SUPPLY CHAIN MANAGEMENT:",
        "PLANIFICACIÓN DE ESCENARIOS:": "SCENARIO PLANNING:",
        "PLANIFICACIÓN ESTRATÉGICA DINÁMICA:": "DYNAMIC STRATEGIC PLANNING:",
        "GESTIÓN DE LA EXPERIENCIA DEL CLIENTE:": "CUSTOMER EXPERIENCE MANAGEMENT:",
        "GESTIÓN DE LA CALIDAD TOTAL:": "TOTAL QUALITY MANAGEMENT:",
        "PROPÓSITO, MISIÓN Y VISIÓN:": "PURPOSE, MISSION AND VISION:",
        "BENCHMARKING:": "BENCHMARKING:",
        "COMPETENCIAS CENTRALES:": "CORE COMPETENCIES:",
        "CUADRO DE MANDO INTEGRAL:": "BALANCED SCORECARD:",
        "ALIANZA ESTRATÉGICA Y CAPITAL DE RIESGO:": "STRATEGIC ALLIANCE AND VENTURE CAPITAL:",
        "OUTSOURCING:": "OUTSOURCING:",
        "SEGMENTACIÓN DE CLIENTES:": "CUSTOMER SEGMENTATION:",
        "FUSIONES Y ADQUISICIONES:": "MERGERS AND ACQUISITIONS:",
        "ASIGNACIÓN Y GESTIÓN DE COSTOS:": "COST ALLOCATION AND MANAGEMENT:",
        "PRESUPUESTO BASE CERO:": "ZERO-BASED BUDGETING:",
        "ESTRATEGIAS DE CRECIMIENTO:": "GROWTH STRATEGIES:",
        "GESTIÓN DEL CONOCIMIENTO:": "KNOWLEDGE MANAGEMENT:",
        "GESTIÓN DEL CAMBIO:": "CHANGE MANAGEMENT:",
        "OPTIMIZACIÓN DE PRECIOS:": "PRICE OPTIMIZATION:",
        "GESTIÓN DE LA LEALTAD DEL CLIENTE:": "CUSTOMER LOYALTY MANAGEMENT:",
        "GESTIÓN DE LA INNOVACIÓN COLABORATIVA:": "COLLABORATIVE INNOVATION MANAGEMENT:",
        "GESTIÓN DEL TALENTO Y COMPROMISO DE EMPLEADOS:": "TALENT AND EMPLOYEE ENGAGEMENT MANAGEMENT:",
        # Specialized terms
        "herramientas de planificación logística": "logistics planning tools",
        "herramientas de análisis estratégico": "strategic analysis tools",
        "sistemas de gestión de calidad": "quality management systems",
        "herramientas de direccionamiento estratégico": "strategic direction tools",
        "herramientas de análisis comparativo": "comparative analysis tools",
        "herramientas de desarrollo estratégico": "strategic development tools",
        "sistemas de gestión del rendimiento": "performance management systems",
        "herramientas para la expansión y diversificación": "expansion and diversification tools",
        "herramientas para optimizar operaciones y reducir costos": "tools to optimize operations and reduce costs",
        "herramientas de análisis de mercado": "market analysis tools",
        "herramientas para la expansión y crecimiento corporativo": "corporate expansion and growth tools",
        "herramientas para gestionar y asignar costos": "tools to manage and allocate costs",
        "herramientas de gestión de presupuesto": "budget management tools",
        "herramientas para la expansión del negocio": "business expansion tools",
        "herramientas para compartir información y gestionar el conocimiento": "tools to share information and manage knowledge",
        "herramientas para facilitar la adopción de cambios": "tools to facilitate change adoption",
        "herramientas para mejorar la definición de precios y tarifas": "tools to improve price and rate definition",
        "herramientas para mejorar la retención y la fidelización de clientes": "tools to improve customer retention and loyalty",
        "metodologías de gestión de innovación": "innovation management methodologies",
        "herramientas para el desarrollo y compromiso de los empleados": "tools for employee development and engagement",
    }

    translated_text = text
    for spanish, english in tool_translations.items():
        translated_text = translated_text.replace(spanish, english)

    return translated_text


def translate_source_name(source_name, language="es"):
    """Translate source names for display in charts and tables"""
    if language == "es":
        return source_name

    # Translation mapping for source names
    source_translations = {
        "Bain - Usabilidad": "Bain - Usability",
        "Bain Usabilidad": "Bain Usability",
        "Bain - Satisfacción": "Bain - Satisfaction",
        "Bain Satisfacción": "Bain Satisfaction",
        "BAIN_Ind_Usabilidad": "Bain - Usability",
        "BAIN_Ind_Satisfacción": "Bain - Satisfaction",
    }

    return source_translations.get(source_name, source_name)


# DOCKER_FIX: Enhanced translation for Docker environment
def enhanced_translate_source_name(source_name, language="es"):
    """
    Enhanced translation function that handles more variations and provides fallbacks.
    This addresses Docker-specific issues with source name translation.

    Args:
        source_name: Source name to translate
        language: Target language ('es' or 'en')

    Returns:
        Translated source name
    """
    # Try the standard translation first
    try:
        return translate_source_name(source_name, language)
    except:
        pass

    # Fallback translations for Docker environment
    if language == "es":
        # English to Spanish
        fallback_translations = {
            "Bain - Usability": "Bain - Usabilidad",
            "Bain Usability": "Bain - Usabilidad",
            "Bain - Satisfaction": "Bain - Satisfacción",
            "Bain Satisfaction": "Bain - Satisfacción",
            "Google Books": "Google Books Ngrams",
            "Crossref": "Crossref.org",
        }
    else:
        # Spanish to English
        fallback_translations = {
            "Bain - Usabilidad": "Bain - Usability",
            "Bain - Satisfacción": "Bain - Satisfaction",
            "Google Books Ngrams": "Google Books",
            "Crossref.org": "Crossref",
        }

    return fallback_translations.get(source_name, source_name)
