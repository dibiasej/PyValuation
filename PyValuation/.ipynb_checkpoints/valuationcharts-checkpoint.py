from PyVal import FinancialData
import yfinance as yf
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import datetime as dt
import pandas_datareader.data as web
import matplotlib.pyplot as plt

class ValuationCharts(FinancialData):
    """
    Instantiate a ValuationCharts calculating operation.
    FinancialData will be inherited as a child class in order to pull financial statements and other financial data.
    Multiple valuation metrics will be calculated and plotted over time.

    :param ticker: Specific stock ticker.
    :type ticker: str
    """    
    def __init__(self, ticker):
        
        super().__init__(ticker)

    
    def _sharesoutstanding_list(self):
        """
        Utilizes BeautifulSoup library in order to scrape web data to pull historical shares outstanding for a given ticker.

        :return: A list of dates and shares outstanding.
        :rtype: list
        """
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
        
        r = requests.get('https://ycharts.com/companies/' + self.ticker + '/shares_outstanding', headers = header)
        
        soup = bs(r.content, 'html.parser')
        
        tables = soup.find_all('table')
        td1 = tables[0].find_all('td', attrs = {'class' : "text-right"})
        td2 = tables[1].find_all('td', attrs = {'class' : "text-right"})
        td3 = tables[0].find_all('td', {"class" : None})
        td4 = tables[1].find_all('td', attrs = {'class' : None})
        
        date1 = [dt.datetime.strptime(td3[i].get_text(), '%B %d, %Y').date() for i in range(len(td3))]
        
        date2 = [dt.datetime.strptime(td4[i].get_text(), '%B %d, %Y').date() for i in range(len(td4))]
        
        year1 = [td3[i].get_text().split(' ')[2] for i in range(len(td3))]

        year2 = [td4[i].get_text().split(' ')[2] for i in range(len(td4))]
        
        solist1 = []
        
        solist2 = []
        
        for i in range(len(td1)):
            
            tdstr = str(td1[i]).split("\n")[2].replace(" ", "")

            letter = tdstr[-1]

            tdstr = tdstr[:-1]

            split1 = tdstr.split(".")

            if len(split1[1]) < 3:

                split1[1] = split1[1] + '0'

            if letter == 'B':

                split1.append('000')
                split1.append('000')

            if letter == 'M':

                split1.append('000')

            number = ''.join(split1)
                
            solist1.append(int(number))
            
        for i in range(len(td2)):
            
            tdstr = str(td2[i]).split("\n")[2].replace(" ", "")

            letter = tdstr[-1]

            tdstr = tdstr[:-1]

            split2 = tdstr.split(".")

            if len(split2[1]) < 3:

                split2[1] = split2[1] + '0'

            if letter == 'B':

                split2.append('000')
                split2.append('000')

            if letter == 'M':

                split2.append('000')

            number = ''.join(split2)
                
            solist2.append(int(number))
            
        solist1.extend(solist2)
        date1.extend(date2)
        year1.extend(year2)
            
        return [date1, solist1, year1]#{'so1' : solist1, 'so2' : solist2, 'date1' : date1, 'date2' : date2}
    
    def sharesoutstanding_chart(self):
        """
        Uses _sharesoutstanding_list function to pull shares outstanding then plots them over time.
        """
        so_list = self._sharesoutstanding_list()
        
        date = so_list[0]
        
        so = so_list[1]
        
        plt.figure()
        plt.plot(date, so)
        plt.xticks(rotation = 45)
        plt.ylabel('Shares Outstanding')
        plt.title(f'{self.ticker}')
    
    def pe_chart(self):
        """
        Calculates Price to Earnings ratio using price and earnings per share from the financial statements then plots it over time.
        """
        stock = yf.Ticker(self.ticker)
        
        so_list = self._sharesoutstanding_list()
        
        stock_date, stock_so, filtdates = so_list[0], so_list[1], so_list[2]
                
        incomestatement = stock.get_financials()
        
        incomestatementdates = incomestatement.columns.to_numpy(dtype=str)

        incomestatementdates = [int(incomestatementdates[i].split('-')[0]) for i in range(len(incomestatementdates))]
        
        filtdates = [int(filtdates[i]) for i in range(len(filtdates))]

        finaldates = [filtdates[t] for t in range(len(filtdates)) if filtdates[t] >= incomestatementdates[-1]]

        stock_so = [stock_so[t] for t in range(len(finaldates))]

        ins = incomestatement.reset_index().to_numpy()
        
        netincome = ins[np.where(ins == 'Net Income')[0][0]][1:]

        stockdf = web.get_data_yahoo(self.ticker, finaldates[-1], dt.datetime.now(), interval = 'm')

        date_num = stockdf.index.to_numpy()

        stock_close = stockdf['Adj Close'].to_numpy()[::-1]

        multiplier = round(int(len(stock_close)) / int(len(stock_so)))

        multincome = round(int(len(stock_close)) / int(len(netincome)))

        netincome_ext = []

        for i in netincome:

            loopinc = [i for j in range(1, multincome + 1)]

            netincome_ext.extend(loopinc)

        stock_extso = []

        for i in stock_so:

            looplist = [i for j in range(1, multiplier + 1)]

            stock_extso.extend(looplist)

        minlen = min(len(netincome_ext), len(stock_extso), len(stock_close))
        netincome_ext = netincome_ext[:minlen]
        stock_extso = stock_extso[:minlen]
        stock_close = stock_close[:minlen]
        eps = np.array(netincome_ext) / np.array(stock_extso)
        pe = stock_close / eps

        mindate = min(len(date_num), len(pe))

        pe = pe[:mindate]

        date_num = date_num[:mindate]
        plt.figure()
        plt.plot(date_num, pe[::-1])
        plt.xticks(rotation = 45)
        plt.ylabel('P/E Ratio')
        plt.title(f'{self.ticker}')
        
    def ps_chart(self):
        """
        Calculates a companys Price to Sales ratio using the companys price and total revenue over time and plots it over time
        """
        stock = yf.Ticker(self.ticker)

        solist = self._sharesoutstanding_list()

        stock_date, stock_so, filtdates = solist[0], solist[1], solist[2] 

        incomestatement = stock.get_financials()

        incomestatementdates = incomestatement.columns.to_numpy(dtype=str)

        incomestatementdates = [int(incomestatementdates[i].split('-')[0]) for i in range(len(incomestatementdates))]

        filtdates = [int(filtdates[i]) for i in range(len(filtdates))]

        finaldates = [filtdates[t] for t in range(len(filtdates)) if filtdates[t] >= incomestatementdates[-1]]

        stock_so = [stock_so[t] for t in range(len(finaldates))]

        ins = incomestatement.reset_index().to_numpy() 

        revenue = ins[np.where(ins == 'Total Revenue')[0][0]][1:]

        stockdf = web.get_data_yahoo(self.ticker, finaldates[-1], dt.datetime.now(), interval = 'm')

        date_num = stockdf.index.to_numpy()

        stock_close = stockdf['Adj Close'].to_numpy()[::-1]

        multiplier = round(int(len(stock_close)) / int(len(stock_so)))

        multincome = round(int(len(stock_close)) / int(len(revenue)))


        revenue_ext = []

        for i in revenue:

            loopinc = [i for j in range(1, multincome + 1)]

            revenue_ext.extend(loopinc)

        stock_extso = []

        for i in stock_so:

            looplist = [i for j in range(1, multiplier + 1)]

            stock_extso.extend(looplist)

        minlen = min(len(revenue_ext), len(stock_extso), len(stock_close))
        revenue_ext = revenue_ext[:minlen]
        stock_extso = stock_extso[:minlen]
        stock_close = stock_close[:minlen]

        ps = (stock_close * np.array(stock_extso)) / np.array(revenue_ext)

        mindate = min(len(date_num), len(ps))

        ps = ps[:mindate]

        date_num = date_num[:mindate]
        plt.figure()
        plt.plot(date_num, ps[::-1])
        plt.xticks(rotation = 45)
        plt.ylabel('P/S Ratio')
        plt.title(f'{self.ticker}')

    def pb_chart(self):
        """
        Calculates a companys Price to Book ratio using the companys price and total stockholder equity over time and plots it.
        """
        stock = yf.Ticker(self.ticker)

        solist = self._sharesoutstanding_list()

        stock_date, stock_so, filtdates = solist[0], solist[1], solist[2] 

        balamcesheet = stock.get_balancesheet()

        balamcesheetdates = balamcesheet.columns.to_numpy(dtype=str)

        balamcesheetdates = [int(balamcesheetdates[i].split('-')[0]) for i in range(len(balamcesheetdates))]

        filtdates = [int(filtdates[i]) for i in range(len(filtdates))]

        finaldates = [filtdates[t] for t in range(len(filtdates)) if filtdates[t] >= balamcesheetdates[-1]]

        stock_so = [stock_so[t] for t in range(len(finaldates))]

        bash = balamcesheet.reset_index().to_numpy() 

        bv_equity = bash[np.where(bash == 'Total Stockholder Equity')[0][0]][1:]

        stockdf = web.get_data_yahoo(self.ticker, finaldates[-1], dt.datetime.now(), interval = 'm')

        date_num = stockdf.index.to_numpy()

        stock_close = stockdf['Adj Close'].to_numpy()[::-1]

        multiplier = round(int(len(stock_close)) / int(len(stock_so)))

        multincome = round(int(len(stock_close)) / int(len(bv_equity)))


        bv_equity_ext = []

        for i in bv_equity:

            loopinc = [i for j in range(1, multincome + 1)]

            bv_equity_ext.extend(loopinc)

        stock_extso = []

        for i in stock_so:

            looplist = [i for j in range(1, multiplier + 1)]

            stock_extso.extend(looplist)

        minlen = min(len(bv_equity_ext), len(stock_extso), len(stock_close))
        bv_equity_ext = bv_equity_ext[:minlen]
        stock_extso = stock_extso[:minlen]
        stock_close = stock_close[:minlen]

        pb = (stock_close * np.array(stock_extso)) / np.array(bv_equity_ext)

        mindate = min(len(date_num), len(pb))

        pb = pb[:mindate]

        date_num = date_num[:mindate]
        plt.figure()
        plt.plot(date_num, pb[::-1])
        plt.xticks(rotation = 45)
        plt.ylabel('P/B Ratio')
        plt.title(f'{self.ticker}')