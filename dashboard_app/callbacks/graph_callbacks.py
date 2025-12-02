"""
Graph callbacks for the Management Tools Analysis Dashboard.

This module contains all callbacks related to graph generation and updates,
including temporal analysis, 3D plots, seasonal analysis, Fourier analysis,
and regression analysis.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import html, callback_context, no_update
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.fft import fft, fftfreq

# Import database and utility functions
from fix_source_mapping import (
    map_display_names_to_source_ids,
    DBASE_OPTIONS as dbase_options,
)
from translations import get_text, get_tool_name, translate_source_name
from database import get_database_manager
from utils import (
    create_combined_dataset2,
    create_translation_mapping,
    get_original_column_name,
    safe_dataframe_column_access,
)

# Get database manager instance
db_manager = get_database_manager()

# Color definitions for graphs
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

source_colors_by_db = {
    "Google Trends": "#1f77b4",
    "Google Books Ngrams": "#ff7f0e",
    "Bain - Usabilidad": "#d62728",
    "Bain - Satisfacción": "#9467bd",
    "Crossref.org": "#2ca02c",
}

color_map = {
    dbase_options[key]: source_colors_by_db.get(
        dbase_options[key], colors[i % len(colors)]
    )
    for i, key in enumerate(dbase_options.keys())
}


def aggregate_data_for_3d(data, frequency, source_name):
    """Aggregate data based on frequency and source type"""
    if frequency == "monthly":
        return data  # Return as-is for monthly

    # Annual aggregation with different methods per source
    if "Google Trends" in source_name:
        # GT: Average
        return data.resample("Y").mean()
    elif "Crossref" in source_name:
        # CR: Sum
        return data.resample("Y").sum()
    elif "Google Books" in source_name:
        # GB: Sum
        return data.resample("Y").sum()
    else:
        # Bain (BU/BS): Average
        return data.resample("Y").mean()


def register_graph_callbacks(app):
    """Register all graph-related callbacks with the Dash app."""

    # Register heatmap click callback for regression analysis
    register_heatmap_click_callback(app)

    @app.callback(
        Output("temporal-2d-graph", "figure"),
        [
            Input("temporal-2d-all", "n_clicks"),
            Input("temporal-2d-20y", "n_clicks"),
            Input("temporal-2d-15y", "n_clicks"),
            Input("temporal-2d-10y", "n_clicks"),
            Input("temporal-2d-5y", "n_clicks"),
            Input("temporal-2d-date-range", "value"),
            Input("keyword-dropdown", "value"),
            Input("data-sources-store-v2", "data"),
            Input("language-store", "data"),
        ],
        prevent_initial_call=True,
    )
    def update_temporal_2d_analysis(
        all_clicks,
        y20_clicks,
        y15_clicks,
        y10_clicks,
        y5_clicks,
        slider_values,
        selected_keyword,
        selected_sources,
        language,
    ):
        print(f"DEBUG: update_temporal_2d_analysis called")
        print(f"DEBUG: selected_keyword={selected_keyword}")
        print(f"DEBUG: selected_sources={selected_sources}")
        print(f"DEBUG: slider_values={slider_values}")

        if selected_sources is None:
            selected_sources = []

        # Map display names to source IDs
        selected_source_ids = map_display_names_to_source_ids(selected_sources)
        print(f"DEBUG: mapped to source IDs: {selected_source_ids}")

        if not selected_keyword or not selected_sources:
            print(f"DEBUG: Returning empty figure - missing keyword or sources")
            return go.Figure()

        try:
            datasets_norm, sl_sc = db_manager.get_data_for_keyword(
                selected_keyword, selected_source_ids
            )
            print(
                f"DEBUG: Retrieved datasets_norm keys: {list(datasets_norm.keys()) if datasets_norm else 'None'}"
            )

            if not datasets_norm:
                print(f"DEBUG: No data retrieved from database")
                return go.Figure()

            combined_dataset = create_combined_dataset2(
                datasets_norm=datasets_norm,
                selected_sources=sl_sc,
                dbase_options=dbase_options,
            )
            print(
                f"DEBUG: Combined dataset shape: {combined_dataset.shape if not combined_dataset.empty else 'Empty'}"
            )

            combined_dataset = combined_dataset.reset_index()
            date_column = combined_dataset.columns[0]
            combined_dataset[date_column] = pd.to_datetime(
                combined_dataset[date_column]
            )
            combined_dataset = combined_dataset.rename(columns={date_column: "Fecha"})

            # Sort by date to ensure chronological order for slider indices
            combined_dataset = combined_dataset.sort_values("Fecha").reset_index(
                drop=True
            )

            # Filter out rows where ALL selected sources are NaN (preserve partial data)
            data_columns = [dbase_options[src_id] for src_id in selected_source_ids]
            combined_dataset = combined_dataset.dropna(subset=data_columns, how="all")

            selected_source_names = [
                translate_source_name(dbase_options[src_id], language)
                for src_id in selected_source_ids
            ]
            print(f"DEBUG: Selected source names: {selected_source_names}")

            # Default to full date range
            start_date = combined_dataset["Fecha"].min().date()
            end_date = combined_dataset["Fecha"].max().date()
            print(f"DEBUG: Default date range: {start_date} to {end_date}")

            # Check if any button was clicked or slider moved
            try:
                ctx = dash.callback_context
                if ctx.triggered and len(ctx.triggered) > 0:
                    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
                    print(f"DEBUG: Triggered by: {trigger_id}")

                    if trigger_id in [
                        "temporal-2d-all",
                        "temporal-2d-20y",
                        "temporal-2d-15y",
                        "temporal-2d-10y",
                        "temporal-2d-5y",
                    ]:
                        # Button was clicked - calculate new date range
                        if trigger_id == "temporal-2d-all":
                            start_date = combined_dataset["Fecha"].min().date()
                            end_date = combined_dataset["Fecha"].max().date()
                        else:
                            # Calculate years back from end
                            years_back = int(trigger_id.split("-")[-1].replace("y", ""))
                            end_date = combined_dataset["Fecha"].max().date()
                            start_date = (
                                pd.to_datetime(end_date)
                                - pd.DateOffset(years=years_back)
                            ).date()
                        print(
                            f"DEBUG: Updated date range from button: {start_date} to {end_date}"
                        )

                    elif trigger_id == "temporal-2d-date-range":
                        # Slider was moved - convert indices to dates
                        if slider_values is not None and len(slider_values) == 2:
                            start_idx, end_idx = slider_values
                            if start_idx < len(combined_dataset) and end_idx < len(
                                combined_dataset
                            ):
                                start_date = (
                                    combined_dataset["Fecha"].iloc[start_idx].date()
                                )
                                end_date = (
                                    combined_dataset["Fecha"].iloc[end_idx].date()
                                )
                                print(
                                    f"DEBUG: Updated date range from slider: {start_date} to {end_date}"
                                )
            except Exception as e:
                # Handle case when callback context is not available (e.g., during testing)
                print(
                    f"DEBUG: No callback context available, using default date range: {e}"
                )
                # Keep default date range (full range)

            print(f"DEBUG: Creating temporal 2D figure...")
            tool_display_name = (
                get_tool_name(selected_keyword, language) if selected_keyword else None
            )

            # Import the create_temporal_2d_figure function from utils
            from utils import create_temporal_2d_figure

            figure = create_temporal_2d_figure(
                combined_dataset,
                selected_source_names,
                language,
                start_date,
                end_date,
                tool_name=tool_display_name,
            )
            print(
                f"DEBUG: Figure created with {len(figure.data) if hasattr(figure, 'data') else 0} traces"
            )
            return figure
        except Exception as e:
            print(f"Error in temporal 2D analysis: {e}")
            import traceback

            traceback.print_exc()
            return go.Figure()

    @app.callback(
        Output("temporal-2d-date-range", "min"),
        Output("temporal-2d-date-range", "max"),
        Output("temporal-2d-date-range", "marks"),
        Output("temporal-2d-date-range", "value"),
        Input("keyword-dropdown", "value"),
        Input("data-sources-store-v2", "data"),
    )
    def update_temporal_slider_properties(selected_keyword, selected_sources):
        print(f"DEBUG: update_temporal_slider_properties called")
        print(f"DEBUG: selected_keyword={selected_keyword}")
        print(f"DEBUG: selected_sources={selected_sources}")

        if selected_sources is None:
            selected_sources = []

        selected_source_ids = map_display_names_to_source_ids(selected_sources)
        print(f"DEBUG: mapped to source IDs: {selected_source_ids}")

        if not selected_keyword or not selected_sources:
            print(
                f"DEBUG: Returning default slider values - missing keyword or sources"
            )
            return 0, 100, {}, [0, 100]

        try:
            datasets_norm, sl_sc = db_manager.get_data_for_keyword(
                selected_keyword, selected_source_ids
            )
            print(
                f"DEBUG: Retrieved datasets_norm keys: {list(datasets_norm.keys()) if datasets_norm else 'None'}"
            )

            if not datasets_norm:
                print(f"DEBUG: No data retrieved from database")
                return 0, 100, {}, [0, 100]

            combined_dataset = create_combined_dataset2(
                datasets_norm=datasets_norm,
                selected_sources=sl_sc,
                dbase_options=dbase_options,
            )
            print(
                f"DEBUG: Combined dataset shape: {combined_dataset.shape if not combined_dataset.empty else 'Empty'}"
            )

            combined_dataset = combined_dataset.reset_index()
            date_column = combined_dataset.columns[0]
            combined_dataset[date_column] = pd.to_datetime(
                combined_dataset[date_column]
            )
            combined_dataset = combined_dataset.rename(columns={date_column: "Fecha"})

            # Filter out rows where ALL selected sources are NaN (preserve partial data)
            data_columns = [dbase_options[src_id] for src_id in selected_source_ids]
            combined_dataset = combined_dataset.dropna(subset=data_columns, how="all")

            print(f"DEBUG: Processed dataset shape: {combined_dataset.shape}")
            print(
                f"DEBUG: Date range: {combined_dataset['Fecha'].min()} to {combined_dataset['Fecha'].max()}"
            )

            # Create marks for the slider
            n_marks = min(5, len(combined_dataset))  # Limit to 5 marks
            mark_indices = [
                int(i * (len(combined_dataset) - 1) / (n_marks - 1))
                for i in range(n_marks)
            ]
            marks = {
                idx: combined_dataset["Fecha"].iloc[idx].strftime("%Y-%m")
                for idx in mark_indices
            }
            print(f"DEBUG: Created {len(marks)} slider marks")

            return 0, len(combined_dataset) - 1, marks, [0, len(combined_dataset) - 1]
        except Exception as e:
            print(f"DEBUG: Error in update_temporal_slider_properties: {e}")
            import traceback

            traceback.print_exc()
            return 0, 100, {}, [0, 100]

    @app.callback(
        Output("temporal-3d-graph", "figure"),
        [
            Input("y-axis-3d", "value"),
            Input("z-axis-3d", "value"),
            Input("temporal-3d-monthly", "n_clicks"),
            Input("temporal-3d-annual", "n_clicks"),
            Input("keyword-dropdown", "value"),
            Input("data-sources-store-v2", "data"),
            Input("language-store", "data"),
        ],
    )
    def update_3d_plot(
        y_axis,
        z_axis,
        monthly_clicks,
        annual_clicks,
        selected_keyword,
        selected_sources,
        language,
    ):
        if selected_sources is None:
            selected_sources = []

        selected_source_ids = map_display_names_to_source_ids(selected_sources)

        if not all([y_axis, z_axis, selected_keyword]) or len(selected_sources) < 2:
            return {}

        # Determine frequency based on button clicks
        ctx = dash.callback_context
        frequency = "monthly"  # Default

        if ctx.triggered:
            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if trigger_id == "temporal-3d-annual":
                frequency = "annual"
            elif trigger_id == "temporal-3d-monthly":
                frequency = "monthly"

        try:
            datasets_norm, sl_sc = db_manager.get_data_for_keyword(
                selected_keyword, selected_source_ids
            )
            combined_dataset = create_combined_dataset2(
                datasets_norm=datasets_norm,
                selected_sources=sl_sc,
                dbase_options=dbase_options,
            )

            combined_dataset = combined_dataset.reset_index()
            date_column = combined_dataset.columns[0]
            combined_dataset[date_column] = pd.to_datetime(
                combined_dataset[date_column]
            )
            combined_dataset = combined_dataset.rename(columns={date_column: "Fecha"})
            combined_dataset = combined_dataset.set_index("Fecha")

            # Create proper translation mapping
            translation_mapping = create_translation_mapping(
                selected_source_ids, language
            )

            # Use safe column access for y_axis
            y_data_column = safe_dataframe_column_access(
                combined_dataset, y_axis, translation_mapping
            )
            z_data_column = safe_dataframe_column_access(
                combined_dataset, z_axis, translation_mapping
            )

            if y_data_column is None or z_data_column is None:
                print(
                    f"ERROR: Could not find columns for 3D plot: y_axis={y_axis}, z_axis={z_axis}"
                )
                return {}

            # Apply aggregation based on frequency and source type
            y_data = aggregate_data_for_3d(y_data_column, frequency, y_axis)
            z_data = aggregate_data_for_3d(z_data_column, frequency, z_axis)

            # Align the data (they might have different date ranges after aggregation)
            common_index = y_data.index.intersection(z_data.index)
            y_data = y_data.loc[common_index]
            z_data = z_data.loc[common_index]

            # Fix color lookup for 3D plot: use original database name for color mapping
            original_y_name = get_original_column_name(y_axis, translation_mapping)
            plot_color = color_map.get(original_y_name, "#000000")
            print(
                f"DEBUG: 3D plot color for {y_axis} -> Original: {original_y_name} -> Color: {plot_color}"
            )

            fig = go.Figure(
                data=[
                    go.Scatter3d(
                        x=common_index,
                        y=y_data.values,
                        z=z_data.values,
                        mode="lines",
                        line=dict(color=plot_color, width=3),
                        name=f"{y_axis} vs {z_axis} ({frequency})",
                    )
                ]
            )

            # Create title with tool name if provided
            base_title = get_text(
                "temporal_3d_title",
                language,
                y_axis=y_axis,
                z_axis=z_axis,
                frequency=frequency.capitalize(),
            )
            tool_display_name = (
                get_tool_name(selected_keyword, language) if selected_keyword else None
            )

            # Create a two-line title with the tool name
            title_line1 = get_text(
                "temporal_3d_title",
                language,
                y_axis=y_axis,
                z_axis=z_axis,
                frequency=frequency.capitalize(),
            )
            title_line2 = (
                get_tool_name(selected_keyword, language) if selected_keyword else None
            )

            # Combine into two lines if tool name is available
            if title_line2:
                full_title = f"{title_line1}<br>{title_line2}"
            else:
                full_title = title_line1

            fig.update_layout(
                title={
                    "text": full_title,
                    "x": 0.5,
                    "xanchor": "center",
                    "y": 0.95,
                    "yanchor": "top",
                    "font": {"size": 14},
                },
                scene=dict(
                    xaxis_title=get_text("date", language),
                    yaxis_title=y_axis,
                    zaxis_title=z_axis,
                ),
                height=600,
            )

            # Add source URL annotation as legend-style outside the graph
            source_text = (
                get_text("source", language) + " https://dashboard.solidum360.com/"
            )
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=1,
                y=1.08,  # Position relative to plot (adjusted for 3D Temporal Analysis)
                text=source_text,
                showarrow=False,
                font=dict(size=12),
                align="left",
            )
            return fig
        except Exception as e:
            print(f"Error in 3D temporal analysis: {e}")
            # Return empty figure instead of empty dict
            fig = go.Figure()
            fig.update_layout(
                title=get_text("temporal_3d_error", language),
                xaxis_title="",
                yaxis_title="",
                height=500,
            )
            return fig

    @app.callback(
        Output("seasonal-analysis-graph", "figure"),
        [
            Input("seasonal-source-select", "value"),
            Input("keyword-dropdown", "value"),
            Input("data-sources-store-v2", "data"),
            Input("language-store", "data"),
        ],
    )
    def update_seasonal_analysis(
        selected_source, selected_keyword, selected_sources, language
    ):
        if selected_sources is None:
            selected_sources = []

        selected_source_ids = map_display_names_to_source_ids(selected_sources)

        if not all([selected_source, selected_keyword]) or not selected_sources:
            return {}

        try:
            datasets_norm, sl_sc = db_manager.get_data_for_keyword(
                selected_keyword, selected_source_ids
            )
            combined_dataset = create_combined_dataset2(
                datasets_norm=datasets_norm,
                selected_sources=sl_sc,
                dbase_options=dbase_options,
            )

            combined_dataset = combined_dataset.reset_index()
            date_column = combined_dataset.columns[0]
            combined_dataset[date_column] = pd.to_datetime(
                combined_dataset[date_column]
            )
            combined_dataset = combined_dataset.rename(columns={date_column: "Fecha"})

            # Create proper translation mapping
            translation_mapping = create_translation_mapping(
                selected_source_ids, language
            )

            # Use safe column access
            ts_data_column = safe_dataframe_column_access(
                combined_dataset, selected_source, translation_mapping
            )
            if ts_data_column is None:
                return {}

            ts_data = ts_data_column.dropna()
            if len(ts_data) < 24:
                return {}

            # Additional safety check for None values in the data
            if ts_data is None or len(ts_data) == 0:
                return {}

            decomposition = seasonal_decompose(ts_data, model="additive", period=12)

            fig = make_subplots(
                rows=4,
                cols=1,
                subplot_titles=[
                    get_text("original_series", language),
                    get_text("trend", language),
                    get_text("seasonal", language),
                    get_text("residuals", language),
                ],
                vertical_spacing=0.1,
            )

            fig.add_trace(
                go.Scatter(x=combined_dataset["Fecha"], y=ts_data, name="Original"),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=combined_dataset["Fecha"], y=decomposition.trend, name="Tendencia"
                ),
                row=2,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=combined_dataset["Fecha"],
                    y=decomposition.seasonal,
                    name="Estacional",
                ),
                row=3,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=combined_dataset["Fecha"], y=decomposition.resid, name="Residuos"
                ),
                row=4,
                col=1,
            )

            # Create title with tool name if provided
            if selected_source:
                base_title = get_text(
                    "seasonal_title", language, source=selected_source
                )
            else:
                base_title = get_text("seasonal_analysis", language)
            tool_display_name = (
                get_tool_name(selected_keyword, language) if selected_keyword else None
            )
            if tool_display_name:
                title_text = f"{base_title} - {tool_display_name}"
            else:
                title_text = base_title

            fig.update_layout(height=600, title=title_text, showlegend=False)

            # Add source URL annotation as legend-style outside the graph
            source_text = (
                get_text("source", language) + " https://dashboard.solidum360.com/"
            )
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=1,
                y=1.1,  # Position relative to plot
                text=source_text,
                showarrow=False,
                font=dict(size=12),
                align="left",
            )
            return fig
        except Exception as e:
            return {}

    # Consolidated regression analysis callback (handles both keyword changes and heatmap clicks)

    @app.callback(
        Output("fourier-analysis-graph", "figure"),
        [
            Input("fourier-source-select", "value"),
            Input("keyword-dropdown", "value"),
            Input("data-sources-store-v2", "data"),
            Input("language-store", "data"),
        ],
    )
    def update_fourier_analysis(
        selected_source, selected_keyword, selected_sources, language
    ):
        if selected_sources is None:
            selected_sources = []

        selected_source_ids = map_display_names_to_source_ids(selected_sources)

        if not selected_keyword or not selected_sources:
            return go.Figure()

        if not selected_source:
            fig = go.Figure()
            fig.add_annotation(
                text=get_text("select_source_fourier", language),
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=14),
            )
            fig.update_layout(
                title=get_text("fourier_analysis_periodogram", language),
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False),
            )
            return fig

        # Map display name back to numeric key
        source_key = None
        for key, name in dbase_options.items():
            if name == selected_source:
                source_key = key
                break

        if source_key is None:
            print(
                f"Fourier: Could not map display name '{selected_source}' to numeric key"
            )
            return go.Figure()

        try:
            # Get data for the selected source
            datasets_norm, _ = db_manager.get_data_for_keyword(
                selected_keyword, selected_source_ids
            )

            # Get the source key from display name
            # Create translation mapping to find the correct source ID
            translation_mapping = create_translation_mapping(
                selected_source_ids, language
            )
            original_name = get_original_column_name(
                selected_source, translation_mapping
            )

            # Find the source key that matches the original name
            source_key = None
            for key, name in dbase_options.items():
                if name == original_name:
                    source_key = key
                    break

            if source_key is None or source_key not in datasets_norm:
                print(
                    f"Fourier: Could not find data for source '{selected_source}' (original: '{original_name}')"
                )
                return go.Figure()

            # Get the data series
            data = datasets_norm[source_key]
            if data.empty:
                print(f"Fourier: Data for source key {source_key} is empty")
                return go.Figure()

            # Extract values and remove NaN
            values = data.iloc[:, 0].dropna().values
            if len(values) < 10:  # Need minimum data points
                return go.Figure()

            # Additional safety check for None values
            if values is None or len(values) == 0:
                return go.Figure()

            # Add data size limits to prevent performance issues
            MAX_FFT_SIZE = 10000
            original_length = len(values)
            if len(values) > MAX_FFT_SIZE:
                # Downsample while preserving frequency content
                downsample_factor = max(1, len(values) // MAX_FFT_SIZE)
                values = values[::downsample_factor]
                print(
                    f"Fourier: Downsampled from {original_length} to {len(values)} points"
                )

            # Single FFT calculation (removed duplicate)
            fft_values = fft(values)
            freqs = fftfreq(len(values))

            # Get magnitude (only positive frequencies)
            n = len(values)
            magnitude = np.abs(fft_values[: n // 2])
            frequencies = freqs[: n // 2]

            # Convert frequencies to periods (cycles per unit time)
            # For monthly data, frequency represents cycles per month
            periods = 1 / frequencies[1:]  # Skip DC component (freq=0)
            magnitude = magnitude[1:]  # Skip DC component

            # Check for valid periods and magnitude
            if (
                periods is None
                or magnitude is None
                or len(periods) == 0
                or len(magnitude) == 0
            ):
                return go.Figure()

            # Simplified significance threshold using percentiles
            # Much faster than chi-squared distribution calculations
            scaled_threshold = np.percentile(magnitude, 95)  # Top 5% are significant

            # Create figure
            fig = go.Figure()

            # Determine significant components
            significant_mask = magnitude >= scaled_threshold

            # Efficient stem plotting with controlled batching
            # Separate significant and non-significant for better legend control
            sig_periods = periods[significant_mask]
            sig_magnitude = magnitude[significant_mask]
            non_sig_periods = periods[~significant_mask]
            non_sig_magnitude = magnitude[~significant_mask]

            # Add stems for significant components (red) - batch add for performance
            if len(sig_periods) > 0:
                # Use bar chart for stems (much more efficient than individual lines)
                fig.add_trace(
                    go.Bar(
                        x=sig_periods,
                        y=sig_magnitude,
                        name=get_text("significant_components", language),
                        marker_color="red",
                        marker_line_width=2,
                        marker_line_color="red",
                        opacity=0.8,
                        showlegend=True,
                        width=[0.5]
                        * len(sig_periods),  # Narrow bars for stem-like appearance
                    )
                )

            # Add stems for non-significant components (grey)
            if len(non_sig_periods) > 0:
                fig.add_trace(
                    go.Bar(
                        x=non_sig_periods,
                        y=non_sig_magnitude,
                        name=get_text("non_significant_components", language),
                        marker_color="grey",
                        marker_line_width=1,
                        marker_line_color="grey",
                        opacity=0.6,
                        showlegend=True,
                        width=[0.3]
                        * len(non_sig_periods),  # Even narrower for less prominent
                    )
                )

            # Add labels for significant components using text mode
            if np.any(significant_mask):
                fig.add_trace(
                    go.Scatter(
                        x=periods[significant_mask],
                        y=magnitude[significant_mask]
                        + max(magnitude) * 0.08,  # Position above markers
                        mode="text",
                        text=[f"{p:.1f}m" for p in periods[significant_mask]],
                        textfont=dict(color="red", size=10, weight="bold"),
                        showlegend=False,
                    )
                )

            # Add significance threshold line
            fig.add_trace(
                go.Scatter(
                    x=[periods.min(), periods.max()],
                    y=[scaled_threshold, scaled_threshold],
                    mode="lines",
                    name=get_text("significance_threshold", language),
                    line=dict(color="purple", width=2, dash="dot"),
                    showlegend=True,
                )
            )

            # Add vertical reference lines for Trimestral, Semestral, Anual
            v_lines = [3, 6, 12]
            v_line_names = [
                get_text("quarterly", language),
                get_text("semiannual", language),
                get_text("annual", language),
            ]
            for val, name in zip(v_lines, v_line_names):
                fig.add_vline(
                    x=val,
                    line_width=1,
                    line_dash="dash",
                    line_color="blue",
                )
                fig.add_annotation(
                    x=val,
                    y=max(magnitude) * 0.85,
                    text=name,
                    showarrow=False,
                    xshift=10,
                    font=dict(color="blue", size=9),
                )

            # Create title with tool name if provided
            if selected_source:
                base_title = get_text("fourier_title", language, source=selected_source)
            else:
                base_title = get_text("fourier_analysis", language)
            tool_display_name = (
                get_tool_name(selected_keyword, language) if selected_keyword else None
            )
            if tool_display_name:
                title_text = f"{base_title} - {tool_display_name}"
            else:
                title_text = base_title

            # Update layout
            fig.update_layout(
                title={
                    "text": title_text,
                    "y": 0.95,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                },
                xaxis_title=get_text("period_months", language),
                yaxis_title=get_text("magnitude", language),
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,  # Moved up 20 lines from -0.5
                    xanchor="center",
                    x=0.5,
                ),
                xaxis=dict(
                    type="log",
                    range=[np.log10(max(1, periods.min())), np.log10(periods.max())],
                    tickformat=".0f",
                ),
                yaxis=dict(autorange=True),
            )

            # Add source URL annotation as legend-style outside the graph
            source_text = (
                get_text("source", language) + " https://dashboard.solidum360.com/"
            )
            fig.add_annotation(
                xref="paper",
                yref="paper",
                x=1,
                y=1.1,  # Position relative to plot
                text=source_text,
                showarrow=False,
                font=dict(size=12),
                align="left",
            )

            return fig

        except Exception as e:
            return go.Figure()


def register_heatmap_click_callback(app):
    """Register heatmap click callback for regression analysis."""

    @app.callback(
        [
            Output("regression-graph", "figure"),
            Output("regression-equations", "children"),
        ],
        [
            Input("correlation-heatmap", "clickData"),
            Input("keyword-dropdown", "value"),
            Input("data-sources-store-v2", "data"),
            Input("language-store", "data"),
        ],
        prevent_initial_call=False,
    )
    def update_regression_from_heatmap(
        click_data, selected_keyword, selected_sources, language
    ):
        # Check if this callback was triggered by correlation-heatmap
        from dash import callback_context

        if not callback_context.triggered:
            # No trigger, skip
            return dash.no_update, dash.no_update

        # Get the trigger prop_id
        trigger_prop_id = callback_context.triggered[0]["prop_id"]

        # Only process if triggered by correlation-heatmap
        if "correlation-heatmap" not in trigger_prop_id:
            print(f"DEBUG: Callback not triggered by correlation-heatmap, skipping")
            return dash.no_update, dash.no_update

        print(f"DEBUG: update_regression_analysis called")
        print(f"DEBUG: click_data={click_data}")
        print(f"DEBUG: selected_keyword={selected_keyword}")
        print(f"DEBUG: selected_sources={selected_sources}")

        if selected_sources is None:
            selected_sources = []

        selected_source_ids = map_display_names_to_source_ids(selected_sources)
        print(f"DEBUG: selected_source_ids={selected_source_ids}")

        # Handle both cases: with click data (heatmap click) and without (auto-select)
        x_var = None
        y_var = None
        click_data_available = False

        # Check if correlation-heatmap click data is available
        if (
            click_data
            and isinstance(click_data, dict)
            and "points" in click_data
            and click_data["points"]
        ):
            try:
                point = click_data["points"][0]
                if isinstance(point, dict) and "x" in point and "y" in point:
                    x_var = point["x"]
                    y_var = point["y"]
                    click_data_available = True
                    print(
                        f"DEBUG: Using variables from heatmap click: x={x_var}, y={y_var}"
                    )
            except (KeyError, IndexError, TypeError) as e:
                print(f"DEBUG: Error extracting variables from click_data: {e}")
                # Fall through to auto-selection below
        else:
            print(
                f"DEBUG: No heatmap click data available (correlation-heatmap may not exist or no click occurred)"
            )

        # If no valid click data, auto-select first two available sources
        if not click_data_available:
            print(f"DEBUG: No click data available, will auto-select variables")
            # Need to get the data first to see available columns
            try:
                db_manager = get_database_manager()
                datasets_norm, sl_sc = db_manager.get_data_for_keyword(
                    selected_keyword, selected_source_ids
                )
                combined_dataset = create_combined_dataset2(
                    datasets_norm=datasets_norm,
                    selected_sources=sl_sc,
                    dbase_options=dbase_options,
                )

                combined_dataset = combined_dataset.reset_index()
                date_column = combined_dataset.columns[0]
                combined_dataset[date_column] = pd.to_datetime(
                    combined_dataset[date_column]
                )
                combined_dataset = combined_dataset.rename(
                    columns={date_column: "Fecha"}
                )

                # Filter out rows where ALL selected sources are NaN (preserve partial data)
                actual_columns = [
                    col for col in combined_dataset.columns if col != "Fecha"
                ]
                if actual_columns:
                    combined_dataset = combined_dataset.dropna(
                        subset=actual_columns, how="all"
                    )

                # Auto-select first two available columns
                available_columns = [
                    col for col in combined_dataset.columns if col != "Fecha"
                ]
                if len(available_columns) >= 2:
                    x_var = available_columns[0]
                    y_var = available_columns[1]
                    print(f"DEBUG: Auto-selected variables: x={x_var}, y={y_var}")
                else:
                    print(f"DEBUG: Insufficient columns for regression analysis")
                    fig = go.Figure()
                    fig.update_layout(
                        title=get_text("need_two_sources", language),
                        xaxis_title="",
                        yaxis_title="",
                        height=400,
                    )
                    return fig, ""
            except Exception as e:
                print(f"DEBUG: Error getting data for auto-selection: {e}")
                fig = go.Figure()
                fig.update_layout(
                    title="Error: Could not auto-select variables",
                    xaxis_title="",
                    yaxis_title="",
                    height=400,
                )
                return fig, ""

        # Basic validation
        if not selected_keyword or len(selected_sources) < 2:
            print(f"DEBUG: Returning empty figure - missing keyword or sources")
            fig = go.Figure()
            fig.update_layout(
                title=get_text("select_heatmap_points", language),
                xaxis_title="",
                yaxis_title="",
                height=400,
            )
            return fig, ""

        if not x_var or not y_var:
            print(f"DEBUG: Missing variables for regression")
            fig = go.Figure()
            fig.update_layout(
                title="Error: Could not determine variables for regression",
                xaxis_title="",
                yaxis_title="",
                height=400,
            )
            return fig, ""

        # Check if variables are the same (diagonal click on heatmap)
        if x_var == y_var:
            print(f"DEBUG: Cannot regress {x_var} against itself")
            error_msg = (
                f"No se puede hacer regresión de {x_var} contra sí mismo."
                if language == "es"
                else f"Cannot regress {x_var} against itself."
            )
            fig = go.Figure()
            fig.update_layout(
                title=error_msg,
                xaxis_title="",
                yaxis_title="",
                height=400,
            )
            return fig, error_msg

        # Get the data for regression analysis
        try:
            db_manager = get_database_manager()
            datasets_norm, sl_sc = db_manager.get_data_for_keyword(
                selected_keyword, selected_source_ids
            )
            combined_dataset = create_combined_dataset2(
                datasets_norm=datasets_norm,
                selected_sources=sl_sc,
                dbase_options=dbase_options,
            )

            combined_dataset = combined_dataset.reset_index()
            date_column = combined_dataset.columns[0]
            combined_dataset[date_column] = pd.to_datetime(
                combined_dataset[date_column]
            )
            combined_dataset = combined_dataset.rename(columns={date_column: "Fecha"})

            # Filter out rows where ALL selected sources are NaN (preserve partial data)
            # Use the actual column names from the combined dataset
            actual_columns = [col for col in combined_dataset.columns if col != "Fecha"]
            combined_dataset = combined_dataset.dropna(subset=actual_columns, how="all")

            # Get the columns that correspond to the selected variables
            translation_mapping = create_translation_mapping(
                selected_source_ids, language
            )

            # Map display names back to original column names
            x_original = get_original_column_name(x_var, translation_mapping)
            y_original = get_original_column_name(y_var, translation_mapping)

            # If mapping doesn't work, try direct match
            if x_original not in combined_dataset.columns:
                x_original = x_var
            if y_original not in combined_dataset.columns:
                y_original = y_var

            print(
                f"DEBUG: x_var={x_var} (original: {x_original}), y_var={y_var} (original: {y_original})"
            )
            print(f"DEBUG: Available columns: {list(combined_dataset.columns)}")

            # Validate that columns exist
            if (
                x_original not in combined_dataset.columns
                or y_original not in combined_dataset.columns
            ):
                error_msg = (
                    f"Variables not found: {x_original}, {y_original}"
                    if language == "es"
                    else f"Variables not found: {x_original}, {y_original}"
                )
                fig = go.Figure()
                fig.update_layout(
                    title=error_msg,
                    xaxis_title="",
                    yaxis_title="",
                    height=400,
                )
                return fig, error_msg

            # Filter out rows where the selected variables are NaN
            regression_data = combined_dataset[
                ["Fecha", x_original, y_original]
            ].dropna()

            if len(regression_data) < 10:
                error_msg = (
                    f"Insufficient data for regression analysis"
                    if language == "es"
                    else "Insufficient data for regression analysis"
                )
                fig = go.Figure()
                fig.update_layout(
                    title=error_msg,
                    xaxis_title="",
                    yaxis_title="",
                    height=400,
                )
                return fig, error_msg

            # Fit polynomial regression models of different degrees
            x = regression_data[x_original].values
            y = regression_data[y_original].values

            degree_names = (
                ["Linear", "Quadratic", "Cubic"]
                if language == "en"
                else ["Lineal", "Cuadrático", "Cúbico"]
            )
            poly_colors = ["red", "blue", "green"]
            annotations = []

            fig = go.Figure()

            # Add scatter plot of actual data points
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="markers",
                    name=f"Data Points ({len(regression_data)})",
                    marker=dict(color="lightblue", size=5, opacity=0.6),
                    showlegend=True,
                )
            )

            # Fit polynomial regression of different degrees
            for degree in range(1, 4):
                try:
                    # Create polynomial features
                    poly_features = PolynomialFeatures(degree=degree)
                    X_poly = poly_features.fit_transform(x.reshape(-1, 1))

                    # Fit the model
                    model = LinearRegression()
                    model.fit(X_poly, y)

                    # Make predictions for plotting
                    x_plot = np.linspace(x.min(), x.max(), 100)
                    X_plot_poly = poly_features.transform(x_plot.reshape(-1, 1))
                    y_pred = model.predict(X_plot_poly)

                    # Calculate R²
                    y_pred_all = model.predict(X_poly)
                    r_squared = r2_score(y, y_pred_all)

                    # Create formula string
                    coef = model.coef_
                    intercept = model.intercept_
                    formula = f"y = {intercept:.3f}"
                    for i, c in enumerate(coef[1:], 1):
                        if c >= 0:
                            formula += f" + {c:.3f}x^{i}"
                        else:
                            formula += f" - {abs(c):.3f}x^{i}"

                    # Add polynomial fit line
                    fig.add_trace(
                        go.Scatter(
                            x=x_plot,
                            y=y_pred,
                            mode="lines",
                            name=f"{degree_names[degree - 1]} (R² = {r_squared:.3f})",
                            line=dict(color=poly_colors[degree - 1], width=2),
                        )
                    )

                    # Add annotation for this degree
                    annotations.append(
                        f"<b>{degree_names[degree - 1]}:</b><br>"
                        f"{formula}<br>"
                        f"R² = {r_squared:.3f}"
                    )
                except Exception as poly_e:
                    print(f"Error fitting degree {degree} polynomial: {poly_e}")
                    # Add error annotation for this degree
                    annotations.append(
                        f"<b>{degree_names[degree - 1]}:</b><br>"
                        f"Error fitting polynomial<br>"
                        f"R² = N/A"
                    )

            # Create title with tool name if provided
            base_title = get_text(
                "regression_title", language, y_var=y_var, x_var=x_var
            )
            tool_display_name = (
                get_tool_name(selected_keyword, language) if selected_keyword else None
            )
            if tool_display_name:
                title_text = f"{base_title} - {tool_display_name}"
            else:
                title_text = base_title

            # Update layout with increased height for legend and equations
            fig.update_layout(
                title={
                    "text": title_text,
                    "y": 0.95,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                },
                xaxis_title=x_var,
                yaxis_title=y_var,
                height=600,  # Increased height to accommodate legend and equations
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,  # Moved 2 lines below the graph
                    xanchor="center",
                    x=0.5,
                ),
                xaxis=dict(
                    title=x_var,
                ),
                yaxis=dict(
                    title=y_var,
                ),
            )

            # Create equations text for the side panel
            equations_text = "<br>".join(annotations)

            print(f"DEBUG: Regression analysis completed successfully")
            return fig, equations_text

        except Exception as e:
            print(f"Error in regression analysis: {e}")
            import traceback

            traceback.print_exc()

            error_msg = (
                f"Error en análisis de regresión: {str(e)}"
                if language == "es"
                else f"Error in regression analysis: {str(e)}"
            )
            fig = go.Figure()
            fig.update_layout(
                title=error_msg,
                xaxis_title="",
                yaxis_title="",
                height=400,
            )
            return fig, error_msg
