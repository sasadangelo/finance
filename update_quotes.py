# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import datetime as dt
import yfinance as yf
import csv
from pathlib import Path

# Modern yfinance doesn't need pdr_override()
# We'll use yf.download() directly instead of web.get_data_yahoo()

start_date = dt.datetime(1970, 1, 1)
end_date = dt.datetime.now() - dt.timedelta(days=1)
# Read ETF.csv file in order to iterate through all the ETF in our database
with open("database/ETF.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    # For each ETF do the following ...
    for row in reader:
        print("Update quotes for ETF ", row["Name"])

        # If a csv file already exist for the current ETF update the quotes in
        # latest one. If a csv file does not exist for that ETF download all
        # quotes for it.
        csv_file_path = Path("database/quotes/" + row["Ticker"] + ".csv")
        if csv_file_path.exists():
            with open(csv_file_path, "r") as csv_file:
                last_quote_date = list(csv.reader(csv_file))[-1][0]
            last_update_date = dt.datetime.strptime(last_quote_date, "%Y-%m-%d")
            last_update_date += dt.timedelta(days=1)

            # Skip if already up to date
            if last_update_date > end_date:
                print(f"  Already up to date (last quote: {last_quote_date})")
                continue

            try:
                df = yf.download(
                    row["Ticker"],
                    start=last_update_date,
                    end=end_date,
                    progress=False,
                    auto_adjust=False,
                )
                if not df.empty:
                    # Round to 2 decimal places for consistency
                    df = df.round(2)
                    # Reorder columns: Date,Open,High,Low,Close,Adj Close,Volume
                    df = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
                    with open(csv_file_path, "a") as csv_file:
                        df.to_csv(csv_file, header=False)
                    print(f"  Updated with {len(df)} new quotes")
                else:
                    print(f"  No new quotes available")
            except Exception as e:
                print(f"  Cannot download quotes for {row['Ticker']} " f"for period: [{last_update_date}, {end_date}]")
                print(f"  Error: {getattr(e, 'message', repr(e))}")
        else:
            df = yf.download(row["Ticker"], start=start_date, end=end_date, progress=False, auto_adjust=False)
            if not df.empty:
                # Round to 2 decimal places for consistency
                df = df.round(2)
                # Reorder columns: Date,Open,High,Low,Close,Adj Close,Volume
                df = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
                df.to_csv("database/quotes/" + row["Ticker"] + ".csv")
