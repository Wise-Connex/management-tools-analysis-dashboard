"""
Key Findings callbacks for the Management Tools Analysis Dashboard.

Reads pre-generated reports from kf_reports_v2.db and renders them
section-by-section in a modal. No live AI calls — all data is pre-generated.
"""

import dash
from dash import html
from dash.dependencies import Input, Output, State
import logging

from translations import get_tool_name
from key_findings.kf_report_db import get_kf_report_db
from fix_source_mapping import DISPLAY_NAMES

logger = logging.getLogger(__name__)

# Source ID -> display name mapping (used to convert IDs back to names)
_SOURCE_ID_TO_DISPLAY = {
    1: "Google Trends",
    2: "Google Books",
    3: "Bain Usability",
    4: "Crossref",
    5: "Bain Satisfaction",
}

# Styling constants
SECTION_TITLE_STYLE = {
    "fontSize": "1.25rem",
    "fontWeight": "600",
    "borderBottom": "2px solid #0d6efd",
    "paddingBottom": "0.5rem",
    "marginTop": "1.5rem",
    "color": "#0d6efd",
}

SECTION_CONTENT_STYLE = {
    "fontSize": "0.95rem",
    "lineHeight": "1.6",
    "whiteSpace": "pre-line",
    "color": "#495057",
    "padding": "0.5rem 0",
}


def _make_title(selected_tool, selected_sources, language):
    """Build a dynamic modal title."""
    tool_display = get_tool_name(selected_tool, language) if selected_tool else "Herramienta"
    src_str = ", ".join(selected_sources) if selected_sources else "Fuentes"
    return f"\U0001f9e0 Hallazgos para {tool_display} ({src_str})"


def _default_return(title="\U0001f9e0 Key Findings"):
    """Five-value tuple for the no-op / close case."""
    return False, "", title, True, None


def _error_return(title, message_es, message_en="", language="es"):
    """Five-value tuple for error cases."""
    msg = message_es if language == "es" else (message_en or message_es)
    body = html.Div([
        html.H4("Error", className="text-danger"),
        html.P(msg, className="text-muted"),
    ])
    return True, body, title, False, None


def _source_names_from_display(selected_sources):
    """Ensure we have display-name strings (not IDs)."""
    result = []
    for s in (selected_sources or []):
        if isinstance(s, int):
            result.append(_SOURCE_ID_TO_DISPLAY.get(s, str(s)))
        else:
            result.append(s)
    return result


def register_kf_callbacks(app, key_findings_service, KEY_FINDINGS_AVAILABLE):
    """Register Key Findings callbacks with the Dash app."""

    @app.callback(
        Output("key-findings-modal", "is_open"),
        Output("key-findings-modal-body", "children"),
        Output("key-findings-modal-title", "children"),
        Output("key-findings-content-ready", "data"),
        Output("key-findings-data-ready", "data"),
        Input("generate-key-findings-btn", "n_clicks"),
        Input("close-key-findings-modal", "n_clicks"),
        Input("key-findings-modal", "is_open"),
        State("keyword-dropdown", "value"),
        State("data-sources-store-v2", "data"),
        State("language-store", "data"),
        State("key-findings-content-ready", "data"),
        prevent_initial_call=True,
    )
    def toggle_key_findings_modal(
        generate_clicks,
        close_clicks,
        modal_is_open,
        selected_tool,
        selected_sources,
        language,
        current_content_ready,
    ):
        ctx = dash.callback_context
        if not ctx.triggered:
            return _default_return()

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        title = _make_title(selected_tool, selected_sources, language)

        # ---- Close actions ----
        if trigger_id == "close-key-findings-modal":
            return _default_return(title)

        if trigger_id == "key-findings-modal" and not modal_is_open:
            return _default_return(title)

        # ---- Generate action ----
        if trigger_id != "generate-key-findings-btn":
            return _default_return(title)

        if not selected_tool or not selected_sources:
            return _error_return(
                title,
                "Por favor seleccione una herramienta y al menos una fuente de datos.",
                "Please select a tool and at least one data source.",
                language,
            )

        source_names = _source_names_from_display(selected_sources)

        try:
            db = get_kf_report_db()
            report = db.get_report(selected_tool, source_names, language)

            if report is None:
                logger.info(f"No v2 report for {selected_tool} + {source_names}")
                no_report_msg_es = (
                    "El informe para esta combinacion aun no ha sido generado. "
                    "Por favor intente con otra herramienta o combinacion de fuentes."
                )
                no_report_msg_en = (
                    "The report for this combination has not been generated yet. "
                    "Please try a different tool or source combination."
                )
                return _error_return(title, no_report_msg_es, no_report_msg_en, language)

            # Build modal body from sections
            modal_sections = []
            for section in report["sections"]:
                content = section["content"]
                if not content or len(content.strip()) < 20:
                    continue

                modal_sections.append(
                    html.Div(
                        [
                            html.H5(
                                section["title"],
                                className="section-title mb-3",
                                style=SECTION_TITLE_STYLE,
                            ),
                            html.Div(
                                content,
                                className="text-justify section-content",
                                style=SECTION_CONTENT_STYLE,
                            ),
                        ],
                        className="mb-4",
                    )
                )

            if not modal_sections:
                return _error_return(
                    title,
                    "El informe existe pero no contiene secciones.",
                    "The report exists but contains no sections.",
                    language,
                )

            # Add metadata footer
            modal_sections.append(
                html.Div(
                    html.Small(
                        f"Modelo: {report.get('model_used', 'N/A')} | "
                        f"Generado: {report.get('generated_at', 'N/A')}",
                        className="text-muted",
                    ),
                    className="border-top pt-2 mt-3",
                )
            )

            final_body = html.Div(
                modal_sections,
                style={"maxHeight": "70vh", "overflowY": "auto"},
            )
            return True, final_body, title, True, None

        except Exception as e:
            logger.error(f"Error loading Key Findings: {e}", exc_info=True)
            return _error_return(
                title,
                f"Error al cargar el informe: {e}",
                f"Error loading report: {e}",
                language,
            )
