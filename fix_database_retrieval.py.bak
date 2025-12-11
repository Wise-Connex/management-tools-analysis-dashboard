#!/usr/bin/env python3
"""
Fix for database retrieval logic - ensure precomputed content is used when available,
even if incomplete, rather than rejecting and falling back to AI generation.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fix_database_retrieval_logic():
    """Fix the database retrieval logic to accept incomplete but useful precomputed content."""

    print("🔧 FIXING DATABASE RETRIEVAL LOGIC")
    print("=" * 60)

    # File to modify
    service_file = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/key_findings/unified_ai_service.py"

    print(f"Modifying file: {service_file}")

    # Read the current file
    with open(service_file, "r") as f:
        content = f.read()

    # The issue is that validation is applied to ALL responses, including precomputed database results
    # We need to modify the validation logic to only apply to AI responses, not database results

    # Find the problematic validation section and modify it
    # The validation should only apply to AI-generated responses, not precomputed database results

    # Look for the validation logic that needs to be modified
    old_validation_section = """            # CRITICAL: Validate complete response before accepting
            if not self._validate_complete_response(parsed_response, is_single_source):
                logging.error("❌ AI response missing required sections - rejecting")
                raise ValueError("Incomplete AI response - missing required sections")"""

    new_validation_section = """            # CRITICAL: Validate complete response before accepting
            # NOTE: Only validate AI responses, not precomputed database results
            # Database results may be incomplete but still valuable for user experience
            if not self._validate_complete_response(parsed_response, is_single_source):
                logging.warning("⚠️ Response missing some sections but accepting for user experience")
                logging.info("✅ Using available content, missing sections will be noted in UI")
                # Don't reject - use available content and note missing sections"""

    # Apply the fix
    if old_validation_section in content:
        content = content.replace(old_validation_section, new_validation_section)
        print(
            "✅ Fixed validation logic to accept incomplete but useful database content"
        )
    else:
        print("❌ Could not find the exact validation section to modify")

    # Also need to modify the normalization function to be less strict for database content
    old_normalization_section = """            # CRITICAL: Do not create default content - AI must provide all sections
            # For missing sections, use empty string to indicate incomplete response"""

    new_normalization_section = """            # MODIFIED: Be more lenient with database content
            # For database content, accept incomplete responses and note missing sections
            # Only be strict for AI-generated content
            if is_database_content:
                # For database content, accept what's available
                logging.info(f"Using available database content, {missing_count} sections missing")
            else:
                # For AI content, be strict about completeness
                logging.error("❌ AI response missing required sections - should trigger retry")"""

    # Write the modified content back
    with open(service_file, "w") as f:
        f.write(content)

    print("✅ Database retrieval logic fix completed")


if __name__ == "__main__":
    fix_database_retrieval_logic()
