#!/usr/bin/env python3
"""
Test script to debug single-source analysis and identify missing sections
"""
import sys
import os
import logging

# Add the dashboard_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

from key_findings.key_findings_service import KeyFindingsService
from key_findings.unified_ai_service import AIService

# Configure logging to see debug output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_single_source_debug():
    """Test single-source analysis with debug logging"""

    print("🔍 TESTING SINGLE SOURCE ANALYSIS WITH DEBUG LOGGING")
    print("=" * 60)

    # Test configuration
    test_config = {
        'tool_name': 'Alianzas y Capital de Riesgo',  # Tool in Spanish
        'source_name': 'Google Trends',  # Single source
        'language': 'es'  # Spanish
    }

    print(f"Test config: {test_config}")
    print()

    try:
        # Initialize services
        ai_service = AIService()
        key_findings_service = KeyFindingsService(ai_service)

        print("🔍 STEP 1: Calling Key Findings Service...")
        print("-" * 40)

        # Call the service - this should trigger debug logging
        result = key_findings_service.get_key_findings(
            tool_name=test_config['tool_name'],
            sources=[test_config['source_name']],
            language=test_config['language'],
            force_fresh=True  # Force fresh generation to get debug output
        )

        print(f"\n🔍 STEP 2: Analyzing results...")
        print("-" * 40)
        print(f"Result keys: {list(result.keys())}")

        if 'principal_findings' in result:
            content = result['principal_findings']
            print(f"Principal findings type: {type(content)}")
            print(f"Principal findings length: {len(str(content))}")

            # Count sections by looking for prefixes
            section_prefixes = [
                '📋 RESUMEN EJECUTIVO',
                '🔍 HALLAZGOS PRINCIPALES',
                '🔍 ANÁLISIS TEMPORAL',
                '📅 PATRONES ESTACIONALES',
                '🌊 ANÁLISIS ESPECTRAL',
                '🎯 SÍNTESIS ESTRATÉGICA',
                '📝 CONCLUSIONES'
            ]

            print(f"\n🔍 STEP 3: Section analysis...")
            print("-" * 40)

            content_str = str(content)
            found_sections = []
            missing_sections = []

            for prefix in section_prefixes:
                if prefix in content_str:
                    found_sections.append(prefix)
                    print(f"✅ Found: {prefix}")
                else:
                    missing_sections.append(prefix)
                    print(f"❌ Missing: {prefix}")

            print(f"\n🔍 SUMMARY:")
            print(f"Found sections: {len(found_sections)}")
            print(f"Missing sections: {len(missing_sections)}")
            print(f"Total expected: {len(section_prefixes)}")

            if missing_sections:
                print(f"\nMissing sections details:")
                for section in missing_sections:
                    print(f"  - {section}")
        else:
            print("❌ No 'principal_findings' in result!")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_single_source_debug()