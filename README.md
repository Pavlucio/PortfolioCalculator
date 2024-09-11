# PortfolioCalculator

## Description
This project is a web-based application designed to allow users to create multiple stock market portfolio prototypes. 

Key features include:
	- User authentication and authorization
	- CRUD portfolios and portfolio items (stocks)
	- Get portfolio current price.
	- Get portfolio historical data in 1-year period montly.
	- Get portfolio absolute and relative gain in 1-year period montly.
	- Possibility to select base currency to perform above methods.

PortfolioCalculator is created for educational reasons and is getting data from publicly available open-source APIs and libraries: Frankfurter API and yfinance 0.2.43.


## Installation
Instructions on how to install and set up your project.

```bash
# Clone the repository
git clone https://github.com/pavelta123/PortfolioCalculator.git

# Navigate to the project directory
cd your-repository

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the dependencies
pip install -r requirements.txt

# Run migrations to create necessary databse tables
python manage.py migrate
```
## Usage
Instructions on how to run the project.

```bash
# To run the project, use:
python manage.py runserver
```
## License

PortfolioCalculator is created for educational reasons and is getting data from publicly available open-source APIs and libraries: Frankfurter API and yfinance 0.2.43.

*** IMPORTANT LEGAL DISCLAIMER *** Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc. yfinance is not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. You should refer to Yahoo!'s terms of use (https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm, https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html, and https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html) for details on your rights to use the actual data downloaded. Remember - the Yahoo! finance API is intended for personal use only.

Legal Stuff yfinance is distributed under the Apache Software License. See the LICENSE.txt file in the release for details. AGAIN - yfinance is not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes. You should refer to Yahoo!'s terms of use (https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm, https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html, and https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html) for details on your rights to use the actual data downloaded.

For yfinance documentation please follow this https://pypi.org/project/yfinance/.

Frankfurter is an open-source API for current and historical foreign exchange rates published by the European Central Bank

For Frankfurter API documentation please follow link https://www.frankfurter.app/docs/.


## Contact Information
Pavel Taranenko
taranenko.pavel@gmail.com
