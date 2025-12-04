"""
Simplified Key Findings Service - Database-First Approach

Main service that integrates all components for AI-powered
doctoral-level analysis with direct database access and no caching layer.
"""

import asyncio
import json
import sqlite3
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date
from pathlib import Path

# Import Key Findings components
from .unified_ai_service import UnifiedAIService, get_unified_ai_service
from .data_aggregator import DataAggregator

# Import translations
try:
    from ..translations import get_text
except ImportError:
    # Fallback for standalone usage
    def get_text(key: str, language: str = "es", **kwargs) -> str:
        """Fallback translation function"""
        translations = {
            "es": {
                "section_prefix_executive_summary": "📋 RESUMEN EJECUTIVO",
                "section_prefix_principal_findings": "🔍 HALLAZGOS PRINCIPALES",
                "section_prefix_temporal_analysis": "🔍 ANÁLISIS TEMPORAL",
                "section_prefix_seasonal_analysis": "📅 PATRONES ESTACIONALES",
                "section_prefix_fourier_analysis": "🌊 ANÁLISIS ESPECTRAL",
                "section_prefix_strategic_synthesis": "🎯 SÍNTESIS ESTRATÉGICA",
                "section_prefix_conclusions": "📝 CONCLUSIONES",
            },
            "en": {
                "section_prefix_executive_summary": "📋 EXECUTIVE SUMMARY",
                "section_prefix_principal_findings": "🔍 PRINCIPAL FINDINGS",
                "section_prefix_temporal_analysis": "🔍 TEMPORAL ANALYSIS",
                "section_prefix_seasonal_analysis": "📅 SEASONAL PATTERNS",
                "section_prefix_fourier_analysis": "🌊 SPECTRAL ANALYSIS",
                "section_prefix_strategic_synthesis": "🎯 STRATEGIC SYNTHESIS",
                "section_prefix_conclusions": "📝 CONCLUSIONS",
            },
        }
        return translations.get(language, {}).get(key, key)


from .prompt_engineer import PromptEngineer
from .modal_component import KeyFindingsModal

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class KeyFindingsService:
    """
    Simplified Key Findings Service - Database-First Approach

    Integrates data aggregation, AI analysis, and direct database access
    to provide doctoral-level insights with optimal performance.
    """

    def __init__(
        self,
        db_manager,
        groq_api_key: str = None,
        openrouter_api_key: str = None,
        config: Dict[str, Any] = None,
    ):
        """
        Initialize Key Findings service.

        Args:
            db_manager: Main database manager instance
            groq_api_key: Groq API key (optional)
            openrouter_api_key: OpenRouter API key (optional)
            config: Configuration dictionary
        """
        self.db_manager = db_manager

        # Initialize Unified AI service (Groq primary, OpenRouter fallback)
        self.ai_service = get_unified_ai_service(
            groq_api_key, openrouter_api_key, config
        )

        # Initialize data aggregator
        self.data_aggregator = DataAggregator(
            db_manager, None
        )  # No cache manager needed

        # Initialize prompt engineer
        self.prompt_engineer = PromptEngineer()

        # Initialize modal component (will be set later with app instance)
        self.modal_component = None

        # Configuration
        self.config = {
            "max_retries": config.get("max_retries", 3) if config else 3,
            "enable_pca_emphasis": config.get("enable_pca_emphasis", True)
            if config
            else True,
            "confidence_threshold": config.get("confidence_threshold", 0.7)
            if config
            else 0.7,
        }

        # Performance tracking
        self.performance_metrics = {
            "total_requests": 0,
            "precomputed_hits": 0,
            "live_ai_requests": 0,
            "avg_response_time_ms": 0,
            "error_count": 0,
        }

    def set_modal_component(self, app, language_store):
        """
        Set the modal component for this service.

        Args:
            app: Dash application instance
            language_store: Language state store
        """
        self.modal_component = KeyFindingsModal(app, language_store)

    def get_modal_component(self):
        """
        Get the modal component instance.

        Returns:
            KeyFindingsModal instance or None
        """
        return self.modal_component

    async def generate_key_findings(
        self,
        tool_name: str,
        selected_sources: List[str],
        language: str = "es",
        force_refresh: bool = False,
        source_display_names: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate Key Findings analysis with direct database access.

        Args:
            tool_name: Selected management tool
            selected_sources: List of selected data source IDs (for database queries)
            language: Analysis language ('es' or 'en')
            force_refresh: Force regeneration even if cached
            source_display_names: Optional list of display names for analysis functions

        Returns:
            Dictionary containing analysis results and metadata
        """
        start_time = time.time()
        self.performance_metrics["total_requests"] += 1

        # Debug: Log function parameters at entry
        logging.info(f"🔍 generate_key_findings ENTRY:")
        logging.info(f"🔍   tool_name: {tool_name}")
        logging.info(
            f"🔍   selected_sources: {selected_sources} (type: {type(selected_sources)})"
        )
        logging.info(f"🔍   language: {language}")
        logging.info(f"🔍   force_refresh: {force_refresh}")

        try:
            # Simplified architecture: Direct query to precomputed findings database
            # No secondary cache layer - query precomputed findings directly

            # Check precomputed findings database directly (primary storage)
            precomputed_result = self._get_precomputed_findings_direct(
                tool_name, selected_sources, language
            )
            if precomputed_result:
                response_time_ms = int((time.time() - start_time) * 1000)

                # Log direct database hit
                logging.info(
                    f"Direct database hit for {tool_name} + {len(selected_sources)} sources"
                )
                self.performance_metrics["precomputed_hits"] += 1

                return {
                    "success": True,
                    "data": precomputed_result,
                    "cache_hit": True,
                    "response_time_ms": response_time_ms,
                    "source": "precomputed_findings",
                }

            # No precomputed data - generate new analysis
            logging.info(
                f"No precomputed data for {tool_name} + {len(selected_sources)} sources - generating new analysis"
            )
            self.performance_metrics["live_ai_requests"] += 1

            # Check if this is a single source analysis
            is_single_source = len(selected_sources) == 1
            if is_single_source:
                logging.info(f"🔍 BEFORE _generate_single_source_analysis call:")
                logging.info(
                    f"🔍   selected_sources: {selected_sources} (type: {type(selected_sources)})"
                )
                logging.info(
                    f"🔍   selected_sources[0]: {selected_sources[0]} (type: {type(selected_sources[0])})"
                )
                logging.info(
                    f"🔍 Single source detected: {selected_sources[0]}. Using single source workflow."
                )
                return await self._generate_single_source_analysis(
                    tool_name,
                    selected_sources,
                    language,
                    start_time,
                    source_display_names,
                )

            # Multi-source analysis path (original implementation)
            # Collect analysis data - convert display names to source IDs
            from fix_source_mapping import map_display_names_to_source_ids

            selected_source_ids = map_display_names_to_source_ids(selected_sources)

            analysis_data = self.data_aggregator.collect_analysis_data(
                tool_name, selected_source_ids, language, selected_sources
            )

            # Update analysis data with original display names for consistency
            if "error" not in analysis_data:
                analysis_data["selected_sources"] = selected_sources

            if "error" in analysis_data:
                raise Exception(f"Data collection failed: {analysis_data['error']}")

            # Generate AI analysis
            ai_result = await self._generate_ai_analysis(
                analysis_data, language, is_single_source=False
            )

            if not ai_result["success"]:
                raise Exception(
                    f"AI analysis failed: {ai_result.get('error', 'Unknown error')}"
                )

            # Prepare report data for direct return (no caching)
            content = ai_result["content"]

            # Extract PCA Analysis from appropriate field
            pca_analysis = ""
            if "pca_analysis" in content:
                pca_analysis = content["pca_analysis"]
            elif "pca_insights" in content and isinstance(
                content["pca_insights"], dict
            ):
                if "analysis" in content["pca_insights"]:
                    pca_analysis = content["pca_insights"]["analysis"]

            # OVERRIDE AI-generated values with correct system values for multi-source
            system_model_used = ai_result["model_used"]  # Actual model from system
            system_data_points = analysis_data.get(
                "data_points_used", 0
            )  # Actual data points from analysis
            system_response_time = ai_result["response_time_ms"]  # Actual response time

            logging.info(
                f"🔧 Multi-source system values - Model: {system_model_used}, Data points: {system_data_points}, Response time: {system_response_time}ms"
            )

            report_data = {
                "tool_name": tool_name,
                "selected_sources": selected_sources,
                "language": language,
                "executive_summary": content.get("executive_summary", ""),
                "principal_findings": content.get("principal_findings", ""),
                "heatmap_analysis": content.get("heatmap_analysis", ""),
                "pca_analysis": pca_analysis,
                "model_used": system_model_used,  # ✅ Use system model, NOT AI-generated
                "api_latency_ms": system_response_time,  # ✅ Use system response time
                "confidence_score": self._calculate_confidence_score(content),
                "data_points_analyzed": system_data_points,  # ✅ Use system data points, NOT AI-generated
                "sources_count": len(selected_sources),
                "analysis_depth": "comprehensive",
                "report_type": "multi_source",
                "analysis_type": "multi_source",  # Add this for modal component compatibility
                "json_structure": content.get("original_structure", "unknown"),
            }

            # Simplified architecture: Return report data directly without caching
            response_time_ms = int((time.time() - start_time) * 1000)

            logging.info(
                f"Generated new analysis for {tool_name} + {len(selected_sources)} sources in {response_time_ms}ms"
            )

            return {
                "success": True,
                "data": report_data,
                "cache_hit": False,
                "response_time_ms": response_time_ms,
                "source": "fresh_generation",
            }

        except Exception as e:
            self.performance_metrics["error_count"] += 1
            response_time_ms = int((time.time() - start_time) * 1000)

            logging.error(f"Key Findings generation failed: {e}")

            return {
                "success": False,
                "error": str(e),
                "response_time_ms": response_time_ms,
                "cache_hit": False,
            }

    async def _generate_single_source_analysis(
        self,
        tool_name: str,
        selected_sources: List[str],
        language: str,
        start_time: float,
        source_display_names: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate single source analysis with temporal, seasonal, and Fourier analysis.

        Args:
            tool_name: Selected management tool
            selected_sources: List containing a single data source ID (for database queries)
            language: Analysis language ('es' or 'en')
            start_time: Analysis start time
            source_display_names: Optional list of display names for analysis functions

        Returns:
            Dictionary containing analysis results and metadata
        """
        try:
            # Collect analysis data for single source
            from fix_source_mapping import map_display_names_to_source_ids

            selected_source_ids = map_display_names_to_source_ids(selected_sources)

            logging.info(
                f"🔍 About to call collect_analysis_data for single source with:"
            )
            logging.info(f"🔍   tool_name: {tool_name}")
            logging.info(f"🔍   selected_source_ids: {selected_source_ids}")
            logging.info(f"🔍   language: {language}")
            logging.info(f"🔍   source_display_names: {source_display_names}")

            analysis_data = self.data_aggregator.collect_analysis_data(
                tool_name, selected_source_ids, language, source_display_names
            )

            # Update analysis data with original display names for consistency
            if "error" not in analysis_data:
                analysis_data["selected_sources"] = selected_sources

            if "error" in analysis_data:
                raise Exception(f"Data collection failed: {analysis_data['error']}")

            # Extract single source insights from the analysis data
            single_source_insights = analysis_data.get("single_source_insights", {})
            logging.info(f"🔍 Single source insights: {single_source_insights}")
            if not single_source_insights:
                logging.warning("⚠️ No single_source_insights found in analysis_data")
                raise Exception(
                    "Single source analysis failed: No insights data available"
                )
            if "error" in single_source_insights:
                logging.error(
                    f"❌ Error in single_source_insights: {single_source_insights['error']}"
                )
                raise Exception(
                    f"Single source analysis failed: {single_source_insights['error']}"
                )

            # Prepare data for single source report generation
            logging.info(
                f"📊 Preparing single source data for {tool_name} with source {selected_sources[0]}"
            )

            # Extract temporal metrics
            temporal_metrics = self._extract_temporal_metrics(single_source_insights)
            logging.info(f"📈 Temporal metrics: {temporal_metrics}")

            # Extract seasonal patterns
            seasonal_patterns = self._extract_seasonal_patterns(single_source_insights)
            logging.info(f"📅 Seasonal patterns: {seasonal_patterns}")

            # Extract Fourier analysis
            fourier_analysis = self._extract_fourier_analysis(single_source_insights)
            logging.info(f"🌊 Fourier analysis: {fourier_analysis}")

            # Extract summary statistics
            summary_statistics = self._extract_summary_statistics(analysis_data)
            logging.info(f"📊 Summary statistics: {summary_statistics}")

            # Extract visualization attributes
            visualization_attributes = self._extract_visualization_attributes(
                single_source_insights
            )
            logging.info(f"📊 Visualization attributes: {visualization_attributes}")

            single_source_data = {
                "tool_name": tool_name,
                "source_name": selected_sources[0],
                "date_range_start": analysis_data.get("date_range_start", "N/A"),
                "date_range_end": analysis_data.get("date_range_end", "N/A"),
                "data_points_analyzed": analysis_data.get("data_points_analyzed", 0),
                # Extract temporal metrics
                "temporal_metrics": temporal_metrics,
                # Extract seasonal patterns
                "seasonal_patterns": seasonal_patterns,
                # Extract Fourier analysis
                "fourier_analysis": fourier_analysis,
                # Extract summary statistics
                "summary_statistics": summary_statistics,
                # Extract visualization attributes
                "visualization_attributes": visualization_attributes,
            }

            logging.info(
                f"✅ Single source data prepared: {len(single_source_data)} fields"
            )

            # Generate AI analysis using the IMPROVED prompts (same method as multi-source)
            logging.info(
                f"🤖 Using IMPROVED narrative prompts for single source analysis"
            )
            ai_result = await self._generate_ai_analysis(
                single_source_data, language, is_single_source=True
            )
            logging.info(
                f"🤖 AI service result: success={ai_result.get('success', False)}"
            )

            if not ai_result["success"]:
                error_msg = ai_result.get("error", "Unknown error")
                logging.error(f"❌ AI service failed: {error_msg}")
                raise Exception(f"Single source AI analysis failed: {error_msg}")

            # Prepare report data for direct return (no caching)
            content = ai_result["content"]
            logging.info(
                f"📝 AI content received: {list(content.keys()) if content else 'None'}"
            )

            # Build proper single-source report structure
            # For single-source, combine all analysis into principal_findings narrative
            principal_findings_content = []

            # Debug: Log what sections the AI generated
            print(f"🔍 SERVICE DEBUG: AI content sections: {list(content.keys())}")
            print(f"🔍 SERVICE DEBUG: Available sections in AI response:")
            for key, value in content.items():
                if value and key in [
                    "executive_summary",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "strategic_synthesis",
                    "conclusions",
                ]:
                    print(f"  - {key}: Present (length: {len(str(value))})")
                elif not value and key in [
                    "executive_summary",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "strategic_synthesis",
                    "conclusions",
                ]:
                    print(f"  - {key}: Missing/Empty")

            # Add executive summary if available
            if content.get("executive_summary"):
                principal_findings_content.append(
                    f"{get_text('section_prefix_executive_summary', language)}\n{content.get('executive_summary')}"
                )

            # Add temporal analysis if available
            if content.get("temporal_analysis"):
                principal_findings_content.append(
                    f"{get_text('section_prefix_temporal_analysis', language)}\n{content.get('temporal_analysis')}"
                )

            # Add seasonal analysis if available
            if content.get("seasonal_analysis"):
                principal_findings_content.append(
                    f"{get_text('section_prefix_seasonal_analysis', language)}\n{content.get('seasonal_analysis')}"
                )
            else:
                print(f"🔍 SERVICE DEBUG: seasonal_analysis section is missing!")

            # Add fourier analysis if available
            if content.get("fourier_analysis"):
                principal_findings_content.append(
                    f"{get_text('section_prefix_fourier_analysis', language)}\n{content.get('fourier_analysis')}"
                )
            else:
                print(f"🔍 SERVICE DEBUG: fourier_analysis section is missing!")

            # Add strategic synthesis if available
            if content.get("strategic_synthesis"):
                principal_findings_content.append(
                    f"{get_text('section_prefix_strategic_synthesis', language)}\n{content.get('strategic_synthesis')}"
                )

            # Add conclusions if available
            if content.get("conclusions"):
                principal_findings_content.append(
                    f"{get_text('section_prefix_conclusions', language)}\n{content.get('conclusions')}"
                )

            print(
                f"🔍 SERVICE DEBUG: Total sections combined: {len(principal_findings_content)}"
            )

            # Combine all sections into principal_findings narrative
            principal_findings_narrative = "\n\n".join(principal_findings_content)

            # Remove statistical summary section if present (this comes from AI-generated content)
            lines_to_remove = [
                "📈 Resumen Estadístico",
                "📈 Statistical Summary",
                "Resumen Estadístico",
                "Statistical Summary",
                "Datos analizados:",
                "Data analyzed:",
                "Puntos de Datos:",
                "Data Points:",
                "Rango temporal:",
                "Time range:",
                "TS:",
            ]

            filtered_lines = []
            for line in principal_findings_narrative.split("\n"):
                should_remove = False
                for remove_pattern in lines_to_remove:
                    if remove_pattern in line:
                        should_remove = True
                        break
                if not should_remove:
                    filtered_lines.append(line)

            principal_findings_narrative = "\n".join(filtered_lines)

            # Clean up any extra blank lines
            principal_findings_narrative = "\n".join(
                [
                    line
                    for line in principal_findings_narrative.split("\n")
                    if line.strip()
                ]
            )

            # For single-source, PCA and heatmap should be empty or contain placeholder
            pca_analysis_content = content.get("pca_insights", "")
            heatmap_analysis_content = content.get("heatmap_analysis", "")

            # If PCA contains placeholder text, make it empty for single-source
            if pca_analysis_content and "No PCA analysis available" in str(
                pca_analysis_content
            ):
                pca_analysis_content = ""

            # If heatmap contains placeholder text, make it empty for single-source
            if heatmap_analysis_content and "No heatmap analysis available" in str(
                heatmap_analysis_content
            ):
                heatmap_analysis_content = ""

            # Log the final single-source content structure
            pca_str = str(pca_analysis_content) if pca_analysis_content else ""
            heatmap_str = (
                str(heatmap_analysis_content) if heatmap_analysis_content else ""
            )
            logging.info(
                f"🔧 Single-source content structure - principal_findings length: {len(principal_findings_narrative)}, pca_analysis: '{pca_str[:50]}...', heatmap_analysis: '{heatmap_str[:50]}...'"
            )

            # Calculate confidence score
            confidence_score = self._calculate_confidence_score_single_source(content)
            logging.info(f"📊 Confidence score: {confidence_score}")

            # OVERRIDE AI-generated values with correct system values
            system_model_used = ai_result["model_used"]  # Actual model from system
            system_data_points = analysis_data.get(
                "data_points_used", 240
            )  # Actual data points from analysis
            system_response_time = ai_result["response_time_ms"]  # Actual response time

            logging.info(
                f"🔧 System values - Model: {system_model_used}, Data points: {system_data_points}, Response time: {system_response_time}ms"
            )

            report_data = {
                "tool_name": tool_name,
                "selected_sources": selected_sources,
                "language": language,
                "executive_summary": content.get("executive_summary", ""),
                "principal_findings": principal_findings_narrative,  # ✅ Combined narrative
                "pca_analysis": pca_analysis_content,  # ✅ Empty or placeholder for single-source
                "heatmap_analysis": heatmap_analysis_content,  # ✅ Empty or placeholder for single-source
                "temporal_analysis": "",  # ✅ Empty (moved to principal_findings)
                "seasonal_analysis": "",  # ✅ Empty (moved to principal_findings)
                "fourier_analysis": "",  # ✅ Empty (moved to principal_findings)
                "strategic_synthesis": content.get("strategic_synthesis", ""),
                "conclusions": content.get("conclusions", ""),
                "model_used": system_model_used,  # ✅ Use system model, NOT AI-generated
                "api_latency_ms": system_response_time,  # ✅ Use system response time
                "confidence_score": confidence_score,
                "data_points_analyzed": system_data_points,  # ✅ Use system data points, NOT AI-generated
                "sources_count": len(selected_sources),
                "analysis_depth": "single_source",
                "report_type": "single_source",
                "analysis_type": "single_source",  # Add this for modal component compatibility
            }

            logging.info(f"📋 Report data prepared: {len(report_data)} fields")

            # Simplified architecture: Return report data directly without caching
            response_time_ms = int((time.time() - start_time) * 1000)

            logging.info(
                f"Generated single source analysis for {tool_name} + {len(selected_sources)} sources in {response_time_ms}ms"
            )

            return {
                "success": True,
                "data": report_data,
                "cache_hit": False,
                "response_time_ms": response_time_ms,
                "source": "fresh_generation",
            }

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            logging.error(f"Single source analysis failed: {e}")

            return {
                "success": False,
                "error": str(e),
                "response_time_ms": response_time_ms,
                "cache_hit": False,
                "report_type": "single_source",
            }

    async def _generate_ai_analysis(
        self,
        analysis_data: Dict[str, Any],
        language: str,
        is_single_source: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate AI analysis using prompt engineering.

        Args:
            analysis_data: Collected analysis data
            language: Analysis language
            is_single_source: Whether this is single source analysis

        Returns:
            AI analysis result
        """
        try:
            # Update prompt engineer language
            self.prompt_engineer.language = language

            # Create comprehensive analysis prompt
            prompt = self.prompt_engineer.create_analysis_prompt(
                analysis_data,
                {
                    "analysis_type": "comprehensive",
                    "emphasis": "pca"
                    if self.config["enable_pca_emphasis"] and not is_single_source
                    else "balanced",
                },
            )

            # Generate AI analysis with single source flag
            ai_result = await self.ai_service.generate_analysis(
                prompt, language=language, is_single_source=is_single_source
            )

            return ai_result

        except Exception as e:
            logging.error(f"AI analysis generation failed: {e}")
            raise

    def _extract_temporal_metrics(
        self, single_source_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract temporal metrics from single source insights.

        Args:
            single_source_insights: Single source analysis insights

        Returns:
            Dictionary with temporal metrics
        """
        temporal_trends = single_source_insights.get("temporal_trends", {})

        if not temporal_trends or "error" in temporal_trends:
            return {
                "trend_direction": "stable",
                "trend_strength": 0.0,
                "volatility": 0.0,
                "momentum": 0.0,
                "acceleration": 0.0,
            }

        # Extract trend information
        linear_trend = temporal_trends.get("linear_trend", {})
        trend_direction = linear_trend.get("trend_direction", "stable")
        trend_strength = abs(linear_trend.get("slope", 0.0))

        # Extract volatility
        volatility = temporal_trends.get("volatility", {}).get("overall", 0.0)

        # Extract momentum (from recent vs historical comparison)
        recent_vs_historical = temporal_trends.get("recent_vs_historical", {})
        momentum = (
            recent_vs_historical.get("change_percentage", 0.0) / 100.0
        )  # Convert to decimal

        # For acceleration, we'll use the difference between recent and historical volatility
        recent_volatility = temporal_trends.get("volatility", {}).get("recent", 0.0)
        overall_volatility = temporal_trends.get("volatility", {}).get("overall", 0.0)
        acceleration = (recent_volatility - overall_volatility) / max(
            overall_volatility, 0.1
        )

        return {
            "trend_direction": trend_direction,
            "trend_strength": min(abs(trend_strength), 1.0),  # Normalize to 0-1
            "volatility": min(volatility, 1.0),  # Normalize to 0-1
            "momentum": min(abs(momentum), 1.0),  # Normalize to 0-1
            "acceleration": max(-1.0, min(acceleration, 1.0)),  # Clamp to -1 to 1
        }

    def _extract_seasonal_patterns(
        self, single_source_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract seasonal patterns from single source insights.

        Args:
            single_source_insights: Single source analysis insights

        Returns:
            Dictionary with seasonal patterns
        """
        seasonal_patterns = single_source_insights.get("seasonal_patterns", {})

        if not seasonal_patterns or "error" in seasonal_patterns:
            return {
                "seasonal_strength": 0.0,
                "peak_season": "N/A",
                "low_season": "N/A",
                "seasonal_periodicity": 12.0,
            }

        # Extract seasonal strength
        seasonality_strength = seasonal_patterns.get("seasonality_strength", {})
        seasonal_strength = seasonality_strength.get("strength_value", 0.0)

        # Extract peak and low seasons
        monthly_patterns = seasonal_patterns.get("monthly_patterns", {})
        peak_month = monthly_patterns.get("peak_month", 0)
        low_month = monthly_patterns.get("low_month", 0)

        # Convert month numbers to season names
        month_to_season = {
            12: "Q4",
            1: "Q1",
            2: "Q1",  # Winter
            3: "Q2",
            4: "Q2",
            5: "Q2",  # Spring
            6: "Q3",
            7: "Q3",
            8: "Q3",  # Summer
            9: "Q4",
            10: "Q4",
            11: "Q4",  # Fall
        }

        peak_season = month_to_season.get(peak_month, "Q1")
        low_season = month_to_season.get(low_month, "Q3")

        # Extract periodicity (default to 12 months for annual patterns)
        seasonal_periodicity = 12.0

        return {
            "seasonal_strength": min(seasonal_strength, 1.0),  # Normalize to 0-1
            "peak_season": peak_season,
            "low_season": low_season,
            "seasonal_periodicity": seasonal_periodicity,
        }

    def _extract_fourier_analysis(
        self, single_source_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract Fourier analysis from single source insights.

        Args:
            single_source_insights: Single source analysis insights

        Returns:
            Dictionary with Fourier analysis
        """
        fourier_analysis = single_source_insights.get("fourier_analysis", {})

        if not fourier_analysis or "error" in fourier_analysis:
            return {
                "dominant_frequency": 0.0,
                "dominant_period": 12.0,
                "spectral_power": {},
                "frequency_peaks": [],
            }

        # Extract dominant frequency and period
        dominant_frequencies = fourier_analysis.get("dominant_frequencies", [])
        if dominant_frequencies:
            dominant_freq = dominant_frequencies[0]
            dominant_frequency = dominant_freq.get("frequency", 0.0)
            dominant_period = dominant_freq.get("period", 12.0)
        else:
            dominant_frequency = 0.0
            dominant_period = 12.0

        # Extract spectral power
        signal_quality = fourier_analysis.get("signal_quality", {})
        spectral_power = {
            "total_power": signal_quality.get("total_power", 0.0),
            "signal_power": signal_quality.get("signal_power", 0.0),
            "noise_power": signal_quality.get("noise_power", 0.0),
        }

        # Extract frequency peaks
        frequency_peaks = []
        for freq_data in dominant_frequencies[:5]:  # Top 5 frequencies
            frequency_peaks.append(
                {
                    "frequency": freq_data.get("frequency", 0.0),
                    "period": freq_data.get("period", 0.0),
                    "power": freq_data.get("power", 0.0),
                }
            )

        return {
            "dominant_frequency": dominant_frequency,
            "dominant_period": dominant_period,
            "spectral_power": spectral_power,
            "frequency_peaks": frequency_peaks,
        }

    def _extract_summary_statistics(
        self, analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract summary statistics from analysis data.

        Args:
            analysis_data: Complete analysis data

        Returns:
            Dictionary with summary statistics
        """
        statistical_summary = analysis_data.get("statistical_summary", {})
        source_statistics = statistical_summary.get("source_statistics", {})

        # Get the first (and only) source's statistics
        if source_statistics:
            first_source_key = next(iter(source_statistics))
            stats = source_statistics[first_source_key]

            return {
                "mean": stats.get("mean", 0.0),
                "std": stats.get("std", 0.0),
                "min": stats.get("min", 0.0),
                "max": stats.get("max", 0.0),
            }

        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}

    def _extract_visualization_attributes(
        self, single_source_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract visualization attributes from single source insights.

        Args:
            single_source_insights: Single source analysis insights

        Returns:
            Dictionary with visualization attributes
        """
        seasonal_patterns = single_source_insights.get("seasonal_patterns", {})
        fourier_analysis = single_source_insights.get("fourier_analysis", {})

        # Extract peak and low months
        monthly_patterns = seasonal_patterns.get("monthly_patterns", {})
        peak_month = monthly_patterns.get("peak_month", 0)
        low_month = monthly_patterns.get("low_month", 0)

        # Convert month numbers to month names
        month_names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }

        peak_months = [month_names.get(peak_month, "January")]
        low_months = [month_names.get(low_month, "July")]

        # Extract seasonal amplitude
        monthly_means = monthly_patterns.get("monthly_means", {})
        if monthly_means:
            max_value = max(monthly_means.values()) if monthly_means else 0
            min_value = min(monthly_means.values()) if monthly_means else 0
            seasonal_amplitude = (max_value - min_value) / max(1.0, max_value)
        else:
            seasonal_amplitude = 0.0

        # Extract periodogram peaks
        dominant_frequencies = fourier_analysis.get("dominant_frequencies", [])
        periodogram_peaks = [
            freq.get("frequency", 0.0) for freq in dominant_frequencies[:5]
        ]

        # Extract significant frequencies
        significant_frequencies = [
            freq.get("frequency", 0.0)
            for freq in dominant_frequencies
            if freq.get("relative_strength", 0) > 0.1
        ]

        # Determine power spectrum shape
        signal_quality = fourier_analysis.get("signal_quality", {})
        signal_to_noise_ratio = signal_quality.get("signal_to_noise_ratio", 0.0)

        if signal_to_noise_ratio > 10:
            power_spectrum_shape = "sharp_peaks"
        elif signal_to_noise_ratio > 5:
            power_spectrum_shape = "moderate_peaks"
        elif signal_to_noise_ratio > 2:
            power_spectrum_shape = "broad_peaks"
        else:
            power_spectrum_shape = "noisy"

        return {
            "peak_months": peak_months,
            "low_months": low_months,
            "seasonal_amplitude": seasonal_amplitude,
            "periodogram_peaks": periodogram_peaks,
            "significant_frequencies": significant_frequencies,
            "power_spectrum_shape": power_spectrum_shape,
        }

    def _calculate_confidence_score_single_source(
        self, ai_content: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score for single source AI-generated content.

        Args:
            ai_content: AI-generated content for single source analysis

        Returns:
            Confidence score between 0 and 1
        """
        try:
            # Base confidence on content quality indicators
            confidence_factors = []

            # Executive summary quality
            executive_summary = ai_content.get("executive_summary", "")
            if executive_summary:
                summary_quality = min(
                    len(executive_summary) / 150, 1.0
                )  # Target 150+ chars
                confidence_factors.append(summary_quality)

            # Temporal analysis quality
            temporal_analysis = ai_content.get("temporal_analysis", "")
            if temporal_analysis:
                temporal_quality = min(
                    len(temporal_analysis) / 300, 1.0
                )  # Target 300+ chars
                confidence_factors.append(temporal_quality)

                # Check for specific temporal terms
                temporal_terms = [
                    "tendencia",
                    "volatilidad",
                    "momento",
                    "aceleración",
                    "temporal",
                ]
                temporal_count = sum(
                    1
                    for term in temporal_terms
                    if term.lower() in temporal_analysis.lower()
                )
                if temporal_count >= 2:
                    confidence_factors.append(0.8)  # Bonus for temporal language

            # Seasonal analysis quality
            seasonal_analysis = ai_content.get("seasonal_analysis", "")
            if seasonal_analysis:
                seasonal_quality = min(
                    len(seasonal_analysis) / 250, 1.0
                )  # Target 250+ chars
                confidence_factors.append(seasonal_quality)

                # Check for seasonal terms
                seasonal_terms = ["estacional", "temporada", "pico", "baja", "ciclo"]
                seasonal_count = sum(
                    1
                    for term in seasonal_terms
                    if term.lower() in seasonal_analysis.lower()
                )
                if seasonal_count >= 2:
                    confidence_factors.append(0.8)  # Bonus for seasonal language

            # Fourier analysis quality
            fourier_analysis = ai_content.get("fourier_analysis", "")
            if fourier_analysis:
                fourier_quality = min(
                    len(fourier_analysis) / 250, 1.0
                )  # Target 250+ chars
                confidence_factors.append(fourier_quality)

                # Check for Fourier terms
                fourier_terms = [
                    "frecuencia",
                    "período",
                    "espectro",
                    "fourier",
                    "armónico",
                ]
                fourier_count = sum(
                    1
                    for term in fourier_terms
                    if term.lower() in fourier_analysis.lower()
                )
                if fourier_count >= 2:
                    confidence_factors.append(0.8)  # Bonus for Fourier language

            # Calculate overall confidence
            if confidence_factors:
                return sum(confidence_factors) / len(confidence_factors)
            else:
                return 0.5  # Default confidence

        except Exception as e:
            logging.error(f"Single source confidence score calculation failed: {e}")
            return 0.5

    def _calculate_confidence_score(self, ai_content: Dict[str, Any]) -> float:
        """
        Calculate confidence score for AI-generated content.

        Args:
            ai_content: AI-generated content

        Returns:
            Confidence score between 0 and 1
        """
        try:
            # Base confidence on content quality indicators
            confidence_factors = []

            # Principal findings quality (now narrative text)
            principal_findings = ai_content.get("principal_findings", "")
            if principal_findings:
                # Check for detailed narrative content
                findings_quality = min(
                    len(principal_findings) / 500, 1.0
                )  # Target 500+ chars for narrative
                confidence_factors.append(findings_quality)

                # Check for academic language indicators
                academic_terms = [
                    "análisis",
                    "componente",
                    "varianza",
                    "carga",
                    "patrón",
                    "tendencia",
                ]
                academic_count = sum(
                    1
                    for term in academic_terms
                    if term.lower() in principal_findings.lower()
                )
                if academic_count >= 2:
                    confidence_factors.append(0.8)  # Bonus for academic language

            # PCA analysis quality (now narrative text)
            pca_analysis = ""

            # Extract PCA Analysis from appropriate field (handle both structures)
            if "pca_analysis" in ai_content:
                pca_analysis = ai_content["pca_analysis"]
            elif "pca_insights" in ai_content and isinstance(
                ai_content["pca_insights"], dict
            ):
                if "analysis" in ai_content["pca_insights"]:
                    pca_analysis = ai_content["pca_insights"]["analysis"]

            if pca_analysis:
                # Check for detailed PCA analysis
                pca_quality = min(
                    len(pca_analysis) / 400, 1.0
                )  # Target 400+ chars for PCA analysis
                confidence_factors.append(pca_quality)

                # Check for paragraph structure (should have 3 paragraphs)
                paragraph_count = len(
                    [p.strip() for p in pca_analysis.split("\n\n") if p.strip()]
                )
                if paragraph_count >= 3:
                    confidence_factors.append(
                        0.8
                    )  # Bonus for proper paragraph structure
                elif paragraph_count >= 2:
                    confidence_factors.append(
                        0.4
                    )  # Partial bonus for some paragraph structure

                # Check for specific numerical values
                import re

                numerical_values = re.findall(r"[+-]?\d+\.?\d*", pca_analysis)
                if (
                    len(numerical_values) >= 3
                ):  # Should have multiple numerical references
                    confidence_factors.append(0.7)  # Bonus for quantitative analysis

            # Executive summary quality
            executive_summary = ai_content.get("executive_summary", "")
            if executive_summary:
                # Check length and completeness
                summary_quality = min(
                    len(executive_summary) / 150, 1.0
                )  # Target 150+ chars
                confidence_factors.append(summary_quality)

            # Calculate overall confidence
            if confidence_factors:
                return sum(confidence_factors) / len(confidence_factors)
            else:
                return 0.5  # Default confidence

        except Exception as e:
            logging.error(f"Confidence score calculation failed: {e}")
            return 0.5

    def _get_precomputed_findings_direct(
        self, tool_name: str, selected_sources: list, language: str = "es"
    ):
        """Get precomputed findings directly from database - simplified approach."""
        try:
            # Convert tool name to Spanish (database stores Spanish names)
            from translations import get_tool_name

            spanish_tool_name = get_tool_name(tool_name, "es")

            # Convert source IDs to display names (database stores display names, not IDs)
            # Handle both numeric IDs and string source IDs
            source_mapping = {
                # String source IDs to display names
                "google_trends": "Google Trends",
                "google_books": "Google Books",
                "bain_usability": "Bain Usability",
                "bain_satisfaction": "Bain Satisfaction",
                "crossref": "Crossref",
                # Numeric IDs to display names
                1: "Google Trends",
                2: "Google Books",
                3: "Bain Usability",
                5: "Bain Satisfaction",
                4: "Crossref",
            }

            # Convert source IDs to display names and sort by numeric ID for consistency
            # The database stores sources in numeric ID order: 1,2,3,4,5
            source_display_pairs = []
            for source_id in selected_sources:
                display_name = source_mapping.get(source_id, str(source_id))
                # Get numeric ID for sorting (handle both int and string IDs)
                numeric_id = (
                    source_id
                    if isinstance(source_id, int)
                    else {
                        "google_trends": 1,
                        "google_books": 2,
                        "bain_usability": 3,
                        "crossref": 4,
                        "bain_satisfaction": 5,
                    }.get(source_id, 999)
                )  # Default to high number for unknown sources
                source_display_pairs.append((numeric_id, display_name))

            # Sort by numeric ID and extract display names
            source_display_pairs.sort(key=lambda x: x[0])
            display_sources = [pair[1] for pair in source_display_pairs]
            sources_text = ", ".join(display_sources)

            # Debug logging to see what we're querying
            logging.info(
                f"🔍 DEBUG: _get_precomputed_findings_direct query parameters:"
            )
            logging.info(
                f"🔍 DEBUG: tool_name='{tool_name}' -> spanish_tool_name='{spanish_tool_name}'"
            )
            logging.info(f"🔍 DEBUG: selected_sources={selected_sources}")
            logging.info(f"🔍 DEBUG: display_sources={display_sources}")
            logging.info(f"🔍 DEBUG: sources_text='{sources_text}'")
            logging.info(f"🔍 DEBUG: language='{language}'")

            db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT executive_summary, principal_findings, temporal_analysis,
                       seasonal_analysis, fourier_analysis, pca_analysis,
                       heatmap_analysis, confidence_score, model_used,
                       data_points_analyzed, analysis_type
                FROM precomputed_findings
                WHERE tool_name = ? AND sources_text = ? AND language = ?
                AND is_active = 1
                LIMIT 1
            """,
                (spanish_tool_name, sources_text, language),
            )

            result = cursor.fetchone()
            conn.close()

            # Debug logging for query results
            if result:
                logging.info(f"🔍 DEBUG: Precomputed findings FOUND!")
                logging.info(f"🔍 DEBUG: Result has {len(result)} fields")
            else:
                logging.info(f"🔍 DEBUG: No precomputed findings found for query")
                # Let's check what combinations exist for this tool
                conn_check = sqlite3.connect(db_path)
                cursor_check = conn_check.cursor()
                cursor_check.execute(
                    """
                    SELECT tool_name, sources_text, language, COUNT(*) as count
                    FROM precomputed_findings
                    WHERE tool_name = ? AND language = ? AND is_active = 1
                    GROUP BY tool_name, sources_text, language
                    ORDER BY count DESC
                    LIMIT 5
                """,
                    (spanish_tool_name, language),
                )
                available_combinations = cursor_check.fetchall()
                conn_check.close()

                if available_combinations:
                    logging.info(
                        f"🔍 DEBUG: Available combinations for {spanish_tool_name} ({language}):"
                    )
                    for combo in available_combinations:
                        logging.info(
                            f"🔍 DEBUG:   Sources: {combo[1]} (count: {combo[3]})"
                        )
                else:
                    logging.info(
                        f"🔍 DEBUG: No combinations found for {spanish_tool_name} ({language})"
                    )

            if not result:
                return None

            # Debug the actual content lengths
            logging.info(f"🔍 DEBUG: Database result field lengths:")
            logging.info(
                f"  result[0] (executive_summary): {len(str(result[0] or ''))}"
            )
            logging.info(
                f"  result[1] (principal_findings): {len(str(result[1] or ''))}"
            )
            logging.info(
                f"  result[2] (temporal_analysis): {len(str(result[2] or ''))}"
            )
            logging.info(
                f"  result[3] (seasonal_analysis): {len(str(result[3] or ''))}"
            )
            logging.info(f"  result[4] (fourier_analysis): {len(str(result[4] or ''))}")

            response_dict = {
                "tool_name": tool_name,
                "selected_sources": selected_sources,
                "language": language,
                "executive_summary": result[0] or "",
                "principal_findings": result[1] or "",
                "temporal_analysis": result[2] or "",
                "seasonal_analysis": result[3] or "",
                "fourier_analysis": result[4] or "",
                "pca_analysis": result[5] or "",
                "heatmap_analysis": result[6] or "",
                "confidence_score": result[7] or 0.8,
                "model_used": result[8] or "precomputed_database",
                "data_points_analyzed": result[9] or 0,
                "sources_count": len(selected_sources),
                "analysis_depth": result[10] or "comprehensive",
                "report_type": "precomputed",
                "is_precomputed": True,
                "sources_text": sources_text,
            }

            # Debug the response dictionary
            logging.info(f"🔍 DEBUG: Response dictionary field lengths:")
            logging.info(
                f"  executive_summary: {len(str(response_dict['executive_summary']))}"
            )
            logging.info(
                f"  principal_findings: {len(str(response_dict['principal_findings']))}"
            )
            logging.info(
                f"  temporal_analysis: {len(str(response_dict['temporal_analysis']))}"
            )
            logging.info(
                f"  seasonal_analysis: {len(str(response_dict['seasonal_analysis']))}"
            )
            logging.info(
                f"  fourier_analysis: {len(str(response_dict['fourier_analysis']))}"
            )

            return response_dict

        except Exception as e:
            logging.error(f"Failed to get precomputed findings: {e}")
            return None

    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get simplified performance metrics.

        Returns:
            Performance metrics dictionary
        """
        # Calculate precomputed hit rate
        total_requests = self.performance_metrics["total_requests"]
        precomputed_hit_rate = (
            (self.performance_metrics["precomputed_hits"] / total_requests * 100)
            if total_requests > 0
            else 0
        )

        return {
            "service_metrics": {
                "total_requests": total_requests,
                "precomputed_hits": self.performance_metrics["precomputed_hits"],
                "live_ai_requests": self.performance_metrics["live_ai_requests"],
                "precomputed_hit_rate": round(precomputed_hit_rate, 2),
                "error_count": self.performance_metrics["error_count"],
                "error_rate": round(
                    self.performance_metrics["error_count"] / total_requests * 100, 2
                )
                if total_requests > 0
                else 0,
            },
            "ai_performance": self.ai_service.get_performance_stats(),
        }

    def reset_performance_metrics(self):
        """Reset performance metrics."""
        self.performance_metrics = {
            "total_requests": 0,
            "precomputed_hits": 0,
            "live_ai_requests": 0,
            "avg_response_time_ms": 0,
            "error_count": 0,
        }
        self.ai_service.reset_performance_stats()


# Global service instance
_key_findings_service = None


def get_key_findings_service(
    db_manager,
    groq_api_key: str = None,
    openrouter_api_key: str = None,
    config: Dict[str, Any] = None,
) -> KeyFindingsService:
    """
    Get or create global Key Findings service instance.

    Args:
        db_manager: Database manager instance
        groq_api_key: Groq API key (optional)
        openrouter_api_key: OpenRouter API key (optional)
        config: Configuration dictionary (optional)

    Returns:
        Key Findings service instance
    """
    global _key_findings_service

    if _key_findings_service is None:
        _key_findings_service = KeyFindingsService(
            db_manager, groq_api_key, openrouter_api_key, config
        )

    return _key_findings_service


def reset_key_findings_service():
    """Reset global Key Findings service instance."""
    global _key_findings_service
    _key_findings_service = None
