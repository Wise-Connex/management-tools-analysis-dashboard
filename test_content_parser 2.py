#!/usr/bin/env python3
"""
Unit Tests for KeyFindingsContentParser

Comprehensive testing of the content parser functionality including:
- Content cleaning and formatting
- Section structure validation
- Language support
- Error handling
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the content parser directly
from dashboard_app.key_findings.content_parser import KeyFindingsContentParser


class TestKeyFindingsContentParser(unittest.TestCase):
    """Test cases for KeyFindingsContentParser."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = KeyFindingsContentParser()

        # Test data - single source
        self.single_source_data = {
            "tool_name": "Calidad Total",
            "selected_sources": ["Google Trends"],
            "language": "es",
            "analysis_type": "single_source",
            "executive_summary": "Este es un resumen ejecutivo de prueba para Calidad Total.",
            "principal_findings": "Los hallazgos principales muestran tendencias importantes.",
            "temporal_analysis": "El análisis temporal revela patrones de adopción a lo largo del tiempo.",
            "seasonal_analysis": "Se observan patrones estacionales en la implementación.",
            "fourier_analysis": "El análisis espectral identifica ciclos de 7-8 años.",
            "strategic_synthesis": "La síntesis estratégica recomienda implementación en fases.",
            "conclusions": "En conclusión, Calidad Total muestra madurez en el mercado.",
            "confidence_score": 0.85,
            "model_used": "kimi-k1",
            "data_points_analyzed": 500,
            "response_time_ms": 50,
        }

        # Test data - multi source
        self.multi_source_data = {
            "tool_name": "Benchmarking",
            "selected_sources": ["Google Trends", "Bain Usability", "Crossref"],
            "language": "en",
            "analysis_type": "multi_source",
            "executive_summary": "This is a test executive summary for Benchmarking.",
            "principal_findings": "The principal findings show important trends across multiple sources.",
            "temporal_analysis": "The temporal analysis reveals adoption patterns over time.",
            "seasonal_analysis": "Seasonal patterns are observed in the implementation.",
            "fourier_analysis": "The spectral analysis identifies 7-8 year cycles.",
            "strategic_synthesis": "The strategic synthesis recommends phased implementation.",
            "conclusions": "In conclusion, Benchmarking shows market maturity.",
            "pca_analysis": "The PCA analysis reveals three main components explaining 85% of variance.",
            "heatmap_analysis": "The heatmap analysis shows strong correlations between sources.",
            "confidence_score": 0.88,
            "model_used": "kimi-k1",
            "data_points_analyzed": 1500,
            "response_time_ms": 75,
        }

    def test_parser_initialization(self):
        """Test parser initialization."""
        self.assertIsNotNone(self.parser)
        self.assertIsNotNone(self.parser.section_styles)
        self.assertIsNotNone(self.parser.section_configs)
        self.assertEqual(len(self.parser.section_configs), 9)  # All sections

    def test_single_source_parsing(self):
        """Test parsing of single-source analysis."""
        result = self.parser.parse_modal_content(self.single_source_data, "es")

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["data"])
        self.assertIsNone(result["error"])

        # Check metadata
        metadata = result["data"]["metadata"]
        self.assertEqual(metadata["tool_name"], "Calidad Total")
        self.assertEqual(metadata["language"], "es")
        self.assertTrue(metadata["is_single_source"])
        self.assertEqual(len(metadata["selected_sources"]), 1)

        # Check sections
        sections = result["data"]["sections"]

        # Should have all 7 core sections
        core_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

        for section in core_sections:
            self.assertIn(section, sections)
            self.assertTrue(sections[section]["present"])
            self.assertGreater(len(sections[section]["content"]), 10)

        # Should NOT have multi-source sections
        self.assertIn("pca_analysis", sections)
        self.assertIn("heatmap_analysis", sections)
        self.assertFalse(sections["pca_analysis"]["present"])
        self.assertFalse(sections["heatmap_analysis"]["present"])

    def test_multi_source_parsing(self):
        """Test parsing of multi-source analysis."""
        result = self.parser.parse_modal_content(self.multi_source_data, "en")

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["data"])
        self.assertIsNone(result["error"])

        # Check metadata
        metadata = result["data"]["metadata"]
        self.assertEqual(metadata["tool_name"], "Benchmarking")
        self.assertEqual(metadata["language"], "en")
        self.assertFalse(metadata["is_single_source"])
        self.assertEqual(len(metadata["selected_sources"]), 3)

        # Check sections
        sections = result["data"]["sections"]

        # Should have all 9 sections (7 core + 2 multi-source)
        all_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
            "pca_analysis",
            "heatmap_analysis",
        ]

        for section in all_sections:
            self.assertIn(section, sections)
            self.assertTrue(sections[section]["present"])
            self.assertGreater(len(sections[section]["content"]), 10)

    def test_content_cleaning(self):
        """Test the content cleaning functionality."""
        # Test with messy content
        messy_content = """
        This   is   a   test   with   excessive   spaces.
        
        
        
        Multiple empty lines should be cleaned.
        
        
        
        Trailing spaces and lines should be removed.   
        """

        cleaned = self.parser._clean_text_content(messy_content)

        # Should not have excessive spaces
        self.assertNotIn("   ", cleaned)
        # Should not have multiple empty lines
        self.assertNotIn("\n\n\n", cleaned)
        # Should be properly trimmed
        self.assertEqual(cleaned.strip(), cleaned)

    def test_empty_content_handling(self):
        """Test handling of empty or minimal content."""
        # Test with empty data
        empty_data = {
            "tool_name": "Test Tool",
            "selected_sources": ["Test Source"],
            "language": "es",
            "analysis_type": "single_source",
            # Missing all content fields
        }

        result = self.parser.parse_modal_content(empty_data, "es")

        self.assertFalse(result["success"])
        self.assertIsNone(result["data"])
        self.assertIn("Insufficient content", result["error"])

    def test_partial_content_handling(self):
        """Test handling of partial content (some sections missing)."""
        partial_data = {
            "tool_name": "Partial Tool",
            "selected_sources": ["Partial Source"],
            "language": "es",
            "analysis_type": "single_source",
            "executive_summary": "Only this section has content",
            "principal_findings": "And this one too",
            # Missing other sections
        }

        result = self.parser.parse_modal_content(partial_data, "es")

        # Should succeed if at least 6 sections are present
        self.assertTrue(result["success"])

        sections = result["data"]["sections"]
        present_sections = sum(1 for s in sections.values() if s.get("present", False))
        self.assertGreaterEqual(present_sections, 2)  # At least the 2 we provided

    def test_language_support(self):
        """Test language-specific section titles."""
        # Test Spanish
        result_es = self.parser.parse_modal_content(self.single_source_data, "es")
        sections_es = result_es["data"]["sections"]

        # Check Spanish titles are available
        all_sections_es = self.parser.get_all_sections("es")
        for section_config in all_sections_es:
            if (
                section_config["name"] in sections_es
                and sections_es[section_config["name"]]["present"]
            ):
                self.assertIn("Resumen Ejecutivo", section_config["title"])
                break

        # Test English
        result_en = self.parser.parse_modal_content(self.multi_source_data, "en")
        sections_en = result_en["data"]["sections"]

        # Check English titles are available
        all_sections_en = self.parser.get_all_sections("en")
        for section_config in all_sections_en:
            if (
                section_config["name"] in sections_en
                and sections_en[section_config["name"]]["present"]
            ):
                self.assertIn("Executive Summary", section_config["title"])
                break

    def test_content_validation(self):
        """Test content structure validation."""
        # Parse valid content
        result = self.parser.parse_modal_content(self.single_source_data, "es")
        self.assertTrue(result["success"])

        # Validate the parsed content
        validation_result = self.parser.validate_content_structure(result)

        self.assertTrue(validation_result["valid"])
        self.assertIn("total_sections", validation_result["stats"])
        self.assertIn("present_sections", validation_result["stats"])
        self.assertGreater(validation_result["stats"]["present_sections"], 5)

    def test_error_handling(self):
        """Test error handling during parsing."""
        # Test with None input
        result = self.parser.parse_modal_content(None, "es")

        self.assertFalse(result["success"])
        self.assertIsNone(result["data"])
        self.assertIn("No report data provided", result["error"])

        # Test with invalid data type
        result = self.parser.parse_modal_content("invalid string", "es")

        self.assertFalse(result["success"])
        self.assertIn("Content parsing failed", result["error"])

    def test_section_config_access(self):
        """Test accessing section configurations."""
        config = self.parser.get_section_config("executive_summary")

        self.assertIsNotNone(config)
        self.assertEqual(config["emoji"], "📋")
        self.assertEqual(config["title_es"], "Resumen Ejecutivo")
        self.assertEqual(config["title_en"], "Executive Summary")

    def test_all_sections_access(self):
        """Test getting all sections in order."""
        all_sections = self.parser.get_all_sections("es")

        self.assertEqual(len(all_sections), 9)

        # Check first section (executive_summary)
        first_section = all_sections[0]
        self.assertEqual(first_section["name"], "executive_summary")
        self.assertIn("📋", first_section["title"])
        self.assertIn("Resumen Ejecutivo", first_section["title"])

        # Check order is correct
        for i, section in enumerate(all_sections):
            expected_order = self.parser.section_configs[section["name"]]["order"]
            self.assertEqual(i + 1, expected_order)

    def test_performance_characteristics(self):
        """Test performance characteristics of parsing."""
        import time

        # Test parsing performance
        start_time = time.time()
        result = self.parser.parse_modal_content(self.single_source_data, "es")
        parse_time = time.time() - start_time

        self.assertTrue(result["success"])
        self.assertLess(parse_time, 0.1)  # Should be very fast (<100ms)

        print(f"Parsing performance: {parse_time * 1000:.2f}ms")


class TestKeyFindingsContentParserEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = KeyFindingsContentParser()

    def test_very_long_content(self):
        """Test handling of very long content."""
        long_content = "This is a very long content. " * 1000  # 28,000+ characters

        long_data = {
            "tool_name": "Test Tool",
            "selected_sources": ["Test Source"],
            "language": "es",
            "analysis_type": "single_source",
            "executive_summary": long_content,
            "principal_findings": "Short findings",
            "temporal_analysis": "Short temporal",
            "seasonal_analysis": "Short seasonal",
            "fourier_analysis": "Short Fourier",
            "strategic_synthesis": "Short synthesis",
            "conclusions": "Short conclusions",
        }

        result = self.parser.parse_modal_content(long_data, "es")

        self.assertTrue(result["success"])
        sections = result["data"]["sections"]
        self.assertGreater(len(sections["executive_summary"]["content"]), 25000)

    def test_special_characters(self):
        """Test handling of special characters."""
        special_content = {
            "tool_name": "Test Tool",
            "selected_sources": ["Test Source"],
            "language": "es",
            "analysis_type": "single_source",
            "executive_summary": "Test with special chars: áéíóú ñ € £ ¥ © ® ™",
            "principal_findings": "Math symbols: ∑ ∏ ∫ ∂ ∇ ≈ ≠ ≤ ≥",
            "temporal_analysis": "Punctuation: !@#$%^&*()_+-=[]{}|;':\",./<>?",
            "seasonal_analysis": "Quotes: \"double\" and 'single' quotes",
            "fourier_analysis": "Newlines:\nShould\nBe\nPreserved",
            "strategic_synthesis": "Tabs:\tShould\tBe\tCleaned",
            "conclusions": "Mixed: áéíóú\n\n\nMultiple\n\n\nlines",
        }

        result = self.parser.parse_modal_content(special_content, "es")

        self.assertTrue(result["success"])
        sections = result["data"]["sections"]

        # Check special characters are preserved
        self.assertIn("áéíóú", sections["executive_summary"]["content"])
        self.assertIn("∑ ∏ ∫", sections["principal_findings"]["content"])

        # Check excessive newlines are cleaned
        cleaned_conclusions = sections["conclusions"]["content"]
        self.assertNotIn("\n\n\n", cleaned_conclusions)

    def test_malformed_data(self):
        """Test handling of malformed data structures."""
        # Test with missing required fields
        malformed_data = {
            "tool_name": None,
            "selected_sources": None,
            "language": None,
            # Missing all content fields
        }

        result = self.parser.parse_modal_content(malformed_data, "es")

        self.assertFalse(result["success"])
        self.assertIn("No report data provided", result["error"])

    def test_content_with_markdown(self):
        """Test handling of markdown-style content."""
        markdown_content = {
            "tool_name": "Test Tool",
            "selected_sources": ["Test Source"],
            "language": "es",
            "analysis_type": "single_source",
            "executive_summary": """
# Executive Summary

This is a **bold** statement and this is *italic*.

- Bullet point 1
- Bullet point 2
- Bullet point 3

## Subsection

More content here with `code` and [links](http://example.com).
            """,
            # Other sections with similar markdown
        }

        result = self.parser.parse_modal_content(markdown_content, "es")

        self.assertTrue(result["success"])
        sections = result["data"]["sections"]

        # Check markdown elements are preserved
        content = sections["executive_summary"]["content"]
        self.assertIn("#", content)
        self.assertIn("**", content)
        self.assertIn("*", content)
        self.assertIn("-", content)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
