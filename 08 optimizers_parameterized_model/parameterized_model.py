"""Build a parameterized model"""


import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


def error(coefficients, data):
	"""Compute error between given line model f(x) = mx + b and observed data

	Parameters:
	coefficients: tuple/list/array (m,b) where m is slope and b is Y-intercept of the line model
	data: 2D array where each row is a point (x, y)
	
	Returns error as a single real value
	"""
	# Error = sum of squared differences between actual Y-axis data and estimated data by the line model
	err = np.sum((data[:, 1] - (coefficients[0] * data[:, 0] + coefficients[1]))**2)
	return err


def fit_line(data, error_func):
	"""Fit a line to given data, using a supplied error function.
	
	Parameters:
	data: 2D array where each row is a point (x, y)
	error_func: function that computes the error between a line and observed data

	Returns line that minimizes the error function
	"""
	# Generate initial guess for line model
	l = np.float32([0, np.mean(data[:, 1])]) # m = 0, b = mean of the data

	# Plot initial guess
	x_initial_guess = np.float32([-5, 5])
	plt.plot(x_initial_guess, l[0] * x_initial_guess + l[1], "m--", linewidth=2.0, label="Initial guess")

	# Call optimizer to minimize error function
	result = spo.minimize(error_func, l, args=(data,), method="SLSQP", options={"disp": True}) # args: used to pass data to error_func
	return result.x


def test_run():
    # Define original line
    l_orig = np.float32([4,2])
    print ("Original line: m = {}, b = {}".format(l_orig[0], l_orig[1]))
    X_orig = np.linspace(0, 10, 21)
    Y_orig = l_orig[0] * X_orig + l_orig[1]
    plt.plot(X_orig, Y_orig, "b--", linewidth=2.0, label="Original line")

    # Generate noisy data points from a normal distribution
    scale = 3.0 # Standard deviation (spread or “width”) of the distribution
    noise = np.random.normal(0.0, scale, Y_orig.shape)
    data = np.asarray([X_orig, Y_orig + noise]).T
    plt.plot(data[:, 0], data[:, 1], "go", label="Data points")

    # Try to fit a line to this data
    l_fit = fit_line(data, error)
    print ("Fitted line: m = {}, b = {}".format(l_fit[0], l_fit[1]))
    plt.plot(data[:, 0], l_fit[0] * data[:, 0] + l_fit[1], "r--", linewidth=2.0, label="Fitted line")

    # Add a legend and show plot
    plt.legend(loc="upper left")
    plt.show()
    

if __name__ == "__main__":
    test_run()
