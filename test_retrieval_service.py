#!/usr/bin/env python3
"""
Unit Tests for KeyFindingsRetrievalService

Comprehensive testing of the retrieval service functionality including:
- Hash generation and consistency
- Source ordering and mapping
- Error handling
- Performance validation
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the database module to avoid dependency issues
sys.modules["database_implementation.precomputed_findings_db"] = Mock()
sys.modules["translations"] = Mock()

# Now import the service
from dashboard_app.key_findings.retrieval_service import KeyFindingsRetrievalService


class TestKeyFindingsRetrievalService(unittest.TestCase):
    """Test cases for KeyFindingsRetrievalService."""

    def setUp(self):
        """Set up test fixtures."""
        # Create service instance
        self.service = KeyFindingsRetrievalService()

        # Mock the database manager
        self.mock_db_manager = Mock()
        self.service.db_manager = self.mock_db_manager

        # Test data
        self.test_tool = "Calidad Total"
        self.test_sources = ["Google Trends", "Bain Usability"]
        self.test_language = "es"

        # Mock database response
        self.mock_db_response = {
            "tool_name": "Calidad Total",
            "sources_text": "Google Trends, Bain Usability",
            "language": "es",
            "executive_summary": "Test executive summary content",
            "principal_findings": "Test principal findings content",
            "temporal_analysis": "Test temporal analysis content",
            "seasonal_analysis": "Test seasonal analysis content",
            "fourier_analysis": "Test Fourier analysis content",
            "strategic_synthesis": "Test strategic synthesis content",
            "conclusions": "Test conclusions content",
            "pca_analysis": "Test PCA analysis content",
            "heatmap_analysis": "Test heatmap analysis content",
            "confidence_score": 0.85,
            "model_used": "kimi-k1",
            "data_points_analyzed": 1000,
            "analysis_type": "multi_source",
        }

    def test_service_initialization(self):
        """Test service initialization."""
        self.assertIsNotNone(self.service)
        self.assertIsNotNone(self.service.source_mapping)
        self.assertIsNotNone(self.service.database_order)
        self.assertEqual(len(self.service.source_mapping), 10)  # 5 sources × 2 formats
        self.assertEqual(len(self.service.database_order), 5)

    def test_source_mapping(self):
        """Test source ID to display name mapping."""
        # Test string IDs
        self.assertEqual(self.service.source_mapping["google_trends"], "Google Trends")
        self.assertEqual(
            self.service.source_mapping["bain_usability"], "Bain Usability"
        )

        # Test numeric IDs
        self.assertEqual(self.service.source_mapping[1], "Google Trends")
        self.assertEqual(self.service.source_mapping[3], "Bain Usability")

        # Test unknown source
        self.assertEqual(self.service.source_mapping["unknown"], "unknown")

    def test_source_ordering(self):
        """Test source ordering for database consistency."""
        # Test with sources in random order
        random_sources = ["Bain Usability", "Google Trends", "Crossref"]
        ordered = self.service._order_sources_for_database(random_sources)

        # Should match database order
        expected_order = ["Google Trends", "Bain Usability", "Crossref"]
        self.assertEqual(ordered, expected_order)

        # Test with numeric IDs
        numeric_sources = [3, 1, 4]  # Bain Usability, Google Trends, Crossref
        ordered_numeric = self.service._order_sources_for_database(numeric_sources)
        self.assertEqual(ordered_numeric, expected_order)

    def test_spanish_tool_name_conversion(self):
        """Test tool name translation to Spanish."""
        with patch(
            "dashboard_app.key_findings.retrieval_service.get_tool_name"
        ) as mock_get_tool_name:
            # Mock successful translation
            mock_get_tool_name.return_value = "Calidad Total"

            result = self.service._get_spanish_tool_name("Quality Management", "en")
            self.assertEqual(result, "Calidad Total")
            mock_get_tool_name.assert_called_once_with("Quality Management", "es")

            # Test already Spanish
            result_es = self.service._get_spanish_tool_name("Calidad Total", "es")
            self.assertEqual(result_es, "Calidad Total")

    def test_successful_retrieval(self):
        """Test successful database retrieval."""
        # Mock successful database response
        self.mock_db_manager.generate_combination_hash.return_value = "test_hash_123"
        self.mock_db_manager.get_combination_by_hash.return_value = (
            self.mock_db_response
        )

        result = self.service.retrieve_precomputed_findings(
            tool_name=self.test_tool,
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        # Verify result structure
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["data"])
        self.assertIsNone(result["error"])
        self.assertEqual(result["source"], "precomputed_findings")
        self.assertIn("response_time_ms", result)

        # Verify data content
        self.assertEqual(result["data"]["tool_name"], "Calidad Total")
        self.assertEqual(result["data"]["confidence_score"], 0.85)

        # Verify database was called
        self.mock_db_manager.generate_combination_hash.assert_called_once()
        self.mock_db_manager.get_combination_by_hash.assert_called_once_with(
            "test_hash_123"
        )

    def test_database_miss(self):
        """Test database miss scenario."""
        # Mock database miss (no results)
        self.mock_db_manager.generate_combination_hash.return_value = "test_hash_123"
        self.mock_db_manager.get_combination_by_hash.return_value = None

        result = self.service.retrieve_precomputed_findings(
            tool_name=self.test_tool,
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        # Verify error handling
        self.assertFalse(result["success"])
        self.assertIsNone(result["data"])
        self.assertIsNotNone(result["error"])
        self.assertEqual(result["source"], "database_miss")
        self.assertIn("suggestion", result)

    def test_invalid_input_handling(self):
        """Test handling of invalid inputs."""
        # Test empty tool name
        result = self.service.retrieve_precomputed_findings(
            tool_name="",
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        self.assertFalse(result["success"])
        self.assertIn("Invalid input parameters", result["error"])

        # Test empty sources
        result = self.service.retrieve_precomputed_findings(
            tool_name=self.test_tool, selected_sources=[], language=self.test_language
        )

        self.assertFalse(result["success"])
        self.assertIn("Invalid input parameters", result["error"])

    def test_performance_metrics(self):
        """Test performance metrics tracking."""
        # Mock successful retrieval
        self.mock_db_manager.generate_combination_hash.return_value = "test_hash_123"
        self.mock_db_manager.get_combination_by_hash.return_value = (
            self.mock_db_response
        )

        # Perform multiple retrievals
        for i in range(5):
            result = self.service.retrieve_precomputed_findings(
                tool_name=f"Test Tool {i}",
                selected_sources=[f"Source {i}"],
                language="es",
            )

        # Check metrics
        metrics = self.service.get_performance_metrics()
        self.assertEqual(metrics["total_requests"], 5)
        self.assertEqual(metrics["successful_retrievals"], 5)
        self.assertEqual(metrics["database_misses"], 0)
        self.assertGreater(metrics["average_response_time_ms"], 0)

    def test_combination_validation(self):
        """Test combination existence validation."""
        # Mock successful retrieval
        self.mock_db_manager.generate_combination_hash.return_value = "test_hash_123"
        self.mock_db_manager.get_combination_by_hash.return_value = (
            self.mock_db_response
        )

        result = self.service.validate_combination_exists(
            tool_name=self.test_tool,
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        self.assertTrue(result)

        # Test non-existent combination
        self.mock_db_manager.get_combination_by_hash.return_value = None

        result = self.service.validate_combination_exists(
            tool_name="Nonexistent Tool",
            selected_sources=["Nonexistent Source"],
            language=self.test_language,
        )

        self.assertFalse(result)

    def test_error_handling(self):
        """Test error handling during retrieval."""
        # Mock database error
        self.mock_db_manager.generate_combination_hash.side_effect = Exception(
            "Database error"
        )

        result = self.service.retrieve_precomputed_findings(
            tool_name=self.test_tool,
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        self.assertFalse(result["success"])
        self.assertIn("Database retrieval failed", result["error"])
        self.assertEqual(result["source"], "error")

    def test_hash_consistency(self):
        """Test that hash generation is consistent."""
        # Same inputs should produce same hash
        hash1 = self.service.db_manager.generate_combination_hash(
            tool_name=self.test_tool,
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        hash2 = self.service.db_manager.generate_combination_hash(
            tool_name=self.test_tool,
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        self.assertEqual(hash1, hash2)

        # Different inputs should produce different hashes
        hash3 = self.service.db_manager.generate_combination_hash(
            tool_name="Different Tool",
            selected_sources=self.test_sources,
            language=self.test_language,
        )

        self.assertNotEqual(hash1, hash3)


class TestKeyFindingsRetrievalServiceIntegration(unittest.TestCase):
    """Integration tests for the complete retrieval workflow."""

    def setUp(self):
        """Set up integration test fixtures."""
        self.service = KeyFindingsRetrievalService()
        self.mock_db_manager = Mock()
        self.service.db_manager = self.mock_db_manager

    def test_complete_workflow_single_source(self):
        """Test complete workflow for single-source analysis."""
        # Mock database response for single source
        single_source_response = {
            "tool_name": "Calidad Total",
            "sources_text": "Google Trends",
            "language": "es",
            "analysis_type": "single_source",
            "executive_summary": "Single source executive summary",
            "principal_findings": "Single source findings",
            "temporal_analysis": "Single source temporal analysis",
            "seasonal_analysis": "Single source seasonal analysis",
            "fourier_analysis": "Single source Fourier analysis",
            "strategic_synthesis": "Single source strategic synthesis",
            "conclusions": "Single source conclusions",
            # Multi-source sections should be empty or minimal
            "pca_analysis": "",
            "heatmap_analysis": "",
            "confidence_score": 0.82,
            "model_used": "kimi-k1",
            "data_points_analyzed": 500,
        }

        self.mock_db_manager.generate_combination_hash.return_value = (
            "single_source_hash"
        )
        self.mock_db_manager.get_combination_by_hash.return_value = (
            single_source_response
        )

        result = self.service.retrieve_precomputed_findings(
            tool_name="Calidad Total", selected_sources=["Google Trends"], language="es"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["analysis_type"], "single_source")
        # Should not have multi-source sections
        self.assertEqual(result["data"]["pca_analysis"], "")
        self.assertEqual(result["data"]["heatmap_analysis"], "")

    def test_complete_workflow_multi_source(self):
        """Test complete workflow for multi-source analysis."""
        # Mock database response for multi source
        multi_source_response = {
            "tool_name": "Benchmarking",
            "sources_text": "Google Trends, Bain Usability, Crossref",
            "language": "en",
            "analysis_type": "multi_source",
            "executive_summary": "Multi source executive summary",
            "principal_findings": "Multi source findings",
            "temporal_analysis": "Multi source temporal analysis",
            "seasonal_analysis": "Multi source seasonal analysis",
            "fourier_analysis": "Multi source Fourier analysis",
            "strategic_synthesis": "Multi source strategic synthesis",
            "conclusions": "Multi source conclusions",
            "pca_analysis": "Multi source PCA analysis",
            "heatmap_analysis": "Multi source heatmap analysis",
            "confidence_score": 0.88,
            "model_used": "kimi-k1",
            "data_points_analyzed": 1500,
        }

        self.mock_db_manager.generate_combination_hash.return_value = (
            "multi_source_hash"
        )
        self.mock_db_manager.get_combination_by_hash.return_value = (
            multi_source_response
        )

        result = self.service.retrieve_precomputed_findings(
            tool_name="Benchmarking",
            selected_sources=["Google Trends", "Bain Usability", "Crossref"],
            language="en",
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["analysis_type"], "multi_source")
        # Should have multi-source sections
        self.assertNotEqual(result["data"]["pca_analysis"], "")
        self.assertNotEqual(result["data"]["heatmap_analysis"], "")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
