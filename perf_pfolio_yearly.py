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

def sumColumn(m):
    total = 0
    for row in range(len(m)):
        total += m[row]
    return total

parser = argparse.ArgumentParser()
parser.add_argument("portfolio", nargs='+', help="Specify the Portfolio name")
parser.add_argument("-s", "--startdate", type=lambda d: dt.datetime.strptime(d, '%Y-%m-%d'), help="Specify start date for backtest period (YYYY-mm-dd)")
parser.add_argument("-e", "--enddate", type=lambda d: dt.datetime.strptime(d, '%Y-%m-%d'), help="Specify end date for backtest period (YYYY-mm-dd)")
args=parser.parse_args()

if args.startdate == None:
    args.startdate=dt.datetime(1970, 1, 1)

if args.enddate == None:
    args.enddate=dt.datetime.now()

output_report = [["2019"], ["2018"], ["2017"], ["2016"], ["2015"], ["2014"], ["2013"], ["2012"], ["2011"], ["2010"], ["2009"], ["2008"], ["2007"], ["2006"], ["2005"]]
headers=['Backtest']

for portfolio in args.portfolio:
    headers.append(portfolio)
    with open('pfolio/' + portfolio + '.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        total_allocation=0

        for row in reader:
            ticker=row['Ticker']
            print(ticker)
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

            if len(all_quotes)==0:
                print("No quotes available for the period specified.")
                sys.exit(0)

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

            only_dates=[row[0] for row in all_quotes]
            years_list = list(dict.fromkeys([dt.datetime.strptime(date, '%Y-%m-%d').year for date in only_dates]))[::-1]
            df_quotes = pd.DataFrame(all_quotes, columns = ["Date", "Close"])
            df_dividends= pd.DataFrame(all_dividends, columns = ["Date", "Dividend"])
            index = 0
            for year in years_list:
                start_date=dt.datetime(year, 1, 1)
                end_date=dt.datetime(year, 12, 31)
                year_df_quotes=df_quotes.loc[(df_quotes['Date'] >= start_date.strftime("%Y-%m-%d")) & (df_quotes['Date'] <= end_date.strftime("%Y-%m-%d"))]
                start_price=year_df_quotes['Close'].values[0]
                end_price=year_df_quotes['Close'].values[-1]

                year_df_dividends=df_dividends.loc[(df_dividends['Date'] >= start_date.strftime("%Y-%m-%d")) & (df_dividends['Date'] <= end_date.strftime("%Y-%m-%d"))]

                total_dividend=0
                if len(all_dividends)!=0:
                    total_dividend=sumColumn(year_df_dividends['Dividend'].tolist())

                # Cumulative Return
                # -----------------
                # Cumulative return is the percentage of total earning from start to finish
                # of the investment. For example, if you invested 1000$ on September 10th
                # 2007 and you sold everything in February 10th 2011 at a prince of 1300$
                # 1300$ you had a cumulative return of 30%.
                #
                # The formula to calculate the cumulative return is:
                # (end price/start price) -1
                # If you want the percentage number multiply the result for 100.
                cum_return_percentage=((((end_price+total_dividend)/start_price)-1)*allocation)
                print(output_report[index])
                output_report[index].append("%.2f %%" % cum_return_percentage)
                index+=1
        print("")
        for i in range(index,len(output_report)):
            output_report[i].append(" -- ")
print("")
print(tabulate(output_report,headers,tablefmt='orgtbl'))
