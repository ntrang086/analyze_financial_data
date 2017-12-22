"""Project: Optimize a portfolio"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from analysis import *
import sys
# Append the path of the directory one level above the current directory to import util
sys.path.append('../')
from util import *


def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=["GOOG","AAPL","GLD","XOM"], gen_plot=False):

    """Optimize a portfolio and compute its statistics

    Parameters:
    sd: A datetime object that represents the start date
    ed: A datetime object that represents the end date
    syms: A list of symbols that make up the portfolio
    gen_plot: If True, create a plot named plot.png

    Returns:
    allocs: A list of allocations to the stocks, must sum to 1.0
    cr: Cumulative return
    adr: Average period return (if sf == 252 this is daily return)
    sddr: Standard deviation of daily return
    sr: Sharpe ratio
    """

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    allocs = find_optimal_allocations(prices, get_negative_sharpe_ratio, syms)

    # Get daily portfolio value
    port_val = get_portfolio_value(prices, allocs, sv=1000000)
    cr, adr, sddr, sr = get_portfolio_stats(port_val, daily_rf=0.0, samples_per_year=252)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=["Portfolio", "SPY"], axis=1)
        plot_normalized_data(df_temp, title="Daily portfolio and SPY", xlabel="Date", ylabel="Normalized price")    

    return allocs, cr, adr, sddr, sr


def find_optimal_allocations(prices, function, syms):
    bounds = ((0,1),(0,1),(0,1),(0,1))

    constraints = ({'type': 'eq', 'fun': lambda x:  np.sum(x)-1.0})

    initial_guess = np.ones((len(syms)), dtype=np.float32)/(len(syms))

    result = spo.minimize(function, initial_guess, args=(prices,), method='SLSQP', constraints=constraints, bounds=bounds)
    return result.x


def get_negative_sharpe_ratio(allocs, prices, sv=1000000, rfr=0.0, sf=252):
    # Get daily portfolio value
    port_val = get_portfolio_value(prices, allocs, sv)

    # Get portfolio statistics
    neg_sr = get_portfolio_stats(port_val, rfr, sf)[3] * (-1)

    return neg_sr