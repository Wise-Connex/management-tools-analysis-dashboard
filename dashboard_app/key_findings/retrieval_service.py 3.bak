"""
Key Findings Retrieval Service

Dedicated service for reliable database retrieval of precomputed findings.
Provides clean, isolated database access with comprehensive error handling.
100% database-driven with no live AI calls.
"""

import sqlite3
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class KeyFindingsRetrievalService:
    """
    Dedicated service for retrieving precomputed findings from database.

    Provides reliable database access with:
    - Consistent hash generation
    - Proper source ordering
    - Comprehensive error handling
    - Performance optimization
    """

    def __init__(self, db_manager=None):
        """
        Initialize retrieval service.

        Args:
            db_manager: PrecomputedFindingsDBManager instance (optional)
        """
        self.db_manager = db_manager
        self.performance_metrics = {
            "total_requests": 0,
            "successful_retrievals": 0,
            "database_misses": 0,
            "average_response_time_ms": 0,
        }

        # Source mapping for consistent ordering
        self.source_mapping = {
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

        # Database order for consistency (critical for hash matching)
        self.database_order = [
            "Google Trends",  # ID 1
            "Bain Usability",  # ID 3
            "Bain Satisfaction",  # ID 5
            "Crossref",  # ID 4
            "Google Books",  # ID 2
        ]

    def retrieve_precomputed_findings(
        self, tool_name: str, selected_sources: List[str], language: str = "es"
    ) -> Dict[str, Any]:
        """
        Retrieve precomputed findings from database with robust error handling.

        Args:
            tool_name: Management tool name (Spanish or English)
            selected_sources: List of selected data source names/IDs
            language: Language code ('es' or 'en')

        Returns:
            Dictionary with retrieval results:
            {
                "success": bool,
                "data": dict or None,  # Complete findings data
                "error": str or None,  # Error message if failed
                "response_time_ms": int,
                "source": "precomputed_findings" or "error"
            }
        """
        start_time = time.time()
        self.performance_metrics["total_requests"] += 1

        logger.info(
            f"🔍 RETRIEVAL_SERVICE: Starting retrieval for {tool_name} + {len(selected_sources)} sources"
        )

        try:
            # Validate inputs
            if not tool_name or not selected_sources:
                return self._create_error_result("Invalid input parameters", start_time)

            if not self.db_manager:
                # Initialize database manager if not provided
                from database_implementation.precomputed_findings_db import (
                    get_precomputed_db_manager,
                )

                self.db_manager = get_precomputed_db_manager()

            # Step 1: Convert tool name to Spanish (database stores Spanish names)
            spanish_tool_name = self._get_spanish_tool_name(tool_name, language)
            if not spanish_tool_name:
                return self._create_error_result(
                    f"Unable to translate tool name: {tool_name}", start_time
                )

            # Step 2: Convert and order sources to match database format
            ordered_sources = self._order_sources_for_database(selected_sources)
            if not ordered_sources:
                return self._create_error_result("No valid sources found", start_time)

            sources_text = ", ".join(ordered_sources)

            # Step 3: Generate combination hash for lookup
            combination_hash = self.db_manager.generate_combination_hash(
                tool_name=spanish_tool_name,
                selected_sources=ordered_sources,
                language=language,
            )

            logger.info(f"🔍 RETRIEVAL_SERVICE: Generated hash: {combination_hash}")
            logger.info(
                f"🔍 RETRIEVAL_SERVICE: Query parameters - tool: {spanish_tool_name}, sources: {sources_text}, language: {language}"
            )

            # Step 4: Query database
            db_start = time.time()
            result = self.db_manager.get_combination_by_hash(combination_hash)
            db_time = (time.time() - db_start) * 1000

            response_time_ms = int((time.time() - start_time) * 1000)

            if result:
                logger.info(
                    f"✅ RETRIEVAL_SERVICE: Found precomputed findings in {db_time:.1f}ms"
                )
                self.performance_metrics["successful_retrievals"] += 1

                # Update performance metrics
                self._update_performance_metrics(response_time_ms)

                return {
                    "success": True,
                    "data": result,
                    "error": None,
                    "response_time_ms": response_time_ms,
                    "source": "precomputed_findings",
                    "combination_hash": combination_hash,
                }
            else:
                logger.warning(
                    f"⚠️ RETRIEVAL_SERVICE: No findings found for hash: {combination_hash}"
                )
                self.performance_metrics["database_misses"] += 1

                return {
                    "success": False,
                    "data": None,
                    "error": f"No precomputed findings found for {tool_name} with {len(selected_sources)} sources in {language}",
                    "response_time_ms": response_time_ms,
                    "source": "database_miss",
                    "suggestion": "This combination may need to be precomputed using the precomputation pipeline",
                }

        except Exception as e:
            logger.error(f"❌ RETRIEVAL_SERVICE: Error during retrieval: {e}")
            import traceback

            traceback.print_exc()

            response_time_ms = int((time.time() - start_time) * 1000)

            return {
                "success": False,
                "data": None,
                "error": f"Database retrieval failed: {str(e)}",
                "response_time_ms": response_time_ms,
                "source": "error",
            }

    def _get_spanish_tool_name(self, tool_name: str, language: str) -> Optional[str]:
        """Convert tool name to Spanish for database queries."""
        try:
            from translations import get_tool_name

            # If already Spanish, return as-is
            if language == "es":
                return tool_name

            # Convert from English to Spanish
            return get_tool_name(tool_name, "es")

        except Exception as e:
            logger.error(f"❌ RETRIEVAL_SERVICE: Error translating tool name: {e}")
            return None

    def _order_sources_for_database(self, selected_sources: List[str]) -> List[str]:
        """
        Convert and order sources to match database storage format.
        Critical for hash consistency.
        """
        try:
            # Convert source IDs to display names
            display_sources = []

            for source_id in selected_sources:
                display_name = self.source_mapping.get(source_id, str(source_id))
                display_sources.append(display_name)

            # Reorder to match database storage format
            ordered_sources = []
            for source in self.database_order:
                if source in display_sources:
                    ordered_sources.append(source)

            logger.info(f"🔍 RETRIEVAL_SERVICE: Ordered sources: {ordered_sources}")
            return ordered_sources

        except Exception as e:
            logger.error(f"❌ RETRIEVAL_SERVICE: Error ordering sources: {e}")
            return display_sources  # Fallback to original order

    def _create_error_result(
        self, error_message: str, start_time: float
    ) -> Dict[str, Any]:
        """Create standardized error result."""
        response_time_ms = int((time.time() - start_time) * 1000)

        return {
            "success": False,
            "data": None,
            "error": error_message,
            "response_time_ms": response_time_ms,
            "source": "error",
        }

    def _update_performance_metrics(self, response_time_ms: int):
        """Update performance tracking metrics."""
        # Calculate running average
        total_time = self.performance_metrics["average_response_time_ms"] * (
            self.performance_metrics["successful_retrievals"] - 1
        )
        total_time += response_time_ms
        self.performance_metrics["average_response_time_ms"] = (
            total_time / self.performance_metrics["successful_retrievals"]
        )

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return self.performance_metrics.copy()

    def validate_combination_exists(
        self, tool_name: str, selected_sources: List[str], language: str
    ) -> bool:
        """
        Check if a specific combination exists in the database.
        Useful for validation before attempting retrieval.
        """
        try:
            result = self.retrieve_precomputed_findings(
                tool_name, selected_sources, language
            )
            return result["success"] and result["data"] is not None
        except Exception as e:
            logger.error(f"❌ RETRIEVAL_SERVICE: Error validating combination: {e}")
            return False


# Singleton instance for easy access
_retrieval_service_instance = None


def get_key_findings_retrieval_service(db_manager=None) -> KeyFindingsRetrievalService:
    """
    Get singleton instance of KeyFindingsRetrievalService.

    Args:
        db_manager: Optional database manager instance

    Returns:
        KeyFindingsRetrievalService instance
    """
    global _retrieval_service_instance

    if _retrieval_service_instance is None:
        _retrieval_service_instance = KeyFindingsRetrievalService(db_manager)

    return _retrieval_service_instance
