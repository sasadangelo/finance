import datetime as dt
import pandas_datareader.data as web
import fix_yahoo_finance as yf
import csv

yf.pdr_override() # <== that's all it takes :-)

start = dt.datetime(2005, 1, 1)
end = dt.datetime.now()

with open('database/ETF.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("Download quotes for ETF ", row['Name'])
        df = web.get_data_yahoo(row['Ticker'], start, end)
        df.to_csv('database/quotes/' + row['Ticker'] + '.csv')
