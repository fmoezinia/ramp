import matplotlib.pyplot as plt
import math


############ LOGISTIC sigmoid GROWTH MODEL #############
# x0 = the x-value of the sigmoid's midpoint,
# k = the logistic growth rate or steepness of the curve.
# x is the month
# C is the number y intercept (number clients in first month)
# L+C- L/(1+e^g*midpoint)) = the curve's maximum value, and


# growth k of 0.1 gets 20 customers to 100 in 40 months


def logistic_growth(month):
    midpoint = 130 # when growth decreases, usually after 3/4 years
    max_number = 4000
    C = 18 # initial no_clients
    growth_rate = 0.01

    denom = 1 + math.exp(-growth_rate*(month-midpoint))
    correction_factor = max_number/(1 + math.exp(growth_rate*midpoint))
    # L = max_number - C #+ correction_factor
    main_function = max_number/denom
    y_axis_correcion = C - correction_factor
    y = main_function + y_axis_correcion
    # print(month, y)
    return y


def util_plotter():
    no_months = 90
    y = [logistic_growth(month) for month in range(no_months)]
    plt.plot(range(no_months), y )
    plt.show()

# util_plotter()
