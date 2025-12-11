#!/usr/bin/env python3
"""
Debug script to analyze correlation heatmap data flow issues
"""
import os
import sys
import pandas as pd

# Add dashboard_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

from database import get_database_manager
from fix_source_mapping import DBASE_OPTIONS, map_display_names_to_source_ids
from utils import create_combined_dataset2, create_correlation_heatmap, create_translation_mapping, get_original_column_name

def debug_correlation_flow():
    """Debug the correlation data flow"""
    print("=== DEBUGGING CORRELATION DATA FLOW ===\n")
    
    # Initialize database
    db_manager = get_database_manager()
    
    # Test with a known keyword and multiple sources
    test_keyword = "benchmarking"
    test_sources = [1, 3, 4]  # Google Trends, Bain Usability, Crossref
    
    print(f"Test keyword: {test_keyword}")
    print(f"Test sources: {test_sources}")
    print(f"Source names: {[DBASE_OPTIONS.get(sid, 'Unknown') for sid in test_sources]}\n")
    
    # Step 1: Get raw data from database
    print("=== STEP 1: Getting data from database ===")
    datasets_norm, valid_sources = db_manager.get_data_for_keyword(test_keyword, test_sources)
    
    print(f"Valid sources: {valid_sources}")
    for source_id, df in datasets_norm.items():
        print(f"Source {source_id} ({DBASE_OPTIONS.get(source_id, 'Unknown')}):")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Index range: {df.index.min()} to {df.index.max()}")
        print(f"  Sample values: {df.head(3).values.flatten()[:3]}")
        print()
    
    # Step 2: Create combined dataset
    print("=== STEP 2: Creating combined dataset ===")
    combined_dataset = create_combined_dataset2(
        datasets_norm=datasets_norm,
        selected_sources=valid_sources,
        dbase_options=DBASE_OPTIONS
    )
    
    print(f"Combined dataset shape: {combined_dataset.shape}")
    print(f"Combined dataset columns: {list(combined_dataset.columns)}")
    print(f"Combined dataset index range: {combined_dataset.index.min()} to {combined_dataset.index.max()}")
    print("Combined dataset sample:")
    print(combined_dataset.head())
    print()
    
    # Step 3: Check data preparation for correlation
    print("=== STEP 3: Checking correlation data preparation ===")
    
    # Simulate the translation mapping
    selected_source_ids = valid_sources
    language = "es"
    translation_mapping = create_translation_mapping(selected_source_ids, language)
    
    print(f"Translation mapping: {translation_mapping}")
    
    # Get original columns for correlation
    original_columns = []
    display_sources = []
    for source_id in valid_sources:
        display_name = DBASE_OPTIONS.get(source_id, f"Source_{source_id}")
        display_sources.append(display_name)
        original_name = get_original_column_name(display_name, translation_mapping)
        if original_name in combined_dataset.columns:
            original_columns.append(original_name)
            print(f"✅ Source {source_id}: {display_name} -> {original_name}")
        else:
            print(f"❌ Source {source_id}: {display_name} -> {original_name} (NOT FOUND)")
    
    print(f"\nOriginal columns for correlation: {original_columns}")
    print(f"Display sources: {display_sources}")
    
    # Step 4: Calculate correlation matrix
    print("\n=== STEP 4: Calculating correlation matrix ===")
    if original_columns:
        corr_data = combined_dataset[original_columns].corr()
        print(f"Correlation matrix shape: {corr_data.shape}")
        print("Correlation matrix:")
        print(corr_data)
        print(f"Correlation matrix is empty: {corr_data.empty}")
        print(f"Correlation matrix is all NaN: {corr_data.isna().all().all()}")
        
        # Check for issues
        for col in original_columns:
            col_data = combined_dataset[col]
            print(f"\nColumn '{col}':")
            print(f"  Non-null count: {col_data.notna().sum()}/{len(col_data)}")
            print(f"  Unique values: {col_data.nunique()}")
            print(f"  Standard deviation: {col_data.std()}")
            if col_data.std() == 0:
                print(f"  ⚠️  WARNING: Column has zero variance (all values are the same)")
    else:
        print("❌ No original columns found for correlation")
    
    # Step 5: Try to create the heatmap
    print("\n=== STEP 5: Creating correlation heatmap ===")
    try:
        heatmap_fig = create_correlation_heatmap(combined_dataset, display_sources, language)
        print(f"✅ Heatmap created successfully")
        print(f"Heatmap has {len(heatmap_fig.data)} traces")
        if hasattr(heatmap_fig.data[0], 'z'):
            print(f"Heatmap data shape: {heatmap_fig.data[0].z.shape}")
    except Exception as e:
        print(f"❌ Error creating heatmap: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_correlation_flow()
