"""
Key Findings callbacks for the Management Tools Analysis Dashboard.

Reads pre-generated reports from kf_reports_v2.db and renders them
section-by-section in a modal. No live AI calls — all data is pre-generated.
"""

import json
import re
import io
import base64
from datetime import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import logging

from translations import get_tool_name, get_text
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
    "color": "#495057",
    "padding": "0.5rem 0",
}


def _extract_lang_content(content: str, lang_key: str) -> str:
    """Extract language-specific content from potentially raw JSON strings.

    Handles three cases:
    1. Normal text (not JSON) — returned as-is
    2. Complete JSON {"es": "...", "en": "..."} — parsed and extracted
    3. Truncated JSON (API response cut off) — regex extraction with unescaping
    """
    stripped = content.strip()
    if not stripped.startswith("{"):
        return content

    # Try complete JSON parse first
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict) and lang_key in parsed:
            return parsed[lang_key]
    except (json.JSONDecodeError, TypeError):
        pass

    # Truncated JSON — extract with regex
    # Match: "es": "..." or "en": "..." (greedy to get as much content as possible)
    other_key = "en" if lang_key == "es" else "es"
    # Try to extract preferred language first, then fallback
    for key in [lang_key, other_key]:
        pattern = rf'"{key}"\s*:\s*"(.*?)"\s*(?:,\s*"{other_key if key == lang_key else lang_key}"|\}})'
        match = re.search(pattern, stripped, re.DOTALL)
        if match:
            text = match.group(1)
            # Unescape JSON string escapes
            text = text.replace("\\n", "\n").replace("\\t", "\t")
            text = text.replace('\\"', '"').replace("\\\\", "\\")
            return text

    # Last resort: grab everything after "lang_key": " until end
    for key in [lang_key, other_key]:
        pattern = rf'"{key}"\s*:\s*"(.*)'
        match = re.search(pattern, stripped, re.DOTALL)
        if match:
            text = match.group(1).rstrip('"} \n')
            text = text.replace("\\n", "\n").replace("\\t", "\t")
            text = text.replace('\\"', '"').replace("\\\\", "\\")
            return text

    return content


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
            lang_key = "es" if language == "es" else "en"
            for section in report["sections"]:
                content = section["content"]
                if not content or len(content.strip()) < 20:
                    continue

                # Handle content that was stored as raw JSON {"es": ..., "en": ...}
                # This happens when the generation pipeline failed to parse bilingual output
                content = _extract_lang_content(content, lang_key)

                modal_sections.append(
                    html.Div(
                        [
                            html.H5(
                                section["title"],
                                className="section-title mb-3",
                                style=SECTION_TITLE_STYLE,
                            ),
                            dcc.Markdown(
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

    # ---- PDF export callback ----

    def _strip_markdown(text: str) -> str:
        """Strip markdown formatting to plain text for PDF rendering."""
        # Remove headers (## Header)
        text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
        # Bold **text** or __text__
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"__(.+?)__", r"\1", text)
        # Italic *text* or _text_
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", text)
        # Inline code `code`
        text = re.sub(r"`(.+?)`", r"\1", text)
        # Links [text](url) -> text
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
        # Horizontal rules
        text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
        # Clean up bullet points: - item or * item -> bullet (use hyphen, Latin-1 safe)
        text = re.sub(r"^\s*[-*+]\s+", "  - ", text, flags=re.MULTILINE)
        # Numbered lists: keep as-is
        # Remove excess blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _sanitize_for_latin1(text: str) -> str:
        """Replace non-Latin-1 characters with ASCII equivalents for PDF rendering.

        Helvetica only supports Latin-1 (ISO 8859-1). This function maps common
        Unicode characters to their closest Latin-1/ASCII equivalents and drops
        any remaining unsupported characters.
        """
        # Common Unicode -> ASCII replacements
        replacements = {
            "\u2022": "-",   # bullet -> hyphen
            "\u2013": "-",   # en dash
            "\u2014": "--",  # em dash
            "\u2018": "'",   # left single quote
            "\u2019": "'",   # right single quote
            "\u201C": '"',   # left double quote
            "\u201D": '"',   # right double quote
            "\u2026": "...", # ellipsis
            "\u03bc": "u",   # Greek mu -> u (micro)
            "\u03b1": "a",   # Greek alpha
            "\u03b2": "b",   # Greek beta
            "\u03b3": "g",   # Greek gamma
            "\u03b4": "d",   # Greek delta
            "\u03c3": "s",   # Greek sigma
            "\u03c0": "pi",  # Greek pi
            "\u2264": "<=",  # less than or equal
            "\u2265": ">=",  # greater than or equal
            "\u2260": "!=",  # not equal
            "\u00b2": "2",   # superscript 2 (Latin-1 safe, but just in case)
            "\u00b3": "3",   # superscript 3
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        # Remove emoji ranges
        text = re.sub(
            "["
            "\U0001F300-\U0001F9FF"
            "\U00002702-\U000027B0"
            "\U0000FE00-\U0000FE0F"
            "\U0000200D"
            "\U00002600-\U000026FF"
            "]+",
            "",
            text,
            flags=re.UNICODE,
        )

        # Drop any remaining non-Latin-1 characters
        result = []
        for ch in text:
            try:
                ch.encode("latin-1")
                result.append(ch)
            except UnicodeEncodeError:
                pass  # skip unsupported characters
        return "".join(result).strip()

    def _generate_pdf(report, tool_name, sources_text, language):
        """Generate a PDF from the report data using fpdf2."""
        from fpdf import FPDF

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.set_margins(left=20, top=20, right=20)

        # ---- Cover / Header on first page ----
        pdf.add_page()

        # Title block
        if language == "es":
            doc_title = "Hallazgos Principales"
            tool_label = "Herramienta"
            sources_label = "Fuentes de Datos"
            authors_label = "Autores"
            date_label = "Fecha"
        else:
            doc_title = "Key Findings"
            tool_label = "Tool"
            sources_label = "Data Sources"
            authors_label = "Authors"
            date_label = "Date"

        # Main title
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(13, 110, 253)  # Bootstrap primary blue
        pdf.cell(0, 12, doc_title, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(2)

        # Horizontal rule
        pdf.set_draw_color(13, 110, 253)
        pdf.set_line_width(0.5)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(6)

        # Metadata block
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(33, 37, 41)

        tool_display = get_tool_name(tool_name, language) or tool_name
        pdf.cell(35, 7, f"{tool_label}:", new_x="END", new_y="TOP")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, tool_display, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(35, 7, f"{sources_label}:", new_x="END", new_y="TOP")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, sources_text)

        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(35, 7, f"{authors_label}:", new_x="END", new_y="TOP")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, "Diomar Anez, Dimar Anez", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(35, 7, f"{date_label}:", new_x="END", new_y="TOP")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(
            0, 7,
            datetime.now().strftime("%Y-%m-%d"),
            new_x="LMARGIN", new_y="NEXT",
        )
        pdf.ln(4)

        # Separator
        pdf.set_draw_color(200, 200, 200)
        pdf.set_line_width(0.3)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(6)

        # ---- Sections ----
        lang_key = "es" if language == "es" else "en"
        for section in report["sections"]:
            content = section["content"]
            if not content or len(content.strip()) < 20:
                continue

            content = _extract_lang_content(content, lang_key)
            clean_content = _strip_markdown(content)

            # Section title (sanitized for Latin-1)
            section_title = _sanitize_for_latin1(section["title"])
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(13, 110, 253)
            pdf.cell(0, 8, section_title, new_x="LMARGIN", new_y="NEXT")

            # Title underline
            pdf.set_draw_color(13, 110, 253)
            pdf.set_line_width(0.4)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(4)

            # Section content (sanitized for Latin-1)
            clean_content = _sanitize_for_latin1(clean_content)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(73, 80, 87)
            pdf.multi_cell(0, 5, clean_content)
            pdf.ln(4)

        # ---- Footer on every page ----
        total_pages = pdf.page
        for page_num in range(1, total_pages + 1):
            pdf.page = page_num
            pdf.set_y(-15)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 5, f"Page {page_num}/{total_pages}", align="L")
            pdf.cell(0, 5, "tempo.solidum360.com", align="R",
                     new_x="LMARGIN", new_y="TOP")

        # Output as bytes
        buf = io.BytesIO()
        pdf.output(buf)
        return buf.getvalue()

    @app.callback(
        Output("export-pdf-link", "href"),
        Output("export-pdf-link", "download"),
        Output("export-pdf-link", "style"),
        Output("export-pdf-text", "children"),
        Input("generate-key-findings-btn", "n_clicks"),
        Input("close-key-findings-modal", "n_clicks"),
        State("keyword-dropdown", "value"),
        State("data-sources-store-v2", "data"),
        State("language-store", "data"),
        prevent_initial_call=True,
    )
    def generate_pdf_link(
        generate_clicks, close_clicks,
        selected_tool, selected_sources, language,
    ):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        btn_text = get_text("export_pdf_button", language or "es")
        hidden = {"textDecoration": "none", "display": "none"}
        visible = {"textDecoration": "none"}

        # Hide on close
        if trigger_id == "close-key-findings-modal":
            return "", "key_findings.pdf", hidden, btn_text

        if trigger_id != "generate-key-findings-btn":
            raise dash.exceptions.PreventUpdate

        if not selected_tool or not selected_sources:
            return "", "key_findings.pdf", hidden, btn_text

        source_names = _source_names_from_display(selected_sources)

        try:
            db = get_kf_report_db()
            report = db.get_report(selected_tool, source_names, language)

            if report is None:
                return "", "key_findings.pdf", hidden, btn_text

            pdf_bytes = _generate_pdf(
                report, selected_tool,
                report["sources_text"], language,
            )

            pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
            data_uri = f"data:application/pdf;base64,{pdf_b64}"

            # Filename
            tool_clean = re.sub(r"[^\w]", "_", selected_tool)
            ts = datetime.now().strftime("%Y%m%d")
            if language == "es":
                filename = f"Hallazgos_{tool_clean}_{ts}.pdf"
            else:
                filename = f"KeyFindings_{tool_clean}_{ts}.pdf"

            return data_uri, filename, visible, btn_text

        except Exception as e:
            logger.error(f"Error generating PDF: {e}", exc_info=True)
            return "", "key_findings.pdf", hidden, btn_text
