import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import sqlite3 as db
import argparse
from dateutil.relativedelta import relativedelta
import sys

def get_start_date(period):
    if (period=='Max'):
        return dt.datetime(1970, 1, 1)
    elif (period=='5Y'):
        return dt.datetime.now() - relativedelta(years=+5)
    elif (period=='1Y'):
        return dt.datetime.now() - relativedelta(years=+1)
    elif (period=='YTD'):
        return dt.datetime(dt.datetime.now().year, 1, 1)
    elif (period=='6M'):
        return dt.datetime.now() - relativedelta(months=+6)
    elif (period=='3M'):
        return dt.datetime.now() - relativedelta(months=+3)
    elif (period=='1M'):
        return dt.datetime.now() - relativedelta(months=+1)
    elif (period=='5D'):
        return dt.datetime.now() - relativedelta(days=+5)


parser = argparse.ArgumentParser()
parser.add_argument("ticker", help="Specify the ETF ticker")
parser.add_argument("-p", "--period", type=str, choices=['Max', '5Y', '1Y', 'YTD', '6M', '3M', '1M', '5D'], help="Specify the period of time")
parser.add_argument("-v", "--volume", action='store_true', help="Specify the volume")
args=parser.parse_args()

etf_name=args.ticker
etf_currency=""
etf_period='Max' if args.period is None else args.period
print(args.volume)

print("Load quotes for ETF: " + args.ticker + " for period " + etf_period)

start_date = get_start_date(etf_period)

try:
    cnx = db.connect('database/etfs.db')
    cur = cnx.cursor()
    cur.execute('SELECT Date, Close, Volume FROM quotes WHERE Ticker="' + args.ticker + '" and Date > ?', [start_date])
    all_rows = cur.fetchall()
except Exception as e:
    print('Failed to load quotes from database:')
    print(e)
finally:
    cnx.close()

if len(all_rows)==0:
    print("No quotes available for the period specified:" + etf_period)
    sys.exit(0)

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
volumes=list(zip(*all_rows))[2]

style.use('ggplot')

if args.volume==False:
   plt.plot(dates, prices)
   plt.title(etf_name)
   plt.ylabel('Prices (' + etf_currency + ')')
else: 
   ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
   ax1.plot(dates, prices)
   ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
   ax2.bar(dates, volumes)
   ax1.set_title(etf_name)
   ax1.set_ylabel('Prices (' + etf_currency + ')')
plt.show()
