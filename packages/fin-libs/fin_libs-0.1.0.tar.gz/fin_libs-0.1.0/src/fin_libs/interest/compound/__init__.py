"""
Library package to calcuate compound interest
"""


"""
Calculate compound interest

Args:
        principal(float): principal amount
        rate(float): interest rate
        time(int): time
Returns:
        interest(float): compound interest
"""


def calculate_compound_interest(principal, rate, time):
    amount = principal * (pow((1 + rate / 100), time))
    interest = amount - principal
    return interest
