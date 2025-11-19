#!/usr/bin/env python3
"""
Key Findings Service Patch - Add Precomputed Database Integration
This patches the KeyFindingsService to use precomputed findings as fallback.
"""

import sys
import re
from pathlib import Path


def patch_key_findings_service():
    """Patch the KeyFindingsService to integrate precomputed findings database."""

    service_file = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/key_findings/key_findings_service.py"

    # Read the file
    with open(service_file, "r") as f:
        content = f.read()

    # Add import for sqlite3 at the top if not present
    if "import sqlite3" not in content:
        content = content.replace(
            "import asyncio\nimport json\nimport time",
            "import asyncio\nimport json\nimport sqlite3\nimport time",
        )

    # Find the class definition and add our method before get_performance_metrics
    pattern = r"(\s+def get_performance_metrics\(self\) -> Dict\[str, Any\]:)"
    replacement = r'''\1
    def _get_precomputed_findings(
        self, tool_name: str, selected_sources: List[str], language: str
    ):
        """
        Get precomputed findings from the database as fallback.
        """
        try:
            # Create sources text (sorted for consistency)
            sources_text = ", ".join(sorted(selected_sources))
            
            # Connect to precomputed findings database
            db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query for exact match
            cursor.execute("""
                SELECT executive_summary, principal_findings, temporal_analysis, 
                       seasonal_analysis, fourier_analysis, pca_analysis, 
                       heatmap_analysis, confidence_score, model_used, 
                       data_points_analyzed, analysis_type
                FROM precomputed_findings 
                WHERE tool_name = ? AND sources_text = ? AND language = ? 
                AND is_active = 1
                LIMIT 1
            """, (tool_name, sources_text, language))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
                
            # Format result to match Key Findings structure
            formatted_result = {
                "tool_name": tool_name,
                "selected_sources": selected_sources,
                "language": language,
                "executive_summary": result[0] or "",
                "principal_findings": result[1] or "",
                "temporal_analysis": result[2] or "",
                "seasonal_analysis": result[3] or "",
                "fourier_analysis": result[4] or "",
                "pca_analysis": result[5] or "",
                "heatmap_analysis": result[6] or "",
                "confidence_score": result[7] or 0.8,
                "model_used": result[8] or "precomputed_database",
                "data_points_analyzed": result[9] or 0,
                "sources_count": len(selected_sources),
                "analysis_depth": result[10] or "comprehensive",
                "report_type": "precomputed",
                "is_precomputed": True,
                "sources_text": sources_text
            }
            
            logging.info(f"Successfully retrieved precomputed findings for {tool_name} with {len(selected_sources)} sources")
            return formatted_result
            
        except Exception as e:
            logging.error(f"Failed to get precomputed findings: {e}")
            return None

'''

    content = re.sub(pattern, replacement, content)

    # Update the generate_key_findings method to check precomputed database
    # Find the cache miss section and add precomputed lookup
    cache_miss_pattern = r'(\s+# Cache miss - generate new analysis\s+self\.performance_metrics\["cache_misses"\] \+= 1\s+logging\.info\(\s+f"Cache miss for scenario \{scenario_hash\[:8\]\}\.\.\.Generating new analysis"\s+\))'

    cache_miss_replacement = r"""\1
            # Check precomputed findings database
            precomputed_result = self._get_precomputed_findings(
                tool_name, selected_sources, language
            )
            if precomputed_result:
                logging.info(
                    f"Precomputed findings found for scenario {scenario_hash[:8]}..."
                )
                response_time_ms = int((time.time() - start_time) * 1000)

                return {
                    "success": True,
                    "data": precomputed_result,
                    "cache_hit": True,
                    "response_time_ms": response_time_ms,
                    "scenario_hash": scenario_hash,
                    "source": "precomputed_findings",
                }

            # No cache or precomputed data - generate new analysis
            logging.info(
                f"No cached or precomputed data for scenario {scenario_hash[:8]}... Generating new analysis"
            )"""

    content = re.sub(cache_miss_pattern, cache_miss_replacement, content)

    # Write the patched file
    with open(service_file, "w") as f:
        f.write(content)

    print("✅ Key Findings Service patched successfully!")
    print("🔧 Added precomputed database integration")
    print("📦 Key Findings now uses fallback from precomputed database")


if __name__ == "__main__":
    patch_key_findings_service()
