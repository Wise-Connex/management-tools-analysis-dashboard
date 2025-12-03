"""
Utility functions for the dashboard application.

This module contains helper functions extracted from app.py to improve code organization
and maintainability. These functions are primarily focused on data processing, caching,
visualization, and analysis utilities.
"""

import re
import asyncio
from datetime import datetime
from typing import Dict, List, Any

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from dash import html
from statsmodels.tsa.seasonal import seasonal_decompose

# Import project-specific modules
from tools import tool_file_dic

# Import mapping and translation functions
from fix_source_mapping import (
    map_display_names_to_source_ids,
    DBASE_OPTIONS as dbase_options,
    DISPLAY_TO_DB_NAME,
)

# Import translation functions
from translations import get_text


# Global cache for processed datasets
_processed_data_cache = {}
_cache_max_size = 10

# Color map for consistent source coloring (matches actual DISPLAY_NAMES)
color_map = {
    # Standard sources (from DISPLAY_NAMES in fix_source_mapping.py)
    "Google Trends": "#1f77b4",  # Blue
    "Google Books": "#ff7f0e",  # Orange
    "Bain Usability": "#2ca02c",  # Green
    "Bain Satisfaction": "#d62728",  # Red
    "Crossref": "#9467bd",  # Purple
    # Spanish translations (for bilingual support)
    "Bain Usabilidad": "#2ca02c",  # Green (same as English)
    "Bain Satisfacción": "#d62728",  # Red (same as English)
}


def parse_text_with_links(text):
    """Parse text and return formatted components with basic markdown support"""
    if not text:
        return [html.Div("No hay notas disponibles", style={"fontSize": "12px"})]

    # Remove source link information that starts with "Fuente:" or similar patterns
    # Look for patterns like "Fuente: http" or "Source: http" and remove everything from there
    import re

    # Pattern to match "Fuente:" or "Source:" followed by URL-like content
    link_pattern = r"\s*(?:Fuente|Source)\s*:\s*https?://[^\s]+.*$"

    # Remove the link information from the end of the text
    cleaned_text = re.sub(link_pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)

    # Also remove any remaining "Fuente:" or "Source:" at the end if not followed by URL
    cleaned_text = re.sub(
        r"\s*(?:Fuente|Source)\s*:\s*$", "", cleaned_text, flags=re.IGNORECASE
    )

    # Clean up any trailing whitespace or punctuation
    cleaned_text = cleaned_text.rstrip(".,;:- \t\n")

    # Split text by newlines and create separate components for each line
    lines = cleaned_text.split("\n")

    # Create a list of components for each line
    components = []

    for line in lines:
        if not line.strip():  # Skip empty lines
            continue

        # Process each line for markdown formatting
        # Use regex to find and replace bold text (**text**)
        parts = []
        last_end = 0

        # Find all bold patterns in the line
        for match in re.finditer(r"\*\*(.*?)\*\*", line):
            # Add text before the bold part
            if match.start() > last_end:
                parts.append(
                    html.Span(
                        line[last_end : match.start()], style={"fontSize": "12px"}
                    )
                )

            # Add the bold part
            parts.append(html.Strong(match.group(1), style={"fontSize": "12px"}))
            last_end = match.end()

        # Add any remaining text after the last bold part
        if last_end < len(line):
            parts.append(html.Span(line[last_end:], style={"fontSize": "12px"}))

        # If no bold text was found, just use the whole line
        if not parts:
            parts = [html.Span(line, style={"fontSize": "12px"})]

        # Create a div for this line with all its parts
        components.append(
            html.Div(parts, style={"fontSize": "12px", "marginBottom": "5px"})
        )

    # If no lines were added, return a default message
    if not components:
        components = [html.Div("No hay notas disponibles", style={"fontSize": "12px"})]

    return components


def get_cache_key(keyword, sources):
    """Generate cache key for processed data"""
    return f"{keyword}_{'_'.join(map(str, sorted(sources)))}"


def get_cached_processed_data(keyword, selected_sources):
    """Get cached processed data or None if not cached"""
    cache_key = get_cache_key(keyword, selected_sources)
    return _processed_data_cache.get(cache_key)


def cache_processed_data(keyword, selected_sources, data):
    """Cache processed data with LRU eviction"""
    global _processed_data_cache

    cache_key = get_cache_key(keyword, selected_sources)
    _processed_data_cache[cache_key] = data

    # Evict oldest if cache is full
    if len(_processed_data_cache) > _cache_max_size:
        oldest_key = next(iter(_processed_data_cache))
        del _processed_data_cache[oldest_key]


def get_all_keywords():
    """Extract all keywords from tool_file_dic"""
    all_keywords = []
    for tool_list in tool_file_dic.values():
        for keyword in tool_list[1]:
            if keyword not in all_keywords:
                all_keywords.append(keyword)
    return all_keywords


def _generate_pca_insights(pattern: Dict[str, Any]) -> List[str]:
    """Generate specific insights from PCA pattern analysis."""
    insights = []

    # Pattern type insights
    pattern_type = pattern.get("pattern_type", "")
    if pattern_type == "contrast_pattern":
        pos_sources = [
            contrib["source"]
            for contrib in pattern.get("source_contributions", [])
            if contrib.get("direction") == "positive"
            and contrib.get("abs_loading", 0) > 0.3
        ]
        neg_sources = [
            contrib["source"]
            for contrib in pattern.get("source_contributions", [])
            if contrib.get("direction") == "negative"
            and contrib.get("abs_loading", 0) > 0.3
        ]

        if pos_sources and neg_sources:
            insights.append(
                f"Contraste entre {', '.join(pos_sources)} y {', '.join(neg_sources)}"
            )

    elif pattern_type == "consensus_pattern":
        strong_sources = [
            contrib["source"]
            for contrib in pattern.get("source_contributions", [])
            if contrib.get("abs_loading", 0) > 0.5
        ]
        if strong_sources:
            insights.append(f"Consenso fuerte en {', '.join(strong_sources)}")

    elif pattern_type == "temporal_divergence":
        insights.append("Divergencia temporal significativa entre fuentes")

    # Loading-based insights
    high_loadings = [
        contrib
        for contrib in pattern.get("source_contributions", [])
        if contrib.get("abs_loading", 0) > 0.6
    ]
    if high_loadings:
        sources = [contrib["source"] for contrib in high_loadings]
        insights.append(f"Influencia dominante de {', '.join(sources)}")

    # Business model insights
    business_models = pattern.get("business_models", [])
    if business_models:
        insights.append(f"Patr�n asociado a modelos: {', '.join(business_models)}")

    return insights


def get_cache_stats(db_manager):
    """Get database and cache statistics for performance monitoring"""
    try:
        table_stats = db_manager.get_table_stats()
        total_records = sum(
            stats.get("row_count", 0)
            for stats in table_stats.values()
            if "error" not in stats
        )
        total_keywords = sum(
            stats.get("keyword_count", 0)
            for stats in table_stats.values()
            if "error" not in stats
        )

        return {
            "processed_data_cache": len(_processed_data_cache),
            "cache_max_size": _cache_max_size,
            "database_records": total_records,
            "database_keywords": total_keywords,
            "database_size_mb": round(db_manager.get_database_size() / 1024 / 1024, 2),
            "cache_hit_rate": 0,  # Could be tracked with more complex caching
        }
    except Exception as e:
        print(f"Error getting cache stats: {e}")
        return {
            "processed_data_cache": 0,
            "cache_max_size": _cache_max_size,
            "database_records": 0,
            "database_keywords": 0,
            "database_size_mb": 0,
            "cache_hit_rate": 0,
        }


def create_combined_dataset(datasets_norm, selected_sources, dbase_options):
    """Create combined dataset with common date range"""
    combined_data = pd.DataFrame()

    for source in selected_sources:
        if source in datasets_norm:
            df = datasets_norm[source]
            column_name = dbase_options[source]
            combined_data[column_name] = df.iloc[:, 0]  # Use first column

    return combined_data


def create_combined_dataset2(datasets_norm, selected_sources, dbase_options):
    """Create combined dataset with all dates from all sources"""
    combined_dataset2 = pd.DataFrame()

    # Get all unique dates from all datasets
    all_dates = set()
    for source in selected_sources:
        if source in datasets_norm and not datasets_norm[source].empty:
            all_dates.update(datasets_norm[source].index)

    # Sort dates
    all_dates = sorted(list(all_dates))

    # Create DataFrame with all dates
    combined_dataset2 = pd.DataFrame(index=all_dates)

    # Add data from each source - use source name directly as column name
    for source in selected_sources:
        if source in datasets_norm and not datasets_norm[source].empty:
            source_name = dbase_options.get(source, source)
            source_data = datasets_norm[source].reindex(all_dates)
            # Use just the source name as the column name (not source_name_col)
            combined_dataset2[source_name] = source_data.iloc[:, 0]

    return combined_dataset2


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


# Note: The following visualization functions are complex and depend on app-specific variables.
# They are included here as placeholders that would need to be adapted with proper imports
# and dependencies when fully migrated.


def create_temporal_2d_figure(
    data, sources, language="es", start_date=None, end_date=None, tool_name=None
):
    """
    Create a 2D temporal visualization figure.

    Adapted from app_old.py working implementation.
    """
    import pandas as pd
    from fix_source_mapping import map_display_names_to_source_ids
    from translations import get_text

    # Basic color map for sources - this should match database column names from DBASE_OPTIONS
    color_map = {
        "Google Trends": "#1f77b4",  # Google Trends - blue
        "Google Books Ngrams": "#ff7f0e",  # Google Books - orange
        "Bain - Usabilidad": "#2ca02c",  # Bain Usability - green
        "Crossref.org": "#d62728",  # Crossref - red
        "Bain - Satisfacción": "#9467bd",  # Bain Satisfaction - purple
    }

    print(f"DEBUG: create_temporal_2d_figure called")
    print(f"DEBUG: data shape: {data.shape}")
    print(f"DEBUG: sources: {sources}")
    print(f"DEBUG: start_date: {start_date}, end_date: {end_date}")
    print(f"DEBUG: tool_name: {tool_name}")
    print(f"DEBUG: Available columns in data: {list(data.columns)}")

    # Filter data by date range if provided
    filtered_data = data.copy()
    if start_date and end_date:
        # Find date column (might be named 'Fecha' or be first column)
        date_col = None
        for col in filtered_data.columns:
            if "fecha" in col.lower() or "date" in col.lower():
                date_col = col
                break
        if date_col is None:
            date_col = filtered_data.columns[0]  # Assume first column is date

        filtered_data = filtered_data[
            (pd.to_datetime(filtered_data[date_col]) >= pd.to_datetime(start_date))
            & (pd.to_datetime(filtered_data[date_col]) <= pd.to_datetime(end_date))
        ]
        print(f"DEBUG: Filtered data shape: {filtered_data.shape}")

    fig = go.Figure()
    trace_count = 0

    # Get source IDs from display names and create translation mapping
    try:
        selected_source_ids = map_display_names_to_source_ids(sources)
        translation_mapping = create_translation_mapping(selected_source_ids, language)
        print(f"DEBUG: Translation mapping: {translation_mapping}")
    except Exception as e:
        print(f"DEBUG: Error creating mapping: {e}")
        # Fallback mapping
        translation_mapping = {source: source for source in sources}
        selected_source_ids = list(range(1, len(sources) + 1))

    # Process each source
    for i, source in enumerate(sources):
        print(f"DEBUG: Processing source: {source}")

        # Use safe column access
        source_data = safe_dataframe_column_access(
            filtered_data, source, translation_mapping
        )

        if source_data is not None and not source_data.empty:
            valid_mask = ~source_data.isna()
            print(
                f"DEBUG: Source {source} has {valid_mask.sum()} valid points out of {len(source_data)}"
            )

            if valid_mask.any():
                # Use lines only for better performance, add markers only for sparse data
                mode = "lines+markers" if valid_mask.sum() < 50 else "lines"
                print(f"DEBUG: Using mode: {mode}")

                # Find date column
                date_col = None
                for col in filtered_data.columns:
                    if "fecha" in col.lower() or "date" in col.lower():
                        date_col = col
                        break
                if date_col is None:
                    date_col = filtered_data.columns[0]

                # Ensure we have valid data to plot
                valid_dates = pd.to_datetime(filtered_data[date_col])[valid_mask]
                valid_values = source_data[valid_mask]

                if len(valid_dates) > 0 and len(valid_values) > 0:
                    # Get color - use original database name for color mapping
                    original_source_name = get_original_column_name(
                        source, translation_mapping
                    )
                    source_color = color_map.get(original_source_name, "#000000")
                    print(
                        f"DEBUG: Source {source} -> Original: {original_source_name} -> Color: {source_color}"
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=valid_dates,
                            y=valid_values,
                            mode=mode,
                            name=source,  # Keep the translated name for display
                            line=dict(color=source_color, width=2),
                            marker=dict(size=4) if mode == "lines+markers" else None,
                            connectgaps=False,
                            hovertemplate=f"{source}: %{{y:.2f}}<br>%{{x|%Y-%m-%d}}<extra></extra>",
                        )
                    )
                    trace_count += 1
                    print(f"DEBUG: Added trace for {source}")
                else:
                    print(f"DEBUG: No valid data points for {source}")
        else:
            print(
                f"DEBUG: Source {source} not found in filtered_data columns or is empty."
            )

    print(f"DEBUG: Total traces added: {trace_count}")
    print(f"DEBUG: Figure has {len(fig.data)} traces after creation")

    # Simplified tick calculation for better performance
    # Find date column and calculate date range
    date_col = None
    for col in filtered_data.columns:
        if "fecha" in col.lower() or "date" in col.lower():
            date_col = col
            break
    if date_col is None:
        date_col = filtered_data.columns[0]

    try:
        date_range_days = (
            pd.to_datetime(filtered_data[date_col]).max()
            - pd.to_datetime(filtered_data[date_col]).min()
        ).days
        print(f"DEBUG: Date range in days: {date_range_days}")

        if date_range_days <= 365:
            tickformat = "%Y-%m"
        elif date_range_days <= 365 * 3:
            tickformat = "%Y-%m"
        else:
            tickformat = "%Y"
    except:
        tickformat = "%Y-%m"

    # Create title with tool name if provided
    base_title = get_text("temporal_analysis_2d", language)
    if tool_name:
        title_text = f"{base_title} - {tool_name}"
    else:
        title_text = base_title

    # Optimized layout with performance settings
    fig.update_layout(
        title=title_text,
        xaxis_title=get_text("date", language),
        yaxis_title=get_text("value", language),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
        xaxis=dict(
            tickformat=tickformat,
            tickangle=45,
            autorange=True,  # Let Plotly optimize tick spacing
        ),
        # Performance optimizations
        hovermode="x unified",
        showlegend=True,
    )

    # Add source URL annotation as legend-style outside the graph
    source_text = get_text("source", language) + " https://dashboard.solidum360.com/"
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

    # Reduce data points for very large datasets
    if len(filtered_data) > 1000:
        fig.update_traces(
            hoverinfo="skip"  # Reduce hover computation for large datasets
        )

    print(f"DEBUG: Final figure has {len(fig.data)} traces")
    return fig


def create_mean_analysis_figure(data, sources, language="es", tool_name=None):
    """
    Create 100% stacked bar chart showing relative contribution of each source.

    Adapted from app_old.py working implementation.
    """
    import pandas as pd
    from fix_source_mapping import map_display_names_to_source_ids
    from translations import get_text

    # Basic color map for sources - this should match database column names from DBASE_OPTIONS
    color_map = {
        "Google Trends": "#1f77b4",  # Google Trends - blue
        "Google Books Ngrams": "#ff7f0e",  # Google Books - orange
        "Bain - Usabilidad": "#2ca02c",  # Bain Usability - green
        "Crossref.org": "#d62728",  # Crossref - red
        "Bain - Satisfacción": "#9467bd",  # Bain Satisfaction - purple
    }

    print(f"DEBUG: create_mean_analysis_figure called with data shape: {data.shape}")
    print(f"DEBUG: sources: {sources}")
    print(f"DEBUG: Available columns in data: {list(data.columns)}")

    # Find date column
    date_col = None
    for col in data.columns:
        if "fecha" in col.lower() or "date" in col.lower():
            date_col = col
            break
    if date_col is None:
        date_col = data.columns[0]

    # Calculate total years in dataset for "Todo" range
    try:
        total_years = (
            pd.to_datetime(data[date_col]).max() - pd.to_datetime(data[date_col]).min()
        ).days / 365.25
    except:
        total_years = 10  # Fallback

    # Create proper translation mapping
    try:
        selected_source_ids = map_display_names_to_source_ids(sources)
        translation_mapping = create_translation_mapping(selected_source_ids, language)
        print(f"DEBUG: Translation mapping: {translation_mapping}")
    except Exception as e:
        print(f"DEBUG: Error creating mapping: {e}")
        # Fallback mapping
        translation_mapping = {source: source for source in sources}
        selected_source_ids = list(range(1, len(sources) + 1))

    # Define time ranges with actual year counts
    time_ranges = [
        ("Todo", None, total_years),  # Full range - actual total years
        ("20 años", 20, 20),
        ("15 años", 15, 15),
        ("10 años", 10, 10),
        ("5 años", 5, 5),
    ]

    # Calculate means for each source and time range
    results = []
    for source in sources:
        # Use safe column access
        source_data = safe_dataframe_column_access(data, source, translation_mapping)

        if source_data is not None and not source_data.empty:
            for range_name, years_back, actual_years in time_ranges:
                if years_back is None:
                    # Full range
                    mean_val = source_data.mean()
                else:
                    # Calculate date range
                    try:
                        end_date = pd.to_datetime(data[date_col]).max()
                        start_date = end_date - pd.DateOffset(years=years_back)
                        mask = (pd.to_datetime(data[date_col]) >= start_date) & (
                            pd.to_datetime(data[date_col]) <= end_date
                        )
                        filtered_data = source_data[mask]
                        mean_val = (
                            filtered_data.mean() if not filtered_data.empty else 0
                        )
                    except:
                        mean_val = source_data.mean()  # Fallback

                results.append(
                    {
                        "Source": source,
                        "Time_Range": range_name,
                        "Mean": mean_val,
                        "Years": actual_years,
                    }
                )

    # Create DataFrame for plotting
    if not results:
        # Return empty figure if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for mean analysis",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16),
        )
        return fig

    results_df = pd.DataFrame(results)

    # Find the maximum mean value across all sources and time ranges for 100% reference
    max_mean_value = results_df["Mean"].max()

    # Create single figure with 100% stacked bars
    fig = go.Figure()

    # Calculate width scale based on years
    max_years = max(r[2] for r in time_ranges)
    width_scale = 1.2 / max_years  # Increased max width to 1.2 for wider bars

    # Add stacked bars for each time range (no legend entries)
    for range_name, _, actual_years in time_ranges:
        range_data = results_df[results_df["Time_Range"] == range_name]
        bar_width = actual_years * width_scale

        # Calculate percentages relative to max value
        for _, row in range_data.iterrows():
            percentage = (
                (row["Mean"] / max_mean_value) * 100 if max_mean_value > 0 else 0
            )

            # Get color using original database name for color mapping
            original_source_name = get_original_column_name(
                row["Source"], translation_mapping
            )
            bar_color = color_map.get(original_source_name, "#000000")
            print(
                f"DEBUG: Bar color for {row['Source']} -> Original: {original_source_name} -> Color: {bar_color}"
            )

            fig.add_trace(
                go.Bar(
                    x=[range_name],
                    y=[percentage],
                    name=row["Source"],  # Same name as lines for unified legend
                    width=bar_width,  # Proportional width based on years
                    marker_color=bar_color,
                    showlegend=False,  # Don't show bars in legend
                    opacity=0.7,  # Make bars slightly transparent for line visibility
                )
            )

    # Add line traces for actual values (secondary y-axis) - these will show in legend
    for source in sources:
        source_data = results_df[results_df["Source"] == source]
        if not source_data.empty:
            x_values = source_data["Time_Range"]
            y_values = source_data["Mean"]

            # Get color using original database name for color mapping
            original_source_name = get_original_column_name(source, translation_mapping)
            line_color = color_map.get(original_source_name, "#000000")
            print(
                f"DEBUG: Line color for {source} -> Original: {original_source_name} -> Color: {line_color}"
            )

            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="lines+markers",
                    name=source,  # Clean source name for legend
                    line=dict(color=line_color, width=3),
                    marker=dict(size=8),
                    yaxis="y2",  # Use secondary y-axis
                    showlegend=True,  # Only lines show in legend
                )
            )

    # Create title with tool name if provided
    base_title = get_text("relative_absolute", language, max_value=max_mean_value)
    if tool_name:
        title_text = f"{base_title} - {tool_name}"
    else:
        title_text = base_title

    # Update layout for combo chart
    fig.update_layout(
        title=title_text,
        xaxis_title=get_text("temporal_range", language),
        yaxis_title=get_text("contribution_relative", language),
        yaxis2=dict(
            title=get_text("absolute_value", language),
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        height=600,  # Fixed height to prevent dynamic resizing
        barmode="stack",  # Stack bars to 100%
        legend_title=get_text("data_sources", language),
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=-0.6,  # Lower position (3 lines below)
            xanchor="center",
            x=0.5,
        ),
        showlegend=True,
        margin=dict(l=50, r=50, t=80, b=150),  # Consistent margins
    )

    # Add source URL annotation as legend-style outside the graph
    source_text = get_text("source", language) + " https://dashboard.solidum360.com/"
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

    # Set primary y-axis to 0-100%
    fig.update_yaxes(range=[0, 100])

    print(f"DEBUG: Created mean analysis figure with {len(fig.data)} traces")
    return fig


def perform_comprehensive_pca_analysis(data, sources, language="es"):
    """
    Perform comprehensive PCA analysis with detailed metrics.

    This uses the same logic as the original app_old.py but in modular format.
    """
    try:
        # Create proper translation mapping (DATAFRAME_INDEXING_FIX)
        selected_source_ids = map_display_names_to_source_ids(sources)
        translation_mapping = create_translation_mapping(selected_source_ids, language)

        # Prepare data for PCA - use original column names
        original_columns = []
        print(f"DEBUG: Comprehensive PCA Analysis - Processing {len(sources)} sources")
        print(f"DEBUG: Input sources: {sources}")
        print(f"DEBUG: Translation mapping: {translation_mapping}")

        for source in sources:
            original_name = get_original_column_name(source, translation_mapping)
            print(f"DEBUG: Processing source '{source}' -> '{original_name}'")
            if original_name in data.columns:
                original_columns.append(original_name)
                print(f"DEBUG: ✓ Found column '{original_name}' in dataset")
            else:
                print(f"DEBUG: ✗ Column '{original_name}' not found in dataset")

        if len(original_columns) < 2:
            print(
                f"DEBUG: Insufficient columns for comprehensive PCA: {len(original_columns)} columns available"
            )
            return {
                "error": f"Insufficient columns for PCA analysis: {len(original_columns)} columns"
            }

        print(f"DEBUG: Valid columns for comprehensive PCA: {original_columns}")
        pca_data = data[original_columns].dropna()
        if len(pca_data) < 2:
            print(f"DEBUG: Insufficient data for PCA analysis: {len(pca_data)} rows")
            return {"error": "Insufficient data for PCA analysis"}

        # Create mapping from original column names back to display names for labeling
        original_to_display = {v: k for k, v in translation_mapping.items()}

        # Standardize data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(pca_data)

        # Perform PCA
        pca = PCA()
        pca_result = pca.fit_transform(scaled_data)

        # Calculate explained variance
        explained_var = pca.explained_variance_ratio_ * 100
        cumulative_var = explained_var.cumsum()

        # Determine number of components to analyze (Kaiser criterion: eigenvalues > 1)
        eigenvalues = pca.explained_variance_
        components_to_analyze = sum(eigenvalues > 1)

        # Basic PCA data structure compatible with visualization
        return {
            "success": True,
            "pca": pca,
            "pca_result": pca_result,
            "explained_variance_ratio": pca.explained_variance_ratio_,
            "components": pca.components_,
            "original_columns": original_columns,
            "original_to_display": original_to_display,
            "translation_mapping": translation_mapping,
            "components_analyzed": components_to_analyze,
            "total_variance_explained": cumulative_var[
                min(components_to_analyze - 1, len(cumulative_var) - 1)
            ]
            if components_to_analyze > 0
            else 0,
            "data_points_used": len(pca_data),
        }
    except Exception as e:
        return {"error": f"PCA analysis failed: {str(e)}"}


def create_pca_figure(data, sources, language="es", tool_name=None):
    """
    Create a PCA visualization figure.

    This matches the original app_old.py implementation with two subplots:
    - Left: Component loadings as arrows
    - Right: Explained variance with cumulative and inverse lines
    """
    # Create proper translation mapping (DATAFRAME_INDEXING_FIX)
    selected_source_ids = map_display_names_to_source_ids(sources)
    translation_mapping = create_translation_mapping(selected_source_ids, language)

    # Prepare data for PCA - map display names to actual DataFrame column names
    original_columns = []
    print(f"DEBUG: PCA Analysis - Processing {len(sources)} sources")
    print(f"DEBUG: Input sources: {sources}")
    print(f"DEBUG: Translation mapping: {translation_mapping}")
    print(f"DEBUG: Available dataset columns: {list(data.columns)}")

    for source in sources:
        # Get the database column name for this display name
        db_column_name = get_original_column_name(source, translation_mapping)
        print(
            f"DEBUG: Processing source '{source}' -> database name '{db_column_name}'"
        )

        # Check if the database column name exists in the DataFrame
        if db_column_name in data.columns:
            original_columns.append(db_column_name)
            print(f"DEBUG: ✓ Found column '{db_column_name}' in dataset")
        else:
            # Fallback: try the original source name directly
            if source in data.columns:
                original_columns.append(source)
                print(f"DEBUG: ✓ Found column '{source}' in dataset (direct match)")
            else:
                print(
                    f"DEBUG: ✗ Column '{db_column_name}' or '{source}' not found in dataset"
                )

    if len(original_columns) < 2:
        print(
            f"DEBUG: Insufficient columns for PCA analysis: {len(original_columns)} columns available"
        )
        print(f"DEBUG: Available dataset columns: {list(data.columns)}")
        print(f"DEBUG: Found original columns: {original_columns}")
        return go.Figure()

    print(f"DEBUG: Valid columns for PCA: {original_columns}")
    pca_data = data[original_columns].dropna()
    if len(pca_data) < 2:
        print(
            f"DEBUG: Insufficient data points for PCA: {len(pca_data)} rows available"
        )
        return go.Figure()

    print(
        f"DEBUG: PCA data prepared - {len(pca_data)} rows, {len(original_columns)} columns"
    )

    # Create mapping from original column names back to display names for labeling
    original_to_display = {v: k for k, v in translation_mapping.items()}

    # Standardize data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(pca_data)

    # Perform PCA
    pca = PCA()
    pca_result = pca.fit_transform(scaled_data)

    # PCA BOUNDS CHECK: Ensure we have at least 2 components for 2D visualization
    if len(pca.components_) < 2:
        print(
            f"DEBUG: Insufficient PCA components for 2D visualization: {len(pca.components_)} components available"
        )
        print(f"DEBUG: Explained variance: {pca.explained_variance_ratio_}")
        print(f"DEBUG: Returning empty figure to prevent bounds error")
        return go.Figure()

    # Create subplot
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            get_text("loadings", language),
            get_text("explained_variance", language),
        ),
        specs=[[{"type": "scatter"}, {"type": "bar"}]],
    )

    # Loadings plot with arrows from origin
    for i, source in enumerate(sources):
        # Use display name for labels
        display_name = source

        # Get color mapping - use display name directly for consistent colors
        # This matches the approach used in temporal analysis functions
        arrow_color = color_map.get(display_name, "#000000")

        # DEBUG: Log color mapping for verification
        print(f"DEBUG PCA: Source '{display_name}' -> Color: '{arrow_color}'")

        # Add arrow line from origin to point
        fig.add_trace(
            go.Scatter(
                x=[0, pca.components_[0, i]],  # From origin to loading
                y=[0, pca.components_[1, i]],  # From origin to loading
                mode="lines",
                line=dict(color=arrow_color, width=2),
                showlegend=False,
            ),
            row=1,
            col=1,
        )

        # Add point with label
        fig.add_trace(
            go.Scatter(
                x=[pca.components_[0, i]],
                y=[pca.components_[1, i]],
                mode="markers+text",
                text=[display_name],
                textposition="top center",
                name=display_name,
                marker=dict(color=arrow_color, size=8),
            ),
            row=1,
            col=1,
        )

    # Explained variance with both cumulative and inverse lines
    explained_var = pca.explained_variance_ratio_ * 100
    pc_labels = [f"PC{i + 1}" for i in range(len(explained_var))]
    cumulative_var = explained_var.cumsum()  # Cumulative sum

    # Add bars
    fig.add_trace(
        go.Bar(
            x=pc_labels,
            y=explained_var,
            name="Varianza Explicada (%)"
            if language == "es"
            else "Explained Variance (%)",
            marker_color="lightblue",
            showlegend=True,
        ),
        row=1,
        col=2,
    )

    # Add cumulative line (secondary y-axis)
    fig.add_trace(
        go.Scatter(
            x=pc_labels,
            y=cumulative_var,
            mode="lines+markers",
            name="Varianza Acumulativa (%)"
            if language == "es"
            else "Cumulative Variance (%)",
            line=dict(color="orange", width=3),
            marker=dict(color="orange", size=8),
            yaxis="y2",  # Use secondary y-axis
        ),
        row=1,
        col=2,
    )

    # Add inverse line (tertiary y-axis) - not normalized
    if len(explained_var) > 1:
        max_var = explained_var.max()
        inverse_values = (
            max_var / explained_var
        )  # Higher variance = lower inverse value

        fig.add_trace(
            go.Scatter(
                x=pc_labels,
                y=inverse_values,
                mode="lines+markers",
                name="Relación Inversa" if language == "es" else "Inverse Relationship",
                line=dict(color="red", width=2, dash="dash"),
                marker=dict(color="red", size=6),
                yaxis="y3",  # Use tertiary y-axis for inverse
            ),
            row=1,
            col=2,
        )

    # Create title with tool name if provided
    base_title = get_text("pca_title", language)
    if tool_name:
        title_text = f"{base_title} - {tool_name}"
    else:
        title_text = base_title

    # Update layout with multiple y-axes
    fig.update_layout(
        title=title_text,
        height=500,
        showlegend=True,
        annotations=[],  # Clear any existing annotations
        yaxis2=dict(
            title=get_text("cumulative_variance", language),
            overlaying="y",
            side="right",
            range=[0, 100],
            showgrid=False,
        ),
        yaxis3=dict(
            title=get_text("inverse_relationship", language),
            overlaying="y",
            side="right",
            position=0.85,  # Position further right
            showgrid=False,
            anchor="free",
        ),
    )

    # Add source URL annotation as legend-style outside the graph
    source_text = get_text("source", language) + " https://dashboard.solidum360.com/"
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=1,
        y=1.2,  # Position relative to plot (higher for PCA Analysis)
        text=source_text,
        showarrow=False,
        font=dict(size=12),
        align="left",
    )

    # Set legend at bottom for each subplot
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )

    # Add origin lines to loadings plot
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)

    # Clear any existing annotations to ensure clean graph
    fig.update_layout(annotations=[])

    # Update legend for loadings plot (left subplot)
    fig.update_layout(
        legend2=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.25,  # Center on left subplot
            xref="paper",
        )
    )

    return fig


def create_correlation_heatmap(data, sources, language="es", tool_name=None):
    """
    Create a correlation heatmap figure.
    """
    print(f"DEBUG: create_correlation_heatmap called with sources: {sources}")

    # Import required functions for translation mapping
    from fix_source_mapping import (
        map_display_names_to_source_ids,
        DBASE_OPTIONS as dbase_options,
    )
    from translations import get_text, translate_source_name

    # DATAFRAME_INDEXING_FIX: Create proper translation mapping
    selected_source_ids = map_display_names_to_source_ids(sources)
    translation_mapping = create_translation_mapping(selected_source_ids, language)

    # Use original column names for correlation calculation
    original_columns = []
    for source in sources:
        original_name = get_original_column_name(source, translation_mapping)
        if original_name in data.columns:
            original_columns.append(original_name)

    if len(original_columns) < 2:
        print(
            f"DEBUG: Insufficient columns for correlation heatmap: {len(original_columns)} columns available"
        )
        print(f"DEBUG: Found columns: {original_columns}")
        print(f"DEBUG: Translation mapping: {translation_mapping}")
        print(f"DEBUG: Data columns: {list(data.columns)}")
        return go.Figure()

    corr_data = data[original_columns].corr()
    print(f"DEBUG: Correlation data shape: {corr_data.shape}")

    # Check if correlation matrix is valid
    if corr_data.empty or corr_data.isna().all().all():
        print(f"DEBUG: Invalid correlation data")
        return go.Figure()

    # Create mapping from original column names back to display names for labeling
    original_to_display = {v: k for k, v in translation_mapping.items()}

    # Update sources list to use display names for labeling
    display_sources = [original_to_display.get(col, col) for col in corr_data.columns]

    # Create custom annotations with better contrast
    annotations = []
    for i, row in enumerate(corr_data.values):
        for j, val in enumerate(row):
            # Determine text color based on background intensity
            # For RdBu colorscale: negative values are blue, positive are red, zero is white
            if abs(val) < 0.3:
                # Light background - use dark text
                text_color = "black"
            else:
                # Dark background - use white text
                text_color = "white"

            annotations.append(
                dict(
                    x=display_sources[j],
                    y=display_sources[i],
                    text=f"{val:.2f}",
                    showarrow=False,
                    font=dict(color=text_color, size=12, weight="bold"),
                )
            )

    # Create heatmap using go.Heatmap for proper click event support
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_data.values,
            x=display_sources,
            y=display_sources,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            hovertemplate="%{x} vs %{y}<br>Correlación: %{z:.3f}<extra></extra>",
            showscale=True,
        )
    )

    # Create title with tool name if provided
    base_title = get_text("correlation_heatmap_title", language)
    if tool_name:
        title_text = f"{base_title} - {tool_name}"
    else:
        title_text = base_title

    # Update layout with annotations and enable click events
    fig.update_layout(
        title=title_text,
        height=400,
        annotations=annotations,  # Keep correlation value annotations inside the heatmap
        xaxis=dict(side="bottom"),
        yaxis=dict(side="left"),
        clickmode="event+select",  # Enable click events
    )

    # Add source URL annotation as legend-style outside the graph
    source_text = get_text("source", language) + " https://dashboard.solidum360.com/"
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


def create_translation_mapping(selected_source_ids, language):
    """
    Create translation mapping for selected source IDs.

    Args:
        selected_source_ids (list): List of source IDs to map
        language (str): Target language code

    Returns:
        dict: Translation mapping
    """
    from translations import translate_source_name
    from fix_source_mapping import DBASE_OPTIONS

    translation_mapping = {}
    for src_id in selected_source_ids:
        original_name = DBASE_OPTIONS.get(src_id, "NOT FOUND")
        translated_name = translate_source_name(original_name, language)
        translation_mapping[translated_name] = original_name
        translated_name_simple = translated_name.replace(" - ", " ")
        translation_mapping[translated_name_simple] = original_name
    return translation_mapping


def get_original_column_name(display_name, translation_mapping):
    """
    Get original column name from display name.

    Args:
        display_name (str): Display name to convert
        translation_mapping (dict): Translation mapping

    Returns:
        str: Original column name
    """
    # First try the translation mapping
    if display_name in translation_mapping:
        return translation_mapping[display_name]

    # Then try the display-to-database name mapping
    try:
        from fix_source_mapping import DISPLAY_TO_DB_NAME

        if display_name in DISPLAY_TO_DB_NAME:
            return DISPLAY_TO_DB_NAME[display_name]
    except ImportError:
        pass

    # Fallback: return the display name as-is
    return display_name


def safe_dataframe_column_access(data, translated_name, translation_mapping):
    """
    Safely access dataframe column by translated name.

    Args:
        data (pd.DataFrame): Dataframe to access
        translated_name (str): Translated column name
        translation_mapping (dict): Translation mapping

    Returns:
        pd.Series: Column data or None if not found
    """
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
