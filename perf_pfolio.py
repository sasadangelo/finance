import datetime as dt
import sqlite3 as db
import argparse
from dateutil.relativedelta import relativedelta
import sys
import pandas as pd
from calendar import isleap
from tabulate import tabulate
import numpy as np
import math as mt
import csv
import math

def sumColumn(m, column):
    total = 0
    for row in range(len(m)):
        total += m[row][column]
    return total

parser = argparse.ArgumentParser()
parser.add_argument("portfolio", nargs='+', help="Specify the portfolio name")
parser.add_argument("-s", "--startdate", type=lambda d: dt.datetime.strptime(d, '%Y-%m-%d'), help="Specify start date for backtest period (YYYY-mm-dd)")
parser.add_argument("-e", "--enddate", type=lambda d: dt.datetime.strptime(d, '%Y-%m-%d'), help="Specify end date for backtest period (YYYY-mm-dd)")
args=parser.parse_args()

if args.startdate == None:
    args.startdate=dt.datetime(1970, 1, 1)

if args.enddate == None:
    args.enddate=dt.datetime.now()

output_report = [[""], ["Start date"], ["End date"], [""], ["Cum. return"], ["Ann. return"], ["Ann. volatility"]]
headers=['Backtest']

for portfolio in args.portfolio:
    headers.append(portfolio)
    with open('pfolio/' + portfolio + '.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        cum_return_percentage=0
        annual_return=0
        annual_variance=0
        total_allocation=0

        for row in reader:
            ticker=row['Ticker']
            allocation=int(row['Allocation'])
            total_allocation=total_allocation+allocation

            output_report_row = []

            try:
                cnx = db.connect('database/etfs.db')
                cur = cnx.cursor()
                cur.execute('SELECT Date, Close FROM quotes WHERE Ticker="' + ticker + '" and Date >= "' + args.startdate.strftime('%Y-%m-%d') + '" and Date <= "' + args.enddate.strftime('%Y-%m-%d') + '"')
                all_quotes = cur.fetchall()
            except Exception as e:
                print('Failed to load quotes from database:')
                print(e)
            finally:
                cnx.close()

            try:
                cnx = db.connect('database/etfs.db')
                cur = cnx.cursor()
                cur.execute('SELECT Date, Dividend FROM dividends WHERE Ticker="' + ticker + '" and Date >= "' + args.startdate.strftime('%Y-%m-%d') + '" and Date <= "' + args.enddate.strftime('%Y-%m-%d') + '"')
                all_dividends = cur.fetchall()
            except Exception as e:
                print('Failed to load dividends from database:')
                print(e)
            finally:
                cnx.close()

            if len(all_quotes)==0:
                print("No quotes available for the period specified.")
                sys.exit(0)

            start_date=dt.datetime.strptime(all_quotes[0][0], '%Y-%m-%d')
            end_date=dt.datetime.strptime(all_quotes[len(all_quotes)-1][0], '%Y-%m-%d')
            start_price=all_quotes[0][1]
            end_price=all_quotes[len(all_quotes)-1][1]

            total_dividend=0
            if len(all_dividends)!=0:
                total_dividend=sumColumn(all_dividends, 1)

            # Cumulative Return
            # -----------------
            cum_return_percentage=cum_return_percentage+((((end_price+total_dividend)/start_price)-1)*allocation)

            # Annual Return (or CAGR)
            # -----------------------
            diffyears=end_date.year - start_date.year
            difference=end_date - start_date.replace(end_date.year)
            days_in_year=isleap(end_date.year) and 366 or 365
            number_years=diffyears + difference.days/days_in_year
            annual_return=annual_return+((pow(((end_price+total_dividend)/start_price),(1/number_years))-1)*allocation)

            # Annual Volatity
            # ---------------
            prices=list(zip(*all_quotes))[1]
            df = pd.DataFrame({'Close':list(prices)})
            annual_volatility=np.std(df['Close'].pct_change()*100)*mt.sqrt(252)
            annual_variance=annual_variance+(annual_volatility**2)*((allocation/100)**2)

        if total_allocation != 100:
            print("Portfolio total asset allocation must be equal to 100")
            sys.exit(0)

        annual_volatility=math.sqrt(annual_variance)
        output_report[1].append(dt.datetime.strftime(start_date, '%Y-%m-%d'))
        output_report[2].append(dt.datetime.strftime(end_date, '%Y-%m-%d'))
        output_report[4].append("%.2f %%" % cum_return_percentage)
        output_report[5].append("%.2f %%" % annual_return)
        output_report[6].append("%.2f %%" % annual_volatility)
print("")
print(tabulate(output_report,headers,tablefmt='orgtbl'))
