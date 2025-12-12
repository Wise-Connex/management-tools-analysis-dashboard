"""
Refactored Key Findings Callbacks - New Architecture

Simplified callback functions that use the new retrieval + parser architecture.
Provides clean separation of concerns with dedicated services for retrieval and parsing.
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import time
import logging
from typing import Dict, List, Any, Optional

# Import the new services
from dashboard_app.key_findings.retrieval_service import (
    get_key_findings_retrieval_service,
)
from dashboard_app.key_findings.content_parser import get_key_findings_content_parser

# Import utility functions
from fix_source_mapping import map_display_names_to_source_ids
from translations import get_text, get_tool_name
from utils import run_async_in_sync_context

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def register_refactored_kf_callbacks(app, key_findings_service, KEY_FINDINGS_AVAILABLE):
    """
    Register refactored Key Findings callbacks with new architecture.

    Uses dedicated services:
    1. KeyFindingsRetrievalService - for database retrieval
    2. KeyFindingsContentParser - for content formatting
    """

    if not KEY_FINDINGS_AVAILABLE or not key_findings_service:
        logger.warning(
            "Key Findings service not available - skipping callback registration"
        )
        return

    # Initialize new services
    retrieval_service = get_key_findings_retrieval_service()
    content_parser = get_key_findings_content_parser()

    @app.callback(
        Output("key-findings-modal", "is_open"),
        Output("key-findings-modal-body", "children"),
        Output("key-findings-modal-title", "children"),
        Output("key-findings-data-ready", "data"),
        Input("generate-key-findings-btn", "n_clicks"),
        Input("close-key-findings-modal", "n_clicks"),
        State("keyword-dropdown", "value"),
        State("data-sources-store-v2", "data"),
        State("language-store", "data"),
        prevent_initial_call=True,
    )
    def handle_key_findings_modal_refactored(
        generate_clicks, close_clicks, selected_tool, selected_sources, language
    ):
        """
        Refactored modal handler using new architecture.

        Workflow:
        1. Validate inputs
        2. Retrieve from database using KeyFindingsRetrievalService
        3. Parse content using KeyFindingsContentParser
        4. Create modal content
        5. Handle errors gracefully
        """

        logger.info("🔍 REFACTORED_MODAL: Starting modal handler")

        # Determine trigger
        ctx = dash.callback_context
        if not ctx.triggered:
            logger.info("🔍 REFACTORED_MODAL: No trigger, returning default")
            return False, "", "🧠 Key Findings - Análisis", None

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        logger.info(f"🔍 REFACTORED_MODAL: Triggered by: {trigger_id}")

        # Handle close button
        if trigger_id == "close-key-findings-modal":
            logger.info("🔍 REFACTORED_MODAL: Closing modal")
            return False, "", "🧠 Key Findings - Análisis", None

        # Handle generate button
        if trigger_id == "generate-key-findings-btn":
            logger.info("🔍 REFACTORED_MODAL: Generate button clicked")

            # Validate inputs
            if not selected_tool or not selected_sources:
                logger.warning("🔍 REFACTORED_MODAL: Missing tool or sources")
                error_content = create_error_modal_content(
                    "Por favor seleccione una herramienta y al menos una fuente de datos.",
                    language or "es",
                )
                return True, error_content, "🧠 Key Findings - Error", None

            try:
                # Step 1: Retrieve from database using new service
                logger.info(
                    f"🔍 REFACTORED_MODAL: Retrieving findings for {selected_tool} + {len(selected_sources)} sources"
                )

                retrieval_result = retrieval_service.retrieve_precomputed_findings(
                    tool_name=selected_tool,
                    selected_sources=selected_sources,
                    language=language or "es",
                )

                logger.info(
                    f"🔍 REFACTORED_MODAL: Retrieval result - success: {retrieval_result['success']}, source: {retrieval_result.get('source')}"
                )

                # Step 2: Parse content if retrieval successful
                if retrieval_result["success"] and retrieval_result["data"]:
                    logger.info("🔍 REFACTORED_MODAL: Parsing content...")

                    parse_result = content_parser.parse_modal_content(
                        retrieval_result["data"], language or "es"
                    )

                    logger.info(
                        f"🔍 REFACTORED_MODAL: Parse result - success: {parse_result['success']}"
                    )

                    if parse_result["success"] and parse_result["data"]:
                        # Step 3: Create modal content
                        logger.info("🔍 REFACTORED_MODAL: Creating modal content...")

                        modal_content = create_modal_content_from_parsed(
                            parse_result["data"], language or "es"
                        )

                        # Create dynamic title
                        tool_display_name = get_tool_name(
                            selected_tool, language or "es"
                        )
                        sources_str = ", ".join(selected_sources)
                        dynamic_title = (
                            f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
                        )

                        logger.info(
                            "✅ REFACTORED_MODAL: Successfully generated modal content"
                        )
                        return (
                            True,
                            modal_content,
                            dynamic_title,
                            retrieval_result["data"],
                        )
                    else:
                        # Parse error
                        logger.error(
                            f"❌ REFACTORED_MODAL: Content parsing failed: {parse_result.get('error')}"
                        )
                        error_content = create_error_modal_content(
                            f"Error al procesar el contenido: {parse_result.get('error', 'Unknown parsing error')}",
                            language or "es",
                        )
                        return True, error_content, "🧠 Key Findings - Error", None
                else:
                    # Database miss or retrieval error
                    error_msg = retrieval_result.get(
                        "error", "Database retrieval failed"
                    )
                    logger.warning(f"⚠️ REFACTORED_MODAL: Retrieval failed: {error_msg}")

                    error_content = create_error_modal_content(
                        error_msg, language or "es"
                    )
                    return True, error_content, "🧠 Key Findings - Error", None

            except Exception as e:
                logger.error(f"❌ REFACTORED_MODAL: Unexpected error: {e}")
                import traceback

                traceback.print_exc()

                error_content = create_error_modal_content(
                    f"Error inesperado: {str(e)}", language or "es"
                )
                return True, error_content, "🧠 Key Findings - Error", None

        # Default return
        return False, "", "🧠 Key Findings - Análisis", None

    logger.info("✅ REFACTORED_MODAL: Callbacks registered successfully")


def create_modal_content_from_parsed(
    parsed_content: Dict[str, Any], language: str
) -> html.Div:
    """
    Create modal content from parsed data using the new architecture.

    Args:
        parsed_content: Structured content from parser
        language: Language code

    Returns:
        HTML Div component with modal content
    """
    try:
        logger.info(f"📝 MODAL_CONTENT: Creating content for {language}")

        metadata = parsed_content.get("metadata", {})
        sections = parsed_content.get("sections", {})

        # Get parser instance for section configurations
        parser = get_key_findings_content_parser()
        section_configs = parser.get_all_sections(language)

        modal_sections = []

        # Add sections in proper order
        for section_config in section_configs:
            section_name = section_config["name"]
            section_data = sections.get(section_name, {})

            if section_data.get("present", False):
                content = section_data.get("content", "")

                if content and len(content.strip()) > 10:
                    # Create section with proper styling
                    section_div = html.Div(
                        [
                            html.H5(
                                section_config["title"],
                                className="mb-3",
                                style={
                                    "fontSize": "1.25rem",
                                    "fontWeight": "600",
                                    "borderBottom": "2px solid #0d6efd",
                                    "paddingBottom": "0.5rem",
                                    "marginTop": "1.5rem",
                                    "color": "#0d6efd",
                                    "display": "flex",
                                    "alignItems": "center",
                                },
                            ),
                            html.Div(
                                content,
                                className="text-justify",
                                style={
                                    "fontSize": "0.95rem",
                                    "lineHeight": "1.6",
                                    "whiteSpace": "pre-line",
                                    "color": "#495057",
                                    "padding": "0.5rem 0",
                                },
                            ),
                        ],
                        className="mb-4",
                    )

                    modal_sections.append(section_div)
                    logger.info(
                        f"📝 MODAL_CONTENT: Added section: {section_name} ({len(content)} chars)"
                    )

        # Add metadata footer
        if metadata:
            footer = html.Div(
                [
                    html.Hr(),
                    html.Div(
                        [
                            html.Small(
                                [
                                    html.Strong("Analysis Metadata: "),
                                    f"Model: {metadata.get('model_used', 'unknown')}, ",
                                    f"Confidence: {metadata.get('confidence_score', 0):.2f}, ",
                                    f"Data Points: {metadata.get('data_points_analyzed', 0)}, ",
                                    f"Response Time: {metadata.get('response_time_ms', 0)}ms",
                                ],
                                className="text-muted",
                            )
                        ],
                        className="mt-3",
                    ),
                ],
                className="mt-4",
            )

            modal_sections.append(footer)

        # Create final content container
        final_content = html.Div(
            modal_sections,
            style={"maxHeight": "70vh", "overflowY": "auto", "padding": "1rem"},
        )

        logger.info(
            f"✅ MODAL_CONTENT: Created content with {len(modal_sections)} sections"
        )
        return final_content

    except Exception as e:
        logger.error(f"❌ MODAL_CONTENT: Error creating modal content: {e}")
        import traceback

        traceback.print_exc()

        return html.Div(
            [
                html.H4("Error Creating Content", className="text-danger"),
                html.P(
                    f"Failed to create modal content: {str(e)}", className="text-muted"
                ),
            ]
        )


def create_error_modal_content(error_message: str, language: str) -> html.Div:
    """
    Create error content for modal display.

    Args:
        error_message: Error message to display
        language: Language code

    Returns:
        HTML Div with error content
    """
    return html.Div(
        [
            html.Div(
                [
                    html.I(className="fas fa-exclamation-triangle text-warning me-2"),
                    html.H4("Error de Análisis", className="d-inline text-warning"),
                ],
                className="mb-3",
            ),
            html.P(error_message, className="text-muted mb-3"),
            html.P(
                "Por favor intente nuevamente. Si el problema persiste, seleccione diferentes fuentes de datos.",
                className="text-muted small",
            ),
        ],
        className="p-4 text-center",
    )
