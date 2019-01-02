#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This script takes a CSV containing stock tickers, creates a filesystem with a directory for each ticker if does not already exist 
counts the number of tickers in the csv, puts them all in a list, slices the aggregate ticker list into 100 ticker batches,
converts a batch to a string, inserts that string into a url request for the iEX api to fetch realtime pricing and volume data.
iEX then returns a JSON load, the script parses the JSON load and populates the ticker file system.
'''

###############
__author__ = "Makoa Santarini"
__copyright__ = "Copyright 2018"
__credits__ = ["Makoa Santarini"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Makoa Santarini"
__email__ = "makoa@makoasystems.com"
__status__ = "Production"
###################

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

# batch request makes the actual batch request to iex and returns JSON

def dataRequest(batchReq):
        response = requests.get('https://api.iextrading.com/1.0/stock/market/batch?symbols=' + str(batchReq)+ '&types=quote,stats')
        jsonLoad = json.loads(response.text)
        return jsonLoad

# jsonParsetoCSV takes the resulting JSON load from dataRequest and parses it
        
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

#start a timer for program so we can see how long it takes
        
start_time = time.time()

#create source folder if it doesnt exist yet
if not os.path.exists('StockDatabase'):
    os.makedirs('StockDatabase')

#open csv containing tickers

with open("nyselist.csv", encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    allTickers = list(reader)
    tickerCount = len(allTickers)
    QtyHundreds = tickerCount/100
    i = 0

    #If there are more than 100 tickers, dice them up into 100 ticker batches

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
    
    #If there are less than 100 tickers perform a batch request

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

#stop timer

elapsed_time = time.time() - start_time
print("Program completed in "+ str(round(elapsed_time, 3)) + " seconds. " + str(round(i/tickerCount * 100, 2)) + "% complete.")
print("Program executed at an average " + str(round(tickerCount/elapsed_time, 2)) + " tickers per second.")
