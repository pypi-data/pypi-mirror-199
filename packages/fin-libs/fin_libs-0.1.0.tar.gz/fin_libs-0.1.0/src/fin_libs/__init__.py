__version__ = '0.1.0'

# flake8: noqa
from .compound_annual_growth_rate import (
    calculate_compound_annual_growth_rate,
    print_calculate_compound_annual_growth_rate,
)

# flake8: noqa
from .dividends import calculate_dividend_rate, calculate_dividend_yield

# flake8: noqa
from .eps import calculate_eps

# flake8: noqa
from .income import calculate_net_income

# flake8: noqa
from .interest.compound import calculate_compound_interest

# flake8: noqa
from .interest.simple import calculate_simple_interest

# flake8: noqa
from .linear_least_squares import do_linear_least_squares_regression, plot_linear_least_squares_regression

# flake8: noqa
from .price import calculate_price_to_book_value

# flake8: noqa
from .weighted_average import compute_weighted_average
