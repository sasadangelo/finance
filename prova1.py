import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
#import pandas as pd
import pandas_datareader.data as web
import fix_yahoo_finance as yf
import sqlite3 as db
#import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ticker", help="Specify the ETF ticker")
args=parser.parse_args()
print("Load quotes for ETF: " + args.ticker)

try:
    cnx = db.connect('database/etfs.db')
#    df = pandas.read_csv('database/ETF.csv')
#    df.to_sql('etfs', conx, if_exists='append', index=False)

    cur = cnx.cursor()
    table_name = 'quotes'
    column='Ticker'
    cur.execute('SELECT Date, Close FROM {tn} WHERE {cn}="CW8.MI"'.\
        format(tn=table_name, cn=column))
    all_rows = cur.fetchall()
    #print(all_rows)

#    sql = '''CREATE TABLE etfs (id integer primary key autoincrement, \
#        'Name' TEXT, 'ISIN' TEXT, 'Ticker' TEXT, 'Date' TEXT, \
#        'Capital' REAL, 'Replication' TEXT, 'Volatility' REAL, \
#        'Dividend' TEXT, 'DividendFrequency' INTEGER, 'Yeld' REAL)'''     

#    cur.execute(sql)
except:
    print('Exception:')
    print(e)
finally:
    cnx.close()

days=list(zip(*all_rows))[0]
prices=list(zip(*all_rows))[1]
print(prices)
#etf_tickers=["WLD.MI", "CW8.MI", "MWRD.MI", "HMWD.MI", "SWDA.MI", "XDWD.MI", "XMWO.MI", "IWRD.MI", "SMSWLD.MI", "WRDEUA.MI"]

yf.pdr_override() # <== that's all it takes :-)

style.use('ggplot')

start = dt.datetime(2005, 1, 1)
end = dt.datetime.now()

#for etf_ticker in etf_tickers:
#    df = web.get_data_yahoo(etf_ticker, start, end)
#    df.to_csv('database/quotes' + etf_ticker + '.csv')

#df = web.get_data_yahoo("CW8.MI", start, end)
#df = web.get_data_yahoo("MWRD.MI", start, end)
#df = web.get_data_yahoo("HMWD.MI", start, end)
#df = web.get_data_yahoo("SWDA.MI", start, end)
#df = web.get_data_yahoo("XDWD.MI", start, end)
#df = web.get_data_yahoo("XMWO.MI", start, end)
#df = web.get_data_yahoo("IWRD.MI", start, end)
#df = web.get_data_yahoo("SMSWLD.MI", start, end)
#df = web.get_data_yahoo("WRDEUA.MI", start, end)
#print(df)
#df = web.DataReader("IWRD", 'morningstar', start, end)
#df.reset_index(inplace=True)
#df.set_index("Date", inplace=True)
#df = df.drop("Symbol", axis=1)
#df['100ma'] = df['Close'].rolling(window=100,min_periods=0).mean()
#ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
#ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
x_pos = np.arange(len(prices))
plt.plot(x_pos, prices)
#ax1.plot(all_rows.index, df['100ma'])
#ax2.bar(all_rows.index, all_rows['Volume'])
#print(df.head())
#df.to_csv('WRDEUA.MI.csv')
#all_rows['Close'].plot()
plt.show()
