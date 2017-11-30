"""Stat analysis for time series"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="../../data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    # Read and join data for each symbol
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', 
        parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        
        # Rename to 'Adj Close' for each symbol to prevent clash
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        
        df = df.join(df_temp)
        if symbol == 'SPY': # drop dates SPY didn't trade
            df = df.dropna(subset=['SPY'])

    return df


def test_run():
    # Define a date range
    dates = pd.date_range('2012-01-01', '2012-12-31')

    # Choose stock symbols to read
    symbols = ['SPY']
    
    # Get stock data
    df = get_data(symbols, dates)

    ax = df.plot(title="SPY Rolling Mean", label='SPY')

    rm_SPY = df.rolling(window=20).mean()

    rm_SPY.plot(label='Rolling mean', ax=ax)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    test_run()
