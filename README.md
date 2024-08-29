# PortfolioCalculator

## Description
PortfolioCalculator App Description
The app PortfolioCalculator is created for educational reasons and is getting data from publicly available open-source APIs and libraries: Frankfurter API and yfinance 0.2.43.

PortfolioCalculator has the following features:

Create user
Login / Logout
Change Password
Each user can create /delete Portfolios (title, date created)
Portfolio title can be changed
Portfolios can contain Items (ticker, quantity)
Each user can add / edit / delete items to/from Portfolios
Each user can see and manipulate only his Portfolios and Items
When entering new Item ticker name, PortfolioCalculator checks this Ticker existence in yfinance library
If ticker name does not exist, the corresponding message appears
If Items with same ticker name already exists in this Portfolio, the corresponding message appears
Three operations can be performed with PortfolioCalculator with Currencies available from Frankfurter API: get Portfolio current price, get Portfolio historical prices within 1-year at 1-month interval and get gain from the beginning of each month within last year.
Get Portfolio current price: returns table with Portfolios each ticker current market price, currency, total ticker price, exchange rate to base currency, total ticker price in base currency, total Portfolio price in base currency, date and time of request. Also method returns a pie chart of all Portfolio tickers with values, percentage in portfolio.
Get Portfolio historical prices within 1-year at 1-month interval
Get gain from the beginning of each month within last year.
IMPORTANT: correct ticker names you should look on https://finance.yahoo.com/ internet page. Just write the Company name in Search bar on the top of the page, select the appropriate ticker, corresponding your company and fill in the field when adding tickers.

Here you can find detailed information about ticker symbol definition.

Additional possible features to include in the future:

Make that the lit for Currency selection would be obtained from Frankfurter API
Make that ticker also contain information about when and for what price it was bought, and each time it is bought the average bought price and average currency exchange rate calculated.
When we would hav average price and exchange rate we can make method to calculate gain correspondingly to the buy price
Make that when new user is created that profile would also be created (with signals)
Make method to obtain dividends from every ticker and total dividends
Make method to enter the date and then calculate the gain from entered date to current date.
Make intraday app to calculate history and gain during the day session.

*** IMPORTANT LEGAL DISCLAIMER *** Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. yfinance is not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. You should refer to Yahoo!'s terms of use (https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm, https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html, and https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html) for details on your rights to use the actual data downloaded. Remember - the Yahoo! finance API is intended for personal use only.

Legal Stuff yfinance is distributed under the Apache Software License. See the LICENSE.txt file in the release for details. AGAIN - yfinance is not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. You should refer to Yahoo!'s terms of use (https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm, https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html, and https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html) for details on your rights to use the actual data downloaded.

For yfinance documentation please follow this https://pypi.org/project/yfinance/.

Frankfurter is an open-source API for current and historical foreign exchange rates published by the European Central Bank

For Frankfurter API documentation please follow this https://www.frankfurter.app/docs/.

## Installation
Instructions on how to install and set up your project.

```bash
# Clone the repository
git clone https://github.com/Pavlucio/PortfolioCalculator.git

# Navigate to the project directory
cd your-repository

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the dependencies
pip install -r requirements.txt
