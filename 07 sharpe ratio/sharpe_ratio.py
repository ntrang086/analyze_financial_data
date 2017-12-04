"""Compute Sharpe ratio"""

import numpy as np


def compute_sharpe_ratio(k, avg_return, risk_free_rate, std_return):
    """
    Compute and return the Sharpe ratio
    :param k: adjustment factor, sqrt(252) for daily data, sqrt(52) for weekly data, sqrt(12) for monthly data
    :param avg_return: daily, weekly or monthly return
    :param risk_free_rate: daily, weekly or monthly risk free rate
    :param std_return: daily, weekly or monthly standard deviation
    :return: sharpe_ratio, k * (avg_return - risk_free_rate) / std_return
    """
    return k * (avg_return - risk_free_rate) / std_return
    


def test_run():
    # 60 days of data
    avg_daily_return = 0.001
    daily_risk_free_rate = 0.0002
    std_daily_return = 0.001

    # Calculate Sharpe ratio for the above data
    print (compute_sharpe_ratio(np.sqrt(252), avg_daily_return, daily_risk_free_rate, std_daily_return))
    
if __name__ == "__main__":
    test_run()
