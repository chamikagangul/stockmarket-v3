import yfinance as yf

import os,csv
import talib
import pandas as pd
from flask import Flask , render_template ,request
from patterns import patterns



app = Flask(__name__)

@app.route('/')
def index():
    pattern = request.args.get('pattern',None)
    stocks = {}

    with open("./datasets/companies.csv") as f:
        for raw in csv.reader(f):
            stocks[raw[0]] = {'company' : raw[1]}

    if pattern:
        datafiles = os.listdir('./datasets/daily')
        for datafile in datafiles:
            df = pd.read_csv('./datasets/daily/'+datafile)
            pattern_function  = getattr(talib , pattern )

            symbol = datafile.split(".")[0]
            try:
                results = pattern_function(df["Open"], df["High"],df["Low"], df["Close"])
                last = results.tail(1).values[0]
                #print(last)
                if last>0:
                    stocks[symbol][pattern] = "bullish" 
                elif last<0:
                    stocks[symbol][pattern] = "berish" 
                else:
                    stocks[symbol][pattern] = None
                    #print("{} trigerd {} value : {}".format(datafile,pattern,last))
            except:
                pass

    return render_template('/index.html',patterns = patterns,stocks = stocks,c_pattern=pattern)



@app.route('/snapshot')
def snapshot():
    with open("./datasets/companies.csv") as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            df = yf.download(symbol, start="2020-01-01", end="2021-01-03")
            df.to_csv('datasets/daily/'+symbol+".csv")

    return 'symbols'



app.run("0.0.0.0",5000)