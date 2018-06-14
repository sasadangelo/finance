import sqlite3 as db
import csv
import os

try:
    cnx = db.connect('database/etfs.db')

    cur = cnx.cursor()
    cur.execute('DROP TABLE IF EXISTS etfs;')

    sql = '''CREATE TABLE etfs ('Ticker' TEXT primary key, \
        'Name' TEXT, 'ISIN' TEXT, 'LaunchDate' TEXT, \
        'Capital' REAL, 'Replication' TEXT, 'Volatility' REAL, \
        'Currency' TEXT, 'Dividend' TEXT, 'DividendFrequency' INTEGER, 'Yeld' REAL)'''     

    cur.execute(sql)

    print("Import ETF ...")
    with open('database/ETF.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        to_db = [(row['Name'], row['ISIN'], row['Ticker'], row['LaunchDate'], row['Capital'], row['Replication'], \
            row['Volatility'], row['Currency'], row['Dividend'], row['DividendFrequency'], row['Yeld']) for row in reader]
    cur.executemany("INSERT INTO etfs (Name, ISIN, Ticker, LaunchDate, Capital, Replication, Volatility, \
        Currency, Dividend, DividendFrequency, Yeld) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)

    print("Import Quotes ...")
    cur.execute('DROP TABLE IF EXISTS quotes;')

    sql = '''CREATE TABLE quotes ('Ticker' TEXT, 'Date' REAL, 'Open' REAL, 'High' REAL, 'Low' REAL, 'Close' REAL, \
        'Adj_Close' REAL, 'Volume' REAL, PRIMARY KEY('Ticker', 'Date'), FOREIGN KEY('Ticker') REFERENCES etfs('Ticker'))'''

    cur.execute(sql)

    for etf_quotes_csv in os.listdir('database/quotes'):
        ticker = etf_quotes_csv[:-4]
        print('Import quotes for ETF: ' + ticker)
        with open('database/quotes/' + etf_quotes_csv) as csvfile:
            reader = csv.DictReader(csvfile)
            to_db = [(row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], \
                row['Volume']) for row in reader]
        for i in range(len(to_db)):
            to_db[i] = (ticker,) + to_db[i]
        cur.executemany("INSERT INTO quotes (Ticker, Date, Open, High, Low, Close, Adj_Close, Volume) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    cnx.commit()
except Exception as e:
    print('Exception:')
    print(e)
finally:
    cnx.close()
