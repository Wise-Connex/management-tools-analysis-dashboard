"""
Key Findings callbacks for the Management Tools Analysis Dashboard.

This module contains all callbacks related to the Key Findings functionality,
including modal management, content generation, and save operations.
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import time
import re
import json

# Import database and utility functions
from fix_source_mapping import map_display_names_to_source_ids
from translations import get_text, get_tool_name
from utils import run_async_in_sync_context


def register_kf_callbacks(app, key_findings_service, KEY_FINDINGS_AVAILABLE):
    """Register all Key Findings-related callbacks with the Dash app."""

    if KEY_FINDINGS_AVAILABLE and key_findings_service:

        @app.callback(
            Output("key-findings-modal", "is_open"),
            Output("key-findings-modal-body", "children"),
            Output("key-findings-modal-title", "children"),
            Output(
                "key-findings-content-ready", "data"
            ),  # New output for content ready state
            Output(
                "key-findings-data-ready", "data"
            ),  # CRITICAL: Add this missing output for modal data
            Input("generate-key-findings-btn", "n_clicks"),
            Input("close-key-findings-modal", "n_clicks"),
            Input("key-findings-modal", "is_open"),  # Listen for modal state changes
            State("keyword-dropdown", "value"),
            State("data-sources-store-v2", "data"),
            State("language-store", "data"),
            State("key-findings-content-ready", "data"),  # Current content ready state
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
            """Handle Key Findings modal toggle and generation"""
            print(
                f"🔍 MODAL CALLBACK: generate_clicks: {generate_clicks}, close_clicks: {close_clicks}, modal_is_open: {modal_is_open}"
            )
            print(f"🔍 MODAL CALLBACK: current_content_ready: {current_content_ready}")

            ctx = dash.callback_context
            print(f"🔍 MODAL CALLBACK: Callback context: {ctx}")
            if ctx.triggered:
                print(
                    f"🔍 MODAL CALLBACK: Triggered by: {ctx.triggered[0]['prop_id']} = {ctx.triggered[0]['value']}"
                )

            if not ctx.triggered:
                print("🔍 MODAL CALLBACK: No triggered context, returning default")
                return False, "", "🧠 Key Findings - Análisis", False, None

            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
            print(f"🔍 MODAL CALLBACK: Trigger ID: {trigger_id}")

            # Handle modal header close button (the "x" in top right corner)
            if trigger_id == "key-findings-modal" and not modal_is_open:
                print("🔍 Modal header close button clicked - restoring key findings")
                # Generate title even when closing to maintain consistency
                tool_display_name = (
                    get_tool_name(selected_tool, language)
                    if selected_tool
                    else "Herramienta"
                )
                sources_str = (
                    ", ".join(selected_sources) if selected_sources else "Fuentes"
                )
                dynamic_title = f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
                # Return empty content to clear modal and restore key findings
                # Also trigger content_ready to reset button state
                return False, "", dynamic_title, True, None

            if trigger_id == "close-key-findings-modal":
                print("🔍 Closing modal via Cerrar button")
                # Generate title even when closing to maintain consistency
                tool_display_name = (
                    get_tool_name(selected_tool, language)
                    if selected_tool
                    else "Herramienta"
                )
                sources_str = (
                    ", ".join(selected_sources) if selected_sources else "Fuentes"
                )
                dynamic_title = f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
                # Also trigger content_ready to reset button state
                return False, "", dynamic_title, True, None

            if trigger_id == "generate-key-findings-btn":
                print("🔍 Generate button clicked")
                if not selected_tool or not selected_sources:
                    print("❌ Missing tool or sources")
                    # Generate title even for error case
                    tool_display_name = (
                        get_tool_name(selected_tool, language)
                        if selected_tool
                        else "Herramienta"
                    )
                    sources_str = (
                        ", ".join(selected_sources) if selected_sources else "Fuentes"
                    )
                    dynamic_title = (
                        f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
                    )
                    return (
                        True,
                        html.Div(
                            [
                                html.H4("Error", className="text-danger"),
                                html.P(
                                    "Por favor seleccione una herramienta y al menos una fuente de datos.",
                                    className="text-muted",
                                ),
                            ]
                        ),
                        dynamic_title,
                        False,
                        None,
                    )

                try:
                    print("🚀 Starting Key Findings generation...")
                    print(
                        f"📋 Parameters: tool='{selected_tool}', sources={selected_sources}, language={language}"
                    )

                    # Check if key_findings_service is available
                    print(f"🔍 Checking key_findings_service: {key_findings_service}")
                    if key_findings_service is None:
                        print("❌ key_findings_service is None")
                        # Generate title even for error case
                        tool_display_name = (
                            get_tool_name(selected_tool, language)
                            if selected_tool
                            else "Herramienta"
                        )
                        sources_str = (
                            ", ".join(selected_sources)
                            if selected_sources
                            else "Fuentes"
                        )
                        dynamic_title = (
                            f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
                        )
                        return (
                            True,
                            html.Div(
                                [
                                    html.H4("Error", className="text-danger"),
                                    html.P(
                                        "Key Findings service not initialized.",
                                        className="text-muted",
                                    ),
                                ]
                            ),
                            dynamic_title,
                            False,
                            None,
                        )

                    print("✅ Key Findings service is available")

                    # Create dynamic title with tool name and sources
                    tool_display_name = get_tool_name(selected_tool, language)
                    sources_str = ", ".join(selected_sources)
                    dynamic_title = (
                        f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
                    )

                    # Skip loading state for precomputed data - go directly to content generation
                    print(
                        "🔄 Skipping loading state - using precomputed data for instant display"
                    )

                    # Use the proper KeyFindingsService method which checks cache and precomputed findings
                    print(
                        "🔍 Using KeyFindingsService.generate_key_findings() for intelligent caching..."
                    )

                    # Initialize timing variables
                    data_collection_start = time.time()
                    ai_start = time.time()
                    analysis_start = time.time()

                    # Map display names to source IDs for database queries
                    # The service needs both: numeric IDs for database queries AND display names for analysis
                    selected_source_ids = map_display_names_to_source_ids(
                        selected_sources
                    )
                    print(
                        f"🔍 Mapped sources: {selected_sources} -> {selected_source_ids}"
                    )

                    key_findings_result = run_async_in_sync_context(
                        key_findings_service.generate_key_findings,
                        tool_name=selected_tool,
                        selected_sources=selected_source_ids,  # Numeric IDs for database queries
                        language=language,
                        force_refresh=False,  # Use cache when available, only generate fresh if cache miss
                        source_display_names=selected_sources,  # Display names for analysis functions
                    )

                    # Calculate timing (approximate since detailed breakdown is internal to service)
                    ai_time = time.time() - ai_start
                    data_collection_time = 0  # Internal to service
                    prompt_time = 0  # Internal to service

                    analysis_time = time.time() - analysis_start
                    print(
                        f"✅ Key Findings generation completed in {analysis_time:.2f}s"
                    )

                    # Extract metadata for analysis_data
                    # Try to get metadata from the result if available, otherwise use defaults
                    result_metadata = key_findings_result.get("metadata", {})
                    analysis_data = {
                        "data_points_analyzed": result_metadata.get(
                            "data_points_analyzed", 0
                        ),
                        "date_range_start": result_metadata.get(
                            "date_range_start", "N/A"
                        ),
                        "date_range_end": result_metadata.get("date_range_end", "N/A"),
                    }

                    # If data_points_analyzed is 0, try to estimate or get from report_data later
                    data_points = analysis_data["data_points_analyzed"]

                    # Check if the result indicates it came from precomputed database
                    if key_findings_result.get("source") == "precomputed_findings":
                        print(
                            "🎯 SUCCESS: Analysis retrieved from precomputed findings database!"
                        )
                    elif key_findings_result.get("cache_hit"):
                        print("🎯 SUCCESS: Analysis retrieved from cache!")
                    else:
                        print("🎯 SUCCESS: New analysis generated!")

                    # Check for success
                    if not key_findings_result.get("success", False):
                        error_msg = key_findings_result.get("error", "Unknown error")
                        print(f"❌ Key Findings generation failed: {error_msg}")
                        return (
                            True,
                            html.Div(
                                [
                                    html.H4(
                                        "Error de Análisis", className="text-danger"
                                    ),
                                    html.P(
                                        f"Error al generar hallazgos clave: {error_msg}",
                                        className="text-muted",
                                    ),
                                ]
                            ),
                            dynamic_title,
                            False,
                            None,
                        )

                    # Extract the report data for processing
                    report_data = key_findings_result.get("data", {})
                    if not report_data:
                        print("❌ No report data in Key Findings result")
                        return (
                            True,
                            html.Div(
                                [
                                    html.H4("Error de Datos", className="text-danger"),
                                    html.P(
                                        "No se pudieron obtener los datos del análisis.",
                                        className="text-muted",
                                    ),
                                ]
                            ),
                            dynamic_title,
                            False,
                            None,
                        )

                    print(f"📊 Report data retrieved: {len(report_data)} fields")
                    response_time = key_findings_result.get("response_time_ms", 0)
                    print(f"⚡ Response time: {response_time}ms")

                    # Continue with existing modal processing using report_data instead of ai_response
                    ai_response = key_findings_result  # Reuse existing variable name for compatibility

                    # CRITICAL FIX: Add None check for ai_response
                    if ai_response is None:
                        print(
                            f"❌ CRITICAL: ai_response is None - AI service returned no response"
                        )
                        return (
                            True,
                            html.Div(
                                [
                                    html.H4("Error de IA", className="text-danger"),
                                    html.P(
                                        "El servicio de IA no devolvió ninguna respuesta. Intente nuevamente.",
                                        className="text-muted",
                                    ),
                                ]
                            ),
                            dynamic_title,
                            False,
                            None,
                        )

                    if not ai_response.get("success", False):
                        print(f"❌ AI service failed: {ai_response}")
                        return (
                            True,
                            html.Div(
                                [
                                    html.H4("Error de IA", className="text-danger"),
                                    html.P(
                                        "El servicio de IA no pudo generar el análisis. Intente nuevamente.",
                                        className="text-muted",
                                    ),
                                ]
                            ),
                            dynamic_title,
                            False,
                            None,
                        )

                    # CRITICAL FIX: Add None check before accessing ai_response properties in main callback
                    if ai_response is None:
                        print(
                            f"❌ CRITICAL: ai_response is None in main callback - AI service returned no response"
                        )
                        return (
                            True,
                            html.Div(
                                [
                                    html.H4("Error de IA", className="text-danger"),
                                    html.P(
                                        "El servicio de IA no devolvió ninguna respuesta. Intente nuevamente.",
                                        className="text-muted",
                                    ),
                                ]
                            ),
                            dynamic_title,
                            False,
                            None,
                        )

                    response_time_ms = ai_response.get("response_time_ms", 0)
                    model_used = ai_response.get("model_used", "unknown")
                    token_count = ai_response.get("token_count", 0)

                    # DEBUG: Check what values we actually have
                    print(f"🔍 DEBUG: ai_response keys: {list(ai_response.keys())}")
                    print(f"🔍 DEBUG: model_used from response: '{model_used}'")
                    print(
                        f"🔍 DEBUG: data_points_analyzed from response: '{ai_response.get('data_points_analyzed', 'MISSING')}'"
                    )
                    print(
                        f"🔍 DEBUG: response_time_ms from response: '{response_time_ms}'"
                    )

                    print(
                        f"✅ AI analysis completed in {response_time_ms}ms using {model_used} ({token_count} tokens)"
                    )

                    # Parse AI response
                    # ai_response is key_findings_result which has 'data' field containing the report
                    # report_data already contains the parsed content
                    ai_content = report_data
                    print(f"📄 AI response parsed:")
                    print(f"   - Available fields: {list(ai_content.keys())}")
                    print(
                        f"   - Executive summary length: {len(ai_content.get('executive_summary', ''))}"
                    )
                    print(
                        f"   - Principal findings length: {len(ai_content.get('principal_findings', []))}"
                    )
                    print(
                        f"   - Heatmap analysis length: {len(ai_content.get('heatmap_analysis', ''))}"
                    )
                    print(
                        f"   - PCA analysis length: {len(ai_content.get('pca_analysis', ''))}"
                    )
                    print(
                        f"   - Heatmap analysis length: {len(ai_content.get('heatmap_analysis', ''))}"
                    )

                    # Helper function to extract text content from AI response with robust parsing
                    def extract_text_content(content):
                        """Extract text content from various data types with robust malformed JSON handling."""
                        # For single-source analysis, skip all parsing and return content as-is
                        # This prevents the extraction of individual sections from the combined principal_findings
                        if len(selected_sources) == 1:
                            print(
                                f"🔍 EXTRACT_TEXT_CONTENT: Single-source detected, returning content as-is"
                            )
                            return content

                        if isinstance(content, str):
                            # First, try to parse as pure JSON
                            cleaned_content = content.strip()

                            # Remove markdown code blocks if present
                            if cleaned_content.startswith("```json"):
                                cleaned_content = cleaned_content[7:]  # Remove ```json
                            if cleaned_content.startswith("```"):
                                cleaned_content = cleaned_content[3:]  # Remove ```
                            if cleaned_content.endswith("```"):
                                cleaned_content = cleaned_content[
                                    :-3
                                ]  # Remove trailing ```

                            cleaned_content = cleaned_content.strip()

                            # Try direct JSON parsing first
                            if cleaned_content.startswith(
                                "{"
                            ) and cleaned_content.endswith("}"):
                                try:
                                    import json

                                    parsed = json.loads(cleaned_content)
                                    # Extract from parsed JSON
                                    if isinstance(parsed, dict):
                                        for field in [
                                            "executive_summary",
                                            "principal_findings",
                                            "pca_analysis",
                                            "bullet_point",
                                            "analysis",
                                        ]:
                                            if field in parsed and isinstance(
                                                parsed[field], str
                                            ):
                                                return parsed[field]
                                except json.JSONDecodeError:
                                    pass

                            # Handle specific malformed patterns from the key findings report
                            # Pattern 1: JSON that gets cut off mid-principal_findings array
                            if (
                                cleaned_content.startswith('{"executive_summary":')
                                and '"principal_findings":' in cleaned_content
                            ):
                                # Extract executive summary
                                import re

                                exec_summary_match = re.search(
                                    r'"executive_summary":\s*"([^"]*(?:\\.[^"]*)*)"',
                                    cleaned_content,
                                )
                                if exec_summary_match:
                                    return exec_summary_match.group(1).replace(
                                        '\\"', '"'
                                    )

                            # Pattern 2: Bullet point containing JSON fragment
                            if (
                                cleaned_content.strip().startswith("•")
                                and '"executive_summary":' in cleaned_content
                            ):
                                # Remove bullet point and extract JSON
                                json_part = cleaned_content.strip()[1:].strip()
                                if json_part.startswith('"'):
                                    json_part = json_part[1:]
                                if json_part.endswith('"'):
                                    json_part = json_part[:-1]

                                import re

                                exec_summary_match = re.search(
                                    r'"executive_summary":\s*"(.*?)"',
                                    json_part,
                                    re.DOTALL,
                                )
                                if exec_summary_match:
                                    return exec_summary_match.group(1).replace(
                                        '\\"', '"'
                                    )

                            # If direct parsing fails, try to extract from markdown sections
                            sections = extract_markdown_sections_from_content(
                                cleaned_content
                            )

                            if sections and "executive_summary" in sections:
                                section_content = sections["executive_summary"]
                                # Try to extract JSON from section
                                json_content = extract_json_from_section_content(
                                    section_content
                                )
                                if json_content and "executive_summary" in json_content:
                                    return json_content["executive_summary"]

                            return content

                        elif isinstance(content, dict):
                            # Extract from dictionary
                            for field in [
                                "executive_summary",
                                "principal_findings",
                                "pca_analysis",
                                "bullet_point",
                                "analysis",
                            ]:
                                if field in content and isinstance(content[field], str):
                                    return content[field]
                        elif isinstance(content, list) and content:
                            # Extract from list
                            first_item = content[0]
                            if isinstance(first_item, dict):
                                for field in ["bullet_point", "text", "content"]:
                                    if field in first_item and isinstance(
                                        first_item[field], str
                                    ):
                                        return first_item[field]
                            elif isinstance(first_item, str):
                                return first_item

                        return str(content) if content else ""

                    def extract_markdown_sections_from_content(content):
                        """Extract content from markdown sections with emoji headers and translate headers."""
                        sections = {}

                        # Define section patterns (Spanish and English) with emoji headers
                        section_patterns = {
                            "executive_summary": [
                                "📋 Resumen Ejecutivo",
                                "📋 Executive Summary",
                                "Resumen Ejecutivo",
                                "Executive Summary",
                            ],
                            "principal_findings": [
                                "🔍 Hallazgos Principales",
                                "🔍 Principal Findings",
                                "Hallazgos Principales",
                                "Principal Findings",
                            ],
                            "pca_analysis": [
                                "📊 Análisis PCA",
                                "📊 PCA Analysis",
                                "Análisis PCA",
                                "PCA Analysis",
                            ],
                        }

                        lines = content.split("\n")
                        current_section = None
                        section_content = []

                        for line in lines:
                            line = line.strip()

                            # Check if this line starts a new section
                            section_started = False
                            for section_key, patterns in section_patterns.items():
                                if any(pattern in line for pattern in patterns):
                                    # Save previous section if exists
                                    if current_section and section_content:
                                        sections[current_section] = "\n".join(
                                            section_content
                                        ).strip()
                                        section_content = []

                                    current_section = section_key
                                    section_content = []
                                    section_started = True
                                    break

                            if not section_started and current_section:
                                # Continue accumulating content for current section
                                section_content.append(line)

                        # Save the last section
                        if current_section and section_content:
                            sections[current_section] = "\n".join(
                                section_content
                            ).strip()

                        return sections

                    def extract_json_from_section_content(section_content):
                        """Extract JSON object from section content."""
                        # First, try to extract from markdown code blocks
                        if "```json" in section_content:
                            start_marker = section_content.find("```json")
                            if start_marker != -1:
                                start_json = section_content.find("{", start_marker)
                                end_marker = section_content.find(
                                    "```", start_marker + 7
                                )
                                if end_marker != -1:
                                    end_json = (
                                        section_content.rfind(
                                            "}", start_marker, end_marker
                                        )
                                        + 1
                                    )
                                    if start_json != -1 and end_json > start_json:
                                        json_str = section_content[start_json:end_json]
                                        try:
                                            import json

                                            return json.loads(json_str)
                                        except json.JSONDecodeError:
                                            pass

                        # Fallback: Find JSON boundaries directly
                        start_idx = section_content.find("{")
                        end_idx = section_content.rfind("}") + 1

                        if start_idx != -1 and end_idx > start_idx:
                            json_str = section_content[start_idx:end_idx]
                            try:
                                import json

                                return json.loads(json_str)
                            except json.JSONDecodeError:
                                pass

                        return None

                    def clean_section_headers(content, language):
                        """Clean up section headers in AI content to match the selected language."""
                        if not content or not isinstance(content, str):
                            return content

                        # Define section header mappings
                        header_mappings = {
                            "en": {
                                "📋 Resumen Ejecutivo": "📋 Executive Summary",
                                "📋 Executive Summary": "📋 Executive Summary",
                                "🔍 Hallazgos Principales": "🔍 Principal Findings",
                                "🔍 Principal Findings": "🔍 Principal Findings",
                                "📊 Análisis PCA": "📊 PCA Analysis",
                                "📊 PCA Analysis": "📊 PCA Analysis",
                                "Resumen Ejecutivo": "Executive Summary",
                                "Hallazgos Principales": "Principal Findings",
                                "Análisis PCA": "PCA Analysis",
                            },
                            "es": {
                                "📋 Executive Summary": "📋 Resumen Ejecutivo",
                                "📋 Resumen Ejecutivo": "📋 Resumen Ejecutivo",
                                "🔍 Principal Findings": "🔍 Hallazgos Principales",
                                "🔍 Hallazgos Principales": "🔍 Hallazgos Principales",
                                "📊 PCA Analysis": "📊 Análisis PCA",
                                "📊 Análisis PCA": "📊 Análisis PCA",
                                "Executive Summary": "Resumen Ejecutivo",
                                "Principal Findings": "Hallazgos Principales",
                                "PCA Analysis": "Análisis PCA",
                            },
                        }

                        # Apply the appropriate mappings
                        mappings = header_mappings.get(language, header_mappings["en"])
                        cleaned_content = content

                        for original, replacement in mappings.items():
                            cleaned_content = cleaned_content.replace(
                                original, replacement
                            )

                        return cleaned_content

                    def extract_markdown_sections_from_content(content):
                        """Extract content from markdown sections with emoji headers."""
                        sections = {}

                        section_patterns = {
                            "executive_summary": [
                                "📋 Resumen Ejecutivo",
                                "📋 Executive Summary",
                            ],
                            "principal_findings": [
                                "🔍 Hallazgos Principales",
                                "🔍 Principal Findings",
                            ],
                            "pca_analysis": ["📊 Análisis PCA", "📊 PCA Analysis"],
                        }

                        lines = content.split("\n")
                        current_section = None
                        section_content = []

                        for line in lines:
                            line = line.strip()

                            # Check if this line starts a new section
                            section_started = False
                            for section_key, patterns in section_patterns.items():
                                if any(pattern in line for pattern in patterns):
                                    # Save previous section if exists
                                    if current_section and section_content:
                                        sections[current_section] = "\n".join(
                                            section_content
                                        ).strip()
                                        section_content = []

                                    current_section = section_key
                                    section_content = []
                                    section_started = True
                                    break

                            if not section_started and current_section:
                                # Continue accumulating content for current section
                                section_content.append(line)

                        # Save the last section
                        if current_section and section_content:
                            sections[current_section] = "\n".join(
                                section_content
                            ).strip()

                        return sections

                    def extract_json_from_section_content(section_content):
                        """Extract JSON object from section content."""
                        # First, try to extract from markdown code blocks
                        if "```json" in section_content:
                            start_marker = section_content.find("```json")
                            if start_marker != -1:
                                start_json = section_content.find("{", start_marker)
                                end_marker = section_content.find(
                                    "```", start_marker + 7
                                )
                                if end_marker != -1:
                                    end_json = (
                                        section_content.rfind(
                                            "}", start_marker, end_marker
                                        )
                                        + 1
                                    )
                                    if start_json != -1 and end_json > start_json:
                                        json_str = section_content[start_json:end_json]
                                        try:
                                            import json

                                            return json.loads(json_str)
                                        except json.JSONDecodeError:
                                            pass

                        # Fallback: Find JSON boundaries directly
                        start_idx = section_content.find("{")
                        end_idx = section_content.rfind("}") + 1

                        if start_idx != -1 and end_idx > start_idx:
                            json_str = section_content[start_idx:end_idx]
                            try:
                                import json

                                return json.loads(json_str)
                            except json.JSONDecodeError:
                                pass

                        return None

                    # Extract text content from AI response
                    executive_summary = extract_text_content(
                        ai_content.get("executive_summary", "No summary available")
                    )
                    principal_findings_raw = ai_content.get(
                        "principal_findings", "No findings available"
                    )
                    pca_analysis_raw = ai_content.get(
                        "pca_analysis", "No PCA analysis available"
                    )
                    heatmap_analysis_raw = ai_content.get(
                        "heatmap_analysis", "No heatmap analysis available"
                    )

                    # Clean up section headers in the content to ensure proper English display
                    executive_summary = clean_section_headers(
                        executive_summary, language
                    )
                    principal_findings_raw = clean_section_headers(
                        principal_findings_raw, language
                    )
                    pca_analysis_raw = clean_section_headers(pca_analysis_raw, language)
                    heatmap_analysis_raw = clean_section_headers(
                        heatmap_analysis_raw, language
                    )

                    # FILTER OUT heatmap and PCA content for single-source analysis
                    if len(selected_sources) == 1:
                        print(
                            f"🔍 FILTERING: Single-source detected, removing heatmap/PCA content from principal findings"
                        )

                        # Import re module for regex operations
                        import re

                        # Remove heatmap analysis content
                        heatmap_patterns = [
                            r"🔥.*Análisis del Mapa de Calor.*",
                            r"🔥.*Heatmap Analysis.*",
                            r"Análisis del Mapa de Calor.*",
                            r"Heatmap Analysis.*",
                        ]

                        for pattern in heatmap_patterns:
                            principal_findings_raw = re.sub(
                                pattern, "", principal_findings_raw, flags=re.IGNORECASE
                            )

                        # Remove PCA analysis content
                        pca_patterns = [
                            r"📊.*Análisis de Componentes Principales.*",
                            r"📊.*Principal Component Analysis.*",
                            r"Análisis de Componentes Principales.*",
                            r"Principal Component Analysis.*",
                        ]

                        for pattern in pca_patterns:
                            principal_findings_raw = re.sub(
                                pattern, "", principal_findings_raw, flags=re.IGNORECASE
                            )

                        # Clean up any empty lines or sections that might result from filtering
                        principal_findings_raw = re.sub(
                            r"\n\s*\n\s*\n", "\n\n", principal_findings_raw
                        )  # Remove excessive empty lines
                        principal_findings_raw = principal_findings_raw.strip()

                        print(
                            f"🔍 FILTERING: Filtered content length: {len(principal_findings_raw)}"
                        )

                    # Use individual sections instead of combined narrative to avoid duplication
                    # For multi-source, we'll display each section separately with proper headers
                    if len(selected_sources) > 1:
                        print(
                            f"🔍 MULTI-SOURCE: Using individual sections instead of combined narrative"
                        )
                        # For multi-source, we'll show sections individually, so clear the combined narrative
                        principal_findings_content = ""
                    else:
                        # For single-source, use the combined narrative
                        principal_findings_content = principal_findings_raw

                    # Create modal content sections
                    modal_sections = []

                    # Header section with dynamic title - use Spanish
                    modal_sections.append(
                        html.H4(
                            f"🧠 Hallazgos Principales - {tool_display_name}",
                            className="text-primary mb-3",
                        )
                    )

                    # Skip metadata section for cleaner display - remove unwanted technical details
                    # metadata_info = html.Div(
                    #     [
                    #         html.H6(
                    #             f"Análisis Multi-Fuente: {', '.join(selected_sources)}",
                    #             className="text-muted mb-2",
                    #         ),
                    #         html.P(
                    #             [
                    #                 html.Small(
                    #                     f"Generated in {response_time_ms}ms using {model_used}",
                    #                     className="text-info",
                    #                 ),
                    #                 html.Br(),
                    #                 html.Small(
                    #                     f"Analysis period: {analysis_data['date_range_start']} to {analysis_data['date_range_end']}",
                    #                     className="text-muted",
                    #                 ),
                    #             ]
                    #         ),
                    #     ],
                    #     className="border-bottom pb-2 mb-3",
                    # )
                    # modal_sections.append(metadata_info)

                    # Executive Summary Section - Display with proper formatting
                    if executive_summary:
                        modal_sections.append(
                            html.Div(
                                [
                                    # Preserve line breaks and formatting from database
                                    html.Div(
                                        executive_summary,
                                        className="text-justify executive-summary-content",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Principal Findings Section - Display with proper formatting (contains all 7 sections)
                    if principal_findings_content:
                        modal_sections.append(
                            html.Div(
                                [
                                    # Preserve line breaks and section formatting from database
                                    html.Div(
                                        principal_findings_content,
                                        className="text-justify principal-findings-narrative",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Temporal Analysis Section (only for multi-source analysis)
                    temporal_analysis_raw = ai_content.get(
                        "temporal_analysis", "No temporal analysis available"
                    )
                    temporal_analysis_raw = clean_section_headers(
                        temporal_analysis_raw, language
                    )

                    if len(selected_sources) > 1 and temporal_analysis_raw:
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "⏰ Temporal Analysis"
                                        if language == "en"
                                        else "⏰ Análisis Temporal",
                                        className="text-info mb-3",
                                    ),
                                    html.Div(
                                        temporal_analysis_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Seasonal Analysis Section (only for multi-source analysis)
                    seasonal_analysis_raw = ai_content.get(
                        "seasonal_analysis", "No seasonal analysis available"
                    )
                    seasonal_analysis_raw = clean_section_headers(
                        seasonal_analysis_raw, language
                    )

                    if len(selected_sources) > 1 and seasonal_analysis_raw:
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "🗓️ Seasonal Analysis"
                                        if language == "en"
                                        else "🗓️ Análisis Estacional",
                                        className="text-success mb-3",
                                    ),
                                    html.Div(
                                        seasonal_analysis_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Fourier Analysis Section (only for multi-source analysis)
                    fourier_analysis_raw = ai_content.get(
                        "fourier_analysis", "No Fourier analysis available"
                    )
                    fourier_analysis_raw = clean_section_headers(
                        fourier_analysis_raw, language
                    )

                    if len(selected_sources) > 1 and fourier_analysis_raw:
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "🔬 Fourier Analysis"
                                        if language == "en"
                                        else "🔬 Análisis de Fourier",
                                        className="text-primary mb-3",
                                    ),
                                    html.Div(
                                        fourier_analysis_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Heatmap Analysis Section (only for multi-source analysis) - MOVED TO END
                    if len(selected_sources) > 1 and heatmap_analysis_raw:
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "🔥 Heatmap Analysis"
                                        if language == "en"
                                        else "🔥 Análisis de Mapa de Calor",
                                        className="text-danger mb-3",
                                    ),
                                    html.Div(
                                        heatmap_analysis_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # PCA Analysis Section (only for multi-source analysis) - MOVED TO END
                    if len(selected_sources) > 1 and pca_analysis_raw:
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "📊 PCA Analysis"
                                        if language == "en"
                                        else "📊 Análisis PCA",
                                        className="text-warning mb-3",
                                    ),
                                    html.Div(
                                        pca_analysis_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Conclusiones Section (Conclusions)
                    conclusions_raw = ai_content.get(
                        "conclusions", "No conclusions available"
                    )
                    conclusions_raw = clean_section_headers(conclusions_raw, language)

                    if conclusions_raw:
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "📝 Conclusions"
                                        if language == "en"
                                        else "📝 Conclusiones",
                                        className="text-secondary mb-3",
                                    ),
                                    html.Div(
                                        conclusions_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "🗓️ Seasonal Analysis"
                                        if language == "en"
                                        else "🗓️ Análisis Estacional",
                                        className="text-success mb-3",
                                    ),
                                    html.Div(
                                        seasonal_analysis_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Fourier Analysis Section (only for multi-source analysis)
                    fourier_analysis_raw = ai_content.get(
                        "fourier_analysis", "No Fourier analysis available"
                    )
                    fourier_analysis_raw = clean_section_headers(
                        fourier_analysis_raw, language
                    )

                    if len(selected_sources) > 1 and fourier_analysis_raw:
                        modal_sections.append(
                            html.Div(
                                [
                                    html.H5(
                                        "🔬 Fourier Analysis"
                                        if language == "en"
                                        else "🔬 Análisis de Fourier",
                                        className="text-primary mb-3",
                                    ),
                                    html.Div(
                                        fourier_analysis_raw,
                                        className="text-justify",
                                        style={
                                            "lineHeight": "1.6",
                                            "whiteSpace": "pre-line",
                                        },
                                    ),
                                ],
                                className="mb-4",
                            )
                        )

                    # Skip technical details section for cleaner display
                    # modal_sections.append(
                    #     html.Div(
                    #         [
                    #             html.H6(
                    #                 "Technical Details",
                    #                 className="text-muted mb-2",
                    #             ),
                    #             html.P(
                    #                 [
                    #                     html.Small(f"Tool: {selected_tool}"),
                    #                     html.Br(),
                    #                     html.Small(
                    #                         f"Sources: {len(selected_sources)} selected"
                    #                     ),
                    #                     html.Br(),
                    #                     html.Small(f"Language: {language}"),
                    #                     html.Br(),
                    #                     html.Small(
                    #                         f"Model: {model_used} ({token_count} tokens)"
                    #                     ),
                    #                 ],
                    #                 className="text-muted small",
                    #             ),
                    #         ],
                    #         className="border-top pt-2 mt-4",
                    #     )
                    # )

                    # Create final modal content
                    final_modal_content = html.Div(
                        modal_sections,
                        style={"maxHeight": "70vh", "overflowY": "auto"},
                    )

                    print("🎉 Modal content generated successfully")
                    return True, final_modal_content, dynamic_title, True, None

                except Exception as e:
                    total_error_time = time.time() - data_collection_start
                    print(
                        f"❌ Error generating Key Findings after {total_error_time:.2f}s: {e}"
                    )
                    import traceback

                    traceback.print_exc()

                    # Generate title even for error case
                    tool_display_name = (
                        get_tool_name(selected_tool, language)
                        if selected_tool
                        else "Herramienta"
                    )
                    sources_str = (
                        ", ".join(selected_sources) if selected_sources else "Fuentes"
                    )
                    dynamic_title = (
                        f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
                    )

                    error_content = html.Div(
                        [
                            html.H4(
                                "Error Generating Key Findings", className="text-danger"
                            ),
                            html.P(
                                f"An error occurred while generating the analysis: {str(e)}",
                                className="text-muted mb-3",
                            ),
                            html.P(
                                "Please try again. If the problem persists, check your internet connection and try selecting different data sources.",
                                className="text-muted small",
                            ),
                            html.P(
                                f"Time elapsed: {total_error_time:.2f}s",
                                className="text-muted small",
                            ),
                        ]
                    )
                    print("🔄 Returning error modal content")
                    return True, error_content, dynamic_title, False, None

            # Default return case - generate title for consistency
            tool_display_name = (
                get_tool_name(selected_tool, language)
                if selected_tool
                else "Herramienta"
            )
            sources_str = ", ".join(selected_sources) if selected_sources else "Fuentes"
            dynamic_title = f"🧠 Hallazgos para {tool_display_name} ({sources_str})"
            return False, "", dynamic_title, False, None

        # Regenerate callback and function removed to fix JavaScript errors
        # Save functionality removed - no longer needed
