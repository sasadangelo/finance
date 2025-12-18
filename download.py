from __future__ import annotations
import datetime as dt
import csv
from pathlib import Path
import argparse
import pandas as pd
import yfinance as yf


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

START_DATE = dt.datetime(1970, 1, 1)
END_DATE = dt.datetime.now() - dt.timedelta(days=1)

ETF_DATABASE_PATH = Path("database/ETF.csv")
QUOTES_DIR = Path("database/quotes")


# -----------------------------------------------------------------------------
# Helper function to normalize yfinance DataFrame
# -----------------------------------------------------------------------------


def normalize_quotes_dataframe(
    df: pd.DataFrame | pd.Series | None,
) -> pd.DataFrame:
    """
    Normalize a yfinance DataFrame to the following flat structure:

    Date,Open,High,Low,Close,Adj Close,Volume
    """
    if df is None or (hasattr(df, "empty") and df.empty):
        return pd.DataFrame()

    # Convert Series to DataFrame if needed
    if isinstance(df, pd.Series):
        result_df: pd.DataFrame = df.to_frame().T
    else:
        result_df = df

    if isinstance(result_df.columns, pd.MultiIndex):
        result_df.columns = result_df.columns.get_level_values(0)

    result_df = result_df.reset_index()

    result_df = result_df[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]

    price_columns = ["Open", "High", "Low", "Close", "Adj Close"]
    result_df[price_columns] = result_df[price_columns].round(2)

    return result_df


# -----------------------------------------------------------------------------
# CLI arguments
# -----------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and update ETF quotes")

    parser.add_argument(
        "-t",
        "--ticker",
        type=str,
        help="Download/update only the specified ticker (e.g. VUSA.MI)",
    )

    return parser.parse_args()


# -----------------------------------------------------------------------------
# Main logic
# -----------------------------------------------------------------------------


def update_ticker(ticker: str, name: str | None = None) -> None:
    display_name = f"{name} ({ticker})" if name else ticker
    print(f"Updating quotes for ETF: {display_name}")

    csv_file_path = QUOTES_DIR / f"{ticker}.csv"

    # -------------------------------------------------------------------------
    # CSV exists → append missing data
    # -------------------------------------------------------------------------
    if csv_file_path.exists():
        with open(csv_file_path, "r") as existing_file:
            last_row = list(csv.reader(existing_file))[-1]
            last_quote_date = dt.datetime.strptime(last_row[0], "%Y-%m-%d")

        start_date = last_quote_date + dt.timedelta(days=1)

        if start_date > END_DATE:
            print(f"  Already up to date (last quote: {last_quote_date.date()})")
            return

        raw_df = yf.download(
            ticker,
            start=start_date,
            end=END_DATE,
            progress=False,
            auto_adjust=False,
        )

        if raw_df is None or (hasattr(raw_df, "empty") and raw_df.empty):
            print("  No new quotes available")
            return

        df = normalize_quotes_dataframe(raw_df)

        with open(csv_file_path, "a", newline="") as csv_file:
            df.to_csv(
                csv_file,
                index=False,
                header=False,
                date_format="%Y-%m-%d",
            )

        print(f"  Appended {len(df)} new rows")

    # -------------------------------------------------------------------------
    # CSV does not exist → full historical download
    # -------------------------------------------------------------------------
    else:
        raw_df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            progress=False,
            auto_adjust=False,
        )

        if raw_df is None or (hasattr(raw_df, "empty") and raw_df.empty):
            print("  No historical data available")
            return

        df = normalize_quotes_dataframe(raw_df)

        df.to_csv(
            csv_file_path,
            index=False,
            header=True,
            date_format="%Y-%m-%d",
        )

        print(f"  Created file with {len(df)} rows")


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    # Ensure output directory exists
    QUOTES_DIR.mkdir(parents=True, exist_ok=True)

    # Case 1: single ticker from CLI
    if args.ticker:
        update_ticker(args.ticker.strip())
        return

    # Case 2: all tickers from ETF database
    with open(ETF_DATABASE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            update_ticker(
                ticker=row["Ticker"],
                name=row.get("Name"),
            )


if __name__ == "__main__":
    main()
