#!/usr/bin/env python3
"""
Script to fix CSV files precision by rounding all numeric values to 2 decimal places.
This ensures consistency across all historical data.

Usage: uv run python fix_csv_precision.py
"""

import pandas as pd
from pathlib import Path
import sys


def fix_csv_file(csv_path):
    """Round all numeric values in a CSV file to 2 decimal places."""
    try:
        # Read the CSV file with explicit date format
        df = pd.read_csv(csv_path, index_col=0, parse_dates=True, date_format="%Y-%m-%d")

        # Round all numeric columns to 2 decimal places
        numeric_columns = df.select_dtypes(include=["float64", "float32"]).columns
        df[numeric_columns] = df[numeric_columns].round(2)

        # Save back to CSV
        df.to_csv(csv_path)

        return True, len(df)
    except Exception as e:
        return False, str(e)


def main():
    """Process all CSV files in database/quotes/"""
    quotes_dir = Path("database/quotes")

    if not quotes_dir.exists():
        print(f"Error: {quotes_dir} directory not found")
        return 1

    csv_files = list(quotes_dir.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {quotes_dir}")
        return 1

    print(f"Found {len(csv_files)} CSV files to process")
    print("=" * 60)

    success_count = 0
    error_count = 0

    for csv_file in sorted(csv_files):
        ticker = csv_file.stem
        success, result = fix_csv_file(csv_file)

        if success:
            print(f"✓ {ticker:15s} - Fixed {result} rows")
            success_count += 1
        else:
            print(f"✗ {ticker:15s} - Error: {result}")
            error_count += 1

    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Success: {success_count}")
    print(f"  Errors:  {error_count}")
    print(f"  Total:   {len(csv_files)}")

    if error_count == 0:
        print("\n✅ All CSV files have been fixed!")
        return 0
    else:
        print(f"\n⚠️  {error_count} files had errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
