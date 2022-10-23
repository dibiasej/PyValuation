from PyValuation import FinancialData
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class RelativeValue(FinancialData):
    """
    Instantiate a RelativeValue object used to calculate multiple relative valuation metrics.
    FinancialData will be inherited as a child class in order to pull financial data.
    Multiple general financial metrics and indicators will be calculated across multiple companys and sectors in order to compare similar companies.

    :param ticker: Specific stock ticker.
    :type ticker: str
    """
    def __init__(self, ticker):
        
        super().__init__(ticker)
            
    def _get_sp500(self):
        """
        Use pandas in order to pull a csv of all the companys in the S&P 500.

        :return: Dataframe containing S&P 500 companies
        :rtype: pd.DataFrame
        """
        df = pd.read_csv('sp500.csv').to_numpy()
        
        return df
            
    def get_industries(self):
        """
        Shows a list of names of every industry.

        :return: Industry list
        :rtype: np.array
        """
        df = self._get_sp500()
        
        industries = [i[2] for i in df]
        
        unqind = np.unique(industries)
        
        return unqind
        
    def _get_tickers(self):
        """
        Gets all the tickers in a certain industry.

        :return: List of tickers in a certain industry
        :rtype: np.array
        """
        df = self._get_sp500()
        
        try:
            
            industry = df[np.where(df == self.ticker)[0][0]][2]
            
        except:
        
            industry = input('Select Industry')
        
        print(f'We are analyzing the {industry} industry')
        
        indarr = df[np.where(df == industry)[0]]
        
        indtick = [i[0] for i in indarr]
        
        return indtick
    
    def zscore_list(self):
        """
        Uses the FinancialData class to calculate the Z-scores for a list of companys in an industry.

        :return: List of Z-scores
        :rtype: dict 
        """
        tickers = self._get_tickers()
        
        zscore_list = {}
        
        for i in tickers:
            
            print(f'Grabbing {i} zscore')
            try:
                zscore = FinancialData(i)._get_zscore()
                
                zscore_list[i] = zscore
            except:
                print('We have to skip this ticker an error was raised')
                pass
            
        return zscore_list

    
    def pb_list(self):
        """
        Uses the FinancialData class to calculate the Price to Book ratio for a list of companys in an industry.

        :return: List of Price to Book ratios
        :rtype: dict 
        """
        tickers = self._get_tickers()
        
        pb_list = {}
        
        for i in tickers:
            
            print(f'Grabbing {i} Price to Book Value')
            try:
                pb = FinancialData(i)._get_pb()
                
                pb_list[i] = pb
            except:
                print('We have to skip this stock an error was raised')
                pass

        return pb_list
    
    def ps_list(self):
        """
        Uses the FinancialData class to calculate the Price to Sales ratio for a list of companys in an industry.

        :return: List of Price to Sales ratios
        :rtype: dict 
        """
        tickers = self._get_tickers()
        
        ps_list = {}
        
        for i in tickers:
            
            print(f'Grabbing {i} Price to Sales')
            try:
                ps = FinancialData(i)._get_ps()
                
                ps_list[i] = ps
            except:
                print('We have to skip this stock an error was raised')
                pass
            
        return ps_list
    
    def pe_list(self):
        """
        Uses the FinancialData class to calculate the Price to Equity ratio for a list of companys in an industry.

        :return: List of Price to Equity ratios
        :rtype: dict 
        """   
        tickers = self._get_tickers()
        
        pe_list = {}
        
        for i in tickers:
            
            print(f'Grabbing {i} Price to Earnings')
            try:
                pe = FinancialData(i)._get_pe()
                
                pe_list[i] = pe
            except:
                print('We have to skip this stock an error was raised')
                pass
            
        return pe_list
    
    def operating_cushion_list(self):
        """
        Uses the FinancialData class to calculate the operating cushion for a list of companys in an industry.

        :return: List of Operating cushion
        :rtype: dict 
        """
        tickers = self._get_tickers()
        
        oc_list = {}
        
        for i in tickers:
            
            print(f'Grabbing {i} Operating Cushion')
            try:
                oc = FinancialData(i)._get_operating_cushion()
                
                oc_list[i] = oc
            except:
                print('We have to skip this stock an error was raised')
                pass
            
        return oc_list
    
    def cogp_list(self):
        """
        Uses the FinancialData class to calculate the core operating operating growth profile for a list of companys in an industry.

        :return: List of Core operating growth profile
        :rtype: dict 
        """    
        tickers = self._get_tickers()
        
        cogp_dict = {}
        
        for i in tickers:
            
            print(f'Grabbing {i} Core Operating Growth Profile')
            try:
                cogp = FinancialData(i)._get_core_operating_growth()
                
                cogp_dict[i] = cogp
            except:
                print('We have to skip this stock an error was raised')
                pass
            
        return cogp_dict
    
    def metrics(self):
        """
        Uses the FinancialData class to calculate the numerous methods for stock valuation for a list of companys in an industry.

        :return: List of stock valuation metrics
        :rtype: dict 
        """

        tickers = self._get_tickers()
        
        metric_list = {'Metrics' : ['Zscore', 'P/B', 'P/E', 'P/S','ROC', 'ROE', 'Gross Margin', 'Net Margin', 'Operating Margin', 'EV/EBITDA', 'EV/Sales', 'EV/Capital', 'Operating Cushion', 'COGP']}
        
        for counter, i in enumerate(tickers, 1):
            print(f'Grabbing {i} Data {counter}/{len(tickers)}')
            
            try:
                
                stock = FinancialData(i)
                
                metric_list[i] = [stock._get_zscore(), stock._get_pb(), stock._get_pe(), stock._get_ps(), stock._get_roc(), stock._get_roe(), stock._get_grossmargin(), stock._get_netmargin(), stock._get_operatingmargin(), stock._get_ev_ebitda(), stock._get_ev_sales(), stock._get_ev_capital(), stock._get_operating_cushion(), stock._get_core_operating_growth()]
            
            except:
                
                print(f'Could Not Retrieve {i} Data')
                
                continue
            
        metricdf = pd.DataFrame(metric_list)
        
        metricdf = metricdf.set_index('Metrics')
        
        print('Finished!')
        
        return metricdf.round(2)
    
    def market_share(self):
        """
        Gathers revenue from every company in an industry and aggregates it.
        Plots pie charts and bar chart showing which companies hold what percent share of revenue in their respective industry
        """
        tickers = self._get_tickers()
        
        ticker_list = []
        
        revenue_list = []
        
        net_income_list = []
        
        op_income_list = []
        
        for count, i in enumerate(tickers, 1):
            
            print(f'Grabbing {i} Data {count}/{len(tickers)}')
            
            try:
                
                incomestatements = FinancialData(i).incomestatement()
                
                revenues = incomestatements[np.where(incomestatements == 'Total Revenue')[0][0]][1]
                
                net_incomes = incomestatements[np.where(incomestatements == 'Net Income')[0][0]][1]
                
                op_incomes = incomestatements[np.where(incomestatements == 'Operating Income')[0][0]][1]
                
            except:
                
                print(f'Could Not Find {i} Revenue')
                                
                continue
            
            revenue_list.append(revenues)
            
            net_income_list.append(net_incomes)
            
            op_income_list.append(op_incomes)
            
            ticker_list.append(i)
        
        revenue = np.array(revenue_list)
        
        net_income = np.array(net_income_list)
        
        operating_income = np.array(op_income_list)
        
        plt.figure()
        plt.bar(ticker_list, revenue, color = 'b')
        plt.ylabel('Companies Revenue (In 100 Billions)')
        plt.xticks(rotation = 45)
        plt.title('Market Share of Revenue')
        
        plt.figure()
        plt.bar(ticker_list, net_income, color = 'r')
        plt.ylabel('Companies Revenue (In Billions)')
        plt.xticks(rotation = 45)
        plt.title('Market Share of Net Income')
        
        plt.figure()
        plt.bar(ticker_list, operating_income, color = 'g')
        plt.ylabel('Companies Revenue (In Billions)')
        plt.xticks(rotation = 45)
        plt.title('Market Share of Operating Income')
        
        plt.figure()
        plt.pie(revenue, labels = ticker_list, radius = 2.5, autopct = "%0.2f%%")