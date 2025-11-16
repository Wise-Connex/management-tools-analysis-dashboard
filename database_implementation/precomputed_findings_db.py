"""
Precomputed Findings Database Manager

Manages SQLite database for pre-populated key findings analyses.
Provides high-performance caching and retrieval for 1,302 combinations.
"""

import sqlite3
import json
import hashlib
from contextlib import contextmanager
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PrecomputedFindingsDBManager:
    """
    Database manager for precomputed findings with high-performance operations.

    Handles storage and retrieval of 1,302 pre-computed combinations
    with optimized queries and connection pooling.
    """

    def __init__(
        self,
        db_path: str = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db",
    ):
        """
        Initialize precomputed findings database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)

        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database schema
        self._initialize_schema()

        # Performance configuration
        self._configure_performance()

    @contextmanager
    def get_connection(self, timeout: float = 30.0):
        """
        Context manager for database connections with performance settings.

        Args:
            timeout: Connection timeout in seconds

        Yields:
            SQLite connection object with optimized settings
        """
        conn = None
        try:
            conn = sqlite3.connect(
                str(self.db_path),
                timeout=timeout,
                isolation_level=None,  # Enable autocommit mode
            )

            # Row factory for easier data access
            conn.row_factory = sqlite3.Row

            # Set performance pragmas for this connection
            self._apply_connection_settings(conn)

            yield conn

        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Database connection error: {e}")
            raise e
        finally:
            if conn:
                conn.close()

    def _configure_performance(self):
        """Apply global SQLite performance settings."""
        with self.get_connection() as conn:
            # Write-Ahead Logging for better concurrency
            conn.execute("PRAGMA journal_mode=WAL")

            # Balance between performance and safety
            conn.execute("PRAGMA synchronous=NORMAL")

            # 64MB cache for better performance
            conn.execute("PRAGMA cache_size=-64000")

            # Store temp tables in memory
            conn.execute("PRAGMA temp_store=MEMORY")

            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys=ON")

    def _apply_connection_settings(self, conn):
        """Apply performance settings to a specific connection."""
        try:
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys=ON")

            # Set cache size for this connection
            conn.execute("PRAGMA cache_size=-64000")

            # Set temp store to memory
            conn.execute("PRAGMA temp_store=MEMORY")

        except Exception as e:
            logging.warning(f"Could not apply all connection settings: {e}")

    def _initialize_schema(self):
        """Create database schema if it doesn't exist."""
        schema_path = Path(__file__).parent / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self.get_connection() as conn:
            # Execute schema creation
            try:
                conn.executescript(schema_sql)
                logging.info("Database schema initialized successfully")
            except Exception as e:
                logging.error(f"Schema initialization failed: {e}")
                raise

    def generate_combination_hash(
        self, tool_name: str, selected_sources: List[str], language: str
    ) -> str:
        """
        Generate reproducible hash for tool + sources + language combination.

        Args:
            tool_name: Management tool name (Spanish)
            selected_sources: List of source display names
            language: 'es' or 'en'

        Returns:
            Unique hash string for caching/retrieval
        """
        # Normalize inputs for consistency
        tool_name_norm = tool_name.lower().replace(" ", "_").replace("-", "_")
        source_names = sorted(
            [
                source.lower().replace(" ", "_").replace("-", "_")
                for source in selected_sources
            ]
        )

        # Create combination data
        combination_data = {
            "tool": tool_name_norm,
            "sources": source_names,
            "language": language,
        }

        # Generate consistent hash
        hash_input = json.dumps(combination_data, sort_keys=True)
        hash_hex = hashlib.md5(hash_input.encode()).hexdigest()[:10]

        return f"{tool_name_norm}_{'_'.join(source_names)}_{language}_{hash_hex}"

    def get_combination_by_hash(
        self, combination_hash: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve findings by combination hash.

        Args:
            combination_hash: Hash generated by generate_combination_hash

        Returns:
            Dictionary with findings data or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT pf.*, 
                       GROUP_CONCAT(va.file_path) as video_paths
                FROM precomputed_findings pf
                LEFT JOIN video_assets va ON pf.combination_hash = va.combination_hash AND va.active = 1
                WHERE pf.combination_hash = ? AND pf.is_active = 1
                GROUP BY pf.id
            """,
                (combination_hash,),
            )

            row = cursor.fetchone()

            if row:
                # Convert sqlite3.Row to dict
                result = dict(row)

                # Parse JSON fields - only check fields that exist
                for field in ["sources_ids", "video_info"]:
                    if result.get(field):
                        try:
                            result[field] = json.loads(result[field])
                        except json.JSONDecodeError:
                            pass  # Keep as string if JSON parsing fails

                # Update access analytics
                self._update_access_analytics(
                    combination_hash, response_time_ms=50
                )  # Fast lookup

                # Increment access count
                conn.execute(
                    """
                    UPDATE precomputed_findings 
                    SET access_count = access_count + 1, last_accessed = CURRENT_TIMESTAMP
                    WHERE combination_hash = ?
                """,
                    (combination_hash,),
                )

                return result

            return None

    def store_precomputed_analysis(
        self,
        combination_hash: str,
        tool_name: str,
        selected_sources: List[str],
        language: str,
        analysis_data: Dict[str, Any],
    ) -> int:
        """
        Store precomputed analysis result.

        Args:
            combination_hash: Generated hash for the combination
            tool_name: Management tool name
            selected_sources: List of selected source names
            language: Analysis language ('es' or 'en')
            analysis_data: Complete analysis results

        Returns:
            ID of the stored record
        """
        with self.get_connection() as conn:
            # Generate sources bitmask (5-bit binary for 5 sources)
            source_bitmask = self._generate_sources_bitmask(selected_sources)

            # Get tool ID (simplified - would need proper tool lookup)
            tool_id = self._get_tool_id(tool_name) or 1

            # Prepare analysis content
            content = {
                "executive_summary": analysis_data.get("executive_summary", ""),
                "principal_findings": analysis_data.get("principal_findings", ""),
                "temporal_analysis": analysis_data.get("temporal_analysis", ""),
                "seasonal_analysis": analysis_data.get("seasonal_analysis", ""),
                "fourier_analysis": analysis_data.get("fourier_analysis", ""),
                "pca_analysis": analysis_data.get("pca_analysis", ""),
                "heatmap_analysis": analysis_data.get("heatmap_analysis", ""),
            }

            # Insert into database
            cursor = conn.execute(
                """
                INSERT INTO precomputed_findings (
                    combination_hash, tool_id, tool_name, tool_display_name,
                    sources_text, sources_ids, sources_bitmask, sources_count,
                    language, analysis_type, executive_summary, principal_findings,
                    temporal_analysis, seasonal_analysis, fourier_analysis,
                    pca_analysis, heatmap_analysis, data_points_analyzed,
                    confidence_score, model_used, computation_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
                (
                    combination_hash,
                    tool_id,
                    tool_name,
                    analysis_data.get("tool_display_name", tool_name),
                    ", ".join(selected_sources),
                    json.dumps(self._get_source_ids(selected_sources)),
                    source_bitmask,
                    len(selected_sources),
                    language,
                    "single_source" if len(selected_sources) == 1 else "multi_source",
                    content["executive_summary"],
                    content["principal_findings"],
                    content["temporal_analysis"],
                    content["seasonal_analysis"],
                    content["fourier_analysis"],
                    content["pca_analysis"],
                    content["heatmap_analysis"],
                    analysis_data.get("data_points_analyzed", 0),
                    analysis_data.get("confidence_score", 0.0),
                    analysis_data.get("model_used", "unknown"),
                ),
            )

            return cursor.lastrowid

    def create_computation_job(
        self,
        tool_name: str,
        selected_sources: List[str],
        language: str,
        priority: int = 0,
    ) -> int:
        """
        Create a new computation job for precomputation pipeline.

        Args:
            tool_name: Management tool name
            selected_sources: List of selected source names
            language: Analysis language
            priority: Job priority (0-100, higher = more important)

        Returns:
            Job ID
        """
        tool_id = self._get_tool_id(tool_name) or 1
        sources_bitmask = self._generate_sources_bitmask(selected_sources)

        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO computation_jobs (
                    tool_id, sources_bitmask, language, priority, status, created_at
                ) VALUES (?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP)
            """,
                (tool_id, sources_bitmask, language, priority),
            )

            return cursor.lastrowid

    def get_next_pending_job(self) -> Optional[Dict[str, Any]]:
        """
        Get the next pending job from the queue.

        Returns:
            Next job data or None if no pending jobs
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT cj.*, mt.name as tool_name
                FROM computation_jobs cj
                JOIN management_tools mt ON cj.tool_id = mt.id
                WHERE cj.status = 'pending'
                ORDER BY cj.priority DESC, cj.created_at ASC
                LIMIT 1
            """)

            row = cursor.fetchone()
            return dict(row) if row else None

    def update_job_status(
        self,
        job_id: int,
        status: str,
        progress_percent: int = None,
        error_message: str = None,
    ) -> bool:
        """
        Update job status with progress and error information.

        Args:
            job_id: Job ID to update
            status: New status ('pending', 'running', 'completed', 'failed', 'retry')
            progress_percent: Progress percentage (0-100)
            error_message: Error details if status is 'failed'

        Returns:
            True if update successful
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                UPDATE computation_jobs 
                SET status = ?, 
                    progress_percent = COALESCE(?, progress_percent),
                    error_message = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (status, progress_percent, error_message, job_id),
            )

            return cursor.rowcount > 0

    def mark_job_completed(self, job_id: int) -> bool:
        """Mark a job as completed."""
        return self.update_job_status(job_id, "completed", progress_percent=100)

    def mark_job_failed(self, job_id: int, error_message: str) -> bool:
        """Mark a job as failed."""
        return self.update_job_status(job_id, "failed", error_message=error_message)

    def populate_reference_data(self):
        """Populate management_tools and data_sources tables."""

        # Management tools data from tools.py
        management_tools = [
            (
                1,
                "Alianzas y Capital de Riesgo",
                "Alianzas y Capital de Riesgo",
                "Strategic Alliances & Venture Capital",
            ),
            (2, "Benchmarking", "Benchmarking", "Benchmarking"),
            (3, "Calidad Total", "Calidad Total", "Total Quality Management"),
            (
                4,
                "Competencias Centrales",
                "Competencias Centrales",
                "Core Competencies",
            ),
            (
                5,
                "Cuadro de Mando Integral",
                "Cuadro de Mando Integral",
                "Balanced Scorecard",
            ),
            (
                6,
                "Estrategias de Crecimiento",
                "Estrategias de Crecimiento",
                "Growth Strategies",
            ),
            (
                7,
                "Experiencia del Cliente",
                "Experiencia del Cliente",
                "Customer Experience",
            ),
            (
                8,
                "Fusiones y Adquisiciones",
                "Fusiones y Adquisiciones",
                "Mergers & Acquisitions",
            ),
            (9, "Gestión de Costos", "Gestión de Costos", "Cost Management"),
            (
                10,
                "Gestión de la Cadena de Suministro",
                "Gestión de la Cadena de Suministro",
                "Supply Chain Management",
            ),
            (11, "Gestión del Cambio", "Gestión del Cambio", "Change Management"),
            (
                12,
                "Gestión del Conocimiento",
                "Gestión del Conocimiento",
                "Knowledge Management",
            ),
            (
                13,
                "Innovación Colaborativa",
                "Innovación Colaborativa",
                "Collaborative Innovation",
            ),
            (14, "Lealtad del Cliente", "Lealtad del Cliente", "Customer Loyalty"),
            (
                15,
                "Liderazgo Transformacional",
                "Liderazgo Transformacional",
                "Transformational Leadership",
            ),
            (16, "Mercadeo Digital", "Mercadeo Digital", "Digital Marketing"),
            (17, "Modelo de Negocio", "Modelo de Negocio", "Business Model"),
            (
                18,
                "Optimización de Procesos",
                "Optimización de Procesos",
                "Process Optimization",
            ),
            (
                19,
                "Reingeniería de Procesos",
                "Reingeniería de Procesos",
                "Business Process Reengineering",
            ),
            (20, "Retención de Talento", "Retención de Talento", "Talent Retention"),
            (
                21,
                "Revolución Industrial 4.0",
                "Revolución Industrial 4.0",
                "Industry 4.0",
            ),
        ]

        # Data sources
        data_sources = [
            (1, "google_trends", "Google Trends", "trends", "#FF6B35", ".csv"),
            (2, "google_books", "Google Books", "books", "#004E89", ".csv"),
            (3, "bain_usage", "Bain Usability", "usage", "#1A936F", ".csv"),
            (4, "crossref", "Crossref", "academic", "#5A189A", ".csv"),
            (
                5,
                "bain_satisfaction",
                "Bain Satisfaction",
                "satisfaction",
                "#DC2F02",
                ".csv",
            ),
        ]

        with self.get_connection() as conn:
            # Insert management tools
            conn.executemany(
                """
                INSERT OR REPLACE INTO management_tools (
                    id, name, display_name_es, display_name_en, active
                ) VALUES (?, ?, ?, ?, 1)
            """,
                management_tools,
            )

            # Insert data sources
            conn.executemany(
                """
                INSERT OR REPLACE INTO data_sources (
                    id, name, display_name, source_type, color_code, file_suffix, active
                ) VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
                data_sources,
            )

            logging.info(
                f"Populated {len(management_tools)} management tools and {len(data_sources)} data sources"
            )

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics for monitoring.

        Returns:
            Dictionary with database statistics
        """
        with self.get_connection() as conn:
            stats = {}

            # Total findings count
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM precomputed_findings WHERE is_active = 1"
            )
            stats["total_findings"] = cursor.fetchone()["count"]

            # Findings by language
            cursor = conn.execute("""
                SELECT language, COUNT(*) as count 
                FROM precomputed_findings 
                WHERE is_active = 1 
                GROUP BY language
            """)
            stats["findings_by_language"] = {
                row["language"]: row["count"] for row in cursor.fetchall()
            }

            # Findings by analysis type
            cursor = conn.execute("""
                SELECT analysis_type, COUNT(*) as count 
                FROM precomputed_findings 
                WHERE is_active = 1 
                GROUP BY analysis_type
            """)
            stats["findings_by_type"] = {
                row["analysis_type"]: row["count"] for row in cursor.fetchall()
            }

            # Job statistics
            cursor = conn.execute("""
                SELECT status, COUNT(*) as count 
                FROM computation_jobs 
                GROUP BY status
            """)
            stats["jobs_by_status"] = {
                row["status"]: row["count"] for row in cursor.fetchall()
            }

            # Most accessed findings
            cursor = conn.execute("""
                SELECT combination_hash, tool_name, access_count
                FROM precomputed_findings 
                WHERE is_active = 1 
                ORDER BY access_count DESC 
                LIMIT 10
            """)
            stats["most_accessed"] = [dict(row) for row in cursor.fetchall()]

            # Database file size
            if self.db_path.exists():
                stats["database_size_mb"] = round(
                    self.db_path.stat().st_size / 1024 / 1024, 2
                )

            return stats

    def _generate_sources_bitmask(self, selected_sources: List[str]) -> str:
        """Generate 5-bit binary mask for source selection."""
        source_mapping = {
            "google trends": "10000",
            "google books": "01000",
            "bain usability": "00100",
            "crossref": "00010",
            "bain satisfaction": "00001",
        }

        bitmask = ["0"] * 5
        for source in selected_sources:
            source_lower = source.lower()
            for i, (source_name, mask) in enumerate(source_mapping.items()):
                if source_name in source_lower:
                    bitmask[i] = "1"
                    break

        return "".join(bitmask)

    def _get_tool_id(self, tool_name: str) -> Optional[int]:
        """Get tool ID from tool name."""
        tool_name_norm = tool_name.lower().replace(" ", "_")

        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id FROM management_tools 
                WHERE LOWER(REPLACE(name, ' ', '_')) = ? OR LOWER(REPLACE(name, ' ', '_')) LIKE ?
            """,
                (tool_name_norm, f"%{tool_name_norm}%"),
            )

            row = cursor.fetchone()
            if row:
                return row["id"]

            # Default to 1 if not found
            logging.warning(f"Tool '{tool_name}' not found, using default ID 1")
            return 1

    def _get_source_ids(self, selected_sources: List[str]) -> List[int]:
        """Get source IDs from source names."""
        source_mapping = {
            "google trends": 1,
            "google books": 2,
            "bain usability": 3,
            "crossref": 4,
            "bain satisfaction": 5,
        }

        source_ids = []
        for source in selected_sources:
            source_lower = source.lower()
            for source_name, source_id in source_mapping.items():
                if source_name in source_lower:
                    source_ids.append(source_id)
                    break

        return source_ids

    def _update_access_analytics(self, combination_hash: str, response_time_ms: int):
        """Update usage analytics for access tracking."""
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO usage_analytics (
                    combination_hash, response_time_ms, found_in_cache, query_timestamp
                ) VALUES (?, ?, 1, CURRENT_TIMESTAMP)
            """,
                (combination_hash, response_time_ms),
            )


# Global database manager instance
_precomputed_db_manager = None


def get_precomputed_db_manager(db_path: str = None) -> PrecomputedFindingsDBManager:
    """
    Get or create global precomputed findings database manager instance.

    Args:
        db_path: Optional database path override

    Returns:
        PrecomputedFindingsDBManager instance
    """
    global _precomputed_db_manager

    if _precomputed_db_manager is None:
        db_path = (
            db_path
            or "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
        )
        _precomputed_db_manager = PrecomputedFindingsDBManager(db_path)

    return _precomputed_db_manager


def reset_precomputed_db_manager():
    """Reset global database manager instance."""
    global _precomputed_db_manager
    _precomputed_db_manager = None
