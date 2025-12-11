import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import pickle


class StockDataLoader:
    """
    Handles data fetching and simple processing of ticker data
    """
    def __init__(self, tickers, start_date=None, end_date=None):
        if isinstance(tickers, list):
            self.tickers = tickers
        else:
            self.tickers = [tickers] # If passed a single stock convert it to a list

        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d') # Set the end date or default it to today if not provided
        self.start_date = start_date or (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d') # Set the start date or default it to 3 years ago if not provided
        self.data = {} # Create an empty dictionary to store the downloaded data


    """
    Collects historical data for all tickers
    """
    def fetch_data(self):
        for tickers in self.tickers:
            try:
                df = yf.download(tickers, self.start_date, self.end_date, progress=False, auto_adjust=True) # Auto adjust accounts for stock splits
                if df.empty: # No data found on the stock
                    continue
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0) # Flattens to simple columns of 'Close' and 'Open'
                self.data[tickers] = df

            except Exception as e:
                print(f'Error fetching {tickers}: {str(e)}')

        return self.data

    """
    Returns stock data on a specific ticker
    """
    def get_stock_data(self, ticker):
        return self.data.get(ticker)

    """
    Creates and returns daily percent change matrix for all tickers.
    Each value is percent change in stock price from the previous day.
    """
    def get_returns_matrix(self):
        return_dict = {}

        for ticker in self.data:
            df = self.data[ticker]
            return_dict[ticker] = df['Close'].pct_change()

        percent_change_matrix = pd.DataFrame(return_dict) # Converts the price dictionary to df (index=date, column=ticker, columnData=percent change)
        percent_change_matrix = percent_change_matrix.dropna()

        return percent_change_matrix

    """
    Save downloaded data to file
    """
    def save_data(self, filepath= ''):
        with open()
        return None

    """
    Load downloaded data
    """
    def load_data(self):
        return None



if __name__ == "__main__":
    tickers = ['META', 'AAPL']
    loader = StockDataLoader(tickers)
    data = loader.fetch_data()
    print(loader.get_returns_matrix())
