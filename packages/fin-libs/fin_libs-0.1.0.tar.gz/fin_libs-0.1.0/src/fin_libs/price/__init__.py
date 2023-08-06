"""
Module to calculate stock price ratios
"""
import yfinance as yf

"""
Calculate Price to Earnings Ratio (P/E)

Args:
        ticker(str): the ticker for which we should calculate the ratio
Returns:
        float: the ratio
"""


def calculate_price_to_earning(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['forwardPE']


"""
Calculate Price to Book Value Ratio (P/BV)

Args:
        ticker(str): the ticker for which we should calculate the ratio
Returns:
        float: the ratio
"""


def calculate_price_to_book_value(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['bookValue']
