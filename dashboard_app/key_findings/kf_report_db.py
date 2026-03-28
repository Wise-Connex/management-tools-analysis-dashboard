"""
Key Findings Report Database Manager (v2).

Language-independent, section-based storage for pre-generated
AI analysis reports. Each report stores bilingual content per section.
"""

import hashlib
import json
import os
import sqlite3
import logging
from contextlib import contextmanager
from typing import Dict, List, Optional

from .kf_sections import get_applicable_sections, get_section_title, SECTIONS

logger = logging.getLogger(__name__)

# Default DB location: <project_root>/data/kf_reports_v2.db
_DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "kf_reports_v2.db",
)


def generate_report_hash(tool_name: str, source_names: List[str]) -> str:
    """Generate a canonical hash for a tool + sources combination.

    This is the single source of truth for hash generation. Both the
    generation pipeline and the retrieval layer must use this function.
    """
    normalized = {
        "tool": tool_name.lower().strip(),
        "sources": sorted([s.lower().strip() for s in source_names]),
    }
    return hashlib.sha256(json.dumps(normalized, sort_keys=True).encode()).hexdigest()[:16]


class KFReportDB:
    """Database manager for v2 key findings reports."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or _DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_schema()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS kf_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    combination_hash TEXT UNIQUE NOT NULL,
                    tool_name TEXT NOT NULL,
                    sources_text TEXT NOT NULL,
                    sources_ids TEXT NOT NULL,
                    sources_count INTEGER NOT NULL,
                    analysis_type TEXT NOT NULL,
                    model_used TEXT,
                    generation_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS kf_report_sections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id INTEGER NOT NULL REFERENCES kf_reports(id),
                    section_key TEXT NOT NULL,
                    content_es TEXT NOT NULL DEFAULT '',
                    content_en TEXT NOT NULL DEFAULT '',
                    section_order INTEGER NOT NULL,
                    min_sources INTEGER NOT NULL DEFAULT 1,
                    UNIQUE(report_id, section_key)
                );

                CREATE INDEX IF NOT EXISTS idx_reports_hash ON kf_reports(combination_hash);
                CREATE INDEX IF NOT EXISTS idx_reports_tool ON kf_reports(tool_name);
                CREATE INDEX IF NOT EXISTS idx_sections_report ON kf_report_sections(report_id);
            """)

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def upsert_report(
        self,
        tool_name: str,
        source_names: List[str],
        source_ids: List[int],
        model_used: str = None,
    ) -> int:
        """Create or update a report record. Returns the report id."""
        combo_hash = generate_report_hash(tool_name, source_names)
        analysis_type = "single_source" if len(source_names) == 1 else "multi_source"
        sources_text = ", ".join(sorted(source_names))
        sources_ids_json = json.dumps(sorted(source_ids))

        with self._conn() as conn:
            conn.execute(
                """INSERT INTO kf_reports
                   (combination_hash, tool_name, sources_text, sources_ids,
                    sources_count, analysis_type, model_used)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(combination_hash) DO UPDATE SET
                       model_used = excluded.model_used,
                       generation_timestamp = CURRENT_TIMESTAMP,
                       is_active = 1
                """,
                (combo_hash, tool_name, sources_text, sources_ids_json,
                 len(source_names), analysis_type, model_used),
            )
            row = conn.execute(
                "SELECT id FROM kf_reports WHERE combination_hash = ?",
                (combo_hash,),
            ).fetchone()
            return row["id"]

    def upsert_section(
        self,
        report_id: int,
        section_key: str,
        content_es: str,
        content_en: str,
    ):
        """Insert or update a single section for a report."""
        section_info = SECTIONS.get(section_key)
        if not section_info:
            logger.warning(f"Unknown section key: {section_key}")
            return
        order, min_src, *_ = section_info

        with self._conn() as conn:
            conn.execute(
                """INSERT INTO kf_report_sections
                   (report_id, section_key, content_es, content_en,
                    section_order, min_sources)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(report_id, section_key) DO UPDATE SET
                       content_es = excluded.content_es,
                       content_en = excluded.content_en
                """,
                (report_id, section_key, content_es, content_en, order, min_src),
            )

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def get_report(
        self,
        tool_name: str,
        source_names: List[str],
        language: str = "es",
    ) -> Optional[Dict]:
        """Retrieve a full report with sections for the given tool + sources.

        Returns None if no report exists, otherwise a dict with:
            tool_name, sources_text, analysis_type, model_used, sections[]
        Each section: {key, title, content, order}
        """
        combo_hash = generate_report_hash(tool_name, source_names)
        num_sources = len(source_names)
        content_col = "content_es" if language == "es" else "content_en"

        with self._conn() as conn:
            report_row = conn.execute(
                """SELECT id, tool_name, sources_text, analysis_type, model_used,
                          generation_timestamp
                   FROM kf_reports
                   WHERE combination_hash = ? AND is_active = 1""",
                (combo_hash,),
            ).fetchone()

            if not report_row:
                return None

            section_rows = conn.execute(
                f"""SELECT section_key, {content_col} as content, section_order, min_sources
                    FROM kf_report_sections
                    WHERE report_id = ? AND min_sources <= ?
                    ORDER BY section_order""",
                (report_row["id"], num_sources),
            ).fetchall()

        sections = []
        for row in section_rows:
            sections.append({
                "key": row["section_key"],
                "title": get_section_title(row["section_key"], language),
                "content": row["content"],
                "order": row["section_order"],
            })

        return {
            "tool_name": report_row["tool_name"],
            "sources_text": report_row["sources_text"],
            "analysis_type": report_row["analysis_type"],
            "model_used": report_row["model_used"],
            "generated_at": report_row["generation_timestamp"],
            "sections": sections,
        }

    def has_report(self, tool_name: str, source_names: List[str]) -> bool:
        """Check if a report exists for the given combination."""
        combo_hash = generate_report_hash(tool_name, source_names)
        with self._conn() as conn:
            row = conn.execute(
                "SELECT 1 FROM kf_reports WHERE combination_hash = ? AND is_active = 1",
                (combo_hash,),
            ).fetchone()
            return row is not None

    def get_section_keys_for_report(
        self, tool_name: str, source_names: List[str]
    ) -> List[str]:
        """Return the section keys that already exist for a report."""
        combo_hash = generate_report_hash(tool_name, source_names)
        with self._conn() as conn:
            report = conn.execute(
                "SELECT id FROM kf_reports WHERE combination_hash = ? AND is_active = 1",
                (combo_hash,),
            ).fetchone()
            if not report:
                return []
            rows = conn.execute(
                "SELECT section_key FROM kf_report_sections WHERE report_id = ? AND length(content_es) > 10",
                (report["id"],),
            ).fetchall()
            return [r["section_key"] for r in rows]

    def get_stats(self) -> Dict:
        """Return summary statistics about stored reports."""
        with self._conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM kf_reports WHERE is_active = 1").fetchone()[0]
            tools = conn.execute("SELECT COUNT(DISTINCT tool_name) FROM kf_reports WHERE is_active = 1").fetchone()[0]
            sections = conn.execute("SELECT COUNT(*) FROM kf_report_sections").fetchone()[0]
            return {"total_reports": total, "unique_tools": tools, "total_sections": sections}


# Singleton
_instance: Optional[KFReportDB] = None


def get_kf_report_db(db_path: str = None) -> KFReportDB:
    """Get or create the singleton KFReportDB instance."""
    global _instance
    if _instance is None:
        _instance = KFReportDB(db_path)
    return _instance
