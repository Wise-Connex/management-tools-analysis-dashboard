#!/usr/bin/env python3
"""
Test script for bullet point formatting fix.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from key_findings.modal_component import KeyFindingsModal


def test_bullet_point_formatting():
    """Test the new bullet point formatting method."""

    # Create a modal instance with minimal required parameters
    # We'll mock the app and language_store since we only need the formatting method
    class MockApp:
        pass

    class MockLanguageStore:
        pass

    modal = KeyFindingsModal(MockApp(), MockLanguageStore())

    # Test data similar to what's in the database
    test_bullet_data = [
        {
            "bullet_point": "Calidad Total ha evolucionado de concepto difuso a disciplina madura",
            "reasoning": "La trayectoria temporal muestra una transición clara desde los picos de interés amplio de 2004-2008 hacia una línea base estable post-2015.",
        },
        {
            "bullet_point": "Los ciclos estacionales revelan ventanas de implementación óptimas",
            "reasoning": "El análisis espectral identifica picos consistentes durante febrero-marzo y septiembre-octubre.",
        },
        {"bullet_point": "La volatilidad decreciente indica consolidación del mercado"},
    ]

    print("=== TESTING BULLET POINT FORMATTING ===")
    print("Input data:")
    for item in test_bullet_data:
        print(f"  - {item['bullet_point']}")
        if "reasoning" in item:
            print(f"    Reasoning: {item['reasoning']}")

    print("\nFormatted output:")
    result = modal._format_bullet_points(test_bullet_data)
    print(result)

    # Test edge cases
    print("\n=== TESTING EDGE CASES ===")

    # Empty list
    print("Empty list:")
    print(f"'{modal._format_bullet_points([])}'")

    # None input
    print("None input:")
    print(f"'{modal._format_bullet_points(None)}'")

    # Invalid data - should return empty string
    print("Invalid data:")
    print(f"'{modal._format_bullet_points('not a list')}'")

    # Missing reasoning
    print("Missing reasoning:")
    incomplete_data = [{"bullet_point": "Test bullet"}]
    print(f"'{modal._format_bullet_points(incomplete_data)}'")

    print("\n=== TEST COMPLETE ===")


if __name__ == "__main__":
    test_bullet_point_formatting()
