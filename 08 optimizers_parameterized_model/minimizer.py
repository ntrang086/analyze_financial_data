"""Minimize an objective function, using SciPy"""

import numpy as np
import scipy.optimize as spo


def f(X):
    """Given a scalar X, return some value (a real number)"""
    Y = (X - 1.5)**2 + 0.5
    print ("X = {}, Y = {}".format(X, Y)) # for tracing
    return Y


def test_run():
    Xguess = 2.0
    min_result = spo.minimize(f, Xguess, method="SLSQP", options={"disp": True})
    print ("Minima found at:")
    print ("X = {}, Y = {}".format(min_result.x, min_result.fun))


if __name__ == "__main__":
    test_run()
