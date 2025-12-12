#!/usr/bin/env python3
"""
Response display utilities for key findings review implementation.
Handles formatting and display of AI responses for evaluation.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


def display_ai_response(response_data: Dict[str, Any], title: str = "AI Response"):
    """
    Display AI response in a formatted way for evaluation.

    Args:
        response_data: Complete AI response data
        title: Title for the display
    """
    print(f"\n{'=' * 80}")
    print(f"🤖 {title}")
    print(f"{'=' * 80}")

    # Display metadata
    print(f"📊 Model: {response_data.get('model_used', 'Unknown')}")
    print(f"⏱️  Response Time: {response_data.get('response_time_ms', 'Unknown')}ms")
    print(f"🎯 Language: {response_data.get('language', 'Unknown')}")
    print(f"💰 Tokens: {response_data.get('token_count', 'Unknown')}")
    print(f"📅 Timestamp: {response_data.get('timestamp', datetime.now())}")

    # Display content sections
    content = response_data.get("content", {})
    if isinstance(content, dict):
        print(f"\n📋 Content Sections ({len(content)} sections):")
        print("-" * 60)

        for section_name, section_content in content.items():
            if section_content and str(section_content).strip():
                print(f"\n🔍 {section_name.upper().replace('_', ' ')}:")
                print(f"   Length: {len(str(section_content))} characters")
                print(f"   Preview: {str(section_content)[:200]}...")

                # Check for markdown formatting
                if "# " in str(section_content):
                    print("   📄 Contains markdown headers")
                if "**" in str(section_content):
                    print("   🔤 Contains bold formatting")
                if "*" in str(section_content):
                    print("   📖 Contains italic formatting")
                if "`" in str(section_content):
                    print("   💻 Contains code formatting")

                # Check for business insights
                insights_keywords = [
                    "tendencia",
                    "patrón",
                    "crecimiento",
                    "declive",
                    "volatilidad",
                    "correlación",
                    "componente",
                    "estrategia",
                ]
                content_lower = str(section_content).lower()
                found_keywords = [kw for kw in insights_keywords if kw in content_lower]
                if found_keywords:
                    print(f"   💡 Business keywords found: {', '.join(found_keywords)}")
    else:
        print(f"\n📄 Content (string): {len(str(content))} characters")
        print(f"Preview: {str(content)[:300]}...")

    # Display quality metrics
    print(f"\n📈 Quality Metrics:")
    print(f"   Content completeness: {'✅ Complete' if content else '❌ Empty'}")
    print(
        f"   Section coverage: {len([s for s in content.values() if s]) if isinstance(content, dict) else 'N/A'}"
    )

    # Display any errors or warnings
    if response_data.get("error"):
        print(f"\n⚠️  Error: {response_data['error']}")

    if response_data.get("warnings"):
        print(f"\n⚠️  Warnings: {response_data['warnings']}")

    print(f"{'=' * 80}")


def save_ai_response(
    response_data: Dict[str, Any],
    tool_name: str,
    selected_sources: list,
    language: str,
    output_dir: str = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/test_results/ai_responses",
) -> str:
    """
    Save AI response to file for detailed analysis.

    Args:
        response_data: Complete AI response data
        tool_name: Management tool name
        selected_sources: List of data sources
        language: Language code
        output_dir: Output directory

    Returns:
        Path to saved file
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Generate filename
    sources_str = "_".join(
        [s.replace(" ", "_").replace("-", "_") for s in selected_sources]
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = (
        f"{tool_name.replace(' ', '_')}_{sources_str}_{language}_{timestamp}.json"
    )
    filepath = os.path.join(output_dir, filename)

    # Prepare data for saving
    save_data = {
        "metadata": {
            "tool_name": tool_name,
            "selected_sources": selected_sources,
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "model_used": response_data.get("model_used", "Unknown"),
            "response_time_ms": response_data.get("response_time_ms", 0),
            "token_count": response_data.get("token_count", 0),
            "provider_used": response_data.get("provider_used", "Unknown"),
        },
        "content": response_data.get("content", {}),
        "raw_response": response_data,
    }

    # Save to file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

        print(f"💾 AI response saved to: {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ Error saving response: {e}")
        return ""


def analyze_response_quality(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the quality of an AI response.

    Args:
        response_data: Complete AI response data

    Returns:
        Quality analysis results
    """
    content = response_data.get("content", {})

    if not isinstance(content, dict):
        return {
            "quality_score": 0,
            "issues": ["Content is not a dictionary"],
            "recommendations": ["Check response format"],
        }

    # Required sections for single-source analysis
    required_single_source_sections = [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "heatmap_analysis",
        "conclusions",
    ]

    # Required sections for multi-source analysis
    required_multi_source_sections = [
        "executive_summary",
        "principal_findings",
        "pca_analysis",
        "heatmap_analysis",
        "strategic_synthesis",
        "conclusions",
    ]

    # Determine analysis type
    sources_count = len(response_data.get("metadata", {}).get("selected_sources", []))
    is_single_source = sources_count == 1

    required_sections = (
        required_single_source_sections
        if is_single_source
        else required_multi_source_sections
    )

    # Check section presence
    present_sections = [
        section
        for section in required_sections
        if content.get(section) and str(content[section]).strip()
    ]
    missing_sections = [
        section for section in required_sections if section not in present_sections
    ]

    # Check content length
    section_lengths = {
        section: len(str(content.get(section, ""))) for section in present_sections
    }
    avg_length = (
        sum(section_lengths.values()) / len(section_lengths) if section_lengths else 0
    )

    # Check for business insights
    business_keywords = [
        "tendencia",
        "patrón",
        "crecimiento",
        "declive",
        "volatilidad",
        "correlación",
        "componente",
        "estrategia",
        "recomendación",
        "análisis",
        "conclusión",
        "trend",
        "pattern",
        "growth",
        "decline",
        "volatility",
        "correlation",
        "component",
        "strategy",
        "recommendation",
        "analysis",
        "conclusion",
    ]

    insights_found = 0
    for section_content in content.values():
        if section_content:
            content_lower = str(section_content).lower()
            insights_found += sum(
                1 for keyword in business_keywords if keyword in content_lower
            )

    # Calculate quality score (0-100)
    section_completeness = (len(present_sections) / len(required_sections)) * 40
    content_length_score = min(
        (avg_length / 500) * 30, 30
    )  # Target ~500 chars per section
    insights_score = min((insights_found / 10) * 30, 30)  # Target ~10 business insights

    quality_score = section_completeness + content_length_score + insights_score

    # Generate recommendations
    recommendations = []

    if missing_sections:
        recommendations.append(f"Add missing sections: {', '.join(missing_sections)}")

    if avg_length < 300:
        recommendations.append("Increase content depth in sections")

    if insights_found < 5:
        recommendations.append("Include more business insights and strategic analysis")

    # Check for markdown formatting
    has_markdown = any(
        "# " in str(content)
        or "**" in str(content)
        or "*" in str(content)
        or "`" in str(content)
        for content in content.values()
        if content
    )

    if not has_markdown:
        recommendations.append("Use markdown formatting for better readability")

    return {
        "quality_score": round(quality_score, 1),
        "section_completeness": f"{len(present_sections)}/{len(required_sections)}",
        "avg_section_length": round(avg_length, 0),
        "business_insights_found": insights_found,
        "missing_sections": missing_sections,
        "has_markdown_formatting": has_markdown,
        "recommendations": recommendations,
        "section_lengths": section_lengths,
    }


def display_quality_analysis(quality_results: Dict[str, Any]):
    """Display quality analysis results."""
    print(f"\n📊 Quality Analysis Results")
    print("=" * 50)
    print(f"Overall Quality Score: {quality_results['quality_score']}/100")
    print(f"Section Completeness: {quality_results['section_completeness']}")
    print(f"Average Section Length: {quality_results['avg_section_length']} characters")
    print(f"Business Insights Found: {quality_results['business_insights_found']}")
    print(
        f"Has Markdown Formatting: {'✅' if quality_results['has_markdown_formatting'] else '❌'}"
    )

    if quality_results["missing_sections"]:
        print(f"Missing Sections: {', '.join(quality_results['missing_sections'])}")

    if quality_results["recommendations"]:
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(quality_results["recommendations"], 1):
            print(f"   {i}. {rec}")

    print("=" * 50)


if __name__ == "__main__":
    # Test with sample data
    sample_response = {
        "model_used": "moonshotai/kimi-k2-instruct",
        "response_time_ms": 2500,
        "language": "es",
        "token_count": 1500,
        "provider_used": "groq",
        "content": {
            "executive_summary": "# Resumen Ejecutivo\n\nEl análisis muestra una tendencia creciente...",
            "principal_findings": "## Hallazgos Principales\n\n**Patrón estacional** detectado...",
            "temporal_analysis": "### Análisis Temporal\n\nLa tendencia muestra crecimiento...",
            "seasonal_analysis": "### Análisis Estacional\n\nSe identificaron patrones...",
            "fourier_analysis": "### Análisis de Fourier\n\nFrecuencias dominantes...",
            "heatmap_analysis": "### Mapa de Calor\n\nCorrelaciones significativas...",
            "conclusions": "### Conclusiones\n\nLas recomendaciones estratégicas...",
        },
    }

    display_ai_response(sample_response, "Sample Response")

    quality_results = analyze_response_quality(sample_response)
    display_quality_analysis(quality_results)
