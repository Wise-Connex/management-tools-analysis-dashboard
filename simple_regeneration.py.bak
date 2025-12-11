#!/usr/bin/env python3
"""
Simple regeneration script for Key Findings
This provides a simple way to regenerate analyses without complex JavaScript
"""

import sys
import os
import time
from pathlib import Path

# Add the tools-dashboard root and dashboard_app to path
tools_dashboard_root = Path(__file__).parent
dashboard_app_path = tools_dashboard_root / "dashboard_app"
sys.path.insert(0, str(tools_dashboard_root))
sys.path.insert(0, str(dashboard_app_path))

from key_findings.key_findings_service import KeyFindingsService
from key_findings.database_manager import KeyFindingsDBManager


def regenerate_analysis(tool_name, selected_sources, language="es"):
    """
    Regenerate a specific Key Findings analysis

    Args:
        tool_name: Management tool name
        selected_sources: List of data sources
        language: Language for analysis (es/en)
    """
    print(
        f"🔄 REGENERATING: {tool_name} with {', '.join(selected_sources)} in {language}"
    )
    print("=" * 60)

    try:
        # Initialize services
        db_path = "./data/key_findings.db"
        kf_db_manager = KeyFindingsDBManager(db_path)
        key_findings_service = KeyFindingsService(
            db_manager=None,  # Use default
            groq_api_key=os.getenv("GROQ_API_KEY"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
            config={"enable_pca_emphasis": True},
        )

        start_time = time.time()

        # Force regeneration with new improved prompts
        result = key_findings_service.generate_key_findings(
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            force_refresh=True,  # This bypasses cache and uses improved prompts
        )

        end_time = time.time()
        duration = (end_time - start_time) * 1000

        if result.get("success", False):
            print(f"✅ REGENERATION SUCCESSFUL!")
            print(f"⏱️  Duration: {duration:.0f}ms")
            print(f"📊 Source: {result.get('source', 'unknown')}")

            # Show analysis preview
            data = result.get("data", {})
            if "executive_summary" in data:
                print(f"📝 Preview: {data['executive_summary'][:200]}...")

            return True
        else:
            print(f"❌ REGENERATION FAILED: {result.get('error', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


def list_available_tools():
    """List available management tools"""
    tools = [
        "Benchmarking",
        "Porter's Five Forces",
        "SWOT Analysis",
        "McKinsey 7S",
        "BCG Matrix",
        "Ansoff Matrix",
        "PESTLE Analysis",
        "Value Chain Analysis",
        "OKR",
        "Balanced Scorecard",
        "Blue Ocean Strategy",
        "Growth-Share Matrix",
        "Business Model Canvas",
        "Lean Startup",
        "Kotler's 4P",
        "Job Theory",
        "Blue Ocean",
        "Disruptive Innovation",
        "Competitive Analysis",
        "Customer Journey",
        "Agile Methodology",
    ]

    print("🛠️ Available Management Tools:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i:2d}. {tool}")
    return tools


def main():
    """Main function for manual regeneration testing"""
    print("🔄 KEY FINDINGS REGENERATION TOOL")
    print("=" * 50)
    print(
        "This tool regenerates Key Findings using the improved 4000+ word narrative prompts"
    )
    print()

    # Show available tools
    tools = list_available_tools()
    print()

    # Get user input
    try:
        tool_choice = int(input(f"Select tool (1-{len(tools)}): ")) - 1
        if tool_choice < 0 or tool_choice >= len(tools):
            print("❌ Invalid selection")
            return

        tool_name = tools[tool_choice]

        # Source selection
        sources = [
            "Google Trends",
            "Bain Usage",
            "Crossref",
            "Google Books",
            "Bain Satisfaction",
        ]
        print(f"\n📊 Available Sources:")
        for i, source in enumerate(sources, 1):
            print(f"  {i}. {source}")

        source_choices = input("Select sources (comma-separated, e.g., 1,2,3): ").split(
            ","
        )
        selected_sources = []
        for choice in source_choices:
            try:
                idx = int(choice.strip()) - 1
                if 0 <= idx < len(sources):
                    selected_sources.append(sources[idx])
            except ValueError:
                pass

        if not selected_sources:
            print("❌ No valid sources selected")
            return

        # Language selection
        language = input("Language (es/en) [es]: ").strip() or "es"

        print(f"\n🚀 Starting regeneration...")
        success = regenerate_analysis(tool_name, selected_sources, language)

        if success:
            print("\n✅ Regeneration completed successfully!")
            print("🎯 New analysis uses improved narrative prompts:")
            print("   • 4000+ word structured format")
            print("   • Business interpretation focus")
            print("   • Primary emphasis on Correlation, PCA, Periodogram")
            print("   • No statistical reporting")
        else:
            print("\n❌ Regeneration failed")

    except KeyboardInterrupt:
        print("\n👋 Regeneration cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
