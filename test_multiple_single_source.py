#!/usr/bin/env python3
"""
Test multiple single-source combinations to verify the fix
"""

import os
import sys
import json

# Add database implementation path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "database_implementation"))

try:
    from precomputed_findings_db import get_precomputed_db_manager

    print("✅ Successfully imported database manager")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_single_source_combinations():
    """Test multiple single-source combinations."""
    print("🧪 Testing Multiple Single-Source Combinations")
    print("=" * 55)

    try:
        # Initialize database manager
        db_manager = get_precomputed_db_manager()

        # Test combinations to verify
        test_combinations = [
            ("Benchmarking", ["Google Trends"], "es"),
            ("Calidad Total", ["Google Trends"], "es"),
            ("Competencias Centrales", ["Google Trends"], "en"),
            ("Cuadro de Mando Integral", ["Google Books"], "es"),
            ("Experiencia del Cliente", ["Bain Usability"], "en"),
            ("Fusiones y Adquisiciones", ["Crossref"], "es"),
            ("Gestión de Costos", ["Bain Satisfaction"], "en"),
            ("Innovación Colaborativa", ["Google Trends"], "es"),
            ("Lealtad del Cliente", ["Google Books"], "en"),
            ("Outsourcing", ["Bain Usability"], "es"),
            ("Planificación Estratégica", ["Crossref"], "en"),
        ]

        success_count = 0
        total_count = len(test_combinations)

        for tool_name, selected_sources, language in test_combinations:
            try:
                # Generate the hash for this combination
                combination_hash = db_manager.generate_combination_hash(
                    tool_name=tool_name,
                    selected_sources=selected_sources,
                    language=language,
                )

                # Retrieve from database
                analysis = db_manager.get_combination_by_hash(combination_hash)

                if not analysis:
                    print(
                        f"❌ {tool_name} + {selected_sources} ({language}): Not found"
                    )
                    continue

                # Check required sections
                required_sections = [
                    "executive_summary",
                    "principal_findings",
                    "temporal_analysis",
                    "seasonal_analysis",
                    "fourier_analysis",
                    "strategic_synthesis",
                    "conclusions",
                ]

                sections_present = 0
                for section in required_sections:
                    content = analysis.get(section, "")
                    if content and len(content.strip()) > 10:
                        sections_present += 1

                # Dashboard validation logic: minimum 6 sections required
                is_valid = sections_present >= 6

                if is_valid:
                    print(
                        f"✅ {tool_name} + {selected_sources} ({language}): {sections_present}/7 sections"
                    )
                    success_count += 1
                else:
                    print(
                        f"❌ {tool_name} + {selected_sources} ({language}): {sections_present}/7 sections"
                    )

            except Exception as e:
                print(f"❌ {tool_name} + {selected_sources} ({language}): Error - {e}")

        print(f"\n📊 Test Results:")
        print(f"  Total tested: {total_count}")
        print(f"  Successful: {success_count}")
        print(f"  Failed: {total_count - success_count}")
        print(f"  Success rate: {(success_count / total_count * 100):.1f}%")

        if success_count >= total_count * 0.8:  # 80% or more
            print(
                f"\n🎉 EXCELLENT: Dashboard should work for most single-source combinations!"
            )
        elif success_count >= total_count * 0.5:  # 50% or more
            print(
                f"\n✅ GOOD: Dashboard should work for many single-source combinations!"
            )
        else:
            print(f"\n⚠️  NEEDS WORK: Still some issues with single-source combinations")

    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_single_source_combinations()
