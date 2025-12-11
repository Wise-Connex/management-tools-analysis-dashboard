#!/usr/bin/env python3
"""
Investigate why the database query is not finding the Calidad Total + 5 sources content.
"""

import sys
sys.path.insert(0, 'dashboard_app')

from database_implementation.precomputed_findings_db import get_precomputed_db_manager

def investigate_database_issue():
    """Investigate why database content is not being found."""
    
    print("🔍 INVESTIGATING DATABASE QUERY ISSUE")
    print("=" * 60)
    
    db_manager = get_precomputed_db_manager()
    
    # Check the exact query being made
    tool_name = 'Calidad Total'
    selected_sources = [1, 2, 3, 5, 4]  # From the logs
    display_sources = ['Google Trends', 'Google Books', 'Bain Usability', 'Crossref', 'Bain Satisfaction']  # From the logs
    language = 'es'
    
    print(f'Tool: {tool_name}')
    print(f'Selected sources: {selected_sources}')
    print(f'Display sources: {display_sources}')
    print(f'Language: {language}')
    
    # Check what combinations actually exist
    print('\n=== CHECKING EXISTING COMBINATIONS ===')
    all_combinations = db_manager.get_all_combinations()
    print(f'Total combinations in database: {len(all_combinations)}')
    
    # Check specifically for Calidad Total
    calidad_combinations = [combo for combo in all_combinations if combo.get('tool_name') == 'Calidad Total' and combo.get('language') == 'es']
    print(f'Calidad Total combinations found: {len(calidad_combinations)}')
    
    print('\nAll Calidad Total combinations:')
    for combo in calidad_combinations:
        print(f'  Sources: {combo.get(\"sources_text\")}')
    
    # Check the specific combination we're looking for
    target_sources_text = 'Google Trends, Google Books, Bain Usability, Crossref, Bain Satisfaction'
    target_combo = None
    for combo in calidad_combinations:
        if combo.get('sources_text') == target_sources_text:
            target_combo = combo
            break
    
    if target_combo:
        print(f'\\n✅ FOUND TARGET COMBINATION:')
        print(f'Tool: {target_combo.get(\"tool_name\")}')
        print(f'Sources: {target_combo.get(\"sources_text\")}')
        print(f'Language: {target_combo.get(\"language\")}')
        print(f'Hash: {target_combo.get(\"combination_hash\")}')
        
        # Get the full content
        full_result = db_manager.get_combination_by_hash(target_combo.get('combination_hash'))
        if full_result:
            print(f'\\n✅ CONTENT FOUND IN DATABASE!')
            print(f'Content keys: {list(full_result.keys())}')
            
            # Check section completeness
            required_sections = ['executive_summary', 'principal_findings', 'temporal_analysis', 'seasonal_analysis', 'fourier_analysis', 'pca_analysis', 'heatmap_analysis', 'strategic_synthesis', 'conclusions']
            print('\nSection analysis:')
            for section in required_sections:
                content = full_result.get(section, '')
                length = len(str(content)) if content else 0
                status = 'OK' if length > 50 else 'MISSING/SHORT'
                print(f'  {section}: {status} ({length} chars)')
        else:
            print('❌ Content not found in database')
    else:
        print('❌ Target combination not found in database')

if __name__ == "__main__":
    investigate_database_issue()