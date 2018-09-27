import csv
import itertools
from itertools import zip_longest
import re
import os
import time
import datetime
import pandas_datareader.data as web
import requests
import json

batch = []

CurrentTicker = "AAPL"

def dataRequest(batchReq):
        response = requests.get('https://api.iextrading.com/1.0/stock/market/batch?symbols=' + str(batchReq)+ '&types=quote,stats')
        jsonLoad = json.loads(response.text)
        return jsonLoad
        #jsonParsetoCSV(jsonLoad, CurrentTicker)

def jsonParsetoCSV(jsonLoad, CurrentTicker):
    with open('StockDatabase/'+ str(CurrentTicker) + '.csv', 'a', encoding="utf-8") as csvfileA:
        fieldnames = ['Date','Time','Price', 'Volume', 'MktCap','SharesOut', 'SharesFloat']
        writer = csv.DictWriter(csvfileA, fieldnames=fieldnames, lineterminator = '\n')
        #to initialize database uncomment writeheader
        #writer.writeheader()
        latestTime = jsonLoad[CurrentTicker]['quote']['latestTime']
        latestPrice = jsonLoad[CurrentTicker]['quote']['latestPrice']
        latestVolume = jsonLoad[CurrentTicker]['quote']['latestVolume']
        marketcap = jsonLoad[CurrentTicker]['stats']['marketcap']
        sharesOutstanding = jsonLoad[CurrentTicker]['stats']['sharesOutstanding']
        sharesFloat = jsonLoad[CurrentTicker]['stats']['float']
        writer.writerow({'Date': datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),'Time': datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S.%f %Z"),'Price': str(latestPrice), 'Volume': str(latestVolume), 'MktCap': str(marketcap),'SharesOut': str(sharesOutstanding), 'SharesFloat': str(sharesFloat)})

start_time = time.time()

#create source folder if it doesnt exist yet
if not os.path.exists('StockDatabase'):
    os.makedirs('StockDatabase')

with open("AmericanTickers.csv", encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    allTickers = list(reader)
    tickerCount = len(allTickers)
    QtyHundreds = tickerCount/100
    i = 0
    if QtyHundreds > 1:
        j = 100
        while QtyHundreds > 1:
            for ticker in allTickers[i:j]:
                for innerStr in ticker:
                    batch.append(innerStr)
            batchReq = ",".join(batch)
            jsonLoad = dataRequest(batchReq)
            for ticker in allTickers[i:j]:
                for innerStr in ticker:
                    CurrentTicker = innerStr
                    jsonParsetoCSV(jsonLoad, CurrentTicker)
            i = i + 100
            j = j + 100
            QtyHundreds = QtyHundreds - 1
            batch = []
            elapsed_time = time.time() - start_time
            print(str(i) + " of " + str(tickerCount) + " tickers completed. " + str(round(i/tickerCount * 100, 2)) + "% complete. " + str(round(elapsed_time, 3))  + " seconds elapsed.")
                  
    if QtyHundreds <= 1:
        for ticker in allTickers[i:tickerCount]:
            for innerStr in ticker:
                batch.append(innerStr)
        batchReq = ",".join(batch)
        jsonLoad = dataRequest(batchReq)
        for ticker in allTickers[i:tickerCount]:
            for innerStr in ticker:
                CurrentTicker = innerStr
                jsonParsetoCSV(jsonLoad, CurrentTicker)
                i = i + 1
    elapsed_time = time.time() - start_time              
    print(str(i) + " of " + str(tickerCount) + " tickers completed. " + str(round(i/tickerCount * 100, 2)) + "% complete. " + str(round(elapsed_time, 3))  + " seconds elapsed.")

elapsed_time = time.time() - start_time
print("Program completed in "+ str(round(elapsed_time, 3)) + " seconds. " + str(round(i/tickerCount * 100, 2)) + "% complete.")
print("Program executed at an average " + str(round(tickerCount/elapsed_time, 2)) + " tickers per second.")
