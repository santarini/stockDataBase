# stockDataBase

Uses IEX to fetch stock data for each ticker iin all the american exchanges.


Work computer test:

Fetched 6294 tickers in 56.782 seconds. Average 110.85 tickers per second.


## To Do
- [x] Strip() spaces from input tickers
- [x] Error handling for tickers not tracked by iEX
- [ ] If ticker file exists append existing file, else create new
- [x] Make it so script can execute with column headers and other columns present
- [x] Code comments so it's clearer what the hell is going on where


## Tickersets

The <a href="http://www.nasdaq.com/screening/company-list.aspx">NASDAQ website</a> does a great job of maintaining up-to-date CSVs containing all the tickers listed on the NYSE, NASDAQ, or AMEX.

Here's a list of direct download links by exchange:
<ul>
  <li><a href="https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download">NYSE</a></li>
  <li><a href="https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download">NASDAQ</a></li>
  <li><a href="https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download">AMEX</a></li>
  <li><a href="https://www.nasdaq.com/investing/etfs/etf-finder-results.aspx?download=Yes">ETFs</a></li>
</ul>

I also have a <a href="https://github.com/santarini/batch-stock-scrape/blob/master/sandp500.csv">S&P 500 csv</a> up here. It may or may not be up-to-date), I haven't spent a lot of time working on error handling, so if you run into a snag using this list it may because the ticker changed or doesn't exist or something.


## Tasks

- [ ] Append and updated ticker csv as tickers get added, removed and changed.

- [ ] Create a schedule for the program to operate during market hours
