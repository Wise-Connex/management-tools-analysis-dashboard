"""
UI Callbacks Module

This module contains all UI-related callbacks for the dashboard application.
These callbacks handle user interface state management, language switching,
button text updates, and other UI-related functionality.

The callbacks are organized into logical groups and are registered through
the register_ui_callbacks function.
"""

import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

# Import translation and utility functions
from translations import get_text
from fix_source_mapping import DISPLAY_NAMES


def register_ui_callbacks(app):
    """
    Register all UI callbacks with the Dash application.

    Args:
        app: The Dash application instance
    """

    # Language management callback
    @app.callback(
        Output("language-store", "data"),
        Input("language-selector", "value"),
        prevent_initial_call=True,
    )
    def update_language_store(selected_language):
        """Update language store when language selector changes"""
        return selected_language

    # Callback to reset source selections when keyword changes
    @app.callback(
        Output("data-sources-store-v2", "data", allow_duplicate=True),
        Input("keyword-dropdown", "value"),
        prevent_initial_call=True,
    )
    def reset_sources_on_keyword_change(selected_tool):
        """Reset source selections when a new keyword is selected"""
        return []

    # Callback to initialize select all button text
    @app.callback(
        Output("select-all-button", "children", allow_duplicate=True),
        Input("keyword-dropdown", "value"),
        Input("language-store", "data"),
        prevent_initial_call=True,
    )
    def initialize_select_all_button_text(selected_tool, language):
        """Initialize the select all button text when a tool is selected"""
        return get_text("select_all", language)

    # Callback to update keyword dropdown options based on language
    @app.callback(
        Output("keyword-dropdown", "options"),
        Output("keyword-dropdown", "placeholder"),
        Input("language-store", "data"),
    )
    def update_keyword_dropdown_options(language):
        """Update keyword dropdown options and placeholder based on language"""
        from tools import get_tool_options  # Import here to avoid circular imports

        options = get_tool_options(language)
        placeholder = get_text("select_management_tool", language)
        return options, placeholder

    # Callback to update sidebar labels and affiliations based on language
    @app.callback(
        Output("tool-label", "children"),
        Output("sources-label", "children"),
        Output("sidebar-affiliations", "children"),
        Input("language-store", "data"),
    )
    def update_sidebar_labels(language):
        """Update sidebar labels and affiliations based on language"""
        tool_label = get_text("select_tool", language)
        sources_label = get_text("select_sources", language)

        affiliations = html.Div(
            [
                html.P(
                    get_text("university", language),
                    style={
                        "margin": "2px 0",
                        "fontSize": "12px",
                        "fontWeight": "normal",
                        "textAlign": "center",
                    },
                ),
                html.P(
                    get_text("postgraduate_coordination", language),
                    style={
                        "margin": "2px 0",
                        "fontSize": "11px",
                        "fontWeight": "normal",
                        "textAlign": "center",
                    },
                ),
                html.P(
                    get_text("doctoral_program", language),
                    style={
                        "margin": "2px 0",
                        "fontSize": "13px",
                        "fontWeight": "bold",
                        "textAlign": "center",
                    },
                ),
            ],
            style={"marginBottom": "15px"},
        )

        return tool_label, sources_label, affiliations

    # Callback to update data sources container
    @app.callback(
        Output("data-sources-container", "children"),
        Input("keyword-dropdown", "value"),
        Input("data-sources-store-v2", "data"),
        Input("language-store", "data"),
    )
    def update_data_sources_container(selected_tool, selected_sources, language):
        if not selected_tool:
            return html.Div(get_text("no_sources_selected", language))

        if selected_sources is None:
            selected_sources = []

        # Import here to avoid circular imports
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from app import source_colors_by_display

        sources = DISPLAY_NAMES

        components = []

        # Map display names to the correct source names for buttons
        display_to_source = {
            "Google Trends": "Google Trends",
            "Google Books": "Google Books",
            "Bain Usability": "Bain Usability",
            "Bain Satisfaction": "Bain Satisfaction",
            "Crossref": "Crossref",
        }

        for source in sources:
            # Use display name for button text
            display_name = source
            if source in display_to_source:
                display_name = display_to_source[source]

            # Determine button style based on selection state
            base_color = source_colors_by_display.get(source, "#6c757d")

            # IMPORTANT: Check if source is in the CURRENT selected_sources list
            is_selected = source in selected_sources

            if is_selected:
                # Selected style - brighter/darker
                button_style = {
                    "backgroundColor": base_color,
                    "borderColor": base_color,
                    "color": "white",
                    "fontSize": "12px",
                    "minWidth": "120px",
                    "boxShadow": "0 0 0 2px rgba(0,123,255,0.5)",
                    "fontWeight": "bold",
                }
            else:
                # Unselected style - outline
                button_style = {
                    "backgroundColor": "transparent",
                    "borderColor": base_color,
                    "color": base_color,
                    "fontSize": "12px",
                    "minWidth": "120px",
                    "fontWeight": "normal",
                }

            # Create button with appropriate style
            button = dbc.Button(
                display_name,
                id={"type": "data-source-button", "index": display_name},
                color="outline-primary",
                size="sm",
                className="me-2 mb-2",
                style=button_style,
            )

            # Info icon beside the button
            icon = html.I(
                className="fas fa-info-circle",
                id={"type": "info-icon", "index": source},
                style={
                    "cursor": "pointer",
                    "marginLeft": "10px",
                    "color": "#007bff",
                    "fontSize": "16px",
                    "verticalAlign": "middle",
                },
            )

            row = html.Div(
                [button, icon],
                style={"display": "flex", "alignItems": "center", "marginBottom": "5px"},
            )
            components.append(row)

        return components

    # Callback to update DOI display
    @app.callback(
        Output("doi-display", "children"),
        Input("keyword-dropdown", "value"),
        Input("language-store", "data"),
    )
    def update_doi_display(selected_tool, language):
        # Import here to avoid circular imports
        from database import get_database_manager

        if not selected_tool:
            return html.Div()

        # Get the IC report DOI from the IC source (Complementary Report)
        db_manager = get_database_manager()
        tool_notes = db_manager.get_tool_notes_and_doi(selected_tool, "IC")

        if tool_notes and len(tool_notes) > 0:
            doi = tool_notes[0].get("doi", "")
            if doi:
                return html.Div(
                    [
                        html.Strong(
                            get_text("ic_report_doi", language) + ": ",
                            style={"fontSize": "12px"},
                        ),
                        html.A(
                            doi,
                            href=f"https://doi.org/{doi}",
                            target="_blank",
                            style={
                                "color": "#007bff",
                                "fontSize": "12px",
                                "textDecoration": "none",
                            },
                        ),
                    ],
                    style={
                        "padding": "8px",
                        "backgroundColor": "#f8f9fa",
                        "borderRadius": "4px",
                        "border": "1px solid #dee2e6",
                    },
                )

        return html.Div(
            get_text("no_doi_available", language),
            style={"fontSize": "11px", "color": "#6c757d", "fontStyle": "italic"},
        )

    # Callback to update selected sources store
    @app.callback(
        Output("data-sources-store-v2", "data"),
        Input({"type": "data-source-button", "index": ALL}, "n_clicks"),
        Input({"type": "data-source-button", "index": ALL}, "id"),
        Input("select-all-button", "n_clicks"),
        State("data-sources-store-v2", "data"),
    )
    def update_selected_sources(n_clicks, ids, select_all_clicks, current_selected):
        if current_selected is None:
            current_selected = []

        # Find which button was clicked
        ctx = dash.callback_context

        if ctx.triggered:
            trigger_id = ctx.triggered[0]["prop_id"]

            # IMPORTANT: Ignore triggers from initial component creation
            if trigger_id.endswith(".n_clicks") and ctx.triggered[0]["value"] is None:
                return current_selected

            # Check if "Seleccionar Todo" button was clicked
            if "select-all-button" in trigger_id:
                # Get all available sources
                all_sources = DISPLAY_NAMES

                # If all sources are already selected, deselect all
                if set(current_selected) == set(all_sources):
                    current_selected = []
                else:
                    # Select all sources
                    current_selected = all_sources.copy()

            elif "data-source-button" in trigger_id:
                # Extract the source name from the triggered button
                button_id = eval(trigger_id.split(".")[0])  # Convert string back to dict
                source = button_id["index"]

                # Toggle selection
                if source in current_selected:
                    current_selected.remove(source)
                else:
                    current_selected.append(source)

        return current_selected

    # Callback to update toggle table button text and handle collapse
    @app.callback(
        Output("collapse-table", "is_open"),
        Output("toggle-table-button", "children"),
        Input("language-store", "data"),
        Input("toggle-table-button", "n_clicks"),
        State("collapse-table", "is_open"),
    )
    def update_toggle_table_button(language, n_clicks, is_open):
        """Update toggle table button text and handle collapse based on language and state"""
        if n_clicks:
            new_state = not is_open
            button_text = (
                get_text("show_table", language)
                if new_state
                else get_text("hide_table", language)
            )
            return new_state, button_text
        else:
            button_text = (
                get_text("hide_table", language)
                if is_open
                else get_text("show_table", language)
            )
            return is_open, button_text

    # Callback to update modal labels
    @app.callback(
        Output("notes-modal-title", "children"),
        Output("close-notes-modal", "children"),
        Output("close-citation-modal", "children"),
        Input("language-store", "data"),
    )
    def update_modal_labels(language):
        """Update modal labels based on language"""
        notes_title = get_text("notes", language)
        close_notes = get_text("close", language)
        close_citation = get_text("close", language)

        return notes_title, close_notes, close_citation

    # Callback to update credits button text
    @app.callback(
        Output("credits-button", "children"),
        Input("language-store", "data"),
    )
    def update_credits_button_text(language):
        """Update credits button text based on language"""
        return get_text("credits", language)

    # Callback to update key findings button text and state
    @app.callback(
        Output("generate-key-findings-btn", "children"),
        Output("key-findings-button-state", "data", allow_duplicate=True),
        Input("language-store", "data"),
        Input("generate-key-findings-btn", "n_clicks"),
        Input("key-findings-reset-trigger", "data"),
        State("keyword-dropdown", "value"),
        State("data-sources-store-v2", "data"),
        prevent_initial_call=True,
    )
    def update_key_findings_button_text_and_state(
        language, n_clicks, reset_trigger, selected_tool, selected_sources
    ):
        """Update key findings button text and manage state based on language and interactions"""
        ctx = dash.callback_context

        if not ctx.triggered:
            # Initial load - set default text
            return get_text("key_findings", language), {"enabled": True, "text": get_text("key_findings", language)}

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle reset trigger
        if trigger_id == "key-findings-reset-trigger" and reset_trigger:
            return get_text("key_findings", language), {"enabled": True, "text": get_text("key_findings", language)}

        # Handle language change
        if trigger_id == "language-store" or (trigger_id == "generate-key-findings-btn" and n_clicks is None):
            button_text = get_text("key_findings", language)
            return button_text, {"enabled": True, "text": button_text}

        # Handle button click
        if trigger_id == "generate-key-findings-btn" and n_clicks:
            button_text = get_text("generating", language)
            return button_text, {"enabled": False, "text": button_text}

        # Default case
        button_text = get_text("key_findings", language)
        return button_text, {"enabled": True, "text": button_text}

    # Callback to update key findings button visibility
    @app.callback(
        Output("generate-key-findings-btn", "disabled"),
        Input("keyword-dropdown", "value"),
        Input("data-sources-store-v2", "data"),
    )
    def update_key_findings_button_visibility(selected_tool, selected_sources):
        """Update key findings button visibility based on tool and sources selection"""
        if not selected_tool:
            return True

        if not selected_sources or len(selected_sources) == 0:
            return True

        return False

    # Callback to update credits content
    @app.callback(
        Output("credits-content", "children"),
        Input("language-store", "data"),
    )
    def update_credits_content(language):
        """Update credits modal content based on language"""

        # Import here to avoid circular imports
        from utils import get_current_date_for_citation

        current_date = get_current_date_for_citation()
        # Extract APA format date for display
        display_date = current_date.get("apa", "")

        if language == "es":
            credits_content = html.Div([
                html.H5("Créditos y Reconocimientos", className="mb-3"),
                html.P("Este dashboard ha sido desarrollado como parte de una investigación doctoral sobre el análisis de tendencias en herramientas de gestión.",
                      className="mb-2"),
                html.P([
                    "Desarrollado por: ",
                    html.Strong("Diego Armando Maradona")
                ], className="mb-2"),
                html.P([
                    "Programa de Doctorado en: ",
                    html.Strong("Administración y Dirección de Empresas")
                ], className="mb-2"),
                html.P([
                    "Universidad: ",
                    html.Strong("Universidad Nacional de La Pampa")
                ], className="mb-2"),
                html.P([
                    html.Strong("Fuentes de datos: "),
                    "Google Trends, Google Books, Bain Survey, Crossref"
                ], className="mb-2"),
                html.P([
                    html.Strong("Fecha de acceso: "),
                    display_date
                ], className="mb-2"),
                html.Hr(),
                html.H6("Tecnologías Utilizadas", className="mt-3 mb-2"),
                html.P("Python, Dash, Plotly, Bootstrap, SQLite", className="mb-2"),
                html.H6("Reconocimiento", className="mt-3 mb-2"),
                html.P("Este trabajo utiliza datos de múltiples fuentes académicas y comerciales para el análisis de tendencias en herramientas de gestión.",
                      className="mb-0", style={"fontSize": "0.9em", "fontStyle": "italic"})
            ])
        else:
            credits_content = html.Div([
                html.H5("Credits and Acknowledgments", className="mb-3"),
                html.P("This dashboard has been developed as part of doctoral research on management tools trend analysis.",
                      className="mb-2"),
                html.P([
                    "Developed by: ",
                    html.Strong("Diego Armando Maradona")
                ], className="mb-2"),
                html.P([
                    "PhD Program: ",
                    html.Strong("Business Administration and Management")
                ], className="mb-2"),
                html.P([
                    "University: ",
                    html.Strong("National University of La Pampa")
                ], className="mb-2"),
                html.P([
                    html.Strong("Data sources: "),
                    "Google Trends, Google Books, Bain Survey, Crossref"
                ], className="mb-2"),
                html.P([
                    html.Strong("Access date: "),
                    display_date
                ], className="mb-2"),
                html.Hr(),
                html.H6("Technologies Used", className="mt-3 mb-2"),
                html.P("Python, Dash, Plotly, Bootstrap, SQLite", className="mb-2"),
                html.H6("Acknowledgment", className="mt-3 mb-2"),
                html.P("This work uses data from multiple academic and commercial sources for the analysis of management tools trends.",
                      className="mb-0", style={"fontSize": "0.9em", "fontStyle": "italic"})
            ])

        return credits_content

    # Callback to update header content
    @app.callback(
        Output("dashboard-header", "children"),
        Output("dashboard-title", "children"),
        Output("dashboard-subtitle", "children"),
        Input("language-store", "data"),
    )
    def update_header_content(language):
        """Update dashboard header content based on language"""

        if language == "es":
            header = html.Div([
                html.H1("Dashboard de Análisis de Herramientas de Gestión",
                       className="text-center mb-4", style={"color": "#2c3e50", "fontWeight": "bold"}),
                html.P("Análisis integral de tendencias en herramientas de gestión mediante múltiples fuentes de datos",
                      className="text-center text-muted mb-4")
            ])
            title = "Dashboard de Análisis de Herramientas de Gestión"
            subtitle = "Análisis integral de tendencias en herramientas de gestión mediante múltiples fuentes de datos"
        else:
            header = html.Div([
                html.H1("Management Tools Analysis Dashboard",
                       className="text-center mb-4", style={"color": "#2c3e50", "fontWeight": "bold"}),
                html.P("Comprehensive analysis of management tools trends through multiple data sources",
                      className="text-center text-muted mb-4")
            ])
            title = "Management Tools Analysis Dashboard"
            subtitle = "Comprehensive analysis of management tools trends through multiple data sources"

        return header, title, subtitle

    # Callback to toggle notes modal
    @app.callback(
        Output("notes-modal", "is_open"),
        Input("open-notes-modal", "n_clicks"),
        Input("close-notes-modal", "n_clicks"),
        State("notes-modal", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_notes_modal(n_open, n_close, is_open):
        """Toggle notes modal open/close state"""
        if n_open or n_close:
            return not is_open
        return is_open

    # Callback to toggle credits manually
    @app.callback(
        Output("credits-modal", "is_open"),
        Input("credits-button", "n_clicks"),
        Input("close-credits-modal", "n_clicks"),
        State("credits-modal", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_credits_manually(n_credits, n_close, is_open):
        """Toggle credits modal manually"""
        if n_credits or n_close:
            return not is_open
        return is_open

    # Callback to update navigation visibility
    @app.callback(
        Output("analysis-navigation", "style"),
        Input("keyword-dropdown", "value"),
        Input("data-sources-store-v2", "data"),
        Input("language-store", "data"),
    )
    def update_navigation_visibility(selected_keyword, selected_sources, language):
        """Update navigation visibility based on selection state"""
        if not selected_keyword or not selected_sources:
            return {"display": "none"}
        return {"display": "block"}

    # Callback to update download button text
    @app.callback(
        Output("download-button", "children"),
        Input("language-store", "data"),
    )
    def update_download_button_text(language):
        """Update download button text based on language"""
        return get_text("download_citation", language)

    # Callback to copy citation to clipboard
    @app.callback(
        Output("copy-store", "data"),
        Input("copy-citation-button", "n_clicks"),
        State("keyword-dropdown", "value"),
        State("language-store", "data"),
        prevent_initial_call=True,
    )
    def copy_citation_to_clipboard(n_clicks, selected_tool, language):
        """Generate citation text for clipboard"""
        if not n_clicks or not selected_tool:
            return ""

        # Import here to avoid circular imports
        from utils import get_current_date_for_citation
        from translations import get_text

        current_date = get_current_date_for_citation()
        # Extract APA format date for citation
        citation_date = current_date.get("apa", "")

        if language == "es":
            citation = f"""Maradona, D. A. ({citation_date}). *Dashboard de Análisis de Herramientas de Gestión*. Programa de Doctorado en Administración y Dirección de Empresas, Universidad Nacional de La Pampa. Recuperado de {dash.get_relative_path('/')}"""
        else:
            citation = f"""Maradona, D. A. ({citation_date}). *Management Tools Analysis Dashboard*. PhD Program in Business Administration and Management, National University of La Pampa. Retrieved from {dash.get_relative_path('/')}"""

        return citation

    # Callback to generate RIS download link
    @app.callback(
        Output("ris-download-link", "href"),
        Input("ris-button", "n_clicks"),
        State("keyword-dropdown", "value"),
        State("language-store", "data"),
        prevent_initial_call=True,
    )
    def generate_ris_download_link(n_clicks, selected_tool, language):
        """Generate RIS format download link for citation"""
        if not n_clicks or not selected_tool:
            return ""

        # Import here to avoid circular imports
        from utils import get_current_date_for_citation

        current_date = get_current_date_for_citation()
        # Extract year part from APA format date for RIS
        citation_year = current_date.get("apa", "").split()[-1]

        # Generate RIS format citation
        ris_content = f"""TY  - COMP
T1  - {'Dashboard de Análisis de Herramientas de Gestión' if language == 'es' else 'Management Tools Analysis Dashboard'}
AU  - Maradona, Diego Armando
PY  - {citation_year}
PB  - {'Programa de Doctorado en Administración y Dirección de Empresas, Universidad Nacional de La Pampa' if language == 'es' else 'PhD Program in Business Administration and Management, National University of La Pampa'}
UR  - {dash.get_relative_path('/')}
ER  - """

        # This would need to be implemented as a proper download endpoint
        # For now, return empty string or placeholder
        return "#"  # Placeholder - would need actual implementation