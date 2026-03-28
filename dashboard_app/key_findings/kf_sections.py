"""
Section registry for Key Findings reports.

Defines all report sections with their properties, ordering,
minimum source requirements, and bilingual title/emoji mappings.
"""

from typing import Dict, List, Tuple

# Section definitions: key -> (order, min_sources, emoji, title_es, title_en)
SECTIONS: Dict[str, Tuple[int, int, str, str, str]] = {
    "executive_summary":  (1, 1, "\U0001f4cb", "RESUMEN EJECUTIVO", "EXECUTIVE SUMMARY"),
    "temporal_2d":        (2, 1, "\U0001f4c8", "ANALISIS TEMPORAL 2D", "2D TEMPORAL ANALYSIS"),
    "mean_analysis":      (3, 1, "\U0001f4ca", "ANALISIS DE MEDIAS", "MEAN ANALYSIS"),
    "seasonal_analysis":  (4, 1, "\U0001f4c5", "PATRONES ESTACIONALES", "SEASONAL PATTERNS"),
    "fourier_analysis":   (5, 1, "\U0001f30a", "ANALISIS ESPECTRAL (FOURIER)", "SPECTRAL ANALYSIS (FOURIER)"),
    "temporal_3d":        (6, 2, "\U0001f4c8", "ANALISIS TEMPORAL 3D", "3D TEMPORAL ANALYSIS"),
    "heatmap_analysis":   (7, 2, "\U0001f525", "MAPA DE CALOR DE CORRELACION", "CORRELATION HEATMAP"),
    "regression_analysis":(8, 2, "\U0001f4c9", "ANALISIS DE REGRESION", "REGRESSION ANALYSIS"),
    "pca_analysis":       (9, 2, "\U0001f9ec", "ANALISIS DE COMPONENTES PRINCIPALES (PCA)", "PRINCIPAL COMPONENT ANALYSIS (PCA)"),
    "conclusions":        (10, 1, "\U0001f4dd", "CONCLUSIONES", "CONCLUSIONS"),
}


def get_section_keys() -> List[str]:
    """Return all section keys in order."""
    return sorted(SECTIONS.keys(), key=lambda k: SECTIONS[k][0])


def get_applicable_sections(num_sources: int) -> List[str]:
    """Return section keys applicable for the given number of sources."""
    return [
        key for key in get_section_keys()
        if SECTIONS[key][1] <= num_sources
    ]


def get_section_title(key: str, language: str = "es") -> str:
    """Return the formatted section title with emoji for a given language."""
    if key not in SECTIONS:
        return key
    order, _, emoji, title_es, title_en = SECTIONS[key]
    title = title_es if language == "es" else title_en
    return f"{emoji} {title}"


def get_section_order(key: str) -> int:
    """Return the display order for a section."""
    return SECTIONS.get(key, (999,))[0]


def get_section_min_sources(key: str) -> int:
    """Return the minimum number of sources required for a section."""
    return SECTIONS.get(key, (0, 1))[1]
