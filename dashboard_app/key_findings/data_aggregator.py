"""
Data Aggregation Pipeline

Aggregates and synthesizes data from multiple dashboard sources
with emphasis on Principal Component Analysis for doctoral-level insights.
"""

import pandas as pd
import numpy as np
import time
from typing import Dict, List, Any, Optional, Tuple
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from scipy import stats
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataAggregator:
    """
    Aggregates and synthesizes data from multiple dashboard sources.
    
    Provides comprehensive data preparation for AI analysis with
    PCA emphasis, statistical summaries, and trend detection.
    """

    def __init__(self, db_manager, cache_manager):
        """
        Initialize data aggregator.
        
        Args:
            db_manager: Database manager instance
            cache_manager: Cache manager instance
        """
        self.db_manager = db_manager
        self.cache_manager = cache_manager

    def collect_analysis_data(self, tool_name: str, selected_sources: List[Any],
                            language: str = 'es', source_display_names: List[str] = None) -> Dict[str, Any]:
        """
        Collect all relevant data for AI analysis.

        Args:
            tool_name: Selected management tool
            selected_sources: List of selected data source IDs (integers)
            language: Analysis language
            source_display_names: Optional list of source display names (strings) for prompts

        Returns:
            Dictionary containing all analysis data
        """
        start_time = time.time()
        logging.info(f"🚀 Starting data collection for tool='{tool_name}', sources={selected_sources}, language={language}")
        logging.info(f"🔍 Function parameters - selected_sources: {selected_sources} (type: {type(selected_sources)})")
        logging.info(f"🔍 Function parameters - source_display_names: {source_display_names} (type: {type(source_display_names)})")

        # Debug the parameter decision logic
        if source_display_names:
            logging.info(f"✅ Will use source_display_names for analysis: {source_display_names}")
        else:
            logging.info(f"⚠️  source_display_names is None/empty, will use selected_sources: {selected_sources}")
        
        # Handle bilingual tool name mapping - convert display name to database name
        # Import the necessary functions for tool name mapping
        try:
            from tools import get_tool_name
            from translations import TOOL_TRANSLATIONS
            
            logging.info(f"🔍 Original tool_name: '{tool_name}' (language: {language})")
            
            # If we're in English and the tool name is in English, translate it to Spanish for database query
            if language == 'en':
                # Find the Spanish key for this English value
                spanish_tool_name = None
                for spanish_name, english_name in TOOL_TRANSLATIONS['en'].items():
                    if english_name == tool_name:
                        spanish_tool_name = spanish_name
                        break
                
                if spanish_tool_name:
                    logging.info(f"🔄 Translated tool name from English to Spanish: '{tool_name}' -> '{spanish_tool_name}'")
                    tool_name = spanish_tool_name
                else:
                    logging.warning(f"⚠️ Could not find Spanish translation for tool '{tool_name}'")
            
            logging.info(f"🔍 Final tool_name for database query: '{tool_name}'")
            
        except ImportError as e:
            logging.warning(f"⚠️ Could not import translation functions: {e}")
        except Exception as e:
            logging.error(f"❌ Error in tool name translation: {e}")
        
        # Get raw data from database with timeout protection
        db_start_time = time.time()
        logging.info(f"📊 Querying database for tool='{tool_name}' with {len(selected_sources)} sources...")
        logging.info(f"🔍 Source list: {selected_sources}")

        # Note: We removed the pre-check that only tested the first source,
        # as it caused false "not found" errors when the first source didn't have data
        # but other sources did. The main query below will handle validation properly.

        try:
            # Add timeout protection for database queries
            import asyncio
            import concurrent.futures

            def db_query_with_timeout():
                return self.db_manager.get_data_for_keyword(tool_name, selected_sources)

            # Run database query with 30 second timeout
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(db_query_with_timeout)
                try:
                    datasets_norm, sl_sc = future.result(timeout=30)  # 30 second timeout
                    db_time = time.time() - db_start_time
                    logging.info(f"✅ Database query completed in {db_time:.2f}s - retrieved {len(datasets_norm)} datasets")
                    logging.info(f"📋 Dataset keys: {list(datasets_norm.keys()) if datasets_norm else 'None'}")
                    logging.info(f"📋 Source list: {sl_sc}")
                except concurrent.futures.TimeoutError:
                    db_time = time.time() - db_start_time
                    logging.error(f"⏰ Database query timed out after {db_time:.2f}s")
                    raise Exception(f"Database query timed out after {db_time:.2f}s. The query may be hanging.")

        except Exception as e:
            db_time = time.time() - db_start_time
            if "timeout" in str(e).lower():
                logging.error(f"⏰ Database query timed out after {db_time:.2f}s")
            else:
                logging.error(f"❌ Database query failed after {db_time:.2f}s: {e}")
            import traceback
            traceback.print_exc()
            raise

        if not datasets_norm:
            logging.warning(f"⚠️ No data available for tool '{tool_name}' with selected sources")
            return {
                'error': f"No data available for tool '{tool_name}' with selected sources",
                'tool_name': tool_name,
                'selected_sources': selected_sources,
                'language': language,
                'data_points_analyzed': 0,
                'sources_count': len(selected_sources)
            }
        
        # Create combined dataset with Key Findings specific method
        combine_start_time = time.time()
        logging.info(f"🔄 Creating Key Findings combined dataset from {len(datasets_norm)} sources...")
        combined_dataset = self._create_combined_dataset(datasets_norm, sl_sc, tool_name)
        combine_time = time.time() - combine_start_time
        logging.info(f"✅ Combined dataset created in {combine_time:.2f}s - shape: {combined_dataset.shape}")

        if combined_dataset.empty:
            logging.warning(f"⚠️ Combined dataset is empty for tool '{tool_name}'")
            return {
                'error': f"No combined data available for tool '{tool_name}'",
                'tool_name': tool_name,
                'selected_sources': selected_sources,
                'language': language,
                'data_points_analyzed': 0,
                'sources_count': len(selected_sources)
            }
        
        # Check if we have single or multiple sources for appropriate analysis
        is_single_source = len(combined_dataset.columns) == 1
        if is_single_source:
            logging.info(f"📊 Single source detected for '{tool_name}'. Performing single source analysis.")
            logging.info(f"🔍 Single source column: {combined_dataset.columns.tolist()}")
        else:
            logging.info(f"📊 Multiple sources detected for '{tool_name}'. Performing multi-source analysis with PCA.")
        
        # Extract insights based on number of sources
        analysis_start_time = time.time()
        try:
            if is_single_source:
                logging.info(f"📈 Starting single source analysis on {len(combined_dataset)} data points...")
                logging.info(f"🔍 selected_sources: {selected_sources}")
                logging.info(f"🔍 source_display_names: {source_display_names}")
                sources_for_analysis = source_display_names if source_display_names else selected_sources
                logging.info(f"🔍 sources_for_analysis: {sources_for_analysis}")
                logging.info(f"🔍 DataFrame columns: {combined_dataset.columns.tolist()}")
                logging.info(f"🔍 Column match check: '{sources_for_analysis[0] if sources_for_analysis else None}' in {combined_dataset.columns.tolist()}")
                single_source_insights = self.extract_single_source_insights(combined_dataset, sources_for_analysis)
                analysis_time = time.time() - analysis_start_time
                logging.info(f"✅ Single source analysis completed in {analysis_time:.2f}s")
                logging.info(f"🔍 Single source insights keys: {list(single_source_insights.keys()) if single_source_insights else 'None'}")
            else:
                logging.info(f"🧮 Starting PCA analysis on {len(combined_dataset)} data points with {len(selected_sources)} sources...")
                logging.info(f"🔍 selected_sources: {selected_sources}")
                logging.info(f"🔍 source_display_names: {source_display_names}")
                sources_for_analysis = source_display_names if source_display_names else selected_sources
                logging.info(f"🔍 sources_for_analysis: {sources_for_analysis}")
                pca_insights = self.extract_pca_insights(combined_dataset, sources_for_analysis)
                analysis_time = time.time() - analysis_start_time
                pca_variance = pca_insights.get('total_variance_explained', 0) if 'error' not in pca_insights else 0
                logging.info(f"✅ PCA analysis completed in {analysis_time:.2f}s - variance explained: {pca_variance:.1f}%")
        except Exception as e:
            logging.error(f"❌ Analysis failed: {e}")
            # Provide fallback analysis results
            analysis_time = time.time() - analysis_start_time
            if is_single_source:
                single_source_insights = {
                    'error': f'Analysis failed: {str(e)}',
                    'temporal_trends': {},
                    'seasonal_patterns': {},
                    'fourier_analysis': {}
                }
            else:
                pca_insights = {
                    'error': f'Analysis failed: {str(e)}',
                    'components_analyzed': 0,
                    'variance_explained': 0,
                    'dominant_patterns': []
                }
            logging.info(f"⚠️ Using fallback analysis results after failure")
        
        # Calculate statistical summaries
        stats_start_time = time.time()
        logging.info(f"📊 Starting statistical analysis...")
        try:
            statistical_summary = self.calculate_statistical_summaries(combined_dataset, selected_sources)
            stats_time = time.time() - stats_start_time
            logging.info(f"✅ Statistical analysis completed in {stats_time:.2f}s")
        except Exception as e:
            logging.error(f"❌ Statistical analysis failed: {e}")
            stats_time = time.time() - stats_start_time
            statistical_summary = {
                'source_statistics': {},
                'correlations': {},
                'overall_data_quality': {'score': 0, 'completeness': 0, 'consistency': 0}
            }
            logging.info(f"⚠️ Using fallback statistical summary after failure")

        # Identify trends and anomalies
        trends_start_time = time.time()
        logging.info(f"📈 Starting trends and anomalies analysis...")
        try:
            trends_analysis = self.identify_trends_and_anomalies(combined_dataset, selected_sources)
            trends_time = time.time() - trends_start_time
            logging.info(f"✅ Trends analysis completed in {trends_time:.2f}s")
        except Exception as e:
            logging.error(f"❌ Trends analysis failed: {e}")
            trends_time = time.time() - trends_start_time
            trends_analysis = {
                'trends': {},
                'anomalies': {},
                'overall_patterns': []
            }
            logging.info(f"⚠️ Using fallback trends analysis after failure")

        # Calculate data quality metrics
        quality_start_time = time.time()
        logging.info(f"🔍 Starting data quality assessment...")
        try:
            data_quality = self.assess_data_quality(combined_dataset, selected_sources)
            quality_time = time.time() - quality_start_time
            logging.info(f"✅ Data quality assessment completed in {quality_time:.2f}s")
        except Exception as e:
            logging.error(f"❌ Data quality assessment failed: {e}")
            quality_time = time.time() - quality_start_time
            data_quality = {
                'completeness': {},
                'consistency': {},
                'timeliness': {},
                'overall_score': 0
            }
            logging.info(f"⚠️ Using fallback data quality assessment after failure")

        # Generate heatmap analysis data
        heatmap_start_time = time.time()
        logging.info(f"🔥 Starting heatmap analysis generation...")
        try:
            # Use display names for heatmap analysis, not source IDs
            source_display_names = source_display_names if source_display_names else selected_sources
            heatmap_analysis = self.generate_heatmap_analysis(combined_dataset, source_display_names)
            heatmap_time = time.time() - heatmap_start_time
            logging.info(f"✅ Heatmap analysis generated in {heatmap_time:.2f}s")
        except Exception as e:
            logging.error(f"❌ Heatmap analysis failed: {e}")
            heatmap_time = time.time() - heatmap_start_time
            heatmap_analysis = {
                'value_ranges': {},
                'most_dense_regions': [],
                'least_dense_regions': [],
                'detected_clusters': [],
                'detected_outliers': [],
                'gradients': {}
            }
            logging.info(f"⚠️ Using fallback heatmap analysis after failure")
        
        # Anonymize sensitive data
        anonymize_start_time = time.time()
        logging.info(f"🔒 Starting data anonymization...")
        try:
            anonymized_data = self.anonymize_sensitive_data(combined_dataset)
            anonymize_time = time.time() - anonymize_start_time
            logging.info(f"✅ Data anonymization completed in {anonymize_time:.2f}s")
        except Exception as e:
            logging.error(f"❌ Data anonymization failed: {e}")
            # Use original data as fallback
            anonymized_data = combined_dataset.copy()
            anonymize_time = time.time() - anonymize_start_time
            logging.info(f"⚠️ Using original data as fallback after anonymization failure")

        # Create data summary with error handling
        try:
            anonymized_data_summary = self._create_data_summary(anonymized_data)
        except Exception as e:
            logging.error(f"❌ Data summary creation failed: {e}")
            anonymized_data_summary = {
                'shape': anonymized_data.shape if hasattr(anonymized_data, 'shape') else (0, 0),
                'columns': list(anonymized_data.columns) if hasattr(anonymized_data, 'columns') else [],
                'date_range': {'start': 'N/A', 'end': 'N/A', 'total_days': 0},
                'basic_statistics': {}
            }
            logging.info(f"⚠️ Using fallback data summary after failure")

        # Calculate total time
        total_time = time.time() - start_time

        # Log performance summary
        analysis_type = "Single source analysis" if is_single_source else "PCA analysis"
        logging.info(f"📋 Data collection completed in {total_time:.2f}s total:")
        logging.info(f"   ├── Database query: {db_time:.2f}s")
        logging.info(f"   ├── Data combination: {combine_time:.2f}s")
        logging.info(f"   ├── {analysis_type}: {analysis_time:.2f}s")
        logging.info(f"   ├── Statistical analysis: {stats_time:.2f}s")
        logging.info(f"   ├── Trends analysis: {trends_time:.2f}s")
        logging.info(f"   ├── Data quality: {quality_time:.2f}s")
        logging.info(f"   ├── Heatmap analysis: {heatmap_time:.2f}s")
        logging.info(f"   └── Data anonymization: {anonymize_time:.2f}s")

        # Use display names for prompts if provided, otherwise use source IDs
        sources_for_prompts = source_display_names if source_display_names else selected_sources
        
        # Safe date range calculation for result
        try:
            if len(combined_dataset.index) > 0:
                if not isinstance(combined_dataset.index, pd.DatetimeIndex):
                    combined_dataset.index = pd.to_datetime(combined_dataset.index)
                date_range_start = combined_dataset.index.min().strftime('%Y-%m-%d')
                date_range_end = combined_dataset.index.max().strftime('%Y-%m-%d')
            else:
                date_range_start = 'N/A'
                date_range_end = 'N/A'
        except Exception as e:
            logging.warning(f"Error calculating date range for result: {e}")
            date_range_start = 'N/A'
            date_range_end = 'N/A'

        result = {
            'tool_name': tool_name,
            'selected_sources': sources_for_prompts,  # Use display names for prompts
            'selected_source_ids': selected_sources,  # Keep original IDs for reference
            'language': language,
            'data_points_analyzed': len(combined_dataset),
            'sources_count': len(selected_sources),
            'date_range_start': date_range_start,
            'date_range_end': date_range_end,
            'pca_insights': pca_insights if not is_single_source else None,
            'single_source_insights': single_source_insights if is_single_source else None,
            'statistical_summary': statistical_summary,
            'trends_analysis': trends_analysis,
            'data_quality': data_quality,
            'heatmap_analysis': heatmap_analysis,
            'anonymized_data_summary': anonymized_data_summary,
            'analysis_timestamp': datetime.now().isoformat(),
            'performance_metrics': {
                'total_time_seconds': total_time,
                'database_query_time': db_time,
                'data_combination_time': combine_time,
                'analysis_time': analysis_time,  # Changed from pca_time to analysis_time
                'statistical_analysis_time': stats_time,
                'trends_analysis_time': trends_time,
                'data_quality_time': quality_time,
                'heatmap_analysis_time': heatmap_time,
                'anonymization_time': anonymize_time
            }
        }

        logging.info(f"📋 Data collection result keys: {list(result.keys())}")
        if is_single_source:
            logging.info(f"🔍 Single source insights in result: {'single_source_insights' in result and result['single_source_insights'] is not None}")

        logging.info(f"🎉 Data collection process completed successfully in {total_time:.2f}s")
        return result

    def extract_single_source_insights(self, data: pd.DataFrame, selected_sources: List[str]) -> Dict[str, Any]:
        """
        Extract insights for single data source analysis including temporal trends,
        seasonal patterns, and Fourier analysis.
        
        Args:
            data: Combined dataset with single source
            selected_sources: List of selected sources (should contain only one source)
            
        Returns:
            Dictionary with single source analysis insights
        """
        if len(selected_sources) != 1:
            return {
                'error': 'Single source analysis requires exactly 1 data source',
                'temporal_trends': {},
                'seasonal_patterns': {},
                'fourier_analysis': {}
            }
        
        source_name = selected_sources[0]
        if source_name not in data.columns:
            return {
                'error': f'Source {source_name} not found in data',
                'temporal_trends': {},
                'seasonal_patterns': {},
                'fourier_analysis': {}
            }
        
        try:
            source_data = data[source_name].dropna()
            if len(source_data) < 12:  # Need at least 12 data points for meaningful analysis
                return {
                    'error': 'Insufficient data for single source analysis (need at least 12 data points)',
                    'temporal_trends': {},
                    'seasonal_patterns': {},
                    'fourier_analysis': {}
                }
            
            # Temporal Trends Analysis
            temporal_trends = self._analyze_temporal_trends(source_data)
            
            # Seasonal Patterns Analysis
            seasonal_patterns = self._analyze_seasonal_patterns(source_data)
            
            # Fourier Analysis
            fourier_analysis = self._perform_fourier_analysis(source_data)
            
            return {
                'source_name': source_name,
                'data_points_used': len(source_data),
                'temporal_trends': temporal_trends,
                'seasonal_patterns': seasonal_patterns,
                'fourier_analysis': fourier_analysis,
                'analysis_success': True
            }
            
        except Exception as e:
            logging.error(f"Single source analysis failed: {e}")
            return {
                'error': f'Single source analysis error: {str(e)}',
                'temporal_trends': {},
                'seasonal_patterns': {},
                'fourier_analysis': {}
            }

    def _analyze_temporal_trends(self, data: pd.Series) -> Dict[str, Any]:
        """Analyze temporal trends in the data."""
        try:
            # Ensure data has a datetime index
            if not isinstance(data.index, pd.DatetimeIndex):
                data.index = pd.to_datetime(data.index)
            
            # Linear trend analysis
            x = np.arange(len(data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
            
            # Moving averages
            ma_3 = data.rolling(window=3, center=True).mean()
            ma_6 = data.rolling(window=6, center=True).mean()
            ma_12 = data.rolling(window=12, center=True).mean()
            
            # Recent vs historical comparison
            recent_period = min(12, len(data) // 4)  # Use last 25% or 12 points
            recent_data = data.iloc[-recent_period:]
            historical_data = data.iloc[:-recent_period] if len(data) > recent_period else data.iloc[:recent_period]
            
            recent_mean = recent_data.mean()
            historical_mean = historical_data.mean()
            change_percentage = ((recent_mean - historical_mean) / historical_mean * 100) if historical_mean != 0 else 0
            
            # Volatility analysis
            volatility = data.rolling(window=3).std().mean()
            recent_volatility = recent_data.rolling(window=min(3, len(recent_data))).std().mean()
            
            return {
                'linear_trend': {
                    'slope': float(slope),
                    'intercept': float(intercept),
                    'r_squared': float(r_value ** 2),
                    'p_value': float(p_value),
                    'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
                    'significance': 'significant' if p_value < 0.05 else 'not_significant'
                },
                'moving_averages': {
                    'ma_3_current': float(ma_3.iloc[-1]) if not ma_3.empty else None,
                    'ma_6_current': float(ma_6.iloc[-1]) if not ma_6.empty else None,
                    'ma_12_current': float(ma_12.iloc[-1]) if not ma_12.empty else None,
                },
                'recent_vs_historical': {
                    'recent_mean': float(recent_mean),
                    'historical_mean': float(historical_mean),
                    'change_percentage': float(change_percentage),
                    'change_direction': 'increasing' if change_percentage > 0 else 'decreasing' if change_percentage < 0 else 'stable'
                },
                'volatility': {
                    'overall': float(volatility),
                    'recent': float(recent_volatility),
                    'volatility_trend': 'increasing' if recent_volatility > volatility else 'decreasing' if recent_volatility < volatility else 'stable'
                }
            }
        except Exception as e:
            logging.error(f"Temporal trends analysis failed: {e}")
            return {'error': f'Temporal trends analysis error: {str(e)}'}

    def _analyze_seasonal_patterns(self, data: pd.Series) -> Dict[str, Any]:
        """Analyze seasonal patterns in the data."""
        try:
            # Ensure data has a datetime index
            if not isinstance(data.index, pd.DatetimeIndex):
                data.index = pd.to_datetime(data.index)
            
            # Extract seasonal components
            data_df = pd.DataFrame({'value': data, 'month': data.index.month, 'quarter': data.index.quarter, 'year': data.index.year})
            
            # Monthly patterns
            monthly_means = data_df.groupby('month')['value'].mean()
            monthly_std = data_df.groupby('month')['value'].std()
            
            # Quarterly patterns
            quarterly_means = data_df.groupby('quarter')['value'].mean()
            quarterly_std = data_df.groupby('quarter')['value'].std()
            
            # Year-over-year patterns
            yearly_means = data_df.groupby('year')['value'].mean()
            if len(yearly_means) > 1:
                yoy_growth = yearly_means.pct_change().mean() * 100
            else:
                yoy_growth = 0
            
            # Seasonality strength (using standard deviation of monthly means)
            seasonality_strength = monthly_std.std() / monthly_means.mean() if monthly_means.mean() != 0 else 0
            
            # Identify peak and low months
            peak_month = monthly_means.idxmax()
            low_month = monthly_means.idxmin()
            
            return {
                'monthly_patterns': {
                    'monthly_means': monthly_means.to_dict(),
                    'monthly_std': monthly_std.to_dict(),
                    'peak_month': int(peak_month),
                    'low_month': int(low_month),
                    'peak_value': float(monthly_means.max()),
                    'low_value': float(monthly_means.min())
                },
                'quarterly_patterns': {
                    'quarterly_means': quarterly_means.to_dict(),
                    'quarterly_std': quarterly_std.to_dict()
                },
                'year_over_year': {
                    'yearly_means': yearly_means.to_dict(),
                    'average_growth_rate': float(yoy_growth)
                },
                'seasonality_strength': {
                    'strength_value': float(seasonality_strength),
                    'strength_level': 'strong' if seasonality_strength > 0.3 else 'moderate' if seasonality_strength > 0.1 else 'weak'
                }
            }
        except Exception as e:
            logging.error(f"Seasonal patterns analysis failed: {e}")
            return {'error': f'Seasonal patterns analysis error: {str(e)}'}

    def _perform_fourier_analysis(self, data: pd.Series) -> Dict[str, Any]:
        """Perform Fourier analysis to identify dominant frequencies."""
        try:
            # Remove NaN values and normalize data
            clean_data = data.dropna()
            if len(clean_data) < 24:  # Need sufficient data points for Fourier analysis
                return {'error': 'Insufficient data for Fourier analysis (need at least 24 data points)'}
            
            # Normalize data (zero mean, unit variance)
            normalized_data = (clean_data - clean_data.mean()) / clean_data.std()
            
            # Perform FFT
            fft_values = np.fft.fft(normalized_data.values)
            fft_freq = np.fft.fftfreq(len(normalized_data))
            
            # Calculate power spectrum
            power_spectrum = np.abs(fft_values) ** 2
            
            # Only consider positive frequencies
            positive_freq_idx = fft_freq > 0
            positive_freq = fft_freq[positive_freq_idx]
            positive_power = power_spectrum[positive_freq_idx]
            
            # Find dominant frequencies (top 5)
            dominant_indices = np.argsort(positive_power)[-5:][::-1]
            dominant_frequencies = positive_freq[dominant_indices]
            dominant_powers = positive_power[dominant_indices]
            
            # Convert frequencies to periods (in data points)
            periods = 1 / dominant_frequencies if np.all(dominant_frequencies != 0) else np.inf * np.ones_like(dominant_frequencies)
            
            # Identify seasonal patterns based on periods
            seasonal_patterns = []
            for i, (freq, power, period) in enumerate(zip(dominant_frequencies, dominant_powers, periods)):
                if 0 < period <= len(clean_data) / 2:  # Meaningful period
                    pattern_type = 'unknown'
                    if 11 <= period <= 13:  # Annual pattern
                        pattern_type = 'annual'
                    elif 5 <= period <= 7:  # Semi-annual pattern
                        pattern_type = 'semi-annual'
                    elif 2.5 <= period <= 4:  # Quarterly pattern
                        pattern_type = 'quarterly'
                    elif 1 <= period <= 2:  # Monthly/bi-monthly pattern
                        pattern_type = 'monthly'
                    
                    seasonal_patterns.append({
                        'frequency': float(freq),
                        'period': float(period),
                        'power': float(power),
                        'pattern_type': pattern_type,
                        'relative_strength': float(power / positive_power.max()) if positive_power.max() > 0 else 0
                    })
            
            # Calculate total signal power and noise
            total_power = np.sum(power_spectrum)
            signal_power = np.sum(positive_power[:len(positive_power)//2])  # Lower frequencies as signal
            noise_power = total_power - signal_power
            signal_to_noise_ratio = signal_power / noise_power if noise_power > 0 else float('inf')
            
            return {
                'dominant_frequencies': seasonal_patterns,
                'signal_quality': {
                    'total_power': float(total_power),
                    'signal_power': float(signal_power),
                    'noise_power': float(noise_power),
                    'signal_to_noise_ratio': float(signal_to_noise_ratio),
                    'quality_level': 'excellent' if signal_to_noise_ratio > 10 else 'good' if signal_to_noise_ratio > 5 else 'fair' if signal_to_noise_ratio > 2 else 'poor'
                },
                'data_points_analyzed': len(clean_data)
            }
        except Exception as e:
            logging.error(f"Fourier analysis failed: {e}")
            return {'error': f'Fourier analysis error: {str(e)}'}

    def extract_pca_insights(self, data: pd.DataFrame, selected_sources: List[str]) -> Dict[str, Any]:
        """
        Extract PCA-specific insights for emphasis.
        
        Args:
            data: Combined dataset
            selected_sources: List of selected sources
            
        Returns:
            Dictionary with PCA insights
        """
        if len(selected_sources) < 2:
            return {
                'error': 'PCA requires at least 2 data sources',
                'components_analyzed': 0,
                'variance_explained': 0,
                'dominant_patterns': []
            }
        
        try:
            # Prepare data for PCA
            pca_data = data.dropna()
            if len(pca_data) < 10:  # Need minimum data points
                return {
                    'error': 'Insufficient data for PCA analysis (need at least 10 data points)',
                    'components_analyzed': 0,
                    'variance_explained': 0,
                    'dominant_patterns': []
                }
            
            # Standardize data
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(pca_data)
            
            # Perform PCA
            n_components = min(len(selected_sources), len(pca_data.columns))
            pca = PCA(n_components=n_components)
            pca_result = pca.fit_transform(scaled_data)
            
            # Calculate explained variance
            explained_variance = pca.explained_variance_ratio_
            cumulative_variance = np.cumsum(explained_variance)
            
            # Analyze component loadings
            loadings = pca.components_.T * np.sqrt(explained_variance)
            
            # Identify dominant patterns
            dominant_patterns = []
            for i in range(min(3, n_components)):  # Top 3 components
                component_loadings = loadings[:, i]
                
                # Find sources with highest loadings
                top_sources_idx = np.argsort(np.abs(component_loadings))[-3:][::-1]
                # Handle both string and integer indices
                if all(isinstance(idx, (int, np.integer)) for idx in top_sources_idx):
                    top_sources = [selected_sources[int(idx)] for idx in top_sources_idx]
                else:
                    top_sources = [str(idx) for idx in top_sources_idx]
                top_loadings = [component_loadings[idx] for idx in top_sources_idx]
                
                # Enhanced component analysis with detailed loadings interpretation
                component_analysis = self._analyze_component_detailed(
                    component_loadings, list(data.columns), i+1, explained_variance[i]
                )

                dominant_patterns.append({
                    'component': f'PC{i+1}',
                    'variance_explained': float(explained_variance[i] * 100),
                    'cumulative_variance': float(cumulative_variance[i] * 100),
                    'dominant_sources': top_sources,
                    'loadings': dict(zip(list(data.columns), component_loadings.tolist())),
                    'interpretation': component_analysis['interpretation'],
                    'loadings_analysis': component_analysis['loadings_analysis'],
                    'source_contributions': component_analysis['source_contributions'],
                    'pattern_type': component_analysis['pattern_type']
                })
            
            return {
                'components_analyzed': n_components,
                'total_variance_explained': float(np.sum(explained_variance) * 100),
                'variance_by_component': explained_variance.tolist(),
                'cumulative_variance': cumulative_variance.tolist(),
                'dominant_patterns': dominant_patterns,
                'data_points_used': len(pca_data),
                'pca_success': True
            }
            
        except Exception as e:
            logging.error(f"PCA analysis failed: {e}")
            return {
                'error': f'PCA analysis error: {str(e)}',
                'components_analyzed': 0,
                'variance_explained': 0,
                'dominant_patterns': []
            }

    def calculate_statistical_summaries(self, data: pd.DataFrame, selected_sources: List[str]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistical summaries.
        
        Args:
            data: Combined dataset
            selected_sources: List of selected sources
            
        Returns:
            Dictionary with statistical summaries
        """
        summaries = {}
        
        for source in selected_sources:
            if source not in data.columns:
                continue
                
            source_data = data[source].dropna()
            
            if len(source_data) == 0:
                continue
            
            # Basic statistics
            stats_dict = {
                'count': len(source_data),
                'mean': float(source_data.mean()),
                'median': float(source_data.median()),
                'std': float(source_data.std()),
                'min': float(source_data.min()),
                'max': float(source_data.max()),
                'range': float(source_data.max() - source_data.min()),
                'q25': float(source_data.quantile(0.25)),
                'q75': float(source_data.quantile(0.75)),
                'iqr': float(source_data.quantile(0.75) - source_data.quantile(0.25)),
                'skewness': float(stats.skew(source_data)),
                'kurtosis': float(stats.kurtosis(source_data)),
                'missing_percentage': float(data[source].isna().sum() / len(data) * 100)
            }
            
            # Advanced statistics
            if len(source_data) > 10:
                # Trend analysis (simple linear trend)
                x = np.arange(len(source_data))
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, source_data)
                stats_dict['trend'] = {
                    'slope': float(slope),
                    'intercept': float(intercept),
                    'r_squared': float(r_value ** 2),
                    'p_value': float(p_value),
                    'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
                    'significance': 'significant' if p_value < 0.05 else 'not_significant'
                }
            
            summaries[source] = stats_dict
        
        # Cross-correlation analysis
        correlations = {}
        if len(selected_sources) >= 2:
            for i, source1 in enumerate(selected_sources):
                for source2 in selected_sources[i+1:]:
                    if source1 in data.columns and source2 in data.columns:
                        corr_data = data[[source1, source2]].dropna()
                        if len(corr_data) > 1:
                            correlation, p_value = stats.pearsonr(corr_data[source1], corr_data[source2])
                            correlations[f"{source1}_vs_{source2}"] = {
                                'correlation': float(correlation),
                                'p_value': float(p_value),
                                'significance': 'significant' if p_value < 0.05 else 'not_significant',
                                'strength': self._interpret_correlation_strength(abs(correlation))
                            }
        
        return {
            'source_statistics': summaries,
            'correlations': correlations,
            'overall_data_quality': self._assess_overall_quality(data)
        }

    def identify_trends_and_anomalies(self, data: pd.DataFrame, selected_sources: List[str]) -> Dict[str, Any]:
        """
        Identify significant trends and anomalies.
        
        Args:
            data: Combined dataset
            selected_sources: List of selected sources
            
        Returns:
            Dictionary with trends and anomalies
        """
        trends = {}
        anomalies = {}
        
        for source in selected_sources:
            if source not in data.columns:
                continue
                
            source_data = data[source].dropna()
            
            if len(source_data) < 12:  # Need at least 1 year of monthly data
                continue
            
            # Moving averages for trend detection
            ma_3 = source_data.rolling(window=3, center=True).mean()
            ma_12 = source_data.rolling(window=12, center=True).mean()
            
            # Trend analysis
            recent_trend = ma_3.iloc[-3:].mean() - ma_3.iloc[-6:-3].mean() if len(ma_3) >= 6 else 0
            long_term_trend = ma_12.iloc[-1] - ma_12.iloc[-13] if len(ma_12) >= 13 else 0
            
            trends[source] = {
                'recent_trend': float(recent_trend),
                'long_term_trend': float(long_term_trend),
                'trend_direction': self._classify_trend(recent_trend, long_term_trend),
                'volatility': float(source_data.rolling(window=3).std().mean()),
                'momentum': float(source_data.pct_change(period=3).iloc[-1] if len(source_data) > 3 else 0)
            }
            
            # Anomaly detection using z-score
            z_scores = np.abs(stats.zscore(source_data))
            anomaly_threshold = 2.5  # 2.5 standard deviations
            
            anomaly_indices = np.where(z_scores > anomaly_threshold)[0]
            if len(anomaly_indices) > 0:
                anomalies[source] = {
                    'count': len(anomaly_indices),
                    'percentage': float(len(anomaly_indices) / len(source_data) * 100),
                    'max_z_score': float(np.max(z_scores)),
                    'recent_anomalies': [
                        {
                            'date': data.index[idx].strftime('%Y-%m-%d'),
                            'value': float(source_data.iloc[idx]),
                            'z_score': float(z_scores[idx])
                        }
                        for idx in anomaly_indices[-5:]  # Last 5 anomalies
                    ]
                }
        
        return {
            'trends': trends,
            'anomalies': anomalies,
            'overall_patterns': self._identify_overall_patterns(trends)
        }

    def assess_data_quality(self, data: pd.DataFrame, selected_sources: List[str]) -> Dict[str, Any]:
        """
        Assess data quality metrics.
        
        Args:
            data: Combined dataset
            selected_sources: List of selected sources
            
        Returns:
            Dictionary with data quality metrics
        """
        quality_metrics = {
            'completeness': {},
            'consistency': {},
            'timeliness': {},
            'overall_score': 0
        }
        
        total_data_points = len(data)
        completeness_scores = []
        
        for source in selected_sources:
            if source not in data.columns:
                continue
                
            source_data = data[source]
            
            # Completeness metrics
            missing_count = source_data.isna().sum()
            completeness_score = (total_data_points - missing_count) / total_data_points * 100
            completeness_scores.append(completeness_score)
            
            quality_metrics['completeness'][source] = {
                'completeness_percentage': float(completeness_score),
                'missing_count': int(missing_count),
                'missing_percentage': float(missing_count / total_data_points * 100)
            }
            
            # Consistency metrics (value ranges, outliers)
            if len(source_data.dropna()) > 0:
                q1, q3 = source_data.quantile([0.25, 0.75])
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                outliers = ((source_data < lower_bound) | (source_data > upper_bound)).sum()
                consistency_score = (total_data_points - outliers) / total_data_points * 100
                
                quality_metrics['consistency'][source] = {
                    'consistency_percentage': float(consistency_score),
                    'outlier_count': int(outliers),
                    'outlier_percentage': float(outliers / total_data_points * 100),
                    'value_range': {
                        'min': float(source_data.min()),
                        'max': float(source_data.max()),
                        'range': float(source_data.max() - source_data.min())
                    }
                }
        
        # Overall quality score
        if completeness_scores:
            quality_metrics['overall_score'] = np.mean(completeness_scores)
        
        # Timeliness (data recency)
        if len(data) > 0:
            try:
                latest_date = data.index.max()
                # Handle case where latest_date might be string or already datetime
                if isinstance(latest_date, str):
                    latest_date = pd.to_datetime(latest_date)
                elif not isinstance(latest_date, datetime):
                    # Try to convert if it's not already datetime
                    latest_date = pd.to_datetime(str(latest_date))

                days_since_latest = (datetime.now() - latest_date).days
                quality_metrics['timeliness'] = {
                    'latest_date': latest_date.strftime('%Y-%m-%d'),
                    'days_since_latest': days_since_latest,
                    'timeliness_score': max(0, 100 - days_since_latest / 365 * 100)  # Decay over year
                }
            except Exception as e:
                logging.warning(f"Error calculating timeliness: {e}")
                quality_metrics['timeliness'] = {
                    'latest_date': 'N/A',
                    'days_since_latest': 0,
                    'timeliness_score': 0
                }
        
        return quality_metrics

    def generate_heatmap_analysis(self, data: pd.DataFrame, selected_sources: List[str]) -> Dict[str, Any]:
        """
        Generate heatmap analysis insights for AI processing.

        Args:
            data: Combined dataset
            selected_sources: List of selected sources

        Returns:
            Dictionary with heatmap analysis data
        """
        if len(selected_sources) < 2:
            # For single source, provide value range analysis instead of correlation analysis
            value_ranges = {}
            for source in selected_sources:
                if source in data.columns:
                    source_data = data[source].dropna()
                    if len(source_data) > 0:
                        value_ranges[source] = {
                            'min': float(source_data.min()),
                            'max': float(source_data.max()),
                            'mean': float(source_data.mean()),
                            'std': float(source_data.std()),
                            'range': float(source_data.max() - source_data.min())
                        }
            
            return {
                'single_source_analysis': True,
                'message': 'Heatmap analysis requires at least 2 data sources. Providing single source value analysis instead.',
                'value_ranges': value_ranges,
                'most_dense_regions': [],
                'least_dense_regions': [],
                'detected_clusters': [],
                'detected_outliers': [],
                'gradients': {}
            }

        try:
            # Calculate correlation matrix for heatmap insights
            # Use the actual column names from the data, not the source IDs
            available_columns = [col for col in data.columns if col in selected_sources]
            if len(available_columns) < 2:
                return {
                    'error': 'Heatmap analysis requires at least 2 data sources',
                    'value_ranges': {},
                    'most_dense_regions': [],
                    'least_dense_regions': [],
                    'detected_clusters': [],
                    'detected_outliers': [],
                    'gradients': {}
                }

            correlation_data = data[available_columns].dropna()
            if len(correlation_data) < 5:  # Need minimum data points
                return {
                    'error': 'Insufficient data for heatmap analysis (need at least 5 data points)',
                    'value_ranges': {},
                    'most_dense_regions': [],
                    'least_dense_regions': [],
                    'detected_clusters': [],
                    'detected_outliers': [],
                    'gradients': {}
                }

            # Calculate correlation matrix
            correlation_matrix = correlation_data.corr()

            # Extract value ranges for each source
            value_ranges = {}
            for source in selected_sources:
                if source in data.columns:
                    source_data = data[source].dropna()
                    if len(source_data) > 0:
                        value_ranges[source] = {
                            'min': float(source_data.min()),
                            'max': float(source_data.max()),
                            'mean': float(source_data.mean()),
                            'std': float(source_data.std())
                        }

            # Identify dense regions (high correlation areas)
            dense_regions = []
            for i in range(len(available_columns)):
                for j in range(i+1, len(available_columns)):
                    source1 = available_columns[i]
                    source2 = available_columns[j]
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:  # Strong correlation
                        dense_regions.append(f"Fuerte correlación entre {source1} y {source2} (r={corr_value:.3f})")

            # Identify sparse regions (low correlation areas)
            sparse_regions = []
            for i in range(len(available_columns)):
                for j in range(i+1, len(available_columns)):
                    source1 = available_columns[i]
                    source2 = available_columns[j]
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) < 0.3:  # Weak correlation
                        sparse_regions.append(f"Correlación débil entre {source1} y {source2} (r={corr_value:.3f})")

            # Detect clusters (groups of highly correlated sources)
            clusters = []
            if len(selected_sources) >= 3:
                # Find groups of sources with high inter-correlations
                high_corr_threshold = 0.6
                cluster_sources = []

                for i, source1 in enumerate(selected_sources):
                    correlated_sources = []
                    for j, source2 in enumerate(selected_sources):
                        if i != j:
                            corr_value = abs(correlation_matrix.iloc[i, j])
                            if corr_value > high_corr_threshold:
                                correlated_sources.append(source2)

                    if len(correlated_sources) >= 2:  # At least 2 other correlated sources
                        cluster_sources.extend(correlated_sources)
                        clusters.append(f"Cluster identificado: {source1} correlacionado con {', '.join(correlated_sources)}")

                # Remove duplicates
                clusters = list(set(clusters))

            # Detect outliers (sources with unusual correlation patterns)
            outliers = []
            for i, source in enumerate(selected_sources):
                # Count how many correlations are above/below certain thresholds
                correlations = correlation_matrix.iloc[i].drop(source) if source in correlation_matrix.index else []
                if len(correlations) > 0:
                    high_corr_count = sum(abs(corr) > 0.7 for corr in correlations)
                    low_corr_count = sum(abs(corr) < 0.2 for corr in correlations)

                    if high_corr_count >= len(correlations) * 0.8:  # Mostly high correlations
                        outliers.append(f"{source}: patrón de alta correlación con otras fuentes")
                    elif low_corr_count >= len(correlations) * 0.8:  # Mostly low correlations
                        outliers.append(f"{source}: patrón de baja correlación con otras fuentes")

            # Identify gradients (temporal patterns in correlations)
            gradients = {}
            if len(data) >= 12:  # Need at least 1 year of data
                # Split data into early and late periods
                split_point = len(data) // 2
                early_data = data.iloc[:split_point][selected_sources].dropna()
                late_data = data.iloc[split_point:][selected_sources].dropna()

                if len(early_data) >= 3 and len(late_data) >= 3:
                    early_corr = early_data.corr()
                    late_corr = late_data.corr()

                    # Find correlations that changed significantly
                    for i in range(len(available_columns)):
                        for j in range(i+1, len(available_columns)):
                            source1 = available_columns[i]
                            source2 = available_columns[j]
                            early_corr_val = early_corr.iloc[i, j]
                            late_corr_val = late_corr.iloc[i, j]
                            change = late_corr_val - early_corr_val

                            if abs(change) > 0.4:  # Significant change
                                direction = "aumentó" if change > 0 else "disminuyó"
                                gradients[f"{source1}_{source2}"] = f"Correlación entre {source1} y {source2} {direction} de {early_corr_val:.3f} a {late_corr_val:.3f}"

            return {
                'value_ranges': value_ranges,
                'most_dense_regions': dense_regions[:5],  # Limit to top 5
                'least_dense_regions': sparse_regions[:5],  # Limit to top 5
                'detected_clusters': clusters[:3],  # Limit to top 3
                'detected_outliers': outliers[:3],  # Limit to top 3
                'gradients': gradients,
                'correlation_matrix_summary': {
                    'strongest_positive': float(correlation_matrix.max().max()) if not correlation_matrix.empty else 0,
                    'strongest_negative': float(correlation_matrix.min().min()) if not correlation_matrix.empty else 0,
                    'average_correlation': float(correlation_matrix.values.mean()) if not correlation_matrix.empty else 0
                }
            }

        except Exception as e:
            logging.error(f"Heatmap analysis generation failed: {e}")
            return {
                'error': f'Heatmap analysis error: {str(e)}',
                'value_ranges': {},
                'most_dense_regions': [],
                'least_dense_regions': [],
                'detected_clusters': [],
                'detected_outliers': [],
                'gradients': {}
            }

    def anonymize_sensitive_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Remove or anonymize sensitive information before LLM processing.
        
        Args:
            data: Combined dataset
            
        Returns:
            Anonymized dataset
        """
        anonymized = data.copy()
        
        # Remove exact dates (keep only relative timing)
        if hasattr(anonymized.index, 'to_period'):
            anonymized.index = anonymized.index.to_period('M')  # Convert to monthly periods
        
        # Add noise to values (very small amount to prevent exact identification)
        noise_factor = 0.001  # 0.1% noise
        for col in anonymized.columns:
            if anonymized[col].dtype in ['float64', 'int64']:
                noise = np.random.normal(0, anonymized[col].std() * noise_factor, len(anonymized[col]))
                anonymized[col] = anonymized[col] + noise
        
        return anonymized

    def _create_combined_dataset(self, datasets_norm: Dict[int, pd.DataFrame],
                              sl_sc: List[int], tool_name: str = None) -> pd.DataFrame:
        """Create combined dataset from normalized data."""
        # Use Key Findings specific method if tool_name is provided
        if tool_name:
            return self._create_combined_dataset_key_findings(datasets_norm, sl_sc, tool_name)
        
        # Original method for other components
        combined_data = pd.DataFrame()
        
        # Get all unique dates from all datasets
        all_dates = set()
        for source_data in datasets_norm.values():
            if source_data is not None and not source_data.empty:
                all_dates.update(source_data.index)
        
        if not all_dates:
            return pd.DataFrame()
        
        # Sort dates
        all_dates = sorted(list(all_dates))
        
        # Create DataFrame with all dates
        combined_data = pd.DataFrame(index=all_dates)
        
        # Add data from each source
        from tools import tool_file_dic
        dbase_options = {}
        for tool_list in tool_file_dic.values():
            for i, source_key in enumerate([1, 2, 3, 4, 5]):
                if i < len(tool_list) and i < len(tool_list[1]):
                    dbase_options[source_key] = tool_list[i]
        
        for source_id in sl_sc:
            if source_id in datasets_norm and source_id in dbase_options:
                source_name = dbase_options[source_id]
                source_data = datasets_norm[source_id]
                
                # Reindex to match all dates
                aligned_data = source_data.reindex(all_dates)
                combined_data[source_name] = aligned_data.iloc[:, 0] if len(aligned_data.columns) > 0 else aligned_data
        
        return combined_data.dropna(how='all')  # Remove rows where all sources are NaN

    def _create_combined_dataset_key_findings(self, datasets_norm: Dict[int, pd.DataFrame],
                                          sl_sc: List[int], tool_name: str) -> pd.DataFrame:
        """Create combined dataset specifically for Key Findings with correct database mapping."""
        
        logging.info(f"🔍 Key Findings - Creating dataset for tool '{tool_name}' with sources {sl_sc}")
        
        # Map source IDs (both numeric and string) to table names and display names
        source_to_table = {
            1: ("google_trends", "Google Trends"),
            2: ("google_books", "Google Books"),
            3: ("bain_usability", "Bain Usability"),
            4: ("crossref", "Crossref"),
            5: ("bain_satisfaction", "Bain Satisfaction"),
            # Also support string IDs directly
            "google_trends": ("google_trends", "Google Trends"),
            "google_books": ("google_books", "Google Books"),
            "bain_usability": ("bain_usability", "Bain Usability"),
            "crossref": ("crossref", "Crossref"),
            "bain_satisfaction": ("bain_satisfaction", "Bain Satisfaction")
        }
        
        # Create combined dataset with proper source names
        combined_data = pd.DataFrame()
        
        # Get all unique dates from all datasets
        all_dates = set()
        for source_data in datasets_norm.values():
            if source_data is not None and not source_data.empty:
                all_dates.update(source_data.index)
        
        if not all_dates:
            logging.warning(f"⚠️ Key Findings - No dates found for tool '{tool_name}'")
            return pd.DataFrame()
        
        # Sort dates
        all_dates = sorted(list(all_dates))
        
        # Create DataFrame with all dates
        combined_data = pd.DataFrame(index=all_dates)
        
        # Add data from each source with correct names
        sources_found = []
        for source_id in sl_sc:
            # Check if source_id exists in datasets_norm (could be string or int)
            if source_id in datasets_norm and source_id in source_to_table:
                table_name, display_name = source_to_table[source_id]
                source_data = datasets_norm[source_id]
                
                # Reindex to match all dates
                aligned_data = source_data.reindex(all_dates)
                combined_data[display_name] = aligned_data.iloc[:, 0] if len(aligned_data.columns) > 0 else aligned_data
                sources_found.append(display_name)
                logging.info(f"✅ Key Findings - Added source '{display_name}' (table: {table_name}) for tool '{tool_name}'")
        
        result = combined_data.dropna(how='all')
        logging.info(f"🎉 Key Findings - Created dataset for '{tool_name}': shape {result.shape}, sources: {sources_found}")
        
        # Validate data quality
        if len(result.columns) < 2:
            logging.warning(f"⚠️ Key Findings - Only {len(result.columns)} source(s) available for '{tool_name}': {list(result.columns)}")
        
        # Check for data mismatches
        if len(result.columns) > 0 and self._is_data_mismatch(tool_name, str(result.columns[0])):
            logging.warning(f"⚠️ Key Findings - Data mismatch detected: tool '{tool_name}' -> data '{list(result.columns)[0]}'")
        
        return result

    def _is_data_mismatch(self, tool_name: str, data_source_name: str) -> bool:
        """Check if the loaded data matches the requested tool (multilingual support)."""
        
        # Common mismatch patterns in multiple languages
        tool_keywords = {
            'Capital': {
                'es': ['capital', 'inversión', 'financiamiento', 'riesgo', 'inversion'],
                'en': ['capital', 'investment', 'financing', 'risk', 'venture']
            },
            'Alianzas': {
                'es': ['alianza', 'sociedad', 'colaboración', 'asociación', 'partnership'],
                'en': ['alliance', 'partnership', 'collaboration', 'association', 'joint venture']
            },
            'Talento': {
                'es': ['talento', 'compromiso', 'empleados', 'rrhh', 'personal'],
                'en': ['talent', 'commitment', 'employees', 'hr', 'personnel']
            },
            'Calidad': {
                'es': ['calidad', 'mejora', 'excelencia', 'seis sigma', 'six sigma'],
                'en': ['quality', 'improvement', 'excellence', 'six sigma']
            },
            'Procesos': {
                'es': ['proceso', 'reingeniería', 'optimización', 'flujo', 'procesos'],
                'en': ['process', 'reengineering', 'optimization', 'flow', 'processes']
            },
            'Benchmarking': {
                'es': ['benchmark', 'comparación', 'referencia', 'benchmarking'],
                'en': ['benchmark', 'comparison', 'reference', 'benchmarking']
            },
            'Gestión': {
                'es': ['gestión', 'administración', 'manejo', 'management'],
                'en': ['management', 'administration', 'handling']
            },
            'Innovación': {
                'es': ['innovación', 'creatividad', 'nuevas ideas', 'innovación'],
                'en': ['innovation', 'creativity', 'new ideas', 'innovation']
            }
        }
        
        # Check if tool name keywords don't match data source name
        for category, lang_keywords in tool_keywords.items():
            # Check in both Spanish and English
            for lang, keywords in lang_keywords.items():
                if any(keyword.lower() in tool_name.lower() for keyword in [category.lower()] + keywords):
                    # Tool belongs to this category, check if data matches
                    if not any(keyword.lower() in data_source_name.lower() for keyword in keywords):
                        return True
        
        return False

    def _create_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Create summary of anonymized data for AI analysis."""
        if data.empty:
            return {}

        summary = {
            'shape': data.shape,
            'columns': list(data.columns),
            'date_range': {},
            'basic_statistics': {}
        }

        # Safe date range calculation with error handling
        try:
            if len(data.index) > 0:
                # Ensure index is datetime
                if not isinstance(data.index, pd.DatetimeIndex):
                    try:
                        data.index = pd.to_datetime(data.index)
                    except Exception as e:
                        logging.warning(f"Could not convert index to datetime: {e}")
                        # Use string representation as fallback
                        summary['date_range'] = {
                            'start': str(data.index.min()),
                            'end': str(data.index.max()),
                            'total_days': 0
                        }
                    else:
                        # Successfully converted to datetime
                        summary['date_range'] = {
                            'start': data.index.min().strftime('%Y-%m-%d'),
                            'end': data.index.max().strftime('%Y-%m-%d'),
                            'total_days': (data.index.max() - data.index.min()).days
                        }
                else:
                    # Already datetime index
                    summary['date_range'] = {
                        'start': data.index.min().strftime('%Y-%m-%d'),
                        'end': data.index.max().strftime('%Y-%m-%d'),
                        'total_days': (data.index.max() - data.index.min()).days
                    }
            else:
                summary['date_range'] = {
                    'start': 'N/A',
                    'end': 'N/A',
                    'total_days': 0
                }
        except Exception as e:
            logging.warning(f"Error calculating date range: {e}")
            summary['date_range'] = {
                'start': 'N/A',
                'end': 'N/A',
                'total_days': 0
            }

        # Safe basic statistics calculation
        for col in data.columns:
            try:
                col_data = data[col].dropna()
                if len(col_data) > 0:
                    summary['basic_statistics'][col] = {
                        'mean': float(col_data.mean()),
                        'std': float(col_data.std()),
                        'min': float(col_data.min()),
                        'max': float(col_data.max())
                    }
            except Exception as e:
                logging.warning(f"Error calculating statistics for column {col}: {e}")
                summary['basic_statistics'][col] = {
                    'mean': 0.0,
                    'std': 0.0,
                    'min': 0.0,
                    'max': 0.0
                }

        return summary

    def _interpret_component(self, loadings: np.ndarray, sources: List[str], component_num: int) -> str:
        """Interpret PCA component based on loadings."""
        # Find sources with highest absolute loadings
        top_indices = np.argsort(np.abs(loadings))[-3:][::-1]
        top_sources = [sources[i] for i in top_indices]
        top_loadings = [loadings[i] for i in top_indices]

        # Determine interpretation based on loading signs and magnitudes
        positive_sources = [sources[i] for i, loading in enumerate(loadings) if loading > 0.3]
        negative_sources = [sources[i] for i, loading in enumerate(loadings) if loading < -0.3]

        interpretation = f"Component {component_num} represents "

        if positive_sources and negative_sources:
            interpretation += f"a contrast between {', '.join(positive_sources)} (positive) and {', '.join(negative_sources)} (negative)"
        elif positive_sources:
            interpretation += f"strong alignment of {', '.join(positive_sources)}"
        elif negative_sources:
            interpretation += f"inverse relationship of {', '.join(negative_sources)}"
        else:
            interpretation += "a balanced combination of all sources"

        return interpretation

    def _analyze_component_detailed(self, loadings: np.ndarray, sources: List[str], component_num: int, variance_explained: float) -> Dict[str, Any]:
        """Provide detailed analysis of a PCA component with focus on loadings and source differences."""
        # Classify sources by loading magnitude
        source_contributions = []
        for i, (source, loading) in enumerate(zip(sources, loadings)):
            abs_loading = abs(loading)

            if abs_loading >= 0.6:
                contribution_level = "high"
                role = "dominant driver"
            elif abs_loading >= 0.3:
                contribution_level = "medium"
                role = "significant contributor"
            else:
                contribution_level = "low"
                role = "minor contributor"

            source_contributions.append({
                'source': source,
                'loading': float(loading),
                'abs_loading': float(abs_loading),
                'contribution_level': contribution_level,
                'role': role,
                'direction': 'positive' if loading > 0 else 'negative' if loading < 0 else 'neutral'
            })

        # Sort by absolute loading (most important first)
        source_contributions.sort(key=lambda x: x['abs_loading'], reverse=True)

        # Determine component pattern type
        positive_loadings = [loading for loading in loadings if loading > 0.3]
        negative_loadings = [loading for loading in loadings if loading < -0.3]

        if len(positive_loadings) > 1 and len(negative_loadings) > 1:
            pattern_type = "contrast_pattern"
            interpretation = f"Component {component_num} reveals contrasting patterns between different source types"
        elif len(positive_loadings) >= 2:
            pattern_type = "alignment_pattern"
            interpretation = f"Component {component_num} shows alignment and synergy between multiple sources"
        elif len(negative_loadings) >= 2:
            pattern_type = "inverse_pattern"
            interpretation = f"Component {component_num} demonstrates inverse relationships between sources"
        else:
            pattern_type = "mixed_pattern"
            interpretation = f"Component {component_num} represents a complex interaction pattern between sources"

        # Create detailed loadings analysis
        loadings_analysis = {
            'component_magnitude': float(variance_explained),
            'dominant_sources': [contrib for contrib in source_contributions if contrib['contribution_level'] == 'high'],
            'supporting_sources': [contrib for contrib in source_contributions if contrib['contribution_level'] == 'medium'],
            'minor_sources': [contrib for contrib in source_contributions if contrib['contribution_level'] == 'low'],
            'positive_contributors': [contrib for contrib in source_contributions if contrib['direction'] == 'positive'],
            'negative_contributors': [contrib for contrib in source_contributions if contrib['direction'] == 'negative']
        }

        # Generate business interpretation
        if pattern_type == "contrast_pattern":
            pos_sources = [contrib['source'] for contrib in loadings_analysis['positive_contributors']]
            neg_sources = [contrib['source'] for contrib in loadings_analysis['negative_contributors']]
            interpretation += f", where {', '.join(pos_sources)} show positive correlation while {', '.join(neg_sources)} show inverse correlation with the main pattern"
        elif pattern_type == "alignment_pattern":
            dom_sources = [contrib['source'] for contrib in loadings_analysis['dominant_sources'][:2]]
            interpretation += f", with {', '.join(dom_sources)} working in synergy to define this pattern"
        elif pattern_type == "inverse_pattern":
            neg_sources = [contrib['source'] for contrib in loadings_analysis['negative_contributors']]
            interpretation += f", characterized by inverse relationships among {', '.join(neg_sources)}"

        return {
            'interpretation': interpretation,
            'loadings_analysis': loadings_analysis,
            'source_contributions': source_contributions,
            'pattern_type': pattern_type
        }

    def _interpret_correlation_strength(self, correlation: float) -> str:
        """Interpret correlation strength."""
        abs_corr = abs(correlation)
        if abs_corr >= 0.8:
            return 'very_strong'
        elif abs_corr >= 0.6:
            return 'strong'
        elif abs_corr >= 0.4:
            return 'moderate'
        elif abs_corr >= 0.2:
            return 'weak'
        else:
            return 'very_weak'

    def _classify_trend(self, recent_trend: float, long_term_trend: float) -> str:
        """Classify trend based on recent and long-term movements."""
        if recent_trend > 0.1 and long_term_trend > 0.1:
            return 'strong_upward'
        elif recent_trend > 0.05 and long_term_trend > 0.05:
            return 'moderate_upward'
        elif recent_trend < -0.1 and long_term_trend < -0.1:
            return 'strong_downward'
        elif recent_trend < -0.05 and long_term_trend < -0.05:
            return 'moderate_downward'
        elif abs(recent_trend) < 0.05 and abs(long_term_trend) < 0.05:
            return 'stable'
        elif recent_trend * long_term_trend < 0:  # Opposite directions
            return 'reversing'
        else:
            return 'mixed'

    def _identify_overall_patterns(self, trends: Dict[str, Any]) -> List[str]:
        """Identify overall patterns across all sources."""
        patterns = []
        
        if not trends:
            return patterns
        
        # Common trend directions
        trend_directions = [trend.get('trend_direction', 'stable') for trend in trends.values()]
        upward_count = trend_directions.count('strong_upward') + trend_directions.count('moderate_upward')
        downward_count = trend_directions.count('strong_downward') + trend_directions.count('moderate_downward')
        
        if upward_count > len(trend_directions) * 0.6:
            patterns.append("Majority of sources showing upward trends")
        elif downward_count > len(trend_directions) * 0.6:
            patterns.append("Majority of sources showing downward trends")
        elif trend_directions.count('stable') > len(trend_directions) * 0.5:
            patterns.append("Most sources showing stable patterns")
        
        # Volatility patterns
        volatilities = [trend.get('volatility', 0) for trend in trends.values()]
        avg_volatility = np.mean(volatilities)
        
        if avg_volatility > np.std(volatilities) * 1.5:
            patterns.append("High volatility detected across sources")
        
        return patterns

    def _assess_overall_quality(self, data: pd.DataFrame) -> Dict[str, float]:
        """Assess overall data quality."""
        if data.empty:
            return {'score': 0, 'completeness': 0, 'consistency': 0}
        
        # Overall completeness
        total_cells = len(data) * len(data.columns)
        missing_cells = data.isna().sum().sum()
        completeness = (total_cells - missing_cells) / total_cells * 100
        
        # Overall consistency (based on outliers)
        outlier_count = 0
        for col in data.columns:
            col_data = data[col].dropna()
            if len(col_data) > 0:
                q1, q3 = col_data.quantile([0.25, 0.75])
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outlier_count += ((col_data < lower_bound) | (col_data > upper_bound)).sum()
        
        consistency = (total_cells - outlier_count) / total_cells * 100
        
        return {
            'score': (completeness + consistency) / 2,
            'completeness': float(completeness),
            'consistency': float(consistency)
        }