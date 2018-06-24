import os
import pandas as pd

def symbol_to_path(symbol, base_dir="../database/quotes"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'WLD.MI' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'WLD.MI')

    for symbol in symbols:
        dfSymbol = pd.read_csv(symbol_to_path(symbol),index_col="Date",
                               parse_dates=True,usecols=["Date","Adj Close"],
                               na_values=['nan'])
        dfSymbol=dfSymbol.rename(columns={'Adj Close': symbol})
        df=df.join(dfSymbol)
        df = df.dropna()
        print(df)
        
    return df

def test_run():
    # Define a date range
    dates = pd.date_range('2017-01-22', '2017-01-26')

    # Choose stock symbols to read
    symbols = ['CW8.MI', 'IWRD.MI', 'SWDA.MI']
    
    # Get stock data
    df = get_data(symbols, dates)

if __name__ == "__main__":
    test_run()

