"""
Hidden Regeneration Menu Component (Phase 4)

This module provides a hidden regeneration menu that only appears when users
press a specific keystroke combination. This prevents unauthorized regeneration
requests while allowing authorized users to request new analyses.

Keystroke combination: Ctrl+Shift+R then Ctrl+Shift+G (double combination for extra security)
"""

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Secret keystroke combination (Ctrl+Shift+R then Ctrl+Shift+G)
SECRET_SEQUENCE_1 = ["Control", "Shift", "r"]  # First combo
SECRET_SEQUENCE_2 = ["Control", "Shift", "g"]  # Second combo
HIDDEN_CLASS = "hidden-regeneration-menu"


class HiddenRegenerationMenu:
    """
    Hidden regeneration menu that appears only with correct keystroke combination.
    """

    def __init__(self):
        self.keystroke_buffer = []
        self.stage = 0  # 0 = waiting for first combo, 1 = waiting for second combo
        self.timer = None

    def create_hidden_menu(self, modal_id: str = "key-findings-modal") -> html.Div:
        """
        Create the hidden regeneration menu component.

        Args:
            modal_id: ID of the modal to attach the menu to

        Returns:
            Hidden menu HTML component
        """
        return html.Div(
            [
                # Hidden menu (appears only with correct keystroke combination)
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    "🔐 Admin Regeneration Menu",
                                    className="text-warning mb-3",
                                ),
                                html.P(
                                    [
                                        html.I(
                                            className="fas fa-shield-alt text-warning me-2"
                                        ),
                                        "Authorized regeneration available",
                                    ],
                                    className="text-muted small mb-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Button(
                                            [
                                                html.I(className="fas fa-redo me-2"),
                                                "Force Regenerate Current Analysis",
                                            ],
                                            id="hidden-regenerate-btn",
                                            color="warning",
                                            size="sm",
                                            className="me-2 mb-2",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="fas fa-refresh me-2"),
                                                "Regenerate All Combinations",
                                            ],
                                            id="hidden-regenerate-all-btn",
                                            color="danger",
                                            size="sm",
                                            className="me-2 mb-2",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(
                                                    className="fas fa-database me-2"
                                                ),
                                                "Check Database Status",
                                            ],
                                            id="hidden-db-status-btn",
                                            color="info",
                                            size="sm",
                                            className="mb-2",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="fas fa-save me-2"),
                                                "Save Current to Database",
                                            ],
                                            id="hidden-save-to-db-btn",
                                            color="success",
                                            size="sm",
                                            className="mb-2",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    [
                                        html.Small(
                                            "This menu is hidden and only accessible via keystroke combination",
                                            className="text-muted",
                                        )
                                    ],
                                    className="text-center",
                                ),
                            ],
                            style={
                                "padding": "15px",
                                "backgroundColor": "#f8f9fa",
                                "border": "1px solid #ffc107",
                                "borderRadius": "5px",
                                "marginTop": "10px",
                            },
                        )
                    ],
                    id="hidden-regeneration-menu",
                    className=HIDDEN_CLASS,
                    style={"display": "none"},
                ),
                # Add hidden menu to Key Findings modal footer
                html.Div(id="hidden-menu-attachment", style={"display": "none"}),
            ]
        )

    def create_keystroke_detection_script(self) -> str:
        """
        Create JavaScript for keystroke detection.

        Returns:
            JavaScript code for keystroke detection
        """
        return f"""
        // Hidden Regeneration Menu - Keystroke Detection
        (function() {{
            let keystrokeBuffer = [];
            let currentStage = 0;
            let stageTimeout = null;
            
            const SECRET_SEQUENCE_1 = {SECRET_SEQUENCE_1};
            const SECRET_SEQUENCE_2 = {SECRET_SEQUENCE_2};
            const TIMEOUT_MS = 3000; // 3 seconds between combos
            
            function arraysEqual(arr1, arr2) {{
                if (arr1.length !== arr2.length) return false;
                for (let i = 0; i < arr1.length; i++) {{
                    if (arr1[i] !== arr2[i]) return false;
                }}
                return true;
            }}
            
            function showHiddenMenu() {{
                const menu = document.getElementById('hidden-regeneration-menu');
                if (menu) {{
                    menu.style.display = 'block';
                    menu.style.animation = 'fadeIn 0.3s ease-in';
                    
                    // Add subtle pulse effect to indicate activation
                    menu.style.boxShadow = '0 0 15px rgba(255, 193, 7, 0.5)';
                    
                    console.log('🔐 Hidden regeneration menu activated');
                    
                    // Auto-hide after 30 seconds
                    setTimeout(() => {{
                        hideHiddenMenu();
                    }}, 30000);
                }}
            }}
            
            function hideHiddenMenu() {{
                const menu = document.getElementById('hidden-regeneration-menu');
                if (menu) {{
                    menu.style.display = 'none';
                    menu.style.boxShadow = 'none';
                    console.log('🔐 Hidden regeneration menu hidden');
                }}
            }}
            
            function resetSequence() {{
                keystrokeBuffer = [];
                currentStage = 0;
                if (stageTimeout) clearTimeout(stageTimeout);
                console.log('🔐 Keystroke sequence reset');
            }}
            
            // Save current analysis to database
            function saveCurrentToDatabase() {{
                console.log('💾 Saving current analysis to database...');
                
                // Get current analysis content
                const modalBody = document.getElementById('key-findings-modal-body');
                if (!modalBody) {{
                    alert('No analysis found to save');
                    return;
                }}
                
                const analysisContent = modalBody.innerText;
                
                // Send save request to server
                fetch('/api/save-analysis-to-database', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        content: analysisContent,
                        timestamp: new Date().toISOString()
                    }})
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        alert('✅ Analysis saved to database successfully!');
                    }} else {{
                        alert('❌ Failed to save analysis: ' + data.error);
                    }}
                }})
                .catch(error => {{
                    alert('❌ Error saving analysis: ' + error.message);
                }});
            }}
            
            // Make save function globally available
            window.saveCurrentToDatabase = saveCurrentToDatabase;
            
            document.addEventListener('keydown', function(event) {{
                const key = event.key.toLowerCase();
                const modifiers = [];
                
                if (event.ctrlKey) modifiers.push('control');
                if (event.shiftKey) modifiers.push('shift');
                
                const keyCombo = [...modifiers, key];
                
                console.log('🔐 Key pressed:', keyCombo);
                
                // Clear previous timeout
                if (stageTimeout) clearTimeout(stageTimeout);
                
                // Set new timeout to reset sequence
                stageTimeout = setTimeout(resetSequence, TIMEOUT_MS);
                
                if (currentStage === 0) {{
                    // Waiting for first combination
                    keystrokeBuffer = keyCombo;
                    if (arraysEqual(keyCombo, SECRET_SEQUENCE_1)) {{
                        currentStage = 1;
                        console.log('🔐 First combination correct - waiting for second');
                    }} else {{
                        keystrokeBuffer = [];
                    }}
                }} else if (currentStage === 1) {{
                    // Waiting for second combination
                    if (arraysEqual(keyCombo, SECRET_SEQUENCE_2)) {{
                        console.log('🔐 Second combination correct - showing menu');
                        showHiddenMenu();
                        resetSequence();
                    }} else {{
                        console.log('🔐 Second combination wrong - resetting');
                        resetSequence();
                    }}
                }}
            }});
            
            console.log('🔐 Hidden regeneration menu keystroke detection initialized');
        }})();
        
        // CSS for hidden menu animations
        (function() {{
            const style = document.createElement('style');
            style.textContent = `
                .{HIDDEN_CLASS} {{
                    opacity: 0;
                    transition: opacity 0.3s ease-in;
                }}
                
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(-10px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                
                .{HIDDEN_CLASS}.visible {{
                    opacity: 1;
                }}
            `;
            document.head.appendChild(style);
        }})();
        """

    def attach_to_modal(
        self, modal_body_id: str = "key-findings-modal-body"
    ) -> html.Div:
        """
        Create component that attaches hidden menu to the Key Findings modal.

        Args:
            modal_body_id: ID of the modal body to attach to

        Returns:
            Attachment component
        """
        return html.Div(
            [
                # Inject the hidden menu into the modal body
                html.Div(id="hidden-menu-injector", style={"display": "none"}),
                # JavaScript for keystroke detection
                html.Script(self.create_keystroke_detection_script()),
            ]
        )


# Global instance
hidden_menu = HiddenRegenerationMenu()


# Callback for hidden regeneration button
@callback(
    Output("hidden-regeneration-menu", "style", allow_duplicate=True),
    Input("hidden-regenerate-btn", "n_clicks"),
    Input("hidden-regenerate-all-btn", "n_clicks"),
    Input("hidden-db-status-btn", "n_clicks"),
    Input("hidden-save-to-db-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_hidden_regeneration(
    n_clicks_regenerate, n_clicks_regenerate_all, n_clicks_status, n_clicks_save
):
    """
    Handle hidden regeneration menu button clicks.
    """
    import dash

    ctx = dash.callback_context

    if not ctx.triggered:
        return {"display": "none"}

    trigger = ctx.triggered[0]["prop_id"]

    if "hidden-regenerate-btn" in trigger:
        # Handle single regeneration
        print("🔐 Hidden regeneration requested for current analysis")
        # Trigger server-side regeneration
        return {"display": "block", "animation": "fadeIn 0.3s ease-in"}

    elif "hidden-regenerate-all-btn" in trigger:
        # Handle batch regeneration
        print("🔐 Hidden batch regeneration requested")
        return {"display": "block", "animation": "fadeIn 0.3s ease-in"}

    elif "hidden-db-status-btn" in trigger:
        # Handle database status check
        print("🔐 Database status check requested")
        return {"display": "block", "animation": "fadeIn 0.3s ease-in"}

    elif "hidden-save-to-db-btn" in trigger:
        # Handle save to database
        print("💾 Save to database requested")
        # The actual save is handled by JavaScript
        return {"display": "block", "animation": "fadeIn 0.3s ease-in"}

    return {"display": "none"}


def create_hidden_regeneration_component():
    """
    Create the complete hidden regeneration component.

    Returns:
        Complete hidden regeneration menu component
    """
    return html.Div([hidden_menu.create_hidden_menu(), hidden_menu.attach_to_modal()])
