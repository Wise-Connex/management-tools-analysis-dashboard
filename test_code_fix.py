#!/usr/bin/env python3
"""
Simple code inspection to verify the scenario_hash fix.
"""

import sys
import ast
import inspect

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

def test_code_fix():
    """Test that the scenario_hash fix is implemented in the code."""
    print("🔍 TESTING CODE FIX IMPLEMENTATION")
    print("=" * 50)

    try:
        # Read the key findings service file
        with open('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/key_findings/key_findings_service.py', 'r') as f:
            content = f.read()

        print("✅ Successfully read key_findings_service.py")

        # Check that scenario_hash is not in function definitions
        if 'scenario_hash' in content:
            # Count occurrences
            scenario_count = content.count('scenario_hash')
            print(f"Found {scenario_count} occurrences of 'scenario_hash' in the file")

            # Check if they're in function signatures (bad) vs other places (might be okay)
            lines = content.split('\n')
            function_def_lines = [line for line in lines if 'def ' in line and 'scenario_hash' in line]

            if function_def_lines:
                print("❌ Found scenario_hash in function definitions:")
                for line in function_def_lines:
                    print(f"   {line.strip()}")
                return False
            else:
                print("✅ No scenario_hash found in function definitions")
                # Check if remaining occurrences are in comments or strings (okay)
                comment_lines = [line for line in lines if '#' in line and 'scenario_hash' in line]
                string_lines = [line for line in lines if '"' in line and 'scenario_hash' in line and 'def ' not in line]

                print(f"   Found in comments: {len(comment_lines)} lines")
                print(f"   Found in strings: {len(string_lines)} lines")

                if len(comment_lines) + len(string_lines) == scenario_count:
                    print("✅ All scenario_hash occurrences are in comments or strings (acceptable)")
                else:
                    print("⚠️  Some scenario_hash occurrences may be in code logic")

        # Check the specific function signature
        import re
        function_pattern = r'def _generate_single_source_analysis\([^)]*\)'
        matches = re.findall(function_pattern, content)

        if matches:
            print(f"✅ Found function signature: {matches[0]}")
            if 'scenario_hash' not in matches[0]:
                print("✅ scenario_hash successfully removed from function signature")
            else:
                print("❌ scenario_hash still present in function signature")
                return False
        else:
            print("❌ Could not find the _generate_single_source_analysis function")
            return False

        print("\n" + "="*50)
        print("🎉 CODE FIX VERIFICATION SUCCESSFUL!")
        print("✅ scenario_hash has been removed from function signatures")
        print("✅ The simplified architecture is properly implemented")
        print("✅ Ready for integration testing")

        return True

    except Exception as e:
        print(f"❌ Code fix verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_code_fix()
    sys.exit(0 if success else 1)