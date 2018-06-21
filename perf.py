import datetime as dt
import sqlite3 as db
import argparse
from dateutil.relativedelta import relativedelta
import sys
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("ticker", help="Specify the ETF ticker")
parser.add_argument("startdate", type=lambda d: dt.datetime.strptime(d, '%Y-%m-%d'), help="Specify start date for backtest period (YYYY-mm-dd)")
args=parser.parse_args()

try:
    cnx = db.connect('database/etfs.db')
    cur = cnx.cursor()
    cur.execute('SELECT Date, Close FROM quotes WHERE Ticker="' + args.ticker + '" and Date > ?', [args.startdate])
    all_rows = cur.fetchall()
except Exception as e:
    print('Failed to load quotes from database:')
    print(e)
finally:
    cnx.close()

if len(all_rows)==0:
    print("No quotes available for the period specified:" + etf_period)
    sys.exit(0)

start_date=all_rows[0][0]
start_price=all_rows[0][1]
end_date=all_rows[len(all_rows)-1][0]
end_price=all_rows[len(all_rows)-1][1]
cum_return_percentage=((end_price/start_price) - 1)*100
print("Backtest")
print("----------------------")
print("Start date: " + str(start_date))
print("End   date: " + str(end_date))
print("----------------------")
print("Cumulative return: %.2f %%" % cum_return_percentage)
