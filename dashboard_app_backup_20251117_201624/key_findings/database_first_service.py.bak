"""
Database-First Key Findings Service (Phase 4)

This module provides database-first functionality for the Key Findings service.
It checks the precomputed findings database first before falling back to live AI.
"""

import sys
import time
import logging
from typing import Dict, List, Any, Optional

# Initialize precomputed database manager with graceful fallback
_precomputed_db_manager = None
try:
    # Add tools-dashboard root to path for imports
    sys.path.insert(0, "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard")
    from database_implementation.precomputed_findings_db import (
        get_precomputed_db_manager,
    )

    _precomputed_db_manager = get_precomputed_db_manager()
    logging.info("✅ Precomputed findings database loaded for Phase 4 integration")
except ImportError as e:
    logging.warning(f"Could not import precomputed findings database: {e}")
    _precomputed_db_manager = None
try:
    from database_implementation.precomputed_findings_db import (
        get_precomputed_db_manager,
    )

    _precomputed_db_manager = get_precomputed_db_manager()
    logging.info("✅ Precomputed findings database loaded for Phase 4 integration")
except ImportError as e:
    logging.warning(f"Could not import precomputed findings database: {e}")
    _precomputed_db_manager = None


class DatabaseFirstService:
    """
    Database-first service that checks precomputed findings before live AI.

    This provides sub-2ms query performance for cached analyses.
    """

    def __init__(self, existing_key_findings_service=None):
        """
        Initialize database-first service.

        Args:
            existing_key_findings_service: Existing KeyFindingsService instance
                                         to fall back to for live AI generation
        """
        self.precomputed_db = _precomputed_db_manager
        self.existing_service = existing_key_findings_service
        self.metrics = {
            "database_hits": 0,
            "database_misses": 0,
            "fallback_calls": 0,
            "avg_query_time_ms": 0,
        }

    def get_analysis_from_database(
        self, tool_name: str, selected_sources: List[str], language: str = "es"
    ) -> Optional[Dict[str, Any]]:
        """
        Try to get analysis from precomputed database (sub-2ms query).

        Args:
            tool_name: Management tool name
            selected_sources: List of data sources
            language: Analysis language

        Returns:
            Analysis data if found, None if not found
        """
        if not self.precomputed_db:
            return None

        try:
            start_time = time.time()

            # Generate combination hash
            combination_hash = self.precomputed_db.generate_combination_hash(
                tool_name, selected_sources, language
            )

            # Query precomputed database
            result = self.precomputed_db.get_combination_by_hash(combination_hash)

            query_time_ms = int((time.time() - start_time) * 1000)

            if result:
                self.metrics["database_hits"] += 1
                # Update average query time as integer
                hits = self.metrics["database_hits"]
                old_avg = self.metrics["avg_query_time_ms"]
                self.metrics["avg_query_time_ms"] = int(
                    (old_avg * (hits - 1) + query_time_ms) / hits
                )

                logging.info(f"✅ Database hit for {tool_name}: {query_time_ms}ms")

                # Convert database result to expected format
                return {
                    "success": True,
                    "data": {
                        "executive_summary": result.get("executive_summary", ""),
                        "principal_findings": result.get("principal_findings", ""),
                        "heatmap_analysis": result.get("heatmap_analysis", ""),
                        "pca_analysis": result.get("pca_analysis", ""),
                        "confidence_score": result.get("confidence_score", 0.8),
                        "model_used": result.get("model_used", "kimi-k2"),
                        "data_points_analyzed": result.get("data_points_analyzed", 0),
                        "sources_count": len(selected_sources),
                        "analysis_depth": "comprehensive",
                        "language": language,
                    },
                    "cache_hit": True,
                    "response_time_ms": query_time_ms,
                    "scenario_hash": combination_hash,
                    "source": "precomputed_database",
                }
            else:
                self.metrics["database_misses"] += 1
                logging.info(f"❌ Database miss for {tool_name} (not in cache)")
                return None

        except Exception as e:
            logging.error(f"Database query error: {e}")
            return None

    def get_analysis_with_fallback(
        self,
        tool_name: str,
        selected_sources: List[str],
        language: str = "es",
        force_fresh: bool = False,
    ) -> Dict[str, Any]:
        """
        Get analysis with database-first strategy, fallback to live AI if needed.

        Args:
            tool_name: Management tool name
            selected_sources: List of data sources
            language: Analysis language
            force_fresh: Force fresh analysis (skip database)

        Returns:
            Analysis result with metadata
        """
        start_time = time.time()

        # Try database first (unless forced fresh)
        if not force_fresh and self.precomputed_db:
            db_result = self.get_analysis_from_database(
                tool_name, selected_sources, language
            )
            if db_result:
                return db_result

        # Database miss or forced fresh - use existing service
        if self.existing_service:
            self.metrics["fallback_calls"] += 1
            logging.info(f"🔄 Falling back to live AI for {tool_name}")

            try:
                # Call existing service
                result = self.existing_service.generate_key_findings(
                    tool_name, selected_sources, language, force_refresh=True
                )

                total_time_ms = int((time.time() - start_time) * 1000)
                result["source"] = "live_ai"
                result["response_time_ms"] = total_time_ms

                return result

            except Exception as e:
                logging.error(f"Live AI fallback failed: {e}")
                return {
                    "success": False,
                    "error": f"Database not available and live AI failed: {e}",
                    "response_time_ms": int((time.time() - start_time) * 1000),
                    "source": "error",
                }
        else:
            return {
                "success": False,
                "error": "No database available and no fallback service configured",
                "response_time_ms": int((time.time() - start_time) * 1000),
                "source": "error",
            }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get service performance metrics."""
        total_attempts = self.metrics["database_hits"] + self.metrics["database_misses"]
        cache_hit_rate = (
            (self.metrics["database_hits"] / total_attempts * 100)
            if total_attempts > 0
            else 0
        )

        return {
            **self.metrics,
            "total_attempts": total_attempts,
            "cache_hit_rate_percent": round(cache_hit_rate, 2),
            "precomputed_db_available": self.precomputed_db is not None,
        }

    def request_regeneration(
        self,
        tool_name: str,
        selected_sources: List[str],
        language: str = "es",
        priority: int = 10,
    ) -> Optional[str]:
        """
        Request regeneration of analysis (for hidden regeneration menu).

        Args:
            tool_name: Management tool name
            selected_sources: List of data sources
            language: Analysis language
            priority: Job priority (1-10, 10 is highest)

        Returns:
            Job ID if created, None if failed
        """
        if not self.precomputed_db:
            logging.warning(
                "Cannot request regeneration: precomputed database not available"
            )
            return None

        try:
            job_id = self.precomputed_db.create_computation_job(
                tool_name, selected_sources, language, priority=priority
            )
            logging.info(f"📋 Regeneration requested: {tool_name} (job {job_id})")
            return job_id
        except Exception as e:
            logging.error(f"Regeneration request failed: {e}")
            return None


def create_database_first_service(
    existing_service=None,
) -> Optional[DatabaseFirstService]:
    """
    Create database-first service instance.

    Args:
        existing_service: Existing KeyFindingsService for fallback

    Returns:
        DatabaseFirstService instance or None if database not available
    """
    if _precomputed_db_manager is None:
        logging.warning(
            "Precomputed database not available - database-first service disabled"
        )
        return None

    return DatabaseFirstService(existing_service)
