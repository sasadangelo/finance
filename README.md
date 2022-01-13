# ETF Finance

This is an ongoing project I am working on to monitor ETF performance. Currently my database contains only few ETFs on Italian market. 

Currently, you have a set of very simple python script where each one has a very small goal:
* **download.py**: download quotes for ETF listed in the CSV file database/ETF.csv.
* **update_quotes.py**: update quotes for ETF listed in the CSV file database/ETF.csv.
* **graph.py**: create the chart for a given ETF for a given period of time. Mobile average can be drawn too.
* **perf.py**: calculate return and risk for one or more ETF for a given period of time.

# How to use

Here the command to download the project and run it:

```
git clone https://github.com/sasadangelo/finance
cd finance
pip3 install pandas --user
pip3 install pandas_datareader --user
pip3 install yfinance --user
pip3 install matplotlib --user
pip3 install tabulate --user
```

The project include the file database/ETF.csv where you should insert the ETF you are interested in. The project already has the quotes for ETF listed in database/ETF.csv file but if you insert a new ETF you need to download its quotes with the following command:

```
python3 download.py <ticker>
```

You can update quotes for all the ETF in database/ETF.csv with the following command:

```
./update_quotes.sh
```

Once you have all ETF with all quotes downloaded in database/quotes/\*.csv you can import them in the database **databse/etfs.db** with the following command:

```
python3 import.py
```

You can view the chart for a single ETF using the following command:

```
python3 graph.py [-p {Max,5Y,1Y,YTD,6M,3M,1M,5D}] [-m {5,10,20,50,100,200}] <ticker>
```

By default the python script draw the chart for the Max period but you can specify the period with the -p option. You can decide to draw the mobile average usng the -m option.

Finally, you can see performance (risk/return) of a single or multiple ETFs in terms of compound return, annual return and volatily with the command:

```
perf.py [-s STARTDATE] [-e ENDDATE] ticker [ticker ...]
```

the option -s and -e allow you to specify the period of time.
