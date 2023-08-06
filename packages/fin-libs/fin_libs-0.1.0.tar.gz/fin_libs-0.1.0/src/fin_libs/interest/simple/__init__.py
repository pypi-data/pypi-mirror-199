"""
Library package to calcuate simple interest
"""

"""
Calculate simple interest

Args:
        principal(float): principal amount
        rate(float): interest rate
        time(int): time
Returns:
        interest(float): simple interest
"""


def calculate_simple_interest(principal, rate, time):
    interest = (principal * rate * time) / 100
    return interest
