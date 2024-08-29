import os
import numpy as np
import yfinance as yf
import requests
import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from portfolio_project import settings


def convert_to_data(portfolio, data):
    """
    This method converts selected class Portfolio object from database to the dictionary which is suitable for class for
    below class Calculator methods:current_portfolio_value, get_history, get_gain
    :param portfolio: selected class 'portfolio_app.models.Portfolio'
    :param data: empty dictionary with pre-defined initial structure data = {'stocks': {}}
    :return: dictionary with ticker names as a keys and quantities as a values.
    """

    for stock in portfolio.stocks.all():
        data['stocks'][stock.ticker] = {'amount': stock.quantity}
    return data

class Calculator:

    def __init__(self, data, base_currency):
        """
        When creating class Calculator object we are initializing data and base currency variables. Data is
         Portfolio item data necessary for calculations. base_currency is a currency in which our results will
          be expressed.
        :param data: dictionary with ticker names as a keys and quantities as a values;
        :param base_currency: currency code, string.
        """
        self.data = data
        self.base_currency = base_currency

    def current_portfolio_value(self):
        """
        Mainly this method is necessary to return a dataframe with information of Portfolio tickers current prices,
        sum prices, total price in base currency, as well as additional important current information.
        :return:    df - dataframe for method get_gain();
                    df_app - dataframe for current_portfolio_value method;
                    portfolio_value - float, total current portfolio value;
                    time_of_request - date and time of request, datetime object;
                    image_name - string of image name (pie chart).
        """
        exchange_rates = self.get_rates(self.base_currency)

        portfolio_ticker_list = []
        amount_list = []
        stock_currency_list = []
        stock_current_price_list = []
        sum_per_stock_list = []
        exchange_rate_list = []
        sum_per_stock_base_currency_list = []

        time_of_request = self.get_date_time()
        date_time_str = datetime.datetime.strftime(time_of_request, '%Y%m%d_%H%M%S')

        file_name = f'portfolio_value_{date_time_str}.csv'

        with open(file_name, 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['Ticker', 'Quantity', 'Ticker currency', 'Current Price', 'totalPerShare', 'Exchange rate',
                             f'totalPerShare, {self.base_currency}'])

        for stock in self.data['stocks']:
            ticker_yahoo = yf.Ticker(stock)

            stock_current_price = ticker_yahoo.info['currentPrice']
            stock_currency = ticker_yahoo.info['currency']
            if stock_currency != self.base_currency:
                exchange_rate = exchange_rates['rates'][stock_currency]
            else:
                exchange_rate = 1.0
            amount = self.data['stocks'][stock]['amount']
            sum_per_stock = round(stock_current_price * amount, 2)
            sum_per_stock_base_currency = round(sum_per_stock / exchange_rate, 2)

            portfolio_ticker_list.append(stock)
            amount_list.append(amount)
            stock_currency_list.append(stock_currency)
            stock_current_price_list.append(stock_current_price)
            sum_per_stock_list.append(sum_per_stock)
            exchange_rate_list.append(exchange_rate)
            sum_per_stock_base_currency_list.append(sum_per_stock_base_currency)

            with open(file_name, 'a') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow([stock, amount, stock_currency, stock_current_price, sum_per_stock, exchange_rate,
                                 sum_per_stock_base_currency])

        portfolio_value = round(sum(sum_per_stock_base_currency_list), 2)

        with open(file_name, 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([''])
            writer.writerow(['currentPortfolioValue:', portfolio_value, self.base_currency, 'timeOfRequest:',
                             time_of_request])

        date_to_str = time_of_request.strftime('%Y-%m-%d')
        date_datetime = datetime.datetime.strptime(date_to_str, '%Y-%m-%d')

        df = pd.DataFrame({
            'Date': portfolio_ticker_list,
            f'{date_datetime}': sum_per_stock_base_currency_list
        })

        df_app = pd.DataFrame({
            'Ticker': portfolio_ticker_list,
            'Amount': amount_list,
            'Ticker currency': stock_currency_list,
            'Current Price': stock_current_price_list,
            'Sum per ticker': sum_per_stock_list,
            'Exchange rate': exchange_rate_list,
            f'Sum per ticker {self.base_currency}': sum_per_stock_base_currency_list,
        })

        plt.figure(figsize=(8, 8))
        plt.title(f'Total portfolio value: {portfolio_value} {self.base_currency} {time_of_request}')
        plt.pie(df[f'{date_datetime}'], labels=df['Date'],
                autopct=lambda pct: '{:.2f}% ({:.2f} {})'.format(pct, ((pct/100)*portfolio_value), self.base_currency),
                pctdistance=1.2, labeldistance=.6, explode=(np.ones(len(portfolio_ticker_list))*0.05), shadow=True)
        image_name = f'pie_portfolio_value_{date_time_str}.png'
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        plt.savefig(image_path)

        return df, df_app, portfolio_value, time_of_request, image_name

    def get_history(self):
        """
        get_history method is necessary to return historical information of ticker sum prices, and total price within
        previous 1-year period on 1-month interval, all in selected base currency.
        :return:    portfolio_history - dataframe with historical values of each ticker and historical total values;
                    image_1_name - string of image name (stackplot);
                    image_2_name - string of image name (plot).
        """

        new_dates_of_period_str = []
        new_dates_of_period = []

        for stock in self.data['stocks']:
            ticker_yahoo = yf.Ticker(stock)
            dates_of_period = ticker_yahoo.history(period='1y', interval='1mo').index.values

            for date in dates_of_period:
                time_to_datetime = pd.to_datetime(date)
                if time_to_datetime.day == 1:
                    time_to_datetime = time_to_datetime - datetime.timedelta(days=1)
                date_to_str = time_to_datetime.strftime('%Y-%m-%d')
                new_dates_of_period_str.append(date_to_str)
                date_datetime = datetime.datetime.strptime(date_to_str, '%Y-%m-%d')
                new_dates_of_period.append(date_datetime)
            break

        start_date = new_dates_of_period_str[0]
        end_date = new_dates_of_period_str[-1]
        exchange_rates = self.get_rates_by_date(self.base_currency, start_date, end_date)

        portfolio_history = pd.DataFrame(data=new_dates_of_period, columns=['Date'])
        portfolio_history.set_index('Date', inplace=True)

        for stock in self.data['stocks']:

            ticker_yahoo = yf.Ticker(stock)

            history_data = ticker_yahoo.history(period='1y', interval='1mo')[['Close']].copy()
            ticker_dates = ticker_yahoo.history(period='1y', interval='1mo').index.values

            new_ticker_dates = []

            for date in ticker_dates:
                time_to_datetime = pd.to_datetime(date)
                if time_to_datetime.day == 1:
                    time_to_datetime = time_to_datetime - datetime.timedelta(days=1)
                date_to_str = time_to_datetime.strftime('%Y-%m-%d')
                date_datetime = datetime.datetime.strptime(date_to_str, '%Y-%m-%d')
                new_ticker_dates.append(date_datetime)

            history_data['Dates'] = new_ticker_dates
            history_data.set_index('Dates', inplace=True)
            portfolio_history[stock] = history_data['Close']

        portfolio_history.fillna(value=portfolio_history.mean(), inplace=True)

        portfolio_history_column_names = portfolio_history.columns
        portfolio_history_dates = portfolio_history.index

        for stock in portfolio_history_column_names:
            ticker_yahoo = yf.Ticker(stock)
            stock_currency = ticker_yahoo.info['currency']
            amount = self.data['stocks'][stock]['amount']
            for date in portfolio_history_dates:
                time_to_datetime = pd.to_datetime(date)
                if time_to_datetime.day == 1:
                    time_to_datetime = time_to_datetime - datetime.timedelta(days=1)
                date_to_str = time_to_datetime.strftime('%Y-%m-%d')

                if stock_currency != self.base_currency:
                    while True:
                        try:
                            exchange_rate = exchange_rates['rates'][date_to_str][stock_currency]
                            break
                        except KeyError:
                            time_to_datetime -= datetime.timedelta(days=1)
                            date_to_str = time_to_datetime.strftime('%Y-%m-%d')
                else:
                    exchange_rate = 1.0
                portfolio_history.loc[date, stock] = round(portfolio_history.loc[date, stock] * amount / exchange_rate, 2)

        ticker_labels = list(portfolio_history_column_names)

        time_of_request = self.get_date_time()
        date_time_str = datetime.datetime.strftime(time_of_request, '%Y%m%d_%H%M%S')

        plt.figure()
        plt.grid(True)
        plt.stackplot(portfolio_history.index, portfolio_history.transpose(), labels=ticker_labels)
        plt.legend(loc='upper left')
        plt.title('Portfolio total price stacked by Ticker')
        plt.xlabel('Time')
        plt.ylabel(f'Price, {self.base_currency}')
        image_1_name = f'portfolio_history_stackplot_{date_time_str}.png'
        image_1_path = os.path.join(settings.MEDIA_ROOT, image_1_name)
        plt.savefig(image_1_path)

        portfolio_history['Sum'] = round(portfolio_history.sum(axis=1), 2)

        plt.figure()
        plt.plot(portfolio_history.index, portfolio_history['Sum'])
        plt.grid(True)
        plt.title('Portfolio total price, 1Y period')
        plt.xlabel('Time')
        plt.ylabel(f'Price, {self.base_currency}')
        image_2_name = f'portfolio_history_sum_{date_time_str}.png'
        image_2_path = os.path.join(settings.MEDIA_ROOT, image_2_name)
        plt.savefig(image_2_path)

        portfolio_history.to_csv(f'portfolio_1Y_data_{date_time_str}.csv', encoding='utf-8')

        return portfolio_history, image_1_name, image_2_name

    def get_gain(self):
        """
        get_gain method is for returning the gain/loss of each ticker sums and total sum from each month until now within
        previous 1-year period, both absolute values in base currency and relative percentage values (calculations
        are also based on convertion of data into base currency).
            :return:    data_gain_abs - dataframe of absolute gain / loss of each ticker and total portfolio from each
            month within year before now in base currency;
                        data_gain - dataframe of relative gain / loss (percentage) of each ticker and total portfolio
                         from each month within year before now (compares current data with each month data, all
                          converted to base currency);
                        image_3_name - string name of image (absolute),
                        image_4_name - string name of image (relative)
        """
        time_of_request = self.get_date_time()
        date_time_str = datetime.datetime.strftime(time_of_request, '%Y%m%d_%H%M%S')

        current_data, _, _, _, _ = self.current_portfolio_value()
        current_data_transposed = current_data.set_index('Date').T
        current_data_transposed['Sum'] = current_data_transposed.sum(axis=1)

        data_history, _, _ = self.get_history()

        data_gain_abs = data_history.copy()
        data_gain = data_history.copy()

        column_names = data_gain.columns
        dates = data_gain.index

        for stock in column_names:
            stock_current_price = float(current_data_transposed[stock].iloc[0])
            for date in dates:
                data_gain_abs.loc[date, stock] = round((stock_current_price - data_gain.loc[date, stock]), 2)
                data_gain.loc[date, stock] = round(((stock_current_price - data_gain.loc[date, stock]) / data_gain.loc[date, stock] * 100), 1)

        data_gain_abs_reverse = data_gain_abs.iloc[::-1]
        data_gain_reverse = data_gain.iloc[::-1]

        plt.figure()
        colors = ['green' if value > 0 else 'red' for value in data_gain_abs_reverse['Sum']]
        plt.bar(data_gain_abs_reverse.index, data_gain_abs_reverse['Sum'], color=colors, width=20)
        plt.grid(True)
        plt.xlabel('Dates')
        plt.ylabel(f'Absolute Gain / Loss {self.base_currency}')
        plt.title(f'Absolute Gain/Loss from each month within last year, {self.base_currency}')
        image_3_name = f'portfolio_gain_absolute_{date_time_str}.png'
        image_3_path = os.path.join(settings.MEDIA_ROOT, image_3_name)
        plt.savefig(image_3_path)

        plt.figure()
        colors = ['green' if value > 0 else 'red' for value in data_gain_reverse['Sum']]
        plt.bar(data_gain_reverse.index, data_gain_reverse['Sum'], color=colors, width=20)
        plt.grid(True)
        plt.xlabel('Dates')
        plt.ylabel(f'Absolute Gain / Loss, %')
        plt.title(f'Relative Gain/Loss from each month within last year, %')
        image_4_name = f'portfolio_gain_percent_{date_time_str}.png'
        image_4_path = os.path.join(settings.MEDIA_ROOT, image_4_name)
        plt.savefig(image_4_path)

        return data_gain_abs, data_gain, image_3_name, image_4_name

    def get_rates(self, currency):
        """
        This method returns dictionary with latest exchange rates of all available currency relatively to the bas
         currency.
        :param currency: currency code, string
        :return: latest (today) exchange rate from Frankfurter API, dictionary
        """
        response = requests.get(f'https://api.frankfurter.app/latest?from={currency}')
        exchange_rates_dict = response.json()
        return exchange_rates_dict

    def get_rates_by_date(self, currency, start, end):
        """
        This method returns dictionary with all exchange rates of working days from the whole period between start and
         end dates of all available currency relatively to the base currency.
        :param currency: currency: currency code, string
        :param start: start date, string
        :param end: end date, string
        :return: exchange rates for every working day in period from start to end from Frankfurter API, dictionary
        """
        response = requests.get(f'https://api.frankfurter.app/{start}..{end}?from={currency}')
        exchange_rates_dict = response.json()
        return exchange_rates_dict

    def get_date_time(self):
        """
        This method is for getting current time and date in local timezone
        :return: returns current date and time in datetime format
        """
        tzinfo = datetime.timezone(datetime.timedelta(hours=3))
        time_of_request = datetime.datetime.now(tzinfo)
        return time_of_request
