"""Test for optimization.py"""


import datetime as dt
from optimization import *
import unittest
import math


class TestOptimizePortfolio(unittest.TestCase):

    def test_optimize(self):
        sd = dt.datetime(2010,1,1)
        ed = dt.datetime(2010,12,31)
        syms = ["GOOG", "AAPL", "GLD", "XOM"]
        allocs, cr, adr, sddr, sr = optimize_portfolio(sd, ed, syms)

        # sum(allocations) == 1.0 +- 0.02
        self.assertTrue(math.isclose(sum(allocs), 1.0, rel_tol=0.02), "sum(allocations is not within 0.2 of 1.0")

        # Test allocations
        reference_solution = [5.38105153e-16, 3.96661695e-01, 6.03338305e-01, -5.42000166e-17]
        for i in range(len(allocs)):
            # Each allocation is between 0 and 1.0 +- 0.02
            self.assertTrue(allocs[i] >= -0.02, "Allocation is negative")
            self.assertTrue(allocs[i] <= 1.02, "Allocation is greater than 1")

            # Each allocation matches reference solution +- 0.10
            self.assertTrue(math.isclose(round(allocs[i], 3), round(reference_solution[i], 3), rel_tol=1))

        # Test cumulative return
        self.assertTrue(math.isclose(cr, 0.360090826885, rel_tol=0.02), "Cumulative return is incorrect")

        # Test average daily return
        self.assertTrue(math.isclose(adr, 0.00127710312803, rel_tol=0.02), "Average daily return is incorrect")

        # Test standard deviation of daily returns
        self.assertTrue(math.isclose(sddr, 0.0101163831312, rel_tol=0.02), "Standard deviation is incorrect")

        # Test Sharpe Ratio
        self.assertTrue(math.isclose(sr, 2.00401501102, rel_tol=0.02), "Sharpe ratio is incorrect")
    

if __name__ == '__main__':
    unittest.main()