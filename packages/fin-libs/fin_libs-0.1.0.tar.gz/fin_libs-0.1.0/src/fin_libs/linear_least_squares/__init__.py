"""
Library package to compute linear least squares regression
"""
import pandas
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

"""
Does linear least squares regression
"""


def do_linear_least_squares_regression(csv_file_path):
    df = pandas.read_csv(csv_file_path)
    x = df.iloc[:, 0].values.reshape(-1, 1)
    y = df.iloc[:, 1].values.reshape(-1, 1)
    lr_helper = LinearRegression()
    lr_helper.fit(x, y)
    y_pred = lr_helper.predict(x)
    return x, y, y_pred


"""
Plot linear least squares regression
"""


def plot_linear_least_squares_regression(x, y, y_pred, color='yellow'):
    plt.scatter(x, y)
    plt.plot(x, y_pred, color=color)
    plt.show()
