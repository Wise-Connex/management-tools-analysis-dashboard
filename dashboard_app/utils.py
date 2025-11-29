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
from dash import html
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose

# Import project-specific modules
from tools import tool_file_dic


# Global cache for processed datasets
_processed_data_cache = {}
_cache_max_size = 10


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
    data, sources, language="es", start_date=None, end_date=None, tool_name=None,
    # These parameters would need to be passed in or made available
    map_display_names_to_source_ids=None, create_translation_mapping=None,
    safe_dataframe_column_access=None, get_original_column_name=None,
    get_text=None, color_map=None
):
    """
    Create a 2D temporal visualization figure.

    This is a placeholder - full implementation would require additional dependencies
    and app-specific functions to be passed as parameters or imported.
    """
    # Simplified implementation - full function requires many app-specific dependencies
    fig = go.Figure()

    # Basic temporal plotting logic would go here
    # For now, return empty figure with error handling
    print("Warning: create_temporal_2d_figure called with placeholder implementation")

    return fig


def create_mean_analysis_figure(data, sources, language="es", tool_name=None):
    """
    Create a mean analysis figure showing relative contributions.

    This is a placeholder - full implementation would require additional dependencies.
    """
    fig = go.Figure()

    # Basic mean analysis logic would go here
    print("Warning: create_mean_analysis_figure called with placeholder implementation")

    return fig


def perform_comprehensive_pca_analysis(data, sources, language="es"):
    """
    Perform comprehensive PCA analysis with detailed metrics.

    This is a placeholder - full implementation would require additional dependencies.
    """
    # Basic PCA analysis
    try:
        # Create a simple PCA analysis
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            return {"error": "No numeric data available for PCA"}

        pca = PCA(n_components=min(2, len(numeric_data.columns)))
        pca_result = pca.fit_transform(numeric_data.fillna(0))

        return {
            "success": True,
            "pca": pca,
            "pca_result": pca_result,
            "explained_variance_ratio": pca.explained_variance_ratio_,
            "components": pca.components_
        }
    except Exception as e:
        return {"error": f"PCA analysis failed: {str(e)}"}


def create_pca_figure(data, sources, language="es", tool_name=None):
    """
    Create a PCA visualization figure.

    This is a placeholder - full implementation would require additional dependencies.
    """
    fig = go.Figure()

    # Basic PCA visualization logic would go here
    print("Warning: create_pca_figure called with placeholder implementation")

    return fig


def create_correlation_heatmap(data, sources, language="es", tool_name=None):
    """
    Create a correlation heatmap figure.

    This is a placeholder - full implementation would require additional dependencies.
    """
    fig = go.Figure()

    # Basic correlation heatmap logic would go here
    print("Warning: create_correlation_heatmap called with placeholder implementation")

    return fig