#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Quick test script to verify the UV setup is working correctly.
Run with: uv run python test_setup.py
"""

import sys


def test_imports():
    """Test that all required packages can be imported."""
    print("Testing package imports...")

    packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("yfinance", "yfinance"),
        ("pandas_datareader", "pandas-datareader"),
        ("matplotlib", "matplotlib"),
        ("tabulate", "tabulate"),
        ("dateutil", "python-dateutil"),
        ("setuptools", "setuptools"),
        ("flask", "flask"),
        ("flask_sqlalchemy", "flask-sqlalchemy"),
    ]

    failed = []
    for module_name, package_name in packages:
        try:
            __import__(module_name)
            print(f"✓ {package_name}")
        except ImportError as e:
            print(f"✗ {package_name}: {e}")
            failed.append(package_name)

    if failed:
        print(f"
❌ Failed to import: {', '.join(failed)}")
        return False
    else:
        print("
✅ All packages imported successfully!")
        return True


def test_python_version():
    """Test Python version."""
    print(f"
Python version: {sys.version}")
    version_info = sys.version_info

    if version_info.major == 3 and version_info.minor >= 13:
        print("✅ Python version is 3.13 or higher")
        return True
    else:
        print(f"⚠️  Python version is {version_info.major}.{version_info.minor}, recommended 3.13+")
        return True  # Warning, not error


def test_database_access():
    """Test database file exists."""
    import os

    print("
Checking database files...")

    files = [
        "database/ETF.csv",
        "database/etfs.db",
    ]

    for file_path in files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"⚠️  {file_path} not found (will be created when needed)")

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("ETF Finance - UV Setup Test")
    print("=" * 60)

    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("Database Files", test_database_access),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"
{'=' * 60}")
        print(f"Test: {test_name}")
        print("=" * 60)
        results.append(test_func())

    print("
" + "=" * 60)
    if all(results):
        print("✅ All tests passed! Setup is complete.")
        print("
You can now run:")
        print("  uv run python download.py -t VUSA.MI")
        print("  uv run python graph.py VUSA.MI")
        print("  uv run python perf.py VUSA.MI")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
