import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.fft import fft, fftfreq
from typing import Dict, List, Any
import warnings
import os
import sys
import re
import time
import asyncio
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not available, using existing environment variables")

# Add parent directory to path for database imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings("ignore")

# Import tools dictionary and database manager
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from tools import tool_file_dic, get_tool_options, translate_tool_key, get_tool_name
from database import get_database_manager

# Import centralized configuration
from dashboard_config import get_dashboard_url, get_citation_url, get_ris_url

# Import centralized source mapping
from fix_source_mapping import (
    map_display_names_to_source_ids,
    DBASE_OPTIONS as dbase_options,
    DISPLAY_NAMES,
)

# Import translation system
from translations import (
    get_text,
    get_available_languages,
    get_language_name,
    translate_database_content,
    translate_source_name,
)

# Import layout components
from layout import create_layout

# Import UI callbacks
from callbacks import register_ui_callbacks

# Import modular callback systems
from callbacks.main_callbacks import register_main_callbacks
from callbacks.graph_callbacks import register_graph_callbacks
from callbacks.kf_callbacks import register_kf_callbacks

# Import utility functions extracted for better organization
from utils import (
    parse_text_with_links,
    get_cache_key,
    get_cached_processed_data,
    cache_processed_data,
    get_all_keywords,
    _generate_pca_insights,
    get_cache_stats,
    create_combined_dataset,
    create_combined_dataset2,
    get_current_date_for_citation,
    run_async_in_sync_context,
    create_temporal_2d_figure,
    create_mean_analysis_figure,
    perform_comprehensive_pca_analysis,
    create_pca_figure,
    create_correlation_heatmap,
    # Import cache variables as well
    _processed_data_cache,
    _cache_max_size,
)

try:
    from key_findings import KeyFindingsService, KeyFindingsModal

    KEY_FINDINGS_AVAILABLE = True
    print("✅ Key Findings module loaded successfully")
except ImportError as e:
    print(f"❌ Warning: Key Findings module not available: {e}")
    KEY_FINDINGS_AVAILABLE = False
# DOCKER_FIX: Enhanced imports for Docker compatibility
try:
    from translations import enhanced_translate_source_name
    from fix_source_mapping import enhanced_display_names_to_ids
    from fix_dataframe_indexing import (
        create_translation_mapping,
        get_original_column_name,
        safe_dataframe_column_access,
    )

    # Replace functions with enhanced versions
    translate_source_name = enhanced_translate_source_name
    map_display_names_to_source_ids = enhanced_display_names_to_ids
    print("Loaded enhanced translation functions for Docker environment")
except ImportError as e:
    print(f"Warning: Could not load enhanced functions: {e}")

    # Fallback functions for non-Docker environments
    def create_translation_mapping(selected_source_ids, language):
        """Fallback implementation of create_translation_mapping"""
        translation_mapping = {}
        for src_id in selected_source_ids:
            original_name = dbase_options.get(src_id, "NOT FOUND")
            translated_name = translate_source_name(original_name, language)
            translation_mapping[translated_name] = original_name
            translated_name_simple = translated_name.replace(" - ", " ")
            translation_mapping[translated_name_simple] = original_name
        return translation_mapping

    def get_original_column_name(display_name, translation_mapping):
        """Fallback implementation of get_original_column_name"""
        return translation_mapping.get(display_name, display_name)

    def safe_dataframe_column_access(data, translated_name, translation_mapping):
        """Fallback implementation of safe_dataframe_column_access"""
        original_name = get_original_column_name(translated_name, translation_mapping)
        if original_name in data.columns:
            return data[original_name]
        elif translated_name in data.columns:
            return data[translated_name]
        else:
            print(
                f"WARNING: Column '{translated_name}' (original: '{original_name}') not found in DataFrame"
            )
            return None


# Get database manager instance
db_manager = get_database_manager()

# Initialize Key Findings service if available (will be initialized after app is created)
key_findings_service = None


def initialize_key_findings_service():
    """Initialize Key Findings service after app is created"""
    global key_findings_service, KEY_FINDINGS_AVAILABLE
    if KEY_FINDINGS_AVAILABLE and key_findings_service is None:
        try:
            print("🔍 DEBUG: Starting Key Findings service initialization...")

            # SIMPLIFIED: Use direct database access without caching layer
            config = {}
            api_key = os.getenv("OPENROUTER_API_KEY")
            print(f"🔍 DEBUG: API key loaded: {bool(api_key)}")

            # Initialize service using factory function
            print("🔍 DEBUG: Importing Key Findings components...")
            from key_findings.key_findings_service import get_key_findings_service

            print("🔍 DEBUG: Creating Key Findings service instance...")
            groq_api_key = os.getenv("GROQ_API_KEY") or ""
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY") or ""

            key_findings_service = get_key_findings_service(
                db_manager, groq_api_key, openrouter_api_key, config
            )

            print("✅ Key Findings service initialized successfully")

            print("✅ Key Findings service initialized successfully")

            # Skip model availability testing to avoid quota usage
            print("ℹ️  Skipping model availability testing to preserve API quota")

        except Exception as e:
            print(f"❌ Error initializing Key Findings service: {e}")
            import traceback

            traceback.print_exc()
            KEY_FINDINGS_AVAILABLE = False


# Initialize KeyFindingsService modal component (after service is initialized)
try:
    if KEY_FINDINGS_AVAILABLE and key_findings_service:
        from key_findings.modal_component import KeyFindingsModal
        from dash import dcc

        # Create a simple language store reference for the modal component
        # The component will use this to access the actual language state during callbacks
        class LanguageStoreRef:
            def __init__(self):
                self.id = "language-store"

        language_store_ref = LanguageStoreRef()
        key_findings_service.set_modal_component(app, language_store_ref)
        print("✅ KeyFindingsService modal component initialized")
except Exception as modal_error:
    print(f"⚠️ Error initializing KeyFindingsService modal component: {modal_error}")
    import traceback

    traceback.print_exc()


# Notes and DOI data is now loaded from the database


# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Management Tools Analysis Dashboard - " + str(time.time()),
    update_title=None,  # Suppress title updates to reduce console noise
)

# Suppress React warnings in development mode
try:
    if app.config.get("DEBUG", False):
        import logging

        logging.getLogger("werkzeug").setLevel(logging.WARNING)
        # Suppress some React warnings by setting environment variables
        import os

        # Suppress React deprecation warnings
        os.environ["REACT_DISABLE_STRICT_MODE_WARNINGS"] = "true"
        os.environ["REACT_DISABLE_FIND_DOM_NODE_WARNINGS"] = "true"
        # Additional React warnings suppression
        os.environ["DASH_SUPPRESS_CALLBACK_EXCEPTIONS"] = "true"
        # Suppress React 18 warnings
        os.environ["NODE_ENV"] = (
            "production"  # Reduces React warnings in production mode
        )
except KeyError:
    # Fallback if DEBUG key doesn't exist
    pass

# ============================================================================
# Production: Expose Flask server and add health check endpoint
# ============================================================================

# Get the underlying Flask server for production deployment
server = app.server


# Add health check endpoint for Dokploy monitoring
@server.route("/health")
def health_check():
    """Health check endpoint for container orchestration and monitoring"""
    from datetime import datetime
    import json

    try:
        db_status = "connected" if db_manager else "unavailable"
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "service": "management-tools-dashboard",
            "database": db_status,
        }
        return json.dumps(health_status), 200, {"Content-Type": "application/json"}
    except Exception as e:
        error_status = {"status": "unhealthy", "error": str(e)}
        return json.dumps(error_status), 500, {"Content-Type": "application/json"}


# Add basic security headers for production
@server.after_request
def add_security_headers(response):
    """Add security headers configured for Dash/Plotly compatibility"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


# Add custom CSS to suppress some browser console warnings
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .nav-link:hover {
                background-color: #e9ecef !important;
                color: #0056b3 !important;
                text-decoration: none !important;
            }
            .nav-link {
                transition: all 0.2s ease;
                font-size: 10px !important;
            }
            html {
                scroll-behavior: smooth;
            }
            .section-anchor {
                scroll-margin-top: 100px;
            }
            /* Suppress some Plotly canvas warnings */
            canvas {
                will-change: auto !important;
            }
            /* Responsive section spacing to prevent overlaps */
            .section-anchor {
                margin-bottom: 20px;
                clear: both;
            }
            #section-mean-analysis {
                min-height: 700px;
                margin-bottom: 60px !important;
            }
            #section-temporal-3d {
                margin-top: 80px !important;
                min-height: 600px;
            }
            /* Responsive adjustments for different screen sizes */
            @media (max-width: 1200px) {
                #section-mean-analysis {
                    min-height: 650px;
                    margin-bottom: 50px !important;
                }
                #section-temporal-3d {
                    margin-top: 60px !important;
                    min-height: 650px;
                }
            }
            @media (max-width: 768px) {
                #section-mean-analysis {
                    min-height: 600px;
                    margin-bottom: 40px !important;
                }
                #section-temporal-3d {
                    margin-top: 50px !important;
                    min-height: 650px;
                }
            }
            /* Ensure graphs maintain their heights */
            .js-plotly-plot {
                min-height: inherit !important;
            }
            /* Prevent margin collapse and ensure section separation */
            .section-anchor + .section-anchor {
                margin-top: 20px;
            }
            /* Force section separation */
            #section-mean-analysis + #section-temporal-3d {
                margin-top: 80px !important;
            }
            /* Ensure content flows properly */
            .w-100 {
                box-sizing: border-box;
            }
            /* Key Findings modal font size overrides */
            .executive-summary-text {
                font-size: 10px !important;
                line-height: 1.7 !important;
            }
            .principal-findings-text {
                font-size: 8px !important;
                line-height: 1.6 !important;
            }
            .pca-analysis-text {
                font-size: 8px !important;
                line-height: 1.6 !important;
            }
            /* Key Findings modal title font size */
            .modal-title {
                font-size: 20px !important;
            }
            /* Pulse animation for spinner */
            @keyframes pulse {
                0% {
                    transform: scale(1);
                    opacity: 1;
                }
                50% {
                    transform: scale(1.1);
                    opacity: 0.7;
                }
                100% {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            
            /* Shake animation for button click feedback */
            @keyframes shake {
                0%, 100% {
                    transform: translateX(0) scale(0.98);
                }
                25% {
                    transform: translateX(-2px) scale(0.98);
                }
                75% {
                    transform: translateX(2px) scale(0.98);
                }
            }
            
            /* Bounce animation for button reset feedback */
            @keyframes bounce {
                0% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.05);
                }
                100% {
                    transform: scale(1);
                }
            }
        </style>
        <script>
            // Suppress React warnings in console
            const originalWarn = console.warn;
            console.warn = function(...args) {
                if (args[0] && typeof args[0] === 'string' &&
                    (args[0].includes('componentWillMount') ||
                     args[0].includes('componentWillReceiveProps') ||
                     args[0].includes('findDOMNode'))) {
                    return; // Suppress these specific warnings
                }
                originalWarn.apply(console, args);
            };

            // Language detection and persistence
            function getBrowserLanguage() {
                const lang = navigator.language || navigator.userLanguage;
                return lang.startsWith('es') ? 'es' : 'en';
            }

            function getStoredLanguage() {
                return localStorage.getItem('dashboard-language');
            }

            function setStoredLanguage(lang) {
                localStorage.setItem('dashboard-language', lang);
            }

            // Initialize language on page load
            document.addEventListener('DOMContentLoaded', function() {
                let initialLang = getStoredLanguage() || getBrowserLanguage();
                // Trigger language change if not Spanish
                if (initialLang !== 'es') {
                    // Small delay to ensure Dash is ready
                    setTimeout(() => {
                        const languageSelector = document.querySelector('[id*="language-selector"]');
                        if (languageSelector) {
                            languageSelector.value = initialLang;
                            languageSelector.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    }, 100);
                }
            });

            // Listen for language changes and store them
            document.addEventListener('change', function(e) {
                if (e.target.matches('[id*="language-selector"]')) {
                    setStoredLanguage(e.target.value);
                }
            });

            // Function to get current URL for fuente/source attribution
            function getCurrentUrl() {
                return window.location.href;
            }

            // Update URL store with current URL
            function updateCurrentURLStore() {
                const currentUrl = getCurrentUrl();
                // Find the hidden URL store element and update it directly
                const urlStore = document.querySelector('[id*="current-url-store"]');
                if (urlStore) {
                    // Create a custom event to trigger the clientside callback
                    const event = new CustomEvent('urlUpdate', { detail: currentUrl });
                    urlStore.dispatchEvent(event);
                }
            }

            // Update URL on page load
            document.addEventListener('DOMContentLoaded', function() {
                // Small delay to ensure Dash is ready
                setTimeout(updateCurrentURLStore, 100);
            });

            // Update URL on navigation (for SPAs)
            window.addEventListener('popstate', function() {
                setTimeout(updateCurrentURLStore, 100);
            });

            // Also update URL periodically (every 30 seconds) in case of direct navigation
            setInterval(function() {
                updateCurrentURLStore();
            }, 30000);

            // Simple manual control for credits - auto-collapse handled by Dash callback
            // when both keyword and sources are selected
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


# Database options are now imported from fix_source_mapping module

# Define color palette for consistent use across buttons and graphs
colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
]

# Define consistent colors for each source by display name (used in buttons)
source_colors_by_display = {
    "Google Trends": "#1f77b4",
    "Google Books": "#ff7f0e",
    "Bain Usability": "#d62728",
    "Bain Satisfaction": "#9467bd",
    "Crossref": "#2ca02c",  # Changed from brown to green
}

# Define consistent colors for each source by database name (used in graphs)
source_colors_by_db = {
    "Google Trends": "#1f77b4",
    "Google Books Ngrams": "#ff7f0e",
    "Bain - Usabilidad": "#d62728",
    "Bain - Satisfacción": "#9467bd",
    "Crossref.org": "#2ca02c",  # Changed from brown to green
}

# Create color_map using the database name colors
color_map = {
    dbase_options[key]: source_colors_by_db.get(
        dbase_options[key], colors[i % len(colors)]
    )
    for i, key in enumerate(dbase_options.keys())
}

# Create and set the main layout using the layout module
app.layout = create_layout()

# Register all callback modules
register_ui_callbacks(app)
register_main_callbacks(app)
register_graph_callbacks(app)

# Initialize Key Findings service after app is created
initialize_key_findings_service()

# Register Key Findings callbacks if service is available
if KEY_FINDINGS_AVAILABLE and key_findings_service:
    register_kf_callbacks(app, key_findings_service, KEY_FINDINGS_AVAILABLE)


def get_current_date_for_citation(language="es"):
    """
    Get the current date formatted for citation styles.

    Args:
        language (str): Language code ('es' or 'en')

    Returns:
        dict: Dictionary with date formats for different citation styles
    """
    now = datetime.now()

    if language == "es":
        # Spanish formats
        day = now.day
        month_names = [
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre",
        ]
        month_name = month_names[now.month - 1]
        year = now.year

        return {
            "chicago": f"{day} de {month_name} de {year}",
            "oscola": f"{day} de {month_name} de {year}",
            "vancouver": f"{day} de {month_name} de {year}",
            "apa": f"{day} de {month_name} de {year}",
            "mla": f"{day} {month_name} {year}",
            "ieee": f"{day} {month_name} {year}",
        }
    else:
        # English formats
        month_names = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        month_name = month_names[now.month - 1]
        day = now.day
        year = now.year

        return {
            "chicago": f"{month_name} {day}, {year}",
            "oscola": f"{day} {month_name} {year}",
            "vancouver": f"{year} {month_name} {day}",
            "apa": f"{month_name} {day}, {year}",
            "mla": f"{day} {month_name} {year}",
            "ieee": f"{month_name} {day}, {year}",
        }


def run_async_in_sync_context(async_func, *args, **kwargs):
    """
    Run an async function in a synchronous context with proper error handling.

    This function handles the common case where async functions need to be called
    from synchronous Dash callbacks without causing event loop conflicts.

    Args:
        async_func: The async function to call
        *args: Positional arguments to pass to the async function
        **kwargs: Keyword arguments to pass to the async function

    Returns:
        The result of the async function, or an error response if execution fails
    """
    try:
        # Check if we're already in an event loop
        try:
            loop = asyncio.get_running_loop()
            print("🔍 Detected running event loop, using create_task")
            # If we're in a running loop, we need to use a different approach
            # This is a complex case - for now, we'll use a simple workaround
            # by creating a new thread to run the async function
            import concurrent.futures
            import threading

            def run_in_thread():
                # Create a new event loop in the thread
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(async_func(*args, **kwargs))
                finally:
                    new_loop.close()

            # Run in a separate thread to avoid event loop conflicts
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result(timeout=30)  # 30 second timeout

        except RuntimeError:
            # No running loop, we can use run_until_complete
            print("🔍 No running event loop, using run_until_complete")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(async_func(*args, **kwargs))
            finally:
                loop.close()

    except Exception as e:
        print(f"❌ Error running async function in sync context: {e}")
        import traceback

        traceback.print_exc()

        # Return a standardized error response
        return {
            "success": False,
            "error": f"Async execution failed: {str(e)}",
            "content": {},
            "model_used": "error",
            "response_time_ms": 0,
            "token_count": 0,
        }


# Callbacks


# Language management callback moved to callbacks/ui_callbacks.py


# Current URL management callback - Dynamic URL detection (clientside only)

# Clientside callback for dynamic URL detection (JavaScript)
app.clientside_callback(
    """
    function getCurrentURL(loadingMainContent, language) {
        // Use the dedicated function to get current URL
        return getCurrentUrl();
    }
    """,
    Output("current-url-store", "data"),
    Input("loading-main-content", "children"),
    Input("language-store", "data"),
    prevent_initial_call=False,
)

# Clientside callback to suppress React findDOMNode warnings
app.clientside_callback(
    """
    function suppressReactWarnings() {
        // Suppress findDOMNode warnings in browser console
        if (typeof console !== 'undefined' && console.warn) {
            const originalWarn = console.warn;
            console.warn = function(...args) {
                const message = args[0];
                if (typeof message === 'string' &&
                    (message.includes('findDOMNode is deprecated') ||
                     message.includes('StrictMode'))) {
                    return; // Suppress these specific warnings
                }
                return originalWarn.apply(console, args);
            };
        }

        // Also suppress console.error for findDOMNode warnings
        if (typeof console !== 'undefined' && console.error) {
            const originalError = console.error;
            console.error = function(...args) {
                const message = args[0];
                if (typeof message === 'string' &&
                    message.includes('findDOMNode is deprecated')) {
                    return; // Suppress findDOMNode error warnings
                }
                return originalError.apply(console, args);
            };
        }

        return true;
    }
    """,
    Output("react-warning-suppression", "data"),
    Input("language-store", "data"),  # Add input to trigger callback
    prevent_initial_call=False,
)

# Clientside callback to copy citation text to clipboard
app.clientside_callback(
    """
    function copyToClipboard(data) {
        if (data && data !== "") {
            // Create a temporary textarea element
            const textarea = document.createElement('textarea');
            textarea.value = data;
            document.body.appendChild(textarea);
            
            // Select and copy the text
            textarea.select();
            document.execCommand('copy');
            
            // Remove the temporary element
            document.body.removeChild(textarea);
            
            return true;
        }
        return false;
    }
    """,
    Output("copy-success", "data"),
    Input("copy-store", "data"),
    prevent_initial_call=True,
)

# Clientside callback for immediate button feedback
app.clientside_callback(
    """
    function showImmediateFeedback(n_clicks) {
        if (n_clicks && n_clicks > 0) {
            // Get the button element
            const button = document.getElementById('generate-key-findings-btn');
            const spinnerContainer = document.getElementById('key-findings-spinner');
            const buttonText = document.getElementById('key-findings-button-text');
            
            if (button && spinnerContainer && buttonText) {
                console.log('🔄 CLIENTSIDE: Showing immediate feedback');
                
                // Immediately show processing state with enhanced visual feedback
                button.disabled = true;
                button.style.backgroundColor = '#f8f9fa';
                button.style.color = '#8b0000';
                button.style.border = '2px solid #8b0000';
                button.style.cursor = 'not-allowed';
                button.style.opacity = '0.8';
                button.style.transform = 'scale(0.98)';
                button.style.boxShadow = '0 0 10px rgba(139, 0, 0, 0.3)';

                // Update text immediately
                buttonText.textContent = '⏳ Procesando...';
                
                // Show spinner with animation
                spinnerContainer.style.display = 'inline-block';
                spinnerContainer.style.animation = 'pulse 1.5s infinite';
                
                // Store original state for potential restoration
                if (!button.hasAttribute('data-original-state')) {
                    button.setAttribute('data-original-state', JSON.stringify({
                        backgroundColor: button.style.backgroundColor || '#17a2b8',
                        color: button.style.color || 'white',
                        border: button.style.border || '1px solid #17a2b8',
                        cursor: button.style.cursor || 'pointer',
                        opacity: button.style.opacity || '1',
                        transform: button.style.transform || 'scale(1)',
                        boxShadow: button.style.boxShadow || 'none',
                        disabled: button.disabled,
                        pointerEvents: button.style.pointerEvents || 'auto'
                    }));
                }
                
                // Add a subtle shake animation to draw attention
                button.style.animation = 'shake 0.3s ease-in-out';
                setTimeout(() => {
                    if (button && button.style) {
                        button.style.animation = '';
                    }
                }, 300);
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("key-findings-button-state", "data", allow_duplicate=True),
    Input("generate-key-findings-btn", "n_clicks"),
    prevent_initial_call=True,
)

# Combined clientside callback to handle all button state changes
app.clientside_callback(
    """
    function handleButtonState(modal_is_open, close_clicks, button_clicks) {
        const button = document.getElementById('generate-key-findings-btn');
        const spinnerContainer = document.getElementById('key-findings-spinner');
        const buttonText = document.getElementById('key-findings-button-text');
        
        if (!button || !spinnerContainer || !buttonText) {
            return window.dash_clientside.no_update;
        }
        
        // Handle modal close (either via X or Cerrar button)
        if (!modal_is_open || (close_clicks && close_clicks > 0)) {
            console.log('🔄 CLIENTSIDE: Modal closed - fully resetting button to original state');
            
            // Force complete reset to initial state
            button.disabled = false;
            button.style.backgroundColor = '#17a2b8';
            button.style.color = 'white';
            button.style.border = '1px solid #17a2b8';
            button.style.cursor = 'pointer';
            button.style.opacity = '1';
            button.style.transform = 'scale(1)';
            button.style.boxShadow = 'none';
            button.style.transition = 'all 0.2s ease';
            button.style.pointerEvents = 'auto';  // Ensure button is clickable
            button.removeAttribute('disabled');
            
            // Reset to original text and hide spinner
            const languageStore = document.getElementById('language-store');
            const currentLanguage = languageStore ? languageStore.value : 'es';
            const originalText = currentLanguage === 'es' ? 'Hallazgos principales' : 'Key Findings';
            buttonText.textContent = originalText;
            spinnerContainer.style.display = 'none';
            spinnerContainer.style.animation = 'none';
            
            // Add a subtle bounce animation to indicate the button is ready again
            button.style.animation = 'bounce 0.3s ease-out';
            setTimeout(() => {
                if (button && button.style) {
                    button.style.animation = '';
                }
            }, 300);
            
            console.log('🔄 CLIENTSIDE: Button state fully reset to original');
        }
        // Handle button click
        else if (button_clicks && button_clicks > 0) {
            console.log('🔄 CLIENTSIDE: Button clicked - showing processing state');
            
            // Show processing state
            button.disabled = true;
            button.style.backgroundColor = '#f8f9fa';
            button.style.color = '#8b0000';
            button.style.border = '2px solid #8b0000';
            button.style.cursor = 'not-allowed';
            button.style.opacity = '0.8';
            button.style.transform = 'scale(0.98)';
            button.style.boxShadow = '0 0 10px rgba(139, 0, 0, 0.3)';

            // Update text and show spinner
            buttonText.textContent = '⏳ Procesando...';
            spinnerContainer.style.display = 'inline-block';
            spinnerContainer.style.animation = 'pulse 1.5s infinite';
            
            // Add shake animation
            button.style.animation = 'shake 0.3s ease-in-out';
            setTimeout(() => {
                if (button && button.style) {
                    button.style.animation = '';
                }
            }, 300);
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("key-findings-button-state", "data", allow_duplicate=True),
    [
        Input("key-findings-modal", "is_open"),
        Input("close-key-findings-modal", "n_clicks"),
        Input("generate-key-findings-btn", "n_clicks"),
    ],
    prevent_initial_call=True,
)

# Additional clientside callback to force reset button state
app.clientside_callback(
    """
    function forceResetButton(trigger) {
        const button = document.getElementById('generate-key-findings-btn');
        const spinnerContainer = document.getElementById('key-findings-spinner');
        const buttonText = document.getElementById('key-findings-button-text');
        
        if (!button || !spinnerContainer || !buttonText) {
            return window.dash_clientside.no_update;
        }
        
        console.log('🔄 CLIENTSIDE: Force resetting button state');
        
        // Force complete reset to initial state
        button.disabled = false;
        button.style.backgroundColor = '#17a2b8';
        button.style.color = 'white';
        button.style.border = '1px solid #17a2b8';
        button.style.cursor = 'pointer';
        button.style.opacity = '1';
        button.style.transform = 'scale(1)';
        button.style.boxShadow = 'none';
        button.style.transition = 'all 0.2s ease';
        button.style.pointerEvents = 'auto';  // Ensure button is clickable
        button.removeAttribute('disabled');
        
        // Reset to original text and hide spinner
        const languageStore = document.getElementById('language-store');
        const currentLanguage = languageStore ? languageStore.value : 'es';
        const originalText = currentLanguage === 'es' ? 'Hallazgos principales' : 'Key Findings';
        buttonText.textContent = originalText;
        spinnerContainer.style.display = 'none';
        spinnerContainer.style.animation = 'none';

        // Add a subtle bounce animation to indicate the button is ready again
        button.style.animation = 'bounce 0.3s ease-out';
        setTimeout(() => {
            if (button && button.style) {
                button.style.animation = '';
            }
        }, 300);
        
        console.log('🔄 CLIENTSIDE: Button state force reset complete');
        return window.dash_clientside.no_update;
    }
    """,
    Output("key-findings-button-state", "data", allow_duplicate=True),
    Input("key-findings-content-ready", "data"),
    prevent_initial_call=True,
)

# Additional clientside callback to reset button when modal is closed
app.clientside_callback(
    """
    function resetButtonOnModalClose(modal_is_open) {
        if (!modal_is_open) {
            const button = document.getElementById('generate-key-findings-btn');
            const spinnerContainer = document.getElementById('key-findings-spinner');
            const buttonText = document.getElementById('key-findings-button-text');
            
            if (!button || !spinnerContainer || !buttonText) {
                return window.dash_clientside.no_update;
            }
            
            console.log('🔄 CLIENTSIDE: Modal closed - resetting button state');
            
            // Force complete reset to initial state
            button.disabled = false;
            button.style.backgroundColor = '#17a2b8';
            button.style.color = 'white';
            button.style.border = '1px solid #17a2b8';
            button.style.cursor = 'pointer';
            button.style.opacity = '1';
            button.style.transform = 'scale(1)';
            button.style.boxShadow = 'none';
            button.style.transition = 'all 0.2s ease';
            button.style.pointerEvents = 'auto';  // Ensure button is clickable
            button.removeAttribute('disabled');
            
            // Reset to original text and hide spinner
            const languageStore = document.getElementById('language-store');
            const currentLanguage = languageStore ? languageStore.value : 'es';
            const originalText = currentLanguage === 'es' ? 'Hallazgos principales' : 'Key Findings';
            buttonText.textContent = originalText;
            spinnerContainer.style.display = 'none';
            spinnerContainer.style.animation = 'none';
            
            // Add a subtle bounce animation to indicate the button is ready again
            button.style.animation = 'bounce 0.3s ease-out';
            setTimeout(() => {
                if (button && button.style) {
                    button.style.animation = '';
                }
            }, 300);
            
            console.log('🔄 CLIENTSIDE: Button state reset complete');
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("key-findings-button-state", "data", allow_duplicate=True),
    Input("key-findings-modal", "is_open"),
    prevent_initial_call=True,
)

# Regenerate button callback removed - regenerate functionality now handled via hidden menu

# Source attribution callbacks removed - source URLs now integrated inside graphs

# Note: Clientside callback removed due to duplicate callback restrictions
# Dynamic URL detection will use server-side fallback for now


# Callback to reset source selections when keyword changes moved to callbacks/ui_callbacks.py


# Callback to initialize select all button text moved to callbacks/ui_callbacks.py


# Callback to update keyword dropdown options based on language moved to callbacks/ui_callbacks.py


# Callback to update sidebar labels and affiliations based on language moved to callbacks/ui_callbacks.py


# Callback to update data sources container moved to callbacks/ui_callbacks.py


# Duplicate DOI display callback removed - now handled in ui_callbacks.py


# Selected sources callback moved to callbacks/ui_callbacks.py


# Callback to update toggle table button text and handle collapse
@app.callback(
    Output("credits-button-text", "children"),
    Output("citation-button-text", "children"),
    Input("language-store", "data"),
)
def update_credits_button_text(language):
    """Update credits button text based on language"""
    return get_text("credits", language) + " ", get_text(
        "cite_this_dashboard", language
    )


# Seasonal analysis callback moved to callbacks/graph_callbacks.py


# Regression analysis callback moved to callbacks/graph_callbacks.py


# Callback for credits toggle - allows manual override
@app.callback(
    Output("credits-collapse", "is_open", allow_duplicate=True),
    Output("credits-chevron", "className"),
    Input("credits-toggle", "n_clicks"),
    State("credits-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_credits_manually(n_clicks, is_open):
    if n_clicks:
        new_state = not is_open
        chevron_class = "fas fa-chevron-up" if new_state else "fas fa-chevron-down"
        return new_state, chevron_class
    return is_open, "fas fa-chevron-down"


# Callback to show/hide navigation menu with dynamic buttons
@app.callback(
    Output("navigation-section", "children"),
    Output("navigation-section", "style"),
    Input("keyword-dropdown", "value"),
    Input("data-sources-store-v2", "data"),
    Input("language-store", "data"),
)
def update_navigation_visibility(selected_keyword, selected_sources, language):
    if selected_sources is None:
        selected_sources = []

    selected_source_ids = map_display_names_to_source_ids(selected_sources)

    if selected_keyword and selected_sources:
        # Define navigation buttons with their requirements
        nav_buttons = [
            # Always visible (basic analysis)
            {
                "id": 1,
                "text": get_text("temporal_2d_nav", language),
                "href": "#section-temporal-2d",
                "color": "#e8f4fd",
                "border": "#b8daff",
                "min_sources": 1,
            },
            {
                "id": 2,
                "text": get_text("mean_analysis_nav", language),
                "href": "#section-mean-analysis",
                "color": "#f0f9ff",
                "border": "#bee3f8",
                "min_sources": 1,
            },
            # Require 2+ sources (multi-source analysis)
            {
                "id": 3,
                "text": get_text("temporal_3d_nav", language),
                "href": "#section-temporal-3d",
                "color": "#fef5e7",
                "border": "#fbd38d",
                "min_sources": 2,
            },
            {
                "id": 4,
                "text": get_text("seasonal_nav", language),
                "href": "#section-seasonal-analysis",
                "color": "#f0fff4",
                "border": "#9ae6b4",
                "min_sources": 1,
            },
            {
                "id": 5,
                "text": get_text("fourier_nav", language),
                "href": "#section-fourier-analysis",
                "color": "#faf5ff",
                "border": "#d6bcfa",
                "min_sources": 1,
            },
            {
                "id": 6,
                "text": get_text("correlation_nav", language),
                "href": "#section-correlation-analysis",
                "color": "#e6fffa",
                "border": "#81e6d9",
                "min_sources": 2,
            },
            {
                "id": 7,
                "text": get_text("regression_nav", language),
                "href": "#section-regression-analysis",
                "color": "#fffaf0",
                "border": "#fce5cd",
                "min_sources": 2,
            },
            {
                "id": 8,
                "text": get_text("pca_nav", language),
                "href": "#section-pca-analysis",
                "color": "#f0f9ff",
                "border": "#bee3f8",
                "min_sources": 2,
            },
            # Always visible (utility sections) - placed at the end
            {
                "id": 9,
                "text": get_text("data_table_nav", language),
                "href": "#section-data-table",
                "color": "#f8f9fa",
                "border": "#dee2e6",
                "min_sources": 1,
            },
            {
                "id": 10,
                "text": get_text("performance_nav", language),
                "href": "#section-performance",
                "color": "#f7fafc",
                "border": "#e2e8f0",
                "min_sources": 1,
            },
        ]

        # Filter buttons based on number of selected sources
        num_sources = len(selected_sources)
        active_buttons = [
            btn for btn in nav_buttons if num_sources >= btn["min_sources"]
        ]

        # Generate button elements
        button_elements = []
        for btn in active_buttons:
            button_elements.append(
                html.Div(
                    [
                        html.A(
                            btn["text"],
                            href=btn["href"],
                            className="nav-link",
                            style={
                                "color": "#2c3e50",
                                "textDecoration": "none",
                                "fontSize": "9px",
                                "fontWeight": "500",
                            },
                        )
                    ],
                    style={
                        "backgroundColor": btn["color"],
                        "padding": "4px 8px",
                        "borderRadius": "4px",
                        "margin": "2px",
                        "display": "inline-block",
                        "border": f"1px solid {btn['border']}",
                    },
                )
            )

        # Show navigation menu with filtered buttons
        return [
            html.Hr(),
            html.Div(
                [
                    html.Div(button_elements, style={"marginBottom": "15px"}),
                ],
                style={
                    "backgroundColor": "#343a40",
                    "border": "2px solid #495057",
                    "borderRadius": "10px",
                    "padding": "15px",
                    "marginTop": "10px",
                    "marginBottom": "10px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            ),
        ], {}
    else:
        # Hide navigation menu
        return [], {"display": "none"}


# Fourier Analysis callback
@app.callback(
    Output("citation-modal", "is_open"),
    Output("citation-modal-body", "children"),
    Output("citation-modal-title", "children"),
    Input("citation-modal-toggle", "n_clicks"),
    Input("close-citation-modal", "n_clicks"),
    State("language-store", "data"),
    prevent_initial_call=True,
)
def toggle_citation_modal(citation_clicks, close_clicks, language):
    """Handle citation modal toggle and content generation"""
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, "", ""

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Close modal if close button is clicked
    if trigger_id == "close-citation-modal":
        return False, "", ""

    # Open modal if citation button is clicked
    if trigger_id == "citation-modal-toggle":
        # Generate citation content based on current language
        current_date = get_current_date_for_citation(language)

        if language == "es":
            # Spanish citations
            citation_content = html.Div(
                [
                    html.H6(get_text("how_to_cite", language), className="mb-3"),
                    html.H6(
                        "APA 7 (Asociación Americana de Psicología)",
                        className="text-primary mt-3",
                    ),
                    html.Div(
                        [
                            html.P(
                                f"Añez, D., y Añez, D. (2025). Herramientas gerenciales: Dinámicas temporales contingentes y antinomias policontextuales [Dashboard de análisis de datos]. Solidum Consulting / Wise Connex. {get_citation_url()}/",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copiar",
                                id={"type": "copy-button", "index": "apa"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6(
                        "Chicago (17.ª ed., autor-fecha)", className="text-primary"
                    ),
                    html.Div(
                        [
                            html.P(
                                f'Añez, Diomar, y Dimar Añez. 2025. "Herramientas Gerenciales: Dinámicas Temporales Contingentes y Antinomias Policontextuales". Dashboard de Análisis. Solidum Consulting / Wise Connex. Consultado el {current_date["chicago"]}. {get_citation_url()}/.',
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copiar",
                                id={"type": "copy-button", "index": "chicago"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("MLA (9.ª ed.)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f"Añez, Diomar, y Dimar Añez. Herramientas Gerenciales: Dinámicas Temporales Contingentes y Antinomias Policontextuales. 2025, Solidum Consulting / Wise Connex, {get_citation_url()}/.",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copiar",
                                id={"type": "copy-button", "index": "mla"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("OSCOLA (Jurídico)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f"Diomar Añez y Dimar Añez, Herramientas gerenciales: Dinámicas temporales contingentes y antinomias policontextuales (Solidum Consulting / Wise Connex, 2025) <{get_citation_url()}/> accedido el {current_date['oscola']}.",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copiar",
                                id={"type": "copy-button", "index": "oscola"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("Vancouver (Medicina/Salud)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f"1. Añez D, Añez D. Herramientas gerenciales: Dinámicas temporales contingentes y antinomias policontextuales [Internet]. Solidum Consulting / Wise Connex; 2025 [citado el {current_date['vancouver']}]. Disponible en: {get_citation_url()}/",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copiar",
                                id={"type": "copy-button", "index": "vancouver"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("IEEE (Ingeniería/Tecnología)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f'[1] D. Añez y D. Añez, "Herramientas gerenciales: Dinámicas temporales contingentes y antinomias policontextuales", Solidum Consulting / Wise Connex, 2025. [En línea]. Disponible: {get_citation_url()}/.',
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copiar",
                                id={"type": "copy-button", "index": "ieee"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.Hr(),
                    html.P(
                        get_text("download_ris_files", language),
                        className="text-muted mb-2",
                    ),
                    html.P(
                        get_text("ris_note", language), className="small text-muted"
                    ),
                ]
            )
        else:
            # English citations
            citation_content = html.Div(
                [
                    html.H6(get_text("how_to_cite", language), className="mb-3"),
                    html.H6(
                        "APA 7 (American Psychological Association)",
                        className="text-primary mt-3",
                    ),
                    html.Div(
                        [
                            html.P(
                                f"Añez, D., & Añez, D. (2025). Management tools: Contingent temporal dynamics and policontextual antinomies [Data analysis dashboard]. Solidum Consulting / Wise Connex. {get_citation_url()}/",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copy",
                                id={"type": "copy-button", "index": "apa"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6(
                        "Chicago (17th ed., author-date)", className="text-primary"
                    ),
                    html.Div(
                        [
                            html.P(
                                f'Añez, Diomar, and Dimar Añez. 2025. "Management Tools: Contingent Temporal Dynamics and Policontextual Antinomies." Analysis Dashboard. Solidum Consulting / Wise Connex. Accessed {current_date["chicago"]}. {get_citation_url()}/.',
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copy",
                                id={"type": "copy-button", "index": "chicago"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("MLA (9th ed.)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f"Añez, Diomar, and Dimar Añez. Management Tools: Contingent Temporal Dynamics and Policontextual Antinomies. 2025, Solidum Consulting / Wise Connex, {get_citation_url()}/.",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copy",
                                id={"type": "copy-button", "index": "mla"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("OSCOLA (Legal)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f"Diomar Añez and Dimar Añez, Management tools: Contingent temporal dynamics and policontextual antinomies (Solidum Consulting / Wise Connex, 2025) <{get_citation_url()}/> accessed {current_date['oscola']}.",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copy",
                                id={"type": "copy-button", "index": "oscola"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("Vancouver (Medicine/Health)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f"1. Añez D, Añez D. Management tools: Contingent temporal dynamics and policontextual antinomies [Internet]. Solidum Consulting / Wise Connex; 2025 [cited {current_date['vancouver']}]. Available from: {get_citation_url()}/",
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copy",
                                id={"type": "copy-button", "index": "vancouver"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.H6("IEEE (Engineering/Tech)", className="text-primary"),
                    html.Div(
                        [
                            html.P(
                                f'[1] D. Añez and D. Añez, "Management tools: Contingent temporal dynamics and policontextual antinomies," Solidum Consulting / Wise Connex, 2025. [Online]. Available: {get_citation_url()}/.',
                                className="mb-2",
                                style={"fontSize": "12px"},
                            ),
                            dbc.Button(
                                "Copy",
                                id={"type": "copy-button", "index": "ieee"},
                                color="outline-primary",
                                size="sm",
                                className="me-2",
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center mb-3",
                    ),
                    html.Hr(),
                    html.P(
                        get_text("download_ris_files", language),
                        className="text-muted mb-2",
                    ),
                    html.P(
                        get_text("ris_note", language), className="small text-muted"
                    ),
                ]
            )

        # Set modal title based on language
        modal_title = get_text("cite_this_dashboard", language)

        return True, citation_content, modal_title

    return False, "", ""


# Callback to update download button text based on language
@app.callback(
    Output("download-current-ris-text", "children"), Input("language-store", "data")
)
def update_download_button_text(language):
    """Update download button text based on language"""
    return get_text("download_ris", language)


# Copy citation callback moved to callbacks/ui_callbacks.py


# Callbacks for downloading RIS files
@app.callback(
    Output("download-current-ris", "href"),
    Output("download-current-ris", "download"),
    Input("citation-modal-toggle", "n_clicks"),
    State("language-store", "data"),
    prevent_initial_call=True,
)
def generate_ris_download_link(n_clicks, language):
    """Generate download link for RIS file based on current language"""
    print(
        f"🔍 DEBUG: generate_ris_download_link called with n_clicks={n_clicks}, language={language}"
    )

    if not n_clicks:
        print("🔍 DEBUG: No clicks detected, returning empty string")
        return "", ""

    # Generate RIS content based on current language
    ris_url = get_ris_url()

    if language == "es":
        # Spanish RIS content
        ris_content = f"""TY  - WEB
AU  - Añez, Diomar
AU  - Añez, Dimar
PY  - 2025
T1  - Herramientas gerenciales: Dinámicas temporales contingentes y antinomias policontextuales
PB  - Solidum Consulting / Wise Connex
N2  - Este dashboard de análisis de datos sirve como base analítica para el proyecto de investigación doctoral: «Dicotomía ontológica en las "Modas Gerenciales"». Desarrollado con Python, Plotly y Dash.
KW  - Herramientas Gerenciales
KW  - Modas Gerenciales
KW  - Visualización de Datos
KW  - Antinomias Policontextuales
UR  - {ris_url}
ER  -"""
        filename = "dashboard_citacion_es.ris"
    else:
        # English RIS content
        ris_content = f"""TY  - WEB
AU  - Añez, Diomar
AU  - Añez, Dimar
PY  - 2025
T1  - Management tools: Contingent temporal dynamics and policontextual antinomies
PB  - Solidum Consulting / Wise Connex
N2  - This data analysis dashboard serves as the analytical basis for the doctoral research project: "Ontological dichotomy in 'Management Fads'." Developed with Python, Plotly, and Dash.
KW  - Management Tools
KW  - Management Fads
KW  - Data Visualization
KW  - Policontextual Antinomies
UR  - {ris_url}
ER  -"""
        filename = "dashboard_citation_en.ris"

    print(
        f"🔍 DEBUG: Generated RIS content for language={language}, length={len(ris_content)}"
    )

    # Create a data URI for the RIS file with proper filename
    import base64
    import urllib.parse

    ris_b64 = base64.b64encode(ris_content.encode("utf-8")).decode("utf-8")

    # Create a proper data URI with filename suggestion
    data_uri = f"data:application/x-research-info-systems;base64,{ris_b64}"
    print(f"🔍 DEBUG: Generated data URI, length={len(data_uri)}")

    return data_uri, filename


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Management Tools Analysis Dashboard")
    parser.add_argument(
        "--port", type=int, default=8050, help="Port to run the dashboard on"
    )
    parser.add_argument(
        "--debug", action="store_true", default=True, help="Enable debug mode"
    )
    args = parser.parse_args()

    app.run(debug=args.debug, host="0.0.0.0", port=args.port)
