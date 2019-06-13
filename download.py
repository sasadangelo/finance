import datetime as dt
import pandas as pd
import argparse
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import fix_yahoo_finance as yf
import csv

yf.pdr_override() # <== that's all it takes :-)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--ticker", help="Specify the ETF ticker")
args=parser.parse_args()

if args.ticker == None:
    print(args.ticker)


start = dt.datetime(2005, 1, 1)
end = dt.datetime.now()

with open('database/ETF.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (args.ticker == None) or (args.ticker == row['Ticker']):
            print("Download quotes for ETF ", row['Name'])
            df = web.get_data_yahoo(row['Ticker'], start, end)
            df.to_csv('database/quotes/' + row['Ticker'] + '.csv')
