import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader import get_data_yahoo as pdr
import datetime as dt
import os
import yfinance as yf
import scipy.optimize as sco
import scipy.interpolate as sci
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PortfolioValuation():
    """
    Instantiate a PortfolioValuation object used for portfolio analysis.

    :param start: Start date
    :type start: int

    :param end: End date
    :type end: int

    :param cash: Portfolio cash
    :type cash: int

    :param tickers: Keyword argument naming multiple ticker as keys and quantitys of shares as values.
    :type tickers: dict
    """    
    def __init__(self, start, end, cash=0, **tickers):
        
        self.start = start
        
        self.end = end
        
        self.cash = cash
        
        self.tickers = tickers
        
    def add_cash(self, cash):
        """
        Adjusts the quantity of cash in the portfolio.

        :param cash: Cash in the portfolio.
        :type cash: int

        :return: cash
        :rtype: int
        """
        self.cash = cash
        
        return self.cash
    
    def _port_ret(self, weights, logrets):
        """
        Internal function to calculate the return of a portfolio.

        :param weights: Random weights
        :type weights: list

        :param logrets: Log returns of portfolio
        :type logrets: list

        :return: Weighted log return of the portfolio
        :rtype: int
        """
        return np.sum(logrets.mean() * weights) * 252
    
    def _port_vol(self, weights, logrets):
        """
        Internal function to calculate the volatility of a portfolio.

        :param weights: Random weights
        :type weights: list

        :param logrets: Log returns of portfolio
        :type logrets: list

        :return: Weighted volatility of the portfolio
        :rtype: int
        """
        return np.sqrt(np.dot(weights.T, np.dot(logrets.cov() * 252, weights)))
    
    def min_func_sharpe(self, weights, logrets):
        """
        Internal function to calculate the sharpe ratio of a portfolio.

        :param weights: Random weights
        :type weights: list

        :param logrets: Log returns of the portfolio
        :type logrets: list

        :return: Sharpe ratio of the portfolio
        :rtype: int
        """
        return -self._port_ret(weights, logrets)/self._port_vol(weights, logrets)

    def portfolio_performance(self):
        """
        Given certain tickers this function calculates the performance over a certain period of time and calculates the cumulative log return of the portfolio over the time period.
        Plots the portfolio price action over the given time period.
        """
        all_ticker_data = pd.DataFrame()

        if self.end == 'today':
            for ticker, quantity in self.tickers.items():
                df = pdr(ticker, dt.datetime(self.start, 1, 1), dt.datetime.now())
                df[ticker] = df['Adj Close'] * quantity
                df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], 1, inplace = True)
                all_ticker_data = pd.concat([all_ticker_data, df], axis = 1)
        else:
            for ticker, quantity in self.tickers.items():
                df = pdr(ticker, dt.datetime(self.start, 1, 1), dt.datetime(self.end, 1, 1))
                df[ticker] = df['Adj Close'] * quantity
                df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], 1, inplace = True)
                all_ticker_data = pd.concat([all_ticker_data, df], axis = 1)

        portfolio = pd.DataFrame(all_ticker_data)

        columns = portfolio.columns

        portfolio['Total Assets'] = 0

        for column in columns:
            portfolio['Total Assets'] += portfolio[column]

        portfolio['Log Returns'] = np.log(portfolio['Total Assets']/portfolio['Total Assets'].shift(1))
        
        end_return = round((portfolio['Total Assets'].iloc[-1] - portfolio['Total Assets'].iloc[0])/portfolio['Total Assets'].iloc[0], 2) * 100
                
        ((portfolio['Log Returns'].cumsum().apply(np.exp) - 1) * 100).plot(figsize=(12, 8))
        plt.title(f'Portfolio Return From {self.start} to {self.end}: {end_return}%')
        plt.ylabel('Percent Return')
        
    def asset_allocation(self):
        """
        Plots pie chart of asset allocation
        """
        ticker_list = ['cash']
        
        price_list = [self.cash]
        
        for ticker, quantity in self.tickers.items():
            
            stock = yf.Ticker(f'{ticker}').history(period='1d')['Close'][0]
            
            price = stock * quantity
            
            ticker_list.append(ticker)
            
            price_list.append(price)
            
        plt.figure()
        plt.pie(price_list, labels = ticker_list, radius = 1.5, autopct = "%0.2f%%")
        
    def efficient_frontier(self, i, j, vol=0):
        """
        Plots the efficient frontier and optimizes portfolio allocation, and plots all possible portfolio combinations.

        :param i: Lowest possible target return.
        :type i: float

        :param j: Highest possible target return.
        :type j: float

        :param vol: Specific volatility for select portfolio weights
        :type vol: float
        """
        df = pd.DataFrame()
        
        for ticker in self.tickers:
            
            stock = pdr(ticker, self.start, self.end)
            
            df[ticker] = stock['Adj Close']
        
        logrets = np.log(df/df.shift(1))
        
        #mean, covariance = logrets.mean() * 252, logrets.cov() * 252
        
        prets = []
        pvols = []
        
        for p in range(2500):
            weights = np.random.random(len(df.columns))
            weights /= np.sum(weights)
            prets.append(self._port_ret(weights, logrets))
            pvols.append(self._port_vol(weights, logrets))
        prets = np.array(prets)
        pvols = np.array(pvols)
        
        eweights = np.array(len(df.columns) * [1. / len(df.columns)])
        
        cons1 = ({'type' : 'eq', 'fun' : lambda x: self._port_ret(x, logrets) - tret},
        {'type' : 'eq', 'fun' : lambda x: np.sum(x) - 1})
        
        bnds1 = tuple((0, 1) for x in weights)
        
        trets = np.linspace(i, j, 50)
        tvols = []
        res1 = {}
        for tret in trets:
            res = sco.minimize(self._port_vol, eweights, args=(logrets), method='SLSQP', bounds=bnds1, constraints=cons1)
            tvols.append(res['fun'].round(3))
            res1[res['fun'].round(3)] = res['x'].round(3) 
        tvols = np.array(tvols)
        
        fig = go.Figure()

        # Add traces
        fig.add_trace(go.Scatter(x=pvols, y=prets,
                            mode='markers',
                            name='Portfolio Weights'))
        fig.add_trace(go.Line(x=tvols, y=trets,
                            mode='lines+markers',
                            name='Optimal Portfolio Weights'))
        
        fig.update_layout(
            title = 'Efficient Frontier',
            yaxis_title='Portfolio Return',
            xaxis_title='Portfolio Volatility',
            autosize=False,
            width=800,
            height=500
        )
        
        fig.show()
        
        if vol == 0:
            
            vol = 0
            
        else:
            
            print(res1[vol])