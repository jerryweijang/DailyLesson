#!/usr/bin/env python3
"""
Test runner script for the Daily Lesson project
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"❌ {description} FAILED (exit code: {result.returncode})")
        return False
    else:
        print(f"✅ {description} PASSED")
        return True


def main():
    parser = argparse.ArgumentParser(description="Run tests for Daily Lesson project")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--slow", action="store_true", help="Include slow tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--file", "-f", help="Run specific test file")
    
    args = parser.parse_args()
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    
    # Determine which tests to run
    if args.file:
        cmd.append(f"tests/{args.file}")
    elif args.unit:
        cmd.extend(["-m", "unit", "tests/"])
    elif args.integration:
        cmd.extend(["-m", "integration", "tests/"])
    else:
        # Run all tests
        cmd.append("tests/")
    
    # Handle slow tests
    if not args.slow:
        cmd.extend(["-m", "not slow"])
    
    success = run_command(cmd, "Running Tests")
    
    if not success:
        print("\n❌ Test run failed!")
        sys.exit(1)
    
    print("\n✅ All tests passed!")
    
    # Additional checks
    if not args.file:
        print("\n" + "="*60)
        print("Running additional checks...")
        print("="*60)
        
        # Check that demo script runs
        demo_success = run_command(
            ["python", "-c", "from orchestrator import create_demo_orchestrator; print('Demo orchestrator created successfully')"],
            "Demo Script Import Test"
        )
        
        # Check that all modules can be imported
        import_success = run_command([
            "python", "-c", 
            "import interfaces, lesson_service, image_service, content_renderer, orchestrator; print('All modules imported successfully')"
        ], "Module Import Test")
        
        if not (demo_success and import_success):
            print("\n❌ Additional checks failed!")
            sys.exit(1)
    
    print("\n🎉 All tests and checks completed successfully!")


if __name__ == "__main__":
    main()