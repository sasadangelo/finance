import pandas as pd

def test_run():
    start_date='2017-01-22'
    end_date='2017-01-26'
    dates=pd.date_range(start_date, end_date)
    df1=pd.DataFrame(index=dates)

    dfCW8 = pd.read_csv("../database/quotes/CW8.MI.csv",index_col="Date",
                        parse_dates=True,usecols=["Date","Adj Close"],
                        na_values=['nan'])
    dfCW8 = dfCW8.rename(columns={'Adj Close': 'CW8.MI'})
    df1=df1.join(dfCW8, how='inner')
    #df1=df1.dropna()

    symbols=['IWRD.MI', 'WLD.MI']

    for symbol in symbols:
        df_temp = pd.read_csv("../database/quotes/" + symbol + ".csv",index_col="Date",
                                 parse_dates=True,usecols=["Date","Adj Close"],
                                 na_values=['nan'])
        df_temp=df_temp.rename(columns={'Adj Close': symbol})
        df1=df1.join(df_temp)
    print(df1)

if __name__ == "__main__":
    test_run()
