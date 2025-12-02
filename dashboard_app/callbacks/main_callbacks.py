"""
Main content callbacks for the Management Tools Analysis Dashboard.

This module contains the main callback that generates the primary content
displayed in the dashboard, including all analysis sections and visualizations.
"""

import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Import database and utility functions
from fix_source_mapping import (
    map_display_names_to_source_ids,
    DBASE_OPTIONS as dbase_options,
)
from translations import get_text, get_tool_name, translate_source_name
from database import get_database_manager
from utils import (
    create_combined_dataset2,
    get_cache_key,
    get_cached_processed_data,
    cache_processed_data,
    _processed_data_cache,
    _cache_max_size,
    perform_comprehensive_pca_analysis,
    create_pca_figure,
    create_correlation_heatmap,
    create_mean_analysis_figure,
)

# Get database manager instance
db_manager = get_database_manager()


def register_main_callbacks(app):
    """Register the main content callback with the Dash app."""

    @app.callback(
        Output("main-content", "children"),
        Output("credits-collapse", "is_open"),
        Input("keyword-dropdown", "value"),
        Input("data-sources-store-v2", "data"),
        Input("language-store", "data"),
        prevent_initial_call=False,
    )
    def update_main_content(selected_keyword, selected_sources, language):
        if selected_sources is None:
            selected_sources = []

        # Use centralized mapping function
        selected_source_ids = map_display_names_to_source_ids(selected_sources)

        # Auto-collapse credits when both keyword and sources are selected
        credits_open = not (selected_keyword and selected_source_ids)

        if not selected_keyword or not selected_sources:
            return html.Div(
                get_text("please_select_tool_and_sources", language)
            ), credits_open

        datasets_norm = None  # Initialize to avoid scoping issues
        try:
            # Check cache first
            cached_data = get_cached_processed_data(selected_keyword, selected_sources)

            if cached_data:
                (
                    combined_dataset,
                    combined_dataset_fecha_formatted,
                    selected_source_names,
                ) = cached_data
            else:
                # Map display names to source IDs
                selected_source_ids = map_display_names_to_source_ids(selected_sources)

                print(
                    f"DEBUG: Getting data for keyword='{selected_keyword}', sources={selected_sources}"
                )
                print(f"DEBUG: Converted to source IDs: {selected_source_ids}")

                datasets_norm, sl_sc = db_manager.get_data_for_keyword(
                    selected_keyword, selected_source_ids
                )
                print(
                    f"DEBUG: Retrieved datasets_norm keys: {list(datasets_norm.keys()) if datasets_norm else 'None'}"
                )
                print(f"DEBUG: Retrieved sl_sc: {sl_sc}")

                if not datasets_norm:
                    print(f"DEBUG: No data retrieved for keyword='{selected_keyword}'")
                    translated_tool = get_tool_name(selected_keyword, language)
                    return html.Div(
                        get_text("no_data_available", language, keyword=translated_tool)
                    ), credits_open

                combined_dataset = create_combined_dataset2(
                    datasets_norm=datasets_norm,
                    selected_sources=sl_sc,
                    dbase_options=dbase_options,
                )
                print(
                    f"DEBUG: Combined dataset shape: {combined_dataset.shape if not combined_dataset.empty else 'Empty'}"
                )

                # Process data
                combined_dataset = combined_dataset.reset_index()
                date_column = combined_dataset.columns[0]
                combined_dataset[date_column] = pd.to_datetime(
                    combined_dataset[date_column]
                )
                combined_dataset = combined_dataset.rename(
                    columns={date_column: "Fecha"}
                )
                # Keep Fecha as datetime for calculations, format only for display in table
                combined_dataset_fecha_formatted = combined_dataset.copy()
                combined_dataset_fecha_formatted["Fecha"] = (
                    combined_dataset_fecha_formatted["Fecha"].dt.strftime("%Y-%m-%d")
                )

                # No longer need Bain/Crossref alignment since we preserve individual date ranges

                # Filter out rows where ALL selected sources are NaN (preserve partial data)
                data_columns = [dbase_options[src_id] for src_id in selected_source_ids]
                combined_dataset = combined_dataset.dropna(
                    subset=data_columns, how="all"
                )

                selected_source_names = [
                    translate_source_name(dbase_options[src_id], language)
                    for src_id in selected_source_ids
                ]

                # Cache the processed data
                cache_processed_data(
                    selected_keyword,
                    selected_sources,
                    (
                        combined_dataset,
                        combined_dataset_fecha_formatted,
                        selected_source_names,
                    ),
                )

            # Create content sections
            content = []

            # 1. Temporal Analysis 2D
            try:
                print(f"DEBUG: Creating initial temporal 2D figure for main content")

                # Use the utility function to create the temporal 2D figure
                from utils import create_temporal_2d_figure

                tool_display_name = (
                    get_tool_name(selected_keyword, language)
                    if selected_keyword
                    else None
                )
                temporal_2d_fig = create_temporal_2d_figure(
                    combined_dataset,
                    selected_source_names,
                    language,
                    tool_name=tool_display_name,
                )

                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("temporal_analysis_2d", language),
                                className="section-title",
                                id="section-temporal",
                            ),
                            html.Div(
                                dcc.Graph(
                                    id="temporal-2d-graph",
                                    figure=temporal_2d_fig,
                                    className="analysis-graph",
                                ),
                                className="graph-container",
                            ),
                            # Add time range filtering controls
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label(
                                                get_text("time_range", language),
                                                className="form-label",
                                            ),
                                            html.Div(
                                                [
                                                    html.Button(
                                                        get_text("all_data", language),
                                                        id="temporal-2d-all",
                                                        n_clicks=0,
                                                        className="btn btn-outline-primary btn-sm me-2",
                                                    ),
                                                    html.Button(
                                                        "20Y",
                                                        id="temporal-2d-20y",
                                                        n_clicks=0,
                                                        className="btn btn-outline-secondary btn-sm me-2",
                                                        title=language
                                                        if language == "es"
                                                        else "Last 20 years",
                                                    ),
                                                    html.Button(
                                                        "15Y",
                                                        id="temporal-2d-15y",
                                                        n_clicks=0,
                                                        className="btn btn-outline-secondary btn-sm me-2",
                                                        title="Últimos 15 años"
                                                        if language == "es"
                                                        else "Last 15 years",
                                                    ),
                                                    html.Button(
                                                        "10Y",
                                                        id="temporal-2d-10y",
                                                        n_clicks=0,
                                                        className="btn btn-outline-secondary btn-sm me-2",
                                                        title="Últimos 10 años"
                                                        if language == "es"
                                                        else "Last 10 years",
                                                    ),
                                                    html.Button(
                                                        "5Y",
                                                        id="temporal-2d-5y",
                                                        n_clicks=0,
                                                        className="btn btn-outline-secondary btn-sm me-2",
                                                        title="Últimos 5 años"
                                                        if language == "es"
                                                        else "Last 5 years",
                                                    ),
                                                ],
                                                className="d-flex flex-wrap gap-2 mb-3",
                                            ),
                                            # Date range slider
                                            html.Div(
                                                dcc.RangeSlider(
                                                    id="temporal-2d-date-range",
                                                    min=0,
                                                    max=100,
                                                    step=1,
                                                    value=[0, 100],
                                                    marks={},
                                                    tooltip={
                                                        "placement": "bottom",
                                                        "always_visible": True,
                                                    },
                                                ),
                                                className="mb-4",
                                            ),
                                        ],
                                        className="col-md-12",
                                    ),
                                ],
                                className="row mb-4",
                            ),
                        ],
                        className="analysis-section",
                        id="section-temporal-2d",
                    )
                )
                print("✅ Temporal Analysis 2D section added to main content")
            except Exception as e:
                print(f"DEBUG: Error creating initial temporal 2D figure: {e}")
                import traceback

                traceback.print_exc()
                temporal_2d_fig = go.Figure()
                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("temporal_analysis_2d", language),
                                className="section-title",
                            ),
                            html.P(
                                f"Error creating temporal analysis: {str(e)}",
                                className="text-danger",
                            ),
                        ],
                        className="analysis-section",
                    )
                )

            # 2. Mean Analysis
            try:
                print(f"DEBUG: Creating mean analysis figure")
                tool_display_name = (
                    get_tool_name(selected_keyword, language)
                    if selected_keyword
                    else None
                )
                mean_fig = create_mean_analysis_figure(
                    datasets_norm, selected_source_ids, language, tool_display_name
                )
                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("mean_analysis_title", language),
                                className="section-title",
                                id="section-mean",
                            ),
                            html.Div(
                                dcc.Graph(
                                    id="mean-analysis-graph",
                                    figure=mean_fig,
                                    className="analysis-graph",
                                ),
                                className="graph-container",
                            ),
                        ],
                        className="analysis-section",
                        id="section-mean-analysis",
                    )
                )
                print("✅ Mean Analysis section added to main content")
            except Exception as e:
                print(f"ERROR: Failed to create mean analysis figure: {e}")
                import traceback

                traceback.print_exc()
                mean_fig = go.Figure()

            # 3. PCA Analysis (only for multiple sources)
            if len(selected_sources) > 1:
                try:
                    print("DEBUG: Running comprehensive PCA analysis")
                    pca_results = perform_comprehensive_pca_analysis(
                        combined_dataset, selected_sources, language
                    )
                    if pca_results.get("success"):
                        # Create visualization using the DataFrame
                        pca_fig = create_pca_figure(
                            combined_dataset, selected_sources, language
                        )

                        content.append(
                            html.Div(
                                [
                                    html.H3(
                                        get_text("pca_title", language),
                                        className="section-title",
                                        id="section-pca",
                                    ),
                                    html.Div(
                                        dcc.Graph(
                                            id="pca-plot",
                                            figure=pca_fig,
                                            className="analysis-graph",
                                        ),
                                        className="graph-container",
                                    ),
                                ],
                                className="analysis-section",
                                id="section-pca-analysis",
                            )
                        )
                        print("✅ PCA Analysis section added to main content")
                    else:
                        print(
                            f"PCA analysis failed: {pca_results.get('error', 'Unknown error')}"
                        )
                        content.append(
                            html.Div(
                                [
                                    html.H3(
                                        get_text("pca_title", language),
                                        className="section-title",
                                    ),
                                    html.P(
                                        f"PCA analysis failed: {pca_results.get('error', 'Unknown error')}",
                                        className="text-warning",
                                    ),
                                ],
                                className="analysis-section",
                            )
                        )
                except Exception as e:
                    print(f"Error in PCA analysis: {e}")
                    import traceback

                    traceback.print_exc()
                    content.append(
                        html.Div(
                            [
                                html.H3(
                                    get_text("pca_title", language),
                                    className="section-title",
                                ),
                                html.P(
                                    f"Error in PCA analysis: {str(e)}",
                                    className="text-danger",
                                ),
                            ],
                            className="analysis-section",
                        )
                    )

            # 4. Correlation Heatmap (only for multiple sources)
            if len(selected_sources) > 1:
                try:
                    print("DEBUG: Creating correlation heatmap")
                    heatmap_fig = create_correlation_heatmap(
                        combined_dataset, selected_sources, language
                    )
                    content.append(
                        html.Div(
                            [
                                html.H3(
                                    get_text("correlation_heatmap_title", language),
                                    className="section-title",
                                    id="section-correlation",
                                ),
                                html.P(
                                    get_text("heatmap_instructions", language),
                                    className="text-muted mb-3",
                                ),
                                html.Div(
                                    dcc.Graph(
                                        id="correlation-heatmap",
                                        figure=heatmap_fig,
                                        className="analysis-graph clickable-heatmap",
                                    ),
                                    className="graph-container",
                                ),
                            ],
                            className="analysis-section",
                            id="section-correlation-analysis",
                        )
                    )
                    print("✅ Correlation Heatmap section added to main content")
                except Exception as e:
                    print(f"Error creating correlation heatmap: {e}")
                    import traceback

                    traceback.print_exc()
                    content.append(
                        html.Div(
                            [
                                html.H3(
                                    get_text("correlation_heatmap_title", language),
                                    className="section-title",
                                ),
                                html.P(
                                    f"Error creating correlation heatmap: {str(e)}",
                                    className="text-danger",
                                ),
                            ],
                            className="analysis-section",
                        )
                    )

            # 5. 3D Temporal Analysis (only for multiple sources)
            if len(selected_sources) > 1:
                try:
                    # Get source options for dropdowns
                    source_options = [
                        {"label": source, "value": source}
                        for source in selected_source_names
                    ]

                    content.append(
                        html.Div(
                            [
                                html.H3(
                                    get_text("temporal_analysis_3d", language),
                                    className="section-title",
                                    id="section-3d",
                                ),
                                html.Div(
                                    [
                                        html.Label(
                                            get_text("select_y_axis", language),
                                            className="form-label",
                                        ),
                                        dcc.Dropdown(
                                            id="y-axis-3d",
                                            options=source_options,
                                            value=selected_source_names[0]
                                            if len(selected_source_names) > 0
                                            else None,
                                            className="mb-3",
                                        ),
                                        html.Label(
                                            get_text("select_z_axis", language),
                                            className="form-label",
                                        ),
                                        dcc.Dropdown(
                                            id="z-axis-3d",
                                            options=source_options,
                                            value=selected_source_names[1]
                                            if len(selected_source_names) > 1
                                            else None,
                                            className="mb-3",
                                        ),
                                        html.Div(
                                            [
                                                html.Button(
                                                    get_text("monthly", language),
                                                    id="temporal-3d-monthly",
                                                    n_clicks=0,
                                                    className="btn btn-outline-primary me-2",
                                                ),
                                                html.Button(
                                                    get_text("annual", language),
                                                    id="temporal-3d-annual",
                                                    n_clicks=0,
                                                    className="btn btn-outline-secondary",
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    dcc.Graph(
                                        id="temporal-3d-graph",
                                        className="analysis-graph",
                                    ),
                                    className="graph-container",
                                ),
                            ],
                            className="analysis-section",
                            id="section-temporal-3d",
                        )
                    )
                    print("✅ 3D Temporal Analysis section added to main content")
                except Exception as e:
                    print(f"Error creating 3D temporal analysis section: {e}")
                    content.append(
                        html.Div(
                            [
                                html.H3(
                                    get_text("temporal_analysis_3d", language),
                                    className="section-title",
                                ),
                                html.P(
                                    f"Error creating 3D temporal analysis: {str(e)}",
                                    className="text-danger",
                                ),
                            ],
                            className="analysis-section",
                        )
                    )

            # 6. Seasonal Analysis (if sufficient data)
            try:
                # Check if any source has sufficient data for seasonal analysis
                has_seasonal_data = False
                for src_id in selected_source_ids:
                    if src_id in datasets_norm:
                        data = datasets_norm[src_id].dropna()
                        if len(data) >= 24:  # Need at least 24 data points
                            has_seasonal_data = True
                            break

                if has_seasonal_data:
                    content.append(
                        html.Div(
                            [
                                html.H3(
                                    get_text("seasonal_analysis", language),
                                    className="section-title",
                                    id="section-seasonal",
                                ),
                                html.Div(
                                    [
                                        html.Label(
                                            get_text("select_source", language),
                                            className="form-label",
                                        ),
                                        dcc.Dropdown(
                                            id="seasonal-source-select",
                                            options=[
                                                {"label": source, "value": source}
                                                for source in selected_source_names
                                            ],
                                            value=selected_source_names[0]
                                            if selected_source_names
                                            else None,
                                            className="mb-3",
                                        ),
                                    ],
                                    className="row mb-3",
                                ),
                                html.Div(
                                    dcc.Graph(
                                        id="seasonal-analysis-graph",
                                        className="analysis-graph",
                                    ),
                                    className="graph-container",
                                ),
                            ],
                            className="analysis-section",
                            id="section-seasonal-analysis",
                        )
                    )
                    print("✅ Seasonal Analysis section added to main content")
            except Exception as e:
                print(f"Error creating seasonal analysis section: {e}")
                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("seasonal_analysis", language),
                                className="section-title",
                            ),
                            html.P(
                                f"Error creating seasonal analysis: {str(e)}",
                                className="text-danger",
                            ),
                        ],
                        className="analysis-section",
                    )
                )

            # 7. Fourier Analysis (if sufficient data)
            try:
                # Check if any source has sufficient data for Fourier analysis
                has_fourier_data = False
                for src_id in selected_source_ids:
                    if src_id in datasets_norm:
                        data = datasets_norm[src_id].dropna()
                        if len(data) >= 10:  # Need at least 10 data points
                            has_fourier_data = True
                            break

                if has_fourier_data:
                    content.append(
                        html.Div(
                            [
                                html.H3(
                                    get_text("fourier_analysis", language),
                                    className="section-title",
                                    id="section-fourier",
                                ),
                                html.Div(
                                    [
                                        html.Label(
                                            get_text("select_source", language),
                                            className="form-label",
                                        ),
                                        dcc.Dropdown(
                                            id="fourier-source-select",
                                            options=[
                                                {"label": source, "value": source}
                                                for source in selected_source_names
                                            ],
                                            value=selected_source_names[0]
                                            if selected_source_names
                                            else None,
                                            className="mb-3",
                                        ),
                                    ],
                                    className="row mb-3",
                                ),
                                html.Div(
                                    dcc.Graph(
                                        id="fourier-analysis-graph",
                                        className="analysis-graph",
                                    ),
                                    className="graph-container",
                                ),
                            ],
                            className="analysis-section",
                            id="section-fourier-analysis",
                        )
                    )
                    print("✅ Fourier Analysis section added to main content")
            except Exception as e:
                print(f"Error creating Fourier analysis section: {e}")
                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("fourier_analysis", language),
                                className="section-title",
                            ),
                            html.P(
                                f"Error creating Fourier analysis: {str(e)}",
                                className="text-danger",
                            ),
                        ],
                        className="analysis-section",
                    )
                )

            # 8. Regression Analysis (only for multiple sources)
            if len(selected_sources) > 1:
                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("regression_analysis", language),
                                className="section-title",
                                id="section-regression",
                            ),
                            html.P(
                                get_text("regression_instructions", language),
                                className="text-muted mb-3",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            id="regression-graph",
                                            className="analysis-graph",
                                        ),
                                        className="col-md-8",
                                    ),
                                    html.Div(
                                        id="regression-equations",
                                        className="col-md-4",
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="analysis-section",
                        id="section-regression-analysis",
                    )
                )
                print("✅ Regression Analysis section added to main content")

            # 9. Data Table
            try:
                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("data_table_title", language),
                                className="section-title",
                                id="section-table",
                            ),
                            dash_table.DataTable(
                                id="data-table",
                                columns=[
                                    {"name": col, "id": col}
                                    for col in combined_dataset_fecha_formatted.columns
                                ],
                                data=combined_dataset_fecha_formatted.to_dict(
                                    "records"
                                ),
                                page_size=10,
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left", "padding": "10px"},
                                style_header={
                                    "backgroundColor": "rgb(230, 230, 230)",
                                    "fontWeight": "bold",
                                },
                                style_data_conditional=[
                                    {
                                        "if": {"row_index": "odd"},
                                        "backgroundColor": "rgb(248, 248, 248)",
                                    }
                                ],
                            ),
                        ],
                        className="analysis-section",
                        id="section-data-table",
                    )
                )
                print("✅ Data Table section added to main content")
            except Exception as e:
                print(f"Error creating data table: {e}")
                content.append(
                    html.Div(
                        [
                            html.H3(
                                get_text("data_table_title", language),
                                className="section-title",
                            ),
                            html.P(
                                f"Error creating data table: {str(e)}",
                                className="text-danger",
                            ),
                        ],
                        className="analysis-section",
                    )
                )

            # 9. Performance Metrics section
            try:
                # Get database stats for performance metrics
                table_stats = (
                    db_manager.get_table_stats()
                    if hasattr(db_manager, "get_table_stats")
                    else {}
                )
                total_records = (
                    sum(
                        stats.get("row_count", 0)
                        for stats in table_stats.values()
                        if "error" not in stats
                    )
                    if table_stats
                    else 0
                )
                total_keywords = (
                    sum(
                        stats.get("keyword_count", 0)
                        for stats in table_stats.values()
                        if "error" not in stats
                    )
                    if table_stats
                    else 0
                )

                # Calculate additional metrics
                data_points = (
                    len(combined_dataset) if "combined_dataset" in locals() else 0
                )
                selected_tool = (
                    get_tool_name(selected_keyword, language)
                    if selected_keyword
                    else "N/A"
                )

                content.append(
                    html.Div(
                        [
                            html.H3(
                                [
                                    html.I(
                                        className="fas fa-tachometer-alt me-2",
                                        style={"color": "#17a2b8"},
                                    ),
                                    get_text("performance_metrics", language),
                                ],
                                className="section-title d-flex align-items-center",
                                id="section-performance",
                            ),
                            html.Div(
                                [
                                    # Database Statistics Card
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H5(
                                                        get_text("database_statistics", language),
                                                        className="card-title text-primary",
                                                    ),
                                                    html.Hr(className="my-2"),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                get_text("total_records", language)
                                                            ),
                                                            f"{total_records:,}",
                                                        ],
                                                        className="mb-2 text-dark",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(get_text("unique_keywords", language)),
                                                            f"{total_keywords:,}",
                                                        ],
                                                        className="mb-2 text-dark",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                get_text("data_sources_count", language)
                                                            ),
                                                            f"{len(selected_sources)}",
                                                        ],
                                                        className="mb-0 text-dark",
                                                    ),
                                                ],
                                                className="card-body",
                                            )
                                        ],
                                        className="card border-primary shadow-sm h-100",
                                    ),
                                    # Current Analysis Card
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H5(
                                                        get_text("current_query", language),
                                                        className="card-title text-success",
                                                    ),
                                                    html.Hr(className="my-2"),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                "Selected Tool: "
                                                            ),
                                                            selected_tool,
                                                        ],
                                                        className="mb-2 text-dark",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                "Data Points: "
                                                            ),
                                                            f"{data_points:,}",
                                                        ],
                                                        className="mb-2 text-dark",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong("Sources: "),
                                                            ", ".join(
                                                                selected_sources[:3]
                                                            )
                                                            + (
                                                                "..."
                                                                if len(selected_sources)
                                                                > 3
                                                                else ""
                                                            ),
                                                        ],
                                                        className="mb-0 text-dark",
                                                    ),
                                                ],
                                                className="card-body",
                                            )
                                        ],
                                        className="card border-success shadow-sm h-100",
                                    ),
                                    # System Performance Card
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H5(
                                                        get_text("system_performance", language),
                                                        className="card-title text-warning",
                                                    ),
                                                    html.Hr(className="my-2"),
                                                    html.P(
                                                        [
                                                            html.Strong(
                                                                get_text("analysis_type", language)
                                                            ),
                                                            get_text("multi_source", language)
                                                            if len(selected_sources) > 1
                                                            else get_text("single_source", language),
                                                        ],
                                                        className="mb-2 text-dark",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(get_text("language_label", language)),
                                                            language.upper(),
                                                        ],
                                                        className="mb-2 text-dark",
                                                    ),
                                                    html.P(
                                                        [
                                                            html.Strong(get_text("dashboard_label", language)),
                                                            get_text("dashboard_name", language),
                                                        ],
                                                        className="mb-0 text-dark",
                                                    ),
                                                ],
                                                className="card-body",
                                            )
                                        ],
                                        className="card border-warning shadow-sm h-100",
                                    ),
                                ],
                                className="row g-3",
                            ),
                            # Performance Footer
                            html.Div(
                                [
                                    html.Hr(),
                                    html.P(
                                        [
                                            html.I(
                                                className="fas fa-info-circle me-2 text-info"
                                            ),
                                            get_text("performance_info", language),
                                        ],
                                        className="text-muted text-center mb-0 small",
                                    ),
                                ],
                                className="mt-3",
                            ),
                        ],
                        className="analysis-section bg-gradient p-4 mt-4",
                        id="section-performance",
                        style={
                            "background": "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)",
                            "border": "2px solid #dee2e6",
                            "borderRadius": "10px",
                        },
                    )
                )
                print("✅ Performance Metrics section added to main content")
            except Exception as e:
                print(f"Error adding performance metrics: {e}")
                # Fallback simple performance section
                content.append(
                    html.Div(
                        [
                            html.H3(
                                [
                                    html.I(
                                        className="fas fa-tachometer-alt me-2",
                                        style={"color": "#17a2b8"},
                                    ),
                                    get_text("performance_metrics", language),
                                ],
                                className="section-title",
                            ),
                            html.P(
                                [
                                    html.Strong(get_text("current_query", language)),
                                    f"{len(selected_sources)} " + (get_text("data_sources_count", language).rstrip(":")),
                                ],
                                className="text-muted",
                            ),
                        ],
                        className="analysis-section bg-light p-3 mt-4",
                        id="section-performance",
                    )
                )

            return html.Div(content), credits_open

        except Exception as e:
            return html.Div(f"Error: {str(e)}"), credits_open
