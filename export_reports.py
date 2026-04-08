#!/usr/bin/env python3
"""Export all Key Findings reports from kf_reports_v2.db to Markdown files."""

import os
import re
import sqlite3
import unicodedata
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "kf_reports_v2.db"
OUTPUT_DIR = Path(__file__).parent / "exported_reports"

SECTION_TITLES_ES = {
    "executive_summary": "Resumen Ejecutivo",
    "temporal_2d": "Análisis Temporal 2D",
    "mean_analysis": "Análisis de Media",
    "seasonal_analysis": "Análisis Estacional",
    "fourier_analysis": "Análisis de Fourier",
    "temporal_3d": "Análisis Temporal 3D",
    "heatmap_analysis": "Análisis de Mapa de Calor",
    "regression_analysis": "Análisis de Regresión",
    "pca_analysis": "Análisis de Componentes Principales (PCA)",
    "conclusions": "Conclusiones",
}

SECTION_TITLES_EN = {
    "executive_summary": "Executive Summary",
    "temporal_2d": "Temporal 2D Analysis",
    "mean_analysis": "Mean Analysis",
    "seasonal_analysis": "Seasonal Analysis",
    "fourier_analysis": "Fourier Analysis",
    "temporal_3d": "Temporal 3D Analysis",
    "heatmap_analysis": "Heatmap Analysis",
    "regression_analysis": "Regression Analysis",
    "pca_analysis": "Principal Component Analysis (PCA)",
    "conclusions": "Conclusions",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return re.sub(r"-+", "-", text)


def build_report(
    tool: str, sources: str, analysis_type: str, sections: list[dict], lang: str
) -> str:
    titles = SECTION_TITLES_ES if lang == "es" else SECTION_TITLES_EN
    content_key = f"content_{lang}"
    tool_label = f"Herramienta: {tool}" if lang == "es" else f"Tool: {tool}"
    sources_label = "Fuentes" if lang == "es" else "Sources"
    type_label = "Tipo de análisis" if lang == "es" else "Analysis type"
    type_value = (
        "Fuente única"
        if analysis_type == "single_source" and lang == "es"
        else "Múltiples fuentes"
        if analysis_type == "multi_source" and lang == "es"
        else "Single source"
        if analysis_type == "single_source"
        else "Multi-source"
    )

    lines = [
        f"# {titles.get('executive_summary', 'Report')}",
        "",
        f"**{tool_label}**",
        "",
        f"**{sources_label}:** {sources}",
        "",
        f"**{type_label}:** {type_value}",
        "",
        "---",
        "",
    ]

    sections.sort(key=lambda s: s["section_order"])
    for sec in sections:
        heading = titles.get(sec["section_key"], sec["section_key"])
        content = sec[content_key]
        if not content or not content.strip():
            continue
        level = "#" if sec["section_key"] == "executive_summary" else "##"
        lines.append(f"{level} {heading}")
        lines.append("")
        lines.append(content.strip())
        lines.append("")

    return "\n".join(lines)


def export_all():
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    reports = conn.execute("""
        SELECT r.id, r.tool_name, r.sources_text, r.sources_count, r.analysis_type
        FROM kf_reports r
        WHERE r.is_active = 1
        ORDER BY r.tool_name, r.sources_count, r.sources_text
    """).fetchall()

    if not reports:
        print("No active reports found.")
        conn.close()
        return

    output_dir = OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    (output_dir / "es").mkdir(exist_ok=True)
    (output_dir / "en").mkdir(exist_ok=True)

    total = 0
    empty = 0

    for report in reports:
        rid = report["id"]
        tool = report["tool_name"]
        sources = report["sources_text"]
        analysis_type = report["analysis_type"]

        sections = conn.execute(
            """
            SELECT section_key, content_es, content_en, section_order
            FROM kf_report_sections
            WHERE report_id = ?
            ORDER BY section_order
        """,
            (rid,),
        ).fetchall()

        slug = f"{slugify(tool)}__{slugify(sources)}"

        for lang in ("es", "en"):
            md = build_report(tool, sources, analysis_type, sections, lang)
            if not md.strip():
                empty += 1
                continue
            folder = output_dir / lang / slugify(tool)
            folder.mkdir(parents=True, exist_ok=True)
            out_path = folder / f"{slug}.md"
            out_path.write_text(md, encoding="utf-8")
            total += 1

    conn.close()

    print(f"Exported {total} reports ({empty} skipped as empty)")
    print(f"Output: {output_dir}")
    print(f"  es/{len(list((output_dir / 'es').rglob('*.md')))} files")
    print(f"  en/{len(list((output_dir / 'en').rglob('*.md')))} files")


if __name__ == "__main__":
    export_all()
