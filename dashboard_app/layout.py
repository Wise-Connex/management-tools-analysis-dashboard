"""
Layout components for the Management Tools Analysis Dashboard.

This module contains all the UI layout components for the dashboard,
including the sidebar, header, modals, and main layout structure.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from translations import get_text


def create_sidebar():
    """Create the sidebar layout with tool selection and controls."""

    sidebar = html.Div(
        [
            # Bloque Superior Izquierdo (Afiliación Académica)
            html.Div(
                [
                    html.Div(id="sidebar-affiliations"),
                    html.Hr(),
                    html.Div(
                        [
                            html.Label(id="tool-label", style={"fontSize": "12px"}),
                            dcc.Dropdown(
                                id="keyword-dropdown",
                                options=[],  # Will be set by callback
                                value=None,
                                placeholder="",  # Will be set by callback
                                className="mb-2",
                                style={"fontSize": "12px"},
                                # Add defensive properties to handle extension conflicts
                                clearable=False,
                                searchable=True,
                                multi=False,
                            ),
                            html.Div(
                                id="keyword-validation",
                                className="text-danger",
                                style={"fontSize": "12px"},
                            ),
                            html.Div(
                                id="doi-display",
                                style={"marginTop": "10px", "marginBottom": "10px"},
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label(
                                id="sources-label",
                                className="form-label",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                id="select-all-button",
                                color="secondary",
                                outline=True,
                                size="sm",
                                className="mb-2 w-100",
                                style={"fontSize": "12px"},
                            ),
                            html.Div(id="data-sources-container"),
                            html.Div(
                                id="datasources-validation",
                                className="text-danger",
                                style={"fontSize": "12px"},
                            ),
                        ]
                    ),
                    # Key Findings button (only show if module is available)
                    html.Div(
                        [
                            dbc.Button(
                                [
                                    html.I(
                                        className="fas fa-brain",
                                        style={"marginRight": "8px"},
                                    ),
                                    html.Span(id="key-findings-button-text"),
                                    html.Div(
                                        id="key-findings-spinner",
                                        className="ms-2",
                                        style={"display": "none"},
                                        children=[
                                            dbc.Spinner(
                                                size="sm",
                                                color="light",
                                                spinner_style={
                                                    "width": "1rem",
                                                    "height": "1rem",
                                                },
                                            )
                                        ],
                                    ),
                                ],
                                id="generate-key-findings-btn",
                                color="info",
                                size="sm",
                                className="w-100 mb-2 position-relative",
                                style={
                                    "fontSize": "12px",
                                    "fontWeight": "bold",
                                    "transition": "all 0.2s ease",
                                },
                                disabled=False,
                            )
                        ],
                        id="key-findings-button-container",
                        style={
                            "display": "none",
                            "marginTop": "10px",
                            "marginBottom": "15px",
                        },
                    ),
                    html.Div(id="navigation-section", style={"display": "none"}),
                ],
                style={
                    "overflowY": "auto",
                    "overflowX": "hidden",
                    "height": "calc(100dvh - 120px)",
                    "paddingRight": "10px",
                },
            ),
            # Credits footer - always at bottom
            html.Div(
                [
                    html.Hr(style={"margin": "5px 0"}),
                    dbc.Button(
                        [
                            html.Span(
                                id="credits-button-text",
                                style={"fontSize": "10px", "fontWeight": "bold"},
                            ),
                            html.I(
                                id="credits-chevron",
                                className="fas fa-chevron-down",
                                style={"fontSize": "8px", "marginLeft": "5px"},
                            ),
                        ],
                        id="credits-toggle",
                        color="link",
                        size="sm",
                        style={
                            "color": "#6c757d",
                            "textDecoration": "none",
                            "padding": "2px 5px",
                            "fontSize": "10px",
                            "width": "100%",
                            "textAlign": "left",
                            "border": "none",
                            "backgroundColor": "transparent",
                            "marginBottom": "5px",
                        },
                    ),
                    # Citation button
                    dbc.Button(
                        [
                            html.I(
                                className="fas fa-quote-right",
                                style={"marginRight": "5px", "fontSize": "8px"},
                            ),
                            html.Span(
                                id="citation-button-text",
                                style={"fontSize": "9px", "fontWeight": "bold"},
                            ),
                        ],
                        id="citation-modal-toggle",
                        color="info",
                        size="sm",
                        outline=True,
                        style={
                            "fontSize": "9px",
                            "width": "100%",
                            "textAlign": "left",
                            "border": "1px solid #17a2b8",
                            "color": "#17a2b8",
                            "backgroundColor": "transparent",
                            "marginBottom": "10px",
                            "padding": "2px 5px",
                        },
                    ),
                    dbc.Collapse(
                        html.Div(
                            id="credits-content",
                            style={
                                "backgroundColor": "#f8f9fa",
                                "padding": "8px 2px 12px 2px",
                                "borderTop": "1px solid #dee2e6",
                                "marginTop": "5px",
                                "width": "100%",
                            },
                        ),
                        id="credits-collapse",
                        is_open=True,
                    ),
                ],
                style={
                    "position": "absolute",
                    "bottom": 0,
                    "left": 0,
                    "right": 0,
                    "backgroundColor": "#f3f4f6",
                    "padding": "5px 2px 10px 2px",
                },
            ),
        ],
        style={
            "backgroundColor": "#f3f4f6",
            "padding": "20px",
            "height": "100dvh",
            "position": "fixed",
            "width": "inherit",
            "display": "flex",
            "flexDirection": "column",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "boxShadow": "2px 0 5px rgba(0,0,0,0.1)",
        },
    )

    return sidebar


def create_header():
    """Create the header layout with title and language selector."""

    header = html.Div(
        [
            # Hamburger menu button — visible only on mobile (<992px)
            html.Button(
                html.I(className="fas fa-bars", style={"fontSize": "20px"}),
                id="sidebar-toggle-btn",
                className="d-lg-none sidebar-hamburger",
                style={
                    "background": "none",
                    "border": "none",
                    "color": "#495057",
                    "padding": "5px 10px",
                    "cursor": "pointer",
                    "position": "absolute",
                    "top": "10px",
                    "left": "10px",
                    "zIndex": 1001,
                },
                **{"n_clicks": 0},
            ),
            # Language selector in top-right corner (flags with language codes)
            html.Div(
                [
                    dcc.Dropdown(
                        id="language-selector",
                        options=[
                            {
                                "label": html.Div(
                                    [
                                        html.Span(
                                            "\U0001f1ea\U0001f1f8",
                                            style={
                                                "fontSize": "16px",
                                                "marginRight": "4px",
                                            },
                                        ),
                                        html.Span(
                                            "ES",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                    ],
                                    style={"display": "flex", "alignItems": "center"},
                                ),
                                "value": "es",
                            },
                            {
                                "label": html.Div(
                                    [
                                        html.Span(
                                            "\U0001f1fa\U0001f1f8",
                                            style={
                                                "fontSize": "16px",
                                                "marginRight": "4px",
                                            },
                                        ),
                                        html.Span(
                                            "EN",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                    ],
                                    style={"display": "flex", "alignItems": "center"},
                                ),
                                "value": "en",
                            },
                        ],
                        value="es",
                        clearable=False,
                        style={"width": "70px", "fontSize": "12px"},
                        searchable=False,
                        multi=False,
                    )
                ],
                className="lang-selector-wrapper",
                style={
                    "position": "absolute",
                    "top": "10px",
                    "right": "20px",
                    "zIndex": 1001,
                },
            ),
            # Text content
            html.Div(
                [
                    html.P(
                        id="header-subtitle",
                        className="header-subtitle",
                        style={
                            "margin": "5px 0",
                            "fontSize": "14px",
                            "fontStyle": "italic",
                            "textAlign": "center",
                            "color": "#6c757d",
                        },
                    ),
                    html.H3(
                        id="header-title",
                        className="header-title",
                        style={
                            "margin": "8px 0",
                            "fontSize": "18px",
                            "fontWeight": "bold",
                            "textAlign": "center",
                            "color": "#212529",
                            "lineHeight": "1.3",
                        },
                    ),
                    html.P(
                        id="header-credits",
                        className="header-credits-text",
                        style={
                            "margin": "5px 0",
                            "fontSize": "13px",
                            "textAlign": "center",
                            "color": "#495057",
                        },
                    ),
                ],
                style={"flex": 1, "textAlign": "center"},
            ),
        ],
        style={
            "position": "sticky",
            "top": 0,
            "zIndex": 1000,
            "backgroundColor": "#ffffff",
            "padding": "15px 20px",
            "borderBottom": "2px solid #dee2e6",
            "width": "100%",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            "marginBottom": "20px",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
        },
    )

    return header


def create_notes_modal():
    """Create the notes modal for displaying methodological information."""

    notes_modal = dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(id="notes-modal-title", style={"fontSize": "16px"})
            ),
            dbc.ModalBody(id="notes-content"),
            dbc.ModalFooter(dbc.Button(id="close-notes-modal", className="ml-auto")),
        ],
        id="notes-modal",
        size="lg",
        centered=True,
    )

    return notes_modal


def create_key_findings_modal():
    """Create the Key Findings modal for displaying AI-generated insights."""

    key_findings_modal = dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    get_text("key_findings_modal_title", "es"),
                    id="key-findings-modal-title",
                )
            ),
            dbc.ModalBody(id="key-findings-modal-body"),
            dbc.ModalFooter(
                [
                    html.A(
                        [
                            html.I(
                                className="fas fa-file-pdf",
                                style={"marginRight": "5px"},
                            ),
                            html.Span(id="export-pdf-text"),
                        ],
                        id="export-pdf-link",
                        href="",
                        download="key_findings.pdf",
                        className="btn btn-success me-2 d-flex align-items-center",
                        style={"textDecoration": "none", "display": "none"},
                    ),
                    dbc.Button(
                        "Cerrar",
                        id="close-key-findings-modal",
                        color="secondary",
                        className="me-2",
                    ),
                ]
            ),
        ],
        id="key-findings-modal",
        size="xl",
        centered=True,
        backdrop="static",
    )

    return key_findings_modal


def create_citation_modal():
    """Create the citation modal for generating and downloading citations."""

    citation_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(id="citation-modal-title")),
            dbc.ModalBody(id="citation-modal-body"),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        id="close-citation-modal",
                        color="secondary",
                        className="me-2",
                    ),
                    html.A(
                        [
                            html.I(
                                className="fas fa-download",
                                style={"marginRight": "5px"},
                            ),
                            html.Span(id="download-current-ris-text"),
                        ],
                        id="download-current-ris",
                        href="",
                        download="dashboard_citation.ris",
                        className="btn btn-success btn-sm",
                        style={"textDecoration": "none"},
                    ),
                ]
            ),
        ],
        id="citation-modal",
        size="lg",
        centered=True,
        backdrop="static",
    )

    return citation_modal


def create_copy_toast():
    """Create the toast notification for copy functionality."""

    copy_toast = dbc.Toast(
        [
            html.Div("Citation copied to clipboard!", className="toast-body"),
        ],
        id="copy-toast",
        header="Success",
        icon="success",
        dismissable=True,
        is_open=False,
        style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "zIndex": "9999",
        },
    )

    return copy_toast


def create_layout():
    """Create the main dashboard layout.

    Returns:
        The complete layout for the Dash app
    """

    sidebar = create_sidebar()
    header = create_header()
    notes_modal = create_notes_modal()

    layout = dbc.Container(
        [
            # Mobile sidebar backdrop overlay
            html.Div(
                id="sidebar-backdrop",
                className="sidebar-backdrop",
                n_clicks=0,
            ),
            dbc.Row(
                [
                    # Sidebar: visible on desktop (lg+), hidden on mobile
                    dbc.Col(
                        [sidebar],
                        id="sidebar-col",
                        lg=2,
                        className="bg-light d-none d-lg-block sidebar-column",
                    ),
                    # Main content: full width on mobile, 10/12 on desktop
                    dbc.Col(
                        [
                            header,
                            html.Div(
                                id="main-title",
                                style={"fontSize": "18px", "marginBottom": "10px"},
                            ),
                            dcc.Store(id="data-sources-store-v2", data=[]),
                            dcc.Store(
                                id="language-store", data="es"
                            ),
                            dcc.Store(id="key-findings-button-state", data="idle"),
                            dcc.Store(
                                id="key-findings-content-ready", data=False
                            ),
                            dcc.Store(
                                id="key-findings-data-ready", data=None
                            ),
                            dcc.Store(
                                id="current-url-store", data=""
                            ),
                            dcc.Store(
                                id="react-warning-suppression", data=False
                            ),
                            dcc.Store(
                                id="copy-store-citation", data=""
                            ),
                            dcc.Store(
                                id="copy-success", data=False
                            ),
                            # Store to track sidebar open state on mobile
                            dcc.Store(id="sidebar-open-store", data=False),
                            dcc.Loading(
                                id="loading-main-content",
                                type="circle",
                                children=[
                                    html.Div(
                                        id="main-content",
                                        className="w-100",
                                        style={
                                            "height": "calc(100dvh - 200px)",
                                            "overflowY": "auto",
                                            "overflowX": "hidden",
                                            "paddingRight": "10px",
                                            "scrollBehavior": "smooth",
                                        },
                                    )
                                ],
                                style={"height": "calc(100dvh - 200px)"},
                            ),
                        ],
                        lg=10,
                        xs=12,
                        className="px-4 main-content-col",
                        style={"height": "100dvh", "overflow": "hidden"},
                    ),
                ],
                className="gx-0",
                style={"height": "100dvh"},
            ),
            notes_modal,
            create_key_findings_modal(),
            create_citation_modal(),
            create_copy_toast(),
            dcc.Store(id="copy-store", data=""),
        ],
        fluid=True,
        className="px-0",
        style={"height": "100dvh"},
    )

    return layout
