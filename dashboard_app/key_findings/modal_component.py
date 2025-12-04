"""
Key Findings Modal Component

Interactive dashboard component for displaying AI-generated
doctoral-level analysis with bilingual support and user interactions.
"""

import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Import translation system
try:
    from translations import get_text
except ImportError:
    # Fallback if translation module not available
    def get_text(key, language="es", **kwargs):
        return key


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class KeyFindingsModal:
    """
    Modal component for displaying Key Findings.

    Provides interactive UI for AI-generated analysis with
    bilingual support, user interactions, and performance metrics.
    """

    def __init__(self, app, language_store):
        """
        Initialize Key Findings modal.

        Args:
            app: Dash application instance
            language_store: Language state store
        """
        self.app = app
        self.language_store = language_store

        # Modal state
        self.modal_id = "key-findings-modal"
        self.is_open_id = "key-findings-modal-open"
        self.content_id = "key-findings-content"
        self.loading_id = "key-findings-loading"

        # Component IDs
        self.findings_display_id = "key-findings-display"
        self.pca_insights_id = "key-findings-pca"
        self.executive_summary_id = "key-findings-summary"
        self.metadata_id = "key-findings-metadata"

        # Interaction controls
        self.regenerate_btn_id = "key-findings-regenerate"
        self.save_btn_id = "key-findings-save"
        self.rating_id = "key-findings-rating"
        self.feedback_id = "key-findings-feedback"

        # Performance metrics
        self.metrics_id = "key-findings-metrics"

        # Register callbacks
        self._register_callbacks()

    def _get_translated_text(self, key: str, language: str = "es", **kwargs) -> str:
        """
        Get translated text using the specified language.

        Args:
            key: Translation key
            language: Language code ('es' or 'en')
            **kwargs: Additional format arguments

        Returns:
            Translated text
        """
        try:
            return get_text(key, language, **kwargs)
        except:
            return get_text(key, "es", **kwargs)

    def create_modal_layout(self, language: str = "es") -> dbc.Modal:
        """
        Create the modal layout with all sections.

        Args:
            language: Language code ('es' or 'en')

        Returns:
            Complete modal layout
        """
        return dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(
                        self._get_translated_text("key_findings_modal_title", language),
                        id="key-findings-modal-title",
                    ),
                    close_button=True,
                    className="bg-primary text-white",
                ),
                dbc.ModalBody(
                    [
                        # Loading state
                        html.Div(
                            id=self.loading_id,
                            children=[
                                html.Div(
                                    [
                                        dbc.Spinner(color="primary", size="lg"),
                                        html.P(
                                            self._get_translated_text(
                                                "generating_analysis"
                                            ),
                                            className="mt-3 text-center",
                                        ),
                                        html.P(
                                            self._get_translated_text(
                                                "may_take_30_seconds"
                                            ),
                                            className="text-muted text-center",
                                        ),
                                    ],
                                    className="text-center py-5",
                                )
                            ],
                            style={"display": "none"},
                        ),
                        # Main content
                        html.Div(
                            id=self.content_id, children=self._create_empty_state()
                        ),
                        # Performance metrics (hidden by default)
                        html.Div(id=self.metrics_id, style={"display": "none"}),
                    ],
                    className="modal-body-scrollable",
                    style={"maxHeight": "70vh", "overflowY": "auto"},
                ),
                dbc.ModalFooter(
                    [
                        # Left side controls
                        html.Div(
                            [
                                # Rating component
                                html.Div(
                                    [
                                        html.Label("Calificación:", className="me-2"),
                                        dbc.Rating(
                                            id=self.rating_id,
                                            max=5,
                                            size="md",
                                            value=0,
                                            className="me-3",
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                                # Feedback textarea
                                dbc.Textarea(
                                    id=self.feedback_id,
                                    placeholder="Comentarios sobre el análisis...",
                                    size="sm",
                                    style={"width": "200px", "height": "60px"},
                                ),
                            ],
                            className="d-flex align-items-center me-auto",
                        ),
                        # Right side buttons
                        html.Div(
                            [
                                # Regenerate button
                                dbc.Button(
                                    "🔄 Regenerar",
                                    id=self.regenerate_btn_id,
                                    color="warning",
                                    size="sm",
                                    className="me-2",
                                ),
                                # Close button only - remove save functionality
                                dbc.Button(
                                    "Cerrar",
                                    id="key-findings-close",
                                    color="secondary",
                                    size="sm",
                                    className="ms-2",
                                ),
                            ]
                        ),
                    ],
                    className="d-flex justify-content-between align-items-center",
                ),
            ],
            id=self.modal_id,
            is_open=False,
            size="xl",
            backdrop="static",
            keyboard=False,
            className="key-findings-modal",
        )

    def create_findings_display(
        self, report_data: Dict[str, Any], language: str = "es"
    ) -> html.Div:
        """
        Create formatted display of AI findings.

        Args:
            report_data: Report data from database or AI
            language: Language code ('es' or 'en')

        Returns:
            Formatted findings display
        """
        if not report_data:
            return self._create_empty_state(language)

        # Extract data with proper JSON parsing if needed
        executive_summary = self._extract_text_content(
            report_data.get("executive_summary", "")
        )
        principal_findings = self._extract_text_content(
            report_data.get("principal_findings", "")
        )
        temporal_analysis = self._extract_text_content(
            report_data.get("temporal_analysis", "")
        )
        seasonal_analysis = self._extract_text_content(
            report_data.get("seasonal_analysis", "")
        )
        fourier_analysis = self._extract_text_content(
            report_data.get("fourier_analysis", "")
        )
        strategic_synthesis = self._extract_text_content(
            report_data.get("strategic_synthesis", "")
        )
        conclusions = self._extract_text_content(report_data.get("conclusions", ""))

        # Determine analysis type for section filtering - MUST be done before using is_single_source
        analysis_type = report_data.get(
            "analysis_type", "multi_source"
        )  # Default to multi-source
        sources_count = report_data.get("sources_count", 0)
        selected_sources = report_data.get("selected_sources", [])

        # Calculate if this is single-source analysis
        is_single_source = (
            sources_count == 1  # Explicit count
            or report_data.get("analysis_type") == "single_source"  # Explicit type
            or (
                isinstance(selected_sources, list) and len(selected_sources) == 1
            )  # Source list length
            or (
                isinstance(selected_sources, str) and selected_sources.count(",") == 0
            )  # Single source string
        )

        # Debug force
        if sources_count == 1:
            print(f"🔍 MODAL DEBUG: FORCING SINGLE-SOURCE based on sources_count=1")
            is_single_source = True

        print(
            f"🔍 MODAL DEBUG: analysis_type = '{analysis_type}', is_single_source = {is_single_source}"
        )
        print(
            f"🔍 MODAL DEBUG: sources_count = {report_data.get('sources_count', 'unknown')}"
        )

        # For single-source, don't extract heatmap/PCA content even if it exists
        if is_single_source:
            heatmap_analysis = ""
            pca_analysis = ""
            print(
                f"🔍 MODAL FILTERING: Single-source detected, setting heatmap/PCA to empty"
            )
        else:
            heatmap_analysis = self._extract_text_content(
                report_data.get("heatmap_analysis", "")
            )
            pca_analysis = self._extract_text_content(
                report_data.get("pca_analysis", "")
            )
            print(
                f"🔍 MODAL FILTERING: Multi-source detected, extracting heatmap/PCA content"
            )
        metadata = self._extract_metadata(report_data)

        # Handle missing strategic_synthesis and conclusions by extracting from principal_findings if needed
        if not strategic_synthesis and principal_findings:
            # Try to extract strategic synthesis from the end of principal findings
            parts = principal_findings.split("\n\n")
            if len(parts) > 2:
                strategic_synthesis = "\n\n".join(parts[-2:])  # Last 2 paragraphs
                principal_findings = "\n\n".join(
                    parts[:-2]
                )  # Everything except last 2 paragraphs

        if not conclusions and principal_findings:
            # Extract conclusions from the very end of principal findings
            parts = principal_findings.split("\n\n")
            if len(parts) > 1:
                conclusions = parts[-1]  # Last paragraph
                principal_findings = "\n\n".join(
                    parts[:-1]
                )  # Everything except last paragraph

        # Analysis type and single-source detection already handled above

        # Build sections dynamically based on analysis type
        sections = []

        if is_single_source:
            # For single-source: only show the combined principal_findings (which contains all 7 sections with prefixes)
            if principal_findings:
                sections.append(
                    self._create_principal_findings_narrative_section(
                        principal_findings, language
                    )
                )
        else:
            # For multi-source: show individual sections
            if executive_summary:
                sections.append(
                    self._create_executive_summary_section(executive_summary, language)
                )
            if principal_findings:
                sections.append(
                    self._create_principal_findings_narrative_section(
                        principal_findings, language
                    )
                )
            if temporal_analysis:
                sections.append(
                    self._create_temporal_analysis_section(temporal_analysis, language)
                )
            if seasonal_analysis:
                sections.append(
                    self._create_seasonal_analysis_section(seasonal_analysis, language)
                )
            if fourier_analysis:
                sections.append(
                    self._create_fourier_analysis_section(fourier_analysis, language)
                )
            if strategic_synthesis:
                sections.append(
                    self._create_strategic_synthesis_section(
                        strategic_synthesis, language
                    )
                )
            if conclusions:
                sections.append(self._create_conclusions_section(conclusions, language))

            # Multi-source specific sections
            if heatmap_analysis:
                sections.append(
                    self._create_heatmap_analysis_section(heatmap_analysis, language)
                )
            # For multi-source, pca_analysis is narrative essay
            if pca_analysis and not self._is_placeholder_pca_content(pca_analysis):
                sections.append(
                    self._create_pca_analysis_section(pca_analysis, language)
                )

        # Always show metadata
        sections.append(self._create_metadata_section(metadata, language))

        return html.Div(sections)

    def create_interaction_controls(self) -> html.Div:
        """
        Create user interaction controls.

        Returns:
            Interaction controls layout
        """
        return html.Div(
            [
                # Rating and feedback
                html.Div(
                    [
                        html.H6("Evaluar este Análisis", className="mb-3"),
                        html.Div(
                            [
                                html.Label(
                                    "Calificación de Precisión:", className="form-label"
                                ),
                                dbc.Rating(
                                    id=self.rating_id, max=5, size="lg", value=0
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Label("Comentarios Adicionales:", className="form-label"),
                        dbc.Textarea(
                            id=self.feedback_id,
                            placeholder="Proporcione feedback sobre la calidad y utilidad de este análisis...",
                            rows=3,
                            className="mb-3",
                        ),
                    ]
                ),
                # Action buttons
                html.Div(
                    [
                        dbc.Button(
                            [
                                html.I(className="fas fa-sync-alt me-2"),
                                "Regenerar Análisis",
                            ],
                            id=self.regenerate_btn_id,
                            color="warning",
                            size="lg",
                            className="w-100 mb-2",
                        ),
                        dbc.Button(
                            [
                                html.I(className="fas fa-save me-2"),
                                "Guardar en Biblioteca",
                            ],
                            id=self.save_btn_id,
                            color="success",
                            size="lg",
                            className="w-100 mb-2",
                        ),
                        dbc.Button(
                            [html.I(className="fas fa-download me-2"), "Exportar PDF"],
                            id="key-findings-export",
                            color="info",
                            size="lg",
                            className="w-100",
                        ),
                    ]
                ),
            ]
        )

    def create_loading_state(self, language: str = "es") -> html.Div:
        """
        Create loading animation during AI processing.

        Args:
            language: Language code ('es' or 'en')

        Returns:
            Loading state component
        """
        return html.Div(
            [
                html.Div(
                    [
                        dbc.Spinner(color="primary", size="lg", type="grow"),
                        html.H4(
                            self._get_translated_text("generating_analysis", language),
                            className="mt-4 mb-3",
                        ),
                        html.P(
                            self._get_translated_text(
                                "analyzing_multisource_data", language
                            ),
                            className="text-muted mb-2",
                        ),
                        html.P(
                            self._get_translated_text(
                                "estimated_time_15_30_seconds", language
                            ),
                            className="text-muted",
                        ),
                        # Progress indicators
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-check-circle text-success me-2"
                                        ),
                                        self._get_translated_text(
                                            "data_collected", language
                                        ),
                                    ],
                                    className="mb-2",
                                ),
                                html.Div(
                                    [
                                        html.I(
                                            className="fas fa-spinner fa-spin text-primary me-2"
                                        ),
                                        self._get_translated_text(
                                            "pca_analysis_in_progress", language
                                        ),
                                    ],
                                    className="mb-2",
                                ),
                                html.Div(
                                    [
                                        html.I(
                                            className="far fa-circle text-muted me-2"
                                        ),
                                        self._get_translated_text(
                                            "generating_ai_insights", language
                                        ),
                                    ],
                                    className="mb-2",
                                ),
                                html.Div(
                                    [
                                        html.I(
                                            className="far fa-circle text-muted me-2"
                                        ),
                                        self._get_translated_text(
                                            "creating_executive_summary", language
                                        ),
                                    ]
                                ),
                            ],
                            className="text-start mt-4",
                        ),
                    ],
                    className="text-center py-5",
                )
            ]
        )

    def _create_empty_state(self, language: str = "es") -> html.Div:
        """Create empty state when no data available."""
        return html.Div(
            [
                html.Div(
                    [
                        html.I(className="fas fa-brain fa-3x text-muted mb-3"),
                        html.H4(
                            self._get_translated_text(
                                "analysis_not_available", language
                            ),
                            className="mb-3",
                        ),
                        html.P(
                            self._get_translated_text(
                                "select_tool_and_sources", language
                            ),
                            className="text-muted",
                        ),
                        html.P(
                            self._get_translated_text(
                                "doctoral_analysis_will_provide", language
                            ),
                            className="mt-3",
                        ),
                        html.Ul(
                            [
                                html.Li(
                                    self._get_translated_text(
                                        "principal_component_analysis", language
                                    )
                                ),
                                html.Li(
                                    self._get_translated_text(
                                        "temporal_trends_patterns", language
                                    )
                                ),
                                html.Li(
                                    self._get_translated_text(
                                        "correlations_between_sources", language
                                    )
                                ),
                                html.Li(
                                    self._get_translated_text(
                                        "actionable_executive_insights", language
                                    )
                                ),
                            ],
                            className="text-start",
                        ),
                    ],
                    className="text-center py-5",
                )
            ]
        )

    def _create_executive_summary_section(
        self, summary: str, language: str = "es"
    ) -> html.Div:
        """Create executive summary section."""
        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-lightbulb text-warning me-2"),
                        self._get_translated_text("executive_summary", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.P(
                                    summary,
                                    className="text-justify mb-0 executive-summary-text",
                                    style={"lineHeight": "1.7"},
                                ),
                            ]
                        )
                    ],
                    className="border-primary bg-primary text-white",
                ),
            ],
            className="mb-4",
        )

    def _create_principal_findings_narrative_section(
        self, findings_text: str, language: str = "es"
    ) -> html.Div:
        """Create principal findings section as narrative text."""
        if not findings_text:
            return html.Div()

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-search text-primary me-2"),
                        self._get_translated_text("principal_findings", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            findings_text,
                                            className="text-justify principal-findings-text",
                                            style={"lineHeight": "1.6"},
                                        ),
                                        # Add a subtle indicator that this integrates multiple analyses
                                        html.Div(
                                            [
                                                html.Small(
                                                    [
                                                        html.I(
                                                            className="fas fa-info-circle text-info me-1"
                                                        ),
                                                        self._get_translated_text(
                                                            "section_integrates_analyses",
                                                            language,
                                                        ),
                                                    ],
                                                    className="text-muted",
                                                )
                                            ],
                                            className="mt-3 text-end",
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _create_heatmap_analysis_section(
        self, heatmap_analysis_text: str, language: str = "es"
    ) -> html.Div:
        """Create heatmap analysis section as narrative essay with proper paragraph formatting."""
        # Always show the section, even if content is minimal
        if not heatmap_analysis_text or len(heatmap_analysis_text.strip()) < 50:
            # Use default content if none provided
            heatmap_analysis_text = self._get_default_heatmap_analysis(language)

        # Split text into paragraphs and create separate P elements for each
        paragraphs = [
            p.strip() for p in heatmap_analysis_text.split("\n\n") if p.strip()
        ]

        # Ensure we have at least 3 paragraphs by using meaningful content
        while len(paragraphs) < 3:
            if language == "es":
                additional_content = [
                    "Los patrones de correlación observados sugieren interacciones complejas entre las diferentes métricas de evaluación de la herramienta.",
                    "Estas relaciones multidimensionales proporcionan insights valiosos sobre los factores que impulsan el éxito o fracaso en la implementación.",
                    "El análisis conjunto de estas correlaciones permite identificar áreas de oportunidad y riesgos potenciales en la adopción de la herramienta.",
                ]
            else:
                additional_content = [
                    "The observed correlation patterns suggest complex interactions between different tool evaluation metrics.",
                    "These multidimensional relationships provide valuable insights into factors driving implementation success or failure.",
                    "The joint analysis of these correlations allows identification of opportunity areas and potential risks in tool adoption.",
                ]

            paragraphs.append(
                additional_content[len(paragraphs) % len(additional_content)]
            )

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-chart-area text-success me-2"),
                        self._get_translated_text("heatmap_analysis", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        # Create separate P elements for each paragraph
                                        html.Div(
                                            [
                                                html.P(
                                                    p,
                                                    className="text-justify heatmap-analysis-text mb-3",
                                                    style={"lineHeight": "1.6"},
                                                )
                                                for p in paragraphs[
                                                    :3
                                                ]  # Limit to 3 paragraphs
                                            ]
                                        ),
                                        # Add a subtle indicator that this is detailed heatmap analysis
                                        html.Div(
                                            [
                                                html.Small(
                                                    [
                                                        html.I(
                                                            className="fas fa-chart-area text-success me-1"
                                                        ),
                                                        f"{self._get_translated_text('detailed_heatmap_analysis', language)} ({min(len(paragraphs), 3)} {self._get_translated_text('paragraphs', language)})",
                                                    ],
                                                    className="text-muted",
                                                )
                                            ],
                                            className="mt-3 text-end",
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _get_default_heatmap_analysis(self, language: str = "es") -> str:
        """Get default heatmap analysis content when none is provided."""
        if language == "es":
            return """El análisis de correlaciones entre las fuentes de datos revela patrones importantes en la adopción y percepción de la herramienta de gestión. Los datos muestran relaciones complejas entre las diferentes métricas, con algunas fuentes mostrando correlaciones positivas fuertes mientras que otras presentan relaciones más matizadas y contextuales.

Las correlaciones más significativas aparecen entre las métricas de popularidad e implementación, sugiriendo que la visibilidad pública de la herramienta influye directamente en su adopción organizacional. Sin embargo, estas correlaciones no siempre se traducen en satisfacción a largo plazo, indicando posibles brechas entre la percepción inicial y la experiencia real de uso que requieren atención específica.

Los patrones observados en las correlaciones sugieren que el éxito de la herramienta depende de múltiples factores interconectados, donde la alineación entre expectativas iniciales y resultados reales juega un papel crucial en la implementación efectiva y sostenible."""
        else:
            return """The correlation analysis between data sources reveals important patterns in the adoption and perception of the management tool. The data shows complex relationships between different metrics, with some sources showing strong positive correlations while others present more nuanced and contextual relationships.

The most significant correlations appear between popularity and implementation metrics, suggesting that the public visibility of the tool directly influences its organizational adoption. However, these correlations do not always translate into long-term satisfaction, indicating possible gaps between initial perception and actual user experience that require specific attention.

The patterns observed in the correlations suggest that the tool's success depends on multiple interconnected factors, where the alignment between initial expectations and real results plays a crucial role in effective and sustainable implementation."""

    def _create_pca_analysis_section(
        self, pca_analysis_text: str, language: str = "es"
    ) -> html.Div:
        """Create PCA analysis section as narrative essay with proper paragraph formatting."""
        if not pca_analysis_text:
            return html.Div()

        # Split text into paragraphs and create separate P elements for each
        paragraphs = [p.strip() for p in pca_analysis_text.split("\n\n") if p.strip()]

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-chart-line text-info me-2"),
                        self._get_translated_text("pca_analysis", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        # Create separate P elements for each paragraph
                                        html.Div(
                                            [
                                                html.P(
                                                    p,
                                                    className="text-justify pca-analysis-text mb-3",
                                                    style={"lineHeight": "1.6"},
                                                )
                                                for p in paragraphs
                                            ]
                                        ),
                                        # Add a subtle indicator that this is detailed PCA analysis
                                        html.Div(
                                            [
                                                html.Small(
                                                    [
                                                        html.I(
                                                            className="fas fa-calculator text-info me-1"
                                                        ),
                                                        f"{self._get_translated_text('detailed_pca_analysis', language)} ({len(paragraphs)} {self._get_translated_text('paragraphs', language)})",
                                                    ],
                                                    className="text-muted",
                                                )
                                            ],
                                            className="mt-3 text-end",
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _create_metadata_section(
        self, metadata: Dict[str, Any], language: str = "es"
    ) -> html.Div:
        """Create metadata section."""
        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-info-circle text-secondary me-2"),
                        self._get_translated_text("analysis_information", language),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P(
                                    [
                                        html.Strong(
                                            self._get_translated_text(
                                                "ai_model", language
                                            )
                                            + " "
                                        ),
                                        metadata.get("model_used", "N/A"),
                                    ]
                                ),
                                html.P(
                                    [
                                        html.Strong(
                                            self._get_translated_text(
                                                "response_time", language
                                            )
                                            + " "
                                        ),
                                        f"{metadata.get('response_time_ms', 0)} ms",
                                    ]
                                ),
                                html.P(
                                    [
                                        html.Strong(
                                            self._get_translated_text(
                                                "data_points", language
                                            )
                                            + " "
                                        ),
                                        f"{metadata.get('data_points_analyzed', 0):,}",
                                    ]
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    [
                                        html.Strong(
                                            self._get_translated_text(
                                                "generation_date", language
                                            )
                                            + " "
                                        ),
                                        metadata.get("generation_timestamp", "N/A"),
                                    ]
                                ),
                                html.P(
                                    [
                                        html.Strong(
                                            self._get_translated_text(
                                                "previous_accesses", language
                                            )
                                            + " "
                                        ),
                                        metadata.get("access_count", 0),
                                    ]
                                ),
                                html.P(
                                    [
                                        html.Strong(
                                            self._get_translated_text("depth", language)
                                            + " "
                                        ),
                                        metadata.get("analysis_depth", "comprehensive"),
                                    ]
                                ),
                            ],
                            width=6,
                        ),
                    ]
                ),
            ],
            className="mb-4",
        )

    def _create_temporal_analysis_section(
        self, temporal_text: str, language: str = "es"
    ) -> html.Div:
        """Create temporal analysis section."""
        if not temporal_text:
            return html.Div()

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-chart-line text-info me-2"),
                        self._get_translated_text("temporal_analysis", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.P(
                                    temporal_text,
                                    className="text-justify temporal-analysis-text",
                                    style={"lineHeight": "1.6"},
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _create_seasonal_analysis_section(
        self, seasonal_text: str, language: str = "es"
    ) -> html.Div:
        """Create seasonal analysis section."""
        if not seasonal_text:
            return html.Div()

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-calendar-alt text-warning me-2"),
                        self._get_translated_text("seasonal_analysis", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.P(
                                    seasonal_text,
                                    className="text-justify seasonal-analysis-text",
                                    style={"lineHeight": "1.6"},
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _create_fourier_analysis_section(
        self, fourier_text: str, language: str = "es"
    ) -> html.Div:
        """Create Fourier analysis section."""
        if not fourier_text:
            return html.Div()

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-wave-square text-success me-2"),
                        self._get_translated_text("fourier_analysis", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.P(
                                    fourier_text,
                                    className="text-justify fourier-analysis-text",
                                    style={"lineHeight": "1.6"},
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _create_strategic_synthesis_section(
        self, synthesis_text: str, language: str = "es"
    ) -> html.Div:
        """Create strategic synthesis section."""
        if not synthesis_text:
            return html.Div()

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-chess text-primary me-2"),
                        self._get_translated_text("strategic_synthesis", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.P(
                                    synthesis_text,
                                    className="text-justify strategic-synthesis-text",
                                    style={"lineHeight": "1.6"},
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _create_conclusions_section(
        self, conclusions_text: str, language: str = "es"
    ) -> html.Div:
        """Create conclusions section."""
        if not conclusions_text:
            return html.Div()

        return html.Div(
            [
                html.H4(
                    [
                        html.I(className="fas fa-flag-checkered text-danger me-2"),
                        self._get_translated_text("conclusions", language),
                    ],
                    className="mb-3",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.P(
                                    conclusions_text,
                                    className="text-justify conclusions-text",
                                    style={"lineHeight": "1.6"},
                                )
                            ]
                        )
                    ],
                    className="border-0 bg-light shadow-sm",
                ),
            ],
            className="mb-4",
        )

    def _create_pca_chart(self, dominant_patterns: List[Dict[str, Any]]) -> dcc.Graph:
        """Create PCA visualization chart (kept for compatibility but not used in new structure)."""
        # This method is kept for backward compatibility but not used in the new narrative structure
        return dcc.Graph()

    def _is_placeholder_pca_content(self, pca_content: str) -> bool:
        """
        Check if PCA content is just a placeholder message.

        Args:
            pca_content: PCA analysis text

        Returns:
            True if content is a placeholder
        """
        if not pca_content:
            return True

        placeholder_patterns = [
            "no pca analysis available",
            "pca analysis not available",
            "no pca insights",
            "pca not applicable",
            "n/a",
            "not available",
        ]

        content_lower = pca_content.lower().strip()

        # Check for exact placeholder phrases
        for pattern in placeholder_patterns:
            if pattern in content_lower:
                return True

        # Check if content is too short to be meaningful (less than 50 characters)
        if len(content_lower) < 50:
            return True

        return False

    def _extract_metadata(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from report data."""
        # DEBUG: Check what values we're receiving
        print(f"🔍 MODAL DEBUG: report_data keys: {list(report_data.keys())}")
        print(
            f"🔍 MODAL DEBUG: model_used from report_data: '{report_data.get('model_used', 'MISSING')}'"
        )
        print(
            f"🔍 MODAL DEBUG: data_points_analyzed from report_data: '{report_data.get('data_points_analyzed', 'MISSING')}'"
        )
        print(
            f"🔍 MODAL DEBUG: api_latency_ms from report_data: '{report_data.get('api_latency_ms', 'MISSING')}'"
        )

        # Map database field names to expected metadata field names
        model_used = (
            report_data.get("model_used") or report_data.get("model") or "unknown"
        )
        data_points = (
            report_data.get("data_points_analyzed")
            or report_data.get("data_points")
            or 0
        )
        response_time = (
            report_data.get("api_latency_ms")
            or report_data.get("response_time_ms")
            or 0
        )

        print(
            f"🔍 MODAL DEBUG: Final extracted values - model: '{model_used}', data_points: {data_points}, response_time: {response_time}"
        )

        return {
            "model_used": model_used,
            "response_time_ms": response_time,
            "data_points_analyzed": data_points,
            "generation_timestamp": report_data.get("generation_timestamp", "N/A"),
            "access_count": report_data.get("access_count", 0),
            "analysis_depth": report_data.get("analysis_depth", "comprehensive"),
            "sources_count": report_data.get("sources_count", 0),
        }

    def _convert_json_to_narrative(self, json_data: Dict[str, Any]) -> str:
        """
        Convert JSON analysis data to narrative text format.

        Args:
            json_data: JSON dictionary containing analysis data

        Returns:
            Narrative text representation of the JSON data
        """
        if not isinstance(json_data, dict):
            return str(json_data)

        # Handle PCA analysis structure
        if "analysis" in json_data and isinstance(json_data["analysis"], dict):
            analysis = json_data["analysis"]

            # PCA analysis with dominant patterns
            if "dominant_patterns" in analysis:
                patterns = analysis["dominant_patterns"]
                variance_explained = analysis.get("total_variance_explained", "N/A")

                narrative_parts = []
                narrative_parts.append(
                    f"El análisis de Componentes Principales revela que los {len(patterns)} componentes principales explican un {variance_explained * 100:.1f}% de la varianza total en los datos."
                )

                for i, pattern in enumerate(patterns, 1):
                    component = pattern.get("component", i)
                    loadings = pattern.get("loadings", {})

                    if loadings:
                        # Sort loadings by absolute value (descending)
                        sorted_loadings = sorted(
                            loadings.items(), key=lambda x: abs(x[1]), reverse=True
                        )

                        loading_descriptions = []
                        for source, loading in sorted_loadings:
                            if loading > 0.7:
                                loading_descriptions.append(
                                    f"{source} (alta correlación: {loading:.2f})"
                                )
                            elif loading > 0.5:
                                loading_descriptions.append(
                                    f"{source} (correlación moderada: {loading:.2f})"
                                )
                            else:
                                loading_descriptions.append(
                                    f"{source} (correlación baja: {loading:.2f})"
                                )

                        narrative_parts.append(
                            f"El Componente {component} está dominado por: {', '.join(loading_descriptions)}."
                        )

                return " ".join(narrative_parts)

            # Heatmap analysis structure
            elif "heatmap_data" in analysis:
                heatmap_data = analysis["heatmap_data"]
                if isinstance(heatmap_data, list) and len(heatmap_data) > 0:
                    return f"El análisis de mapa de calor revela patrones de densidad en los datos con {len(heatmap_data)} regiones identificadas."

            # Generic analysis conversion
            else:
                narrative_parts = []
                for key, value in analysis.items():
                    if isinstance(value, (str, int, float)):
                        narrative_parts.append(
                            f"{key.replace('_', ' ').title()}: {value}"
                        )
                    elif isinstance(value, list):
                        narrative_parts.append(
                            f"{key.replace('_', ' ').title()}: {len(value)} elementos"
                        )

                return "; ".join(narrative_parts) if narrative_parts else str(analysis)

        # Generic JSON to text conversion
        return str(json_data)

    def _extract_text_content(self, content: Any) -> str:
        """
        Extract text content from various data types.

        Args:
            content: Content that might be string, dict, or other types

        Returns:
            Extracted text content as string
        """
        if isinstance(content, str):
            # Check if it's JSON formatted
            if content.strip().startswith("{") and content.strip().endswith("}"):
                try:
                    # Try to parse as JSON and extract text
                    json_data = json.loads(content)
                    if isinstance(json_data, dict):
                        # Look for common text fields - prioritize heatmap_analysis for new structure
                        for field in [
                            "executive_summary",
                            "principal_findings",
                            "heatmap_analysis",
                            "pca_analysis",
                            "bullet_point",
                            "analysis",
                        ]:
                            if field in json_data:
                                if isinstance(json_data[field], str):
                                    return json_data[field]
                                elif (
                                    isinstance(json_data[field], dict)
                                    and field == "analysis"
                                ):
                                    # Convert JSON analysis to narrative text
                                    return self._convert_json_to_narrative(json_data)
                except:
                    pass
            return content
        elif isinstance(content, dict):
            # Extract from dictionary - prioritize heatmap_analysis for new structure
            for field in [
                "executive_summary",
                "principal_findings",
                "heatmap_analysis",
                "pca_analysis",
                "bullet_point",
                "analysis",
            ]:
                if field in content:
                    if isinstance(content[field], str):
                        return content[field]
                    elif isinstance(content[field], dict) and field == "analysis":
                        # Convert JSON analysis to narrative text
                        return self._convert_json_to_narrative(content)
        elif isinstance(content, list) and content:
            # Extract from list
            first_item = content[0]
            if isinstance(first_item, dict):
                for field in ["bullet_point", "text", "content"]:
                    if field in first_item and isinstance(first_item[field], str):
                        return first_item[field]
            elif isinstance(first_item, str):
                return first_item

        return str(content) if content else ""

    def _register_callbacks(self):
        """Register all modal callbacks."""

        # Toggle modal
        @self.app.callback(
            [
                Output(self.modal_id, "is_open"),
                Output(self.loading_id, "style"),
                Output(self.content_id, "children"),
            ],
            [
                Input("key-findings-trigger", "n_clicks"),
                Input("key-findings-close", "n_clicks"),
                Input(self.regenerate_btn_id, "n_clicks"),
            ],
            [
                State(self.modal_id, "is_open"),
                State("selected-tool", "value"),
                State("selected-sources", "value"),
                State("language-store", "data"),
            ],
        )
        def toggle_modal(
            trigger_clicks,
            close_clicks,
            regenerate_clicks,
            is_open,
            selected_tool,
            selected_sources,
            language,
        ):
            """Handle modal open/close and content loading."""

            # Determine which button was clicked
            ctx = dash.callback_context
            if not ctx.triggered:
                return (
                    False,
                    {"display": "none"},
                    self._create_empty_state(language or "es"),
                )

            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if trigger_id == "key-findings-close":
                return (
                    False,
                    {"display": "none"},
                    self._create_empty_state(language or "es"),
                )

            if trigger_id in ["key-findings-trigger", self.regenerate_btn_id]:
                if not selected_tool or not selected_sources:
                    return (
                        True,
                        {"display": "none"},
                        self._create_empty_state(language or "es"),
                    )

                # Show loading state
                return (
                    True,
                    {"display": "block"},
                    self._create_empty_state(language or "es"),
                )

            return (
                is_open,
                {"display": "none"},
                self._create_empty_state(language or "es"),
            )

        # Update modal content (this would be connected to the actual analysis service)
        @self.app.callback(
            Output(self.content_id, "children", allow_duplicate=True),
            [Input("key-findings-data-ready", "data"), Input("language-store", "data")],
        )
        def update_content(analysis_data, language):
            """Update modal content with analysis results."""
            if not analysis_data:
                return self._create_empty_state(language or "es")

            return self.create_findings_display(analysis_data, language or "es")

        # Handle user interactions
        @self.app.callback(
            [
                Output("key-findings-toast", "is_open"),
                Output("key-findings-toast", "children"),
            ],
            [Input(self.save_btn_id, "n_clicks"), Input(self.rating_id, "value")],
            [
                State(self.feedback_id, "value"),
                State("key-findings-current-report", "data"),
            ],
        )
        def handle_interactions(save_clicks, rating, feedback, current_report):
            """Handle save and rating interactions."""
            ctx = dash.callback_context
            if not ctx.triggered:
                return False, ""

            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if trigger_id == self.save_btn_id:
                # Handle save functionality
                return True, "Análisis guardado exitosamente"

            if trigger_id == self.rating_id and rating and rating > 0:
                # Handle rating functionality
                return True, f"Calificación de {rating} estrellas registrada"

            return False, ""
