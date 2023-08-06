"""
Library module to compute dividend information
"""
import yfinance as yf


"""
Calculate dividend rate

Args:
        ticker(str): name of the ticker
Returns:
        float: dividend rate
"""


def calculate_dividend_rate(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['dividendRate']


"""
Calculate dividend yield

Args:
        ticker(str): name of the ticker
Returns:
        float: dividend yield
"""


def calculate_dividend_yield(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['dividendYield']
