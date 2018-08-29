import datetime as dt
import sqlite3 as db
import argparse
from dateutil.relativedelta import relativedelta
import sys
import pandas as pd
from calendar import isleap

parser = argparse.ArgumentParser()
parser.add_argument("ticker", nargs='+', help="Specify the ETF ticker")
parser.add_argument("-s", "--startdate", type=lambda d: dt.datetime.strptime(d, '%Y-%m-%d'), help="Specify start date for backtest period (YYYY-mm-dd)")
parser.add_argument("-e", "--enddate", type=lambda d: dt.datetime.strptime(d, '%Y-%m-%d'), help="Specify end date for backtest period (YYYY-mm-dd)")
args=parser.parse_args()

if args.startdate == None:
    args.startdate=dt.datetime(1970, 1, 1)

if args.enddate == None:
    args.enddate=dt.datetime.now()

print(args.startdate)

for ticker in args.ticker:
    try:
        cnx = db.connect('database/etfs.db')
        cur = cnx.cursor()
        cur.execute('SELECT Date, Close FROM quotes WHERE Ticker="' + ticker + '" and Date >= "' + args.startdate.strftime('%Y-%m-%d') + '" and Date <= "' + args.enddate.strftime('%Y-%m-%d') + '"')
        all_rows = cur.fetchall()
    except Exception as e:
        print('Failed to load quotes from database:')
        print(e)
    finally:
        cnx.close()

    if len(all_rows)==0:
        print("No quotes available for the period specified.")
        sys.exit(0)

    start_date=dt.datetime.strptime(all_rows[0][0], '%Y-%m-%d')
    end_date=dt.datetime.strptime(all_rows[len(all_rows)-1][0], '%Y-%m-%d')
    start_price=all_rows[0][1]
    end_price=all_rows[len(all_rows)-1][1]

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
    cum_return_percentage=((end_price/start_price) - 1)*100

    # Annual Return (or CAGR)
    # -----------------------
    # The Cumulative Return is a good measure to know the total return of an
    # investement and to compare two investments if they occurred on the same
    # period of time. A better measure of return is the Annual Return (or CAGR) 
    # because it calculate the return of the investment over a long period of
    # times (usually years) annually.
    # Suppose you have 100$ invested over 4 years and at the end of 4th year 
    # sold everything at 146.41$.you 
    #
    # Initial capital: 100$
    # 2007: 110.00$ -> 10% earning
    # 2008: 121.00$ -> 10% earning
    # 2008: 133.10$ -> 10% earning
    # 2009: 146.41$ -> 10% earning
    # 
    # Your Cumulative earning was 46.41$ for a Cumulative Return of 46.41%. 
    # Now if you try to divide the cumulative return by 4 you get:
    #
    # Cumulative Return/4=11.60%
    #
    # As you can see this is not a measure of the Annual Return because it 
    # does not take in consideration the compound interest. In fact, this 
    # formula measure the so called Average Annual Return.
    #
    # Average Annual Return=Cumulative Return/N
    #
    # where N is the number of years. In a time series where start date is not 
    # exactly January 1st and end date exactly the December 31th you should 
    # count the number of years plus the additional days. For example, in a 
    # date frame of Semptember 10th 2007 to February 10th 2011 we have 3 years 
    # and 122 days. 
    # 122 days=122/365=0.33 years so N=3.33 years.
    #
    # The formula to calculate the Annual Return is:
    # Annual Return=(Final Capital/Initial Capital)^(1/N)-1
    #
    # Let's apply the formula to the above example.
    #
    # Annual Return=(146.41/100)^(1/4)-1=0,10
    #
    # Multiplying this value for 100 we get the original 10% growth rate you 
    # observed at the beginning of the example. Also for this formula are valid 
    # the considerations about N when we have a date frame that is not perfectly
    # a multiple of one year.

    # Since we already have the start and end price, to calculate the annual 
    # return we need only to calculate N
    diffyears=end_date.year - start_date.year
    difference=end_date - start_date.replace(end_date.year)
    days_in_year=isleap(end_date.year) and 366 or 365
    number_years=diffyears + difference.days/days_in_year
    annual_return=(pow((end_price/start_price),(1/number_years))-1)*100

    print("")
    print("Backtest " + ticker)
    print("-------------------------")
    print("")
    print("-------------------------")
    print("Start date  | " + dt.datetime.strftime(start_date, '%Y-%m-%d'))
    print("End date    | " + dt.datetime.strftime(end_date, '%Y-%m-%d'))
    print("-------------------------")
    print("Cum. return | %.2f %%" % cum_return_percentage)
    print("Ann. return | %.2f %%" % annual_return)
    print("-------------------------")
