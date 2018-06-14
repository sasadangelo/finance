import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import sqlite3 as db
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ticker", help="Specify the ETF ticker")
parser.add_argument("-p", "--period", type=str, choices=['Max', '5Y', '1Y', 'YTD', '6M', '3M', '1M', '5D'], help="Specify the period of time")
args=parser.parse_args()

etf_name=args.ticker
etf_currency=""
etf_period='Max' if args.period is None else args.period

print("Load quotes for ETF: " + args.ticker + " for period " + etf_period)

#start = dt.datetime(2005, 1, 1)
#end = dt.datetime.now()

try:
    cnx = db.connect('database/etfs.db')
    cur = cnx.cursor()
    cur.execute('SELECT Date, Close FROM quotes WHERE Ticker="' + args.ticker + '"')
    all_rows = cur.fetchall()
except Exception as e:
    print('Failed to load quotes from database:')
    print(e)
finally:
    cnx.close()

try:
    cnx = db.connect('database/etfs.db')
    cur = cnx.cursor()
    cur.execute('SELECT Name, Currency FROM etfs WHERE Ticker="' + args.ticker + '"')
    etf_data=cur.fetchone()
    etf_name=etf_data[0]
    etf_currency=etf_data[1] 
except Exception as e:
    print(e)
finally:
    cnx.close()

days=list(zip(*all_rows))[0]
dates = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in days]
prices=list(zip(*all_rows))[1]

style.use('ggplot')

x_pos = np.arange(len(prices))
plt.plot(dates, prices)
plt.title(etf_name)
plt.ylabel('Prices (' + etf_currency + ')')
plt.show()
