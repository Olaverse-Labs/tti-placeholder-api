#!/usr/bin/env python3
"""
Test runner for the Text-to-Image Placeholder API
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite."""
    print("Running Text-to-Image Placeholder API tests...")
    print("=" * 50)
    
    # Run pytest with verbose output
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "test_main.py", 
        "-v", 
        "--tb=short"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 