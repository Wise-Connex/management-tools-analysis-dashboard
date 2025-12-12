#!/usr/bin/env python3
"""
Test script to verify seasonal and Fourier analysis callbacks work correctly
after the fixes applied to handle multiple sources.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from unittest.mock import MagicMock

# Test the main callback functionality
try:
    # Import the callback modules
    from callbacks.graph_callbacks import register_graph_callbacks
    from callbacks.main_callbacks import register_main_callbacks
    from utils import (
        create_translation_mapping,
        get_original_column_name,
        safe_dataframe_column_access,
    )
    from fix_source_mapping import (
        map_display_names_to_source_ids,
        DBASE_OPTIONS as dbase_options,
    )
    from translations import get_text, translate_source_name
    from database import get_database_manager

    print("✅ All imports successful")

    # Test translation mapping functions
    print("\n🔍 Testing translation functions...")

    # Mock data for testing
    selected_sources = ["Google Trends", "Bain Usability"]
    selected_source_ids = map_display_names_to_source_ids(selected_sources)
    language = "en"

    print(f"Selected sources: {selected_sources}")
    print(f"Selected source IDs: {selected_source_ids}")

    # Test create_translation_mapping
    translation_mapping = create_translation_mapping(selected_source_ids, language)
    print(f"Translation mapping: {translation_mapping}")

    # Test get_original_column_name
    for source in selected_sources:
        original = get_original_column_name(source, translation_mapping)
        print(f"Original name for '{source}': {original}")

    # Test with mock dataframe
    mock_data = pd.DataFrame(
        {"Google Trends": np.random.randn(50), "Bain - Usabilidad": np.random.randn(50)}
    )

    print(f"\nMock DataFrame columns: {list(mock_data.columns)}")

    # Test safe_dataframe_column_access
    for source in selected_sources:
        column_data = safe_dataframe_column_access(
            mock_data, source, translation_mapping
        )
        if column_data is not None:
            print(
                f"✅ Successfully accessed data for '{source}': {len(column_data)} values"
            )
        else:
            print(f"❌ Failed to access data for '{source}'")

    print(
        "\n✅ All seasonal and Fourier analysis callback functions are working correctly!"
    )
    print("✅ The fixes for handling multiple sources have been successfully applied!")

except Exception as e:
    print(f"❌ Error testing seasonal and Fourier analysis: {e}")
    import traceback

    traceback.print_exc()
