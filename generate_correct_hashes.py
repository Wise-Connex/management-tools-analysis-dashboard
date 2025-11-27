#!/usr/bin/env python3
"""
Generate the correct combination hashes that match the system's hash generation algorithm.
"""

import hashlib
import json

def generate_system_hash(tool_name, sources_text, language):
    """Generate hash exactly as the system does."""

    # Create combination data exactly as the system does
    combination_data = {
        "tool_name": tool_name,
        "sources_text": sources_text,
        "language": language
    }

    # Convert to JSON with sorted keys
    combination_json = json.dumps(combination_data, sort_keys=True)

    # Generate SHA256 hash
    return hashlib.sha256(combination_json.encode('utf-8')).hexdigest()

def main():
    print("🔑 Generating Correct Combination Hashes")
    print("=" * 60)

    # Test cases based on the logs
    test_cases = [
        {
            "tool_name": "Benchmarking",
            "sources_text": "Google Trends",
            "language": "es"
        },
        {
            "tool_name": "Benchmarking",
            "sources_text": "Google Trends, Google Books, Bain Usability, Crossref, Bain Satisfaction",
            "language": "es"
        }
    ]

    print("\\n🧪 Generating hashes for test cases:")

    for i, test_case in enumerate(test_cases, 1):
        print(f"\\nTest Case {i}:")
        print(f"  Tool: {test_case['tool_name']}")
        print(f"  Sources: {test_case['sources_text']}")
        print(f"  Language: {test_case['language']}")

        hash_result = generate_system_hash(
            test_case['tool_name'],
            test_case['sources_text'],
            test_case['language']
        )

        print(f"  Generated Hash: {hash_result}")
        print(f"  Length: {len(hash_result)} characters")

        # Compare with what we found in the database
        expected_hashes = [
            "f9ae16b8d0f8b35a4ceb0a71ebbc60bcb26d1449e17c3a277c06c27009941991",
            "25d60d2f605e0a93f2732f1dd9db00be04d686a314653efb00f5783d074d301f"
        ]

        if i <= len(expected_hashes):
            expected = expected_hashes[i-1]
            match = hash_result == expected
            print(f"  Expected Hash:  {expected}")
            print(f"  Match: {'✅ YES' if match else '❌ NO'}")

    print("\\n" + "=" * 60)
    print("✅ Hash Generation Complete!")
    print("=" * 60)
    print("Use these exact hashes when populating the precomputed findings database!")

if __name__ == "__main__":
    main()

print("\\n" + "="*60)
print("🔑 Hash Generation Complete!")
print("="*60)
print("These hashes should match the system's hash generation exactly!")
print("="*60)

# For immediate use, here are the correct hashes:
print("\\n📋 CORRECT HASHES FOR YOUR TEST DATA:")
print("="*50)
print("Single Source (Google Trends, es):")
print("  Hash: f9ae16b8d0f8b35a4ceb0a71ebbc60bcb26d1449e17c3a277c06c27009941991")
print("\\nMulti-Source (5 sources, es):")
print("  Hash: 25d60d2f605e0a93f2732f1dd9db00be04d686a314653efb00f5783d074d301f")
print("="*50)