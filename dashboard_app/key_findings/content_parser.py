"""
Key Findings Content Parser

Dedicated parser for transforming raw database content into structured modal format.
Ensures flawless formatting with no data corruption or parsing artifacts.
"""

import re
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class KeyFindingsContentParser:
    """
    Dedicated parser for transforming raw database content into modal-ready format.

    Provides:
    - Direct field extraction (no complex JSON parsing)
    - Language-aware section formatting
    - Zero parsing artifacts
    - Consistent content structure
    """

    def __init__(self):
        """Initialize content parser."""
        self.section_styles = {
            "title": {
                "fontSize": "1.25rem",
                "fontWeight": "600",
                "borderBottom": "2px solid #0d6efd",
                "paddingBottom": "0.5rem",
                "marginTop": "1.5rem",
                "color": "#0d6efd",
                "display": "flex",
                "alignItems": "center",
            },
            "content": {
                "fontSize": "0.95rem",
                "lineHeight": "1.6",
                "whiteSpace": "pre-line",
                "color": "#495057",
                "padding": "0.5rem 0",
                "textAlign": "justify",
            },
        }

        # Section configurations with emojis and translations
        self.section_configs = {
            "executive_summary": {
                "emoji": "📋",
                "title_en": "Executive Summary",
                "title_es": "Resumen Ejecutivo",
                "order": 1,
            },
            "principal_findings": {
                "emoji": "🔍",
                "title_en": "Principal Findings",
                "title_es": "Hallazgos Principales",
                "order": 2,
            },
            "temporal_analysis": {
                "emoji": "📈",
                "title_en": "Temporal Analysis",
                "title_es": "Análisis Temporal",
                "order": 3,
            },
            "seasonal_analysis": {
                "emoji": "📅",
                "title_en": "Seasonal Analysis",
                "title_es": "Análisis Estacional",
                "order": 4,
            },
            "fourier_analysis": {
                "emoji": "🌊",
                "title_en": "Fourier Analysis",
                "title_es": "Análisis de Fourier",
                "order": 5,
            },
            "strategic_synthesis": {
                "emoji": "🎯",
                "title_en": "Strategic Synthesis",
                "title_es": "Síntesis Estratégica",
                "order": 8,
            },
            "conclusions": {
                "emoji": "✅",
                "title_en": "Conclusions",
                "title_es": "Conclusiones",
                "order": 9,
            },
            "pca_analysis": {
                "emoji": "📊",
                "title_en": "PCA Analysis",
                "title_es": "Análisis PCA",
                "order": 7,
                "multi_source_only": True,
            },
            "heatmap_analysis": {
                "emoji": "🌡️",
                "title_en": "Heatmap Analysis",
                "title_es": "Análisis de Mapa de Calor",
                "order": 6,
                "multi_source_only": True,
            },
        }

    def parse_modal_content(
        self, raw_report_data: Dict[str, Any], language: str = "es"
    ) -> Dict[str, Any]:
        """
        Transform raw database content into structured modal content.

        Args:
            raw_report_data: Raw data from database
            language: Language code ('es' or 'en')

        Returns:
            Structured content ready for modal display
        """
        logger.info(f"📝 PARSER: Starting content parsing for {language}")

        try:
            # Validate input
            if not raw_report_data:
                return self._create_error_content("No report data provided")

            # Determine analysis type
            analysis_type = raw_report_data.get("analysis_type", "multi_source")
            selected_sources = raw_report_data.get("selected_sources", [])
            is_single_source = len(selected_sources) == 1

            logger.info(
                f"📝 PARSER: Analysis type: {analysis_type}, Sources: {len(selected_sources)}, Single source: {is_single_source}"
            )

            # Extract all sections directly from database fields
            parsed_content = {
                "metadata": {
                    "tool_name": raw_report_data.get("tool_name", ""),
                    "selected_sources": selected_sources,
                    "language": language,
                    "analysis_type": analysis_type,
                    "is_single_source": is_single_source,
                    "confidence_score": raw_report_data.get("confidence_score", 0.0),
                    "model_used": raw_report_data.get("model_used", "unknown"),
                    "data_points_analyzed": raw_report_data.get(
                        "data_points_analyzed", 0
                    ),
                    "response_time_ms": raw_report_data.get("response_time_ms", 0),
                },
                "sections": {},
            }

            # Parse core sections (always present)
            core_sections = [
                "executive_summary",
                "principal_findings",
                "temporal_analysis",
                "seasonal_analysis",
                "fourier_analysis",
                "strategic_synthesis",
                "conclusions",
            ]

            for section_name in core_sections:
                raw_content = raw_report_data.get(section_name, "")
                cleaned_content = self._clean_text_content(raw_content)

                if cleaned_content and len(cleaned_content.strip()) > 10:
                    parsed_content["sections"][section_name] = {
                        "content": cleaned_content,
                        "length": len(cleaned_content),
                        "present": True,
                    }
                    logger.info(
                        f"📝 PARSER: ✅ {section_name}: {len(cleaned_content)} chars"
                    )
                else:
                    parsed_content["sections"][section_name] = {
                        "content": f"No {section_name.replace('_', ' ')} available",
                        "length": 0,
                        "present": False,
                    }
                    logger.info(f"📝 PARSER: ⚠️ {section_name}: Missing or too short")

            # Handle multi-source only sections
            if not is_single_source:
                multi_sections = ["pca_analysis", "heatmap_analysis"]
                for section_name in multi_sections:
                    raw_content = raw_report_data.get(section_name, "")
                    cleaned_content = self._clean_text_content(raw_content)

                    if cleaned_content and len(cleaned_content.strip()) > 10:
                        parsed_content["sections"][section_name] = {
                            "content": cleaned_content,
                            "length": len(cleaned_content),
                            "present": True,
                        }
                        logger.info(
                            f"📝 PARSER: ✅ {section_name}: {len(cleaned_content)} chars (multi-source)"
                        )
                    else:
                        parsed_content["sections"][section_name] = {
                            "content": f"No {section_name.replace('_', ' ')} available",
                            "length": 0,
                            "present": False,
                        }
                        logger.info(
                            f"📝 PARSER: ⚠️ {section_name}: Missing (multi-source)"
                        )

            # Validate we have sufficient content
            present_sections = sum(
                1
                for section in parsed_content["sections"].values()
                if section["present"]
            )
            logger.info(
                f"📝 PARSER: Total present sections: {present_sections}/{len(self.section_configs)}"
            )

            if present_sections >= 6:  # Minimum for valid analysis
                logger.info("📝 PARSER: ✅ Content parsing completed successfully")
                return {"success": True, "data": parsed_content, "error": None}
            else:
                logger.warning(
                    f"📝 PARSER: ⚠️ Insufficient content: only {present_sections} sections present"
                )
                return {
                    "success": False,
                    "data": None,
                    "error": f"Insufficient content: only {present_sections} sections present (minimum 6 required)",
                }

        except Exception as e:
            logger.error(f"❌ PARSER: Error during content parsing: {e}")
            import traceback

            traceback.print_exc()

            return {
                "success": False,
                "data": None,
                "error": f"Content parsing failed: {str(e)}",
            }

    def _clean_text_content(self, content: str) -> str:
        """
        Simple text cleaning without complex parsing.
        Just removes excessive whitespace and ensures proper formatting.

        Args:
            content: Raw text content from database

        Returns:
            Cleaned text content
        """
        if not content or not isinstance(content, str):
            return ""

        # Basic cleanup
        content = content.strip()

        # Remove excessive whitespace and empty lines
        content = re.sub(
            r"\n\s*\n\s*\n", "\n\n", content
        )  # Multiple empty lines to double
        content = re.sub(r"[ \t]+", " ", content)  # Multiple spaces to single
        content = re.sub(r"\n\s*\n\s*$", "", content)  # Trailing empty lines

        # Ensure proper paragraph breaks
        content = re.sub(
            r"([.!?])\s*\n", r"\1\n\n", content
        )  # Sentence ends get paragraph break

        return content.strip()

    def _create_error_content(self, error_message: str) -> Dict[str, Any]:
        """Create error response structure."""
        return {"success": False, "data": None, "error": error_message}

    def get_section_config(self, section_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific section."""
        return self.section_configs.get(section_name)

    def get_all_sections(self, language: str = "es") -> List[Dict[str, Any]]:
        """Get all sections in display order with proper titles."""
        sections = []

        # Sort by order
        sorted_configs = sorted(
            self.section_configs.items(), key=lambda x: x[1]["order"]
        )

        for section_name, config in sorted_configs:
            title = config[f"title_{language}"]
            emoji = config["emoji"]

            sections.append(
                {"name": section_name, "title": f"{emoji} {title}", "config": config}
            )

        return sections

    def validate_content_structure(
        self, parsed_content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate that parsed content has required structure.

        Returns:
            Validation results with any issues found
        """
        validation_result = {"valid": True, "issues": [], "warnings": [], "stats": {}}

        try:
            data = parsed_content.get("data", {})
            sections = data.get("sections", {})
            metadata = data.get("metadata", {})

            # Check metadata
            required_metadata = ["tool_name", "language", "is_single_source"]
            for field in required_metadata:
                if not metadata.get(field):
                    validation_result["issues"].append(
                        f"Missing metadata field: {field}"
                    )
                    validation_result["valid"] = False

            # Check sections
            if not sections:
                validation_result["issues"].append("No sections found in content")
                validation_result["valid"] = False
            else:
                # Count present sections
                present_sections = sum(
                    1 for section in sections.values() if section.get("present", False)
                )
                validation_result["stats"]["total_sections"] = len(sections)
                validation_result["stats"]["present_sections"] = present_sections

                if present_sections < 6:
                    validation_result["warnings"].append(
                        f"Only {present_sections} sections present (minimum 6 recommended)"
                    )

                # Check individual sections
                for section_name, section_data in sections.items():
                    if section_data.get("present", False):
                        content = section_data.get("content", "")
                        length = section_data.get("length", 0)

                        if length < 10:
                            validation_result["warnings"].append(
                                f"Section '{section_name}' is very short ({length} chars)"
                            )

                        if not content or content.strip() == "":
                            validation_result["issues"].append(
                                f"Section '{section_name}' has empty content"
                            )
                            validation_result["valid"] = False

            logger.info(f"📝 PARSER VALIDATION: {validation_result['stats']}")
            if validation_result["warnings"]:
                logger.warning(
                    f"📝 PARSER VALIDATION WARNINGS: {validation_result['warnings']}"
                )
            if validation_result["issues"]:
                logger.error(
                    f"📝 PARSER VALIDATION ISSUES: {validation_result['issues']}"
                )

            return validation_result

        except Exception as e:
            logger.error(f"❌ PARSER VALIDATION: Error during validation: {e}")
            return {
                "valid": False,
                "issues": [f"Validation failed: {str(e)}"],
                "warnings": [],
                "stats": {},
            }


# Singleton instance for easy access
_parser_instance = None


def get_key_findings_content_parser() -> KeyFindingsContentParser:
    """
    Get singleton instance of KeyFindingsContentParser.

    Returns:
        KeyFindingsContentParser instance
    """
    global _parser_instance

    if _parser_instance is None:
        _parser_instance = KeyFindingsContentParser()

    return _parser_instance
