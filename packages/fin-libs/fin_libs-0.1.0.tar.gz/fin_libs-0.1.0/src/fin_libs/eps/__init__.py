"""
Library module to compute earnings per share
"""
import yfinance as yf

"""
Calculate Earnings per Share

Args:
        ticker(str): the ticker for which we should calculate the EPS
Returns:
        float: the EPS
"""


def calculate_eps(ticker):
    tick = yf.Ticker(ticker)
    return tick.info['forwardEps']
