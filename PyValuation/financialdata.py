import yfinance as yf
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests

class FinancialStatements():
    """
    Instantiate a financial statements operation.
    Financial statements will be pulled for a given ticker.

    :param ticker: Specific stock ticker.
    :type ticker: str

    """
    def __init__(self, ticker):
        
        self.ticker = ticker
        
    def _get_ticker(self):
        """
        Get yahoo finance data for a given ticker.

        :return: Specific ticker data
        """
        return yf.Ticker(self.ticker)
    
    def balancesheet(self):
        """
        Get the balance sheet of a specific company

        :return: Balance sheet given specific ticker
        :rtype: object
        """
        ticker = self._get_ticker()
        
        try:
            
            balancesheet = ticker.get_balancesheet().fillna(0)
            
        except:
            
            print(f"The balance sheet for {self.ticker} could not be found, this may be an etf, try another ticker")
        
        balancesheet1 = balancesheet.reset_index().to_numpy()
                
        return balancesheet1

    def soupbalancesheet(self):
        """
        Get the Balance sheet of a specific company directly from the yahoo website via webscrapping

        :return: Balance sheet given a specific ticker 
        """
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

        r = requests.get('https://finance.yahoo.com/quote/' + self.ticker + '/balance-sheet?p=' + self.ticker + '', headers = header)

        soup = bs(r.content, 'html.parser')

        finrow = soup.find_all('div', {'data-test' : "fin-row"})

        balance = [finrow[i].find_all('span') for i in range(len(finrow))]

        balancesheet = []

        for i in range(len(balance)):
            
            row = [balance[i][j].get_text() for j in range(len(balance[i]))]
            
            metric = row[0]
                
            numrow = [int(row[k + 1].replace(",", "")) for k in range(len(row) - 1)]
            
            numrow.insert(0, metric)

            balancesheet.append(numrow)

        return balancesheet
    
    def incomestatement(self):
        """
        Get the Income statement of a specific company

        :return: Income statement given specific ticker
        :rtype: object
        """
        ticker = self._get_ticker()
        
        try:
            
            incomestatement = ticker.get_financials().fillna(0)
            
        except:
            
            print(f"The income statement for {self.ticker} could not be found, this may be an etf, try another ticker")
        
        incomestatement1 = incomestatement.reset_index().to_numpy()
        
        return incomestatement1

    def soupincomestatement(self):
        """
        Get the Income statement of a specific company directly from the yahoo website via webscrapping

        :return: Income statement given a specific ticker 
        """

        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

        r = requests.get('https://finance.yahoo.com/quote/' + self.ticker + '/financials?p=' + self.ticker + '', headers = header)

        soup = bs(r.content, 'html.parser')

        finrow = soup.find_all('div', {'data-test' : "fin-row"})

        income = [finrow[i].find_all('span') for i in range(len(finrow))]

        incomestatement = []

        for i in range(len(income)):
            
            row = [income[i][j].get_text() for j in range(len(income[i]))]
            
            metric = row[0]
                
            numrow = [int(row[k + 1].replace(",", "")) for k in range(len(row) - 1)]
            
            numrow.insert(0, metric)
            #metric.append(numrow)
            #print(metric)
            #print(numrow)

            incomestatement.append(numrow)

        return incomestatement
    
    def cashflowstatement(self):
        """
        Get the Cash flow statement of a specific company

        :return: Cash flow statement given specific ticker
        :rtype: object
        """        
        ticker = self._get_ticker()
        
        try:
            
            cashflowstatement = ticker.get_cashflow().fillna(0)
            
        except:
            
            print(f"The cash flow statement for {self.ticker} could not be found, this may be an etf, try another ticker")
        
        cashflowstatement1 = cashflowstatement.reset_index().to_numpy()
        
        return cashflowstatement1

    def soupcashflowstatement(self):
        """
        Get the Cash flow statement of a specific company directly from the yahoo website via webscrapping

        :return: Cash flow statement given a specific ticker 
        """
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

        r = requests.get('https://finance.yahoo.com/quote/'+ self.ticker +'/cash-flow?p=' + self.ticker + '', headers = header)

        soup = bs(r.content, 'html.parser')

        finrow = soup.find_all('div', {'data-test' : "fin-row"})

        cashflow = [finrow[i].find_all('span') for i in range(len(finrow))]

        cashflowstatement = []

        for i in range(len(cashflow)):
            
            row = [cashflow[i][j].get_text() for j in range(len(cashflow[i]))]
            
            metric = row[0]
                
            numrow = [int(row[k + 1].replace(",", "")) for k in range(len(row) - 1)]
            
            numrow.insert(0, metric)

            cashflowstatement.append(numrow)

        return cashflowstatement

class FinancialData(FinancialStatements):
    """
    Instantiate a financial data calculating operation.
    Financial statements will be inherited as a child class in order to pull financial statements.
    Multiple general financial metrics and indicators will be calculated for use in other classes.

    :param ticker: Specific stock ticker.
    :type ticker: str
    
    :param tax_rate: Corporation tax rate
    :type tax_rate: float

    :param risk_free_rate: Riskless rate at which a portion of cash will grow over time
    :type risk_free_rate: float

    :param equity_risk_premium: Return over the risk free rate that an investor is compensated with for investing in equities
    :type equity_risk_premium: float
    """    
    def __init__(self, ticker, tax_rate = .28, risk_free_rate = .04, equity_risk_premium = 0.12):
        
        super().__init__(ticker)
        
        self.tax_rate = tax_rate
        
        self.risk_free_rate = risk_free_rate
        
        self.equity_risk_premium = equity_risk_premium

        self.bsheet = super().balancesheet()

        self.ins = super().incomestatement()

        self.cf = super().cashflowstatement()
        
    def change_tax_rate(self, tax_rate):
        """
        Change the current coporate tax rate

        :param tax_rate: The corporate tax rate
        :type tax_rate: float

        :return: The updated tax rate
        :rtype: float
        """
        self.tax_rate = tax_rate
        
        return self.tax_rate
    
    def change_rfr(self, risk_free_rate):
        """
        Change the current risk free rate

        :param risk_free_rate: The risk free rate
        :type risk_free_rate: float

        :return: The updated risk free rate
        :rtype: float
        """  
        self.risk_free_rate = risk_free_rate
        
        return self.risk_free_rate
    
    def change_erp(self, equity_risk_premium):
        """
        Change the current equity risk premium

        :param equity_risk_premium: The equity risk premium
        :type equity_risk_premium: float

        :return: The updated equity risk premium
        :rtype: float
        """
        self.equity_risk_premium = equity_risk_premium
        
        return self.equity_risk_premium
        
    def _getprice(self):
        """
        Get the current price of the given ticker

        :return: Stock current price
        :rtype: float
        """
        ticker = yf.Ticker(self.ticker)
        
        pricedata = ticker.history(period='1d')
        
        return pricedata['Close'][0]
    
    def _sharesoutstanding(self):
        """
        Get the current shares outstanding of the given ticker

        :return: Shares outstanding
        :rtype: int
        """
        ticker = yf.Ticker(self.ticker)
        
        sharesoutstanding = ticker.info
        
        return sharesoutstanding['sharesOutstanding']
    
    def _debttoequity(self):
        """
        Get the current Debt to Equity ratio of the given ticker

        :return: Debt to Equity ratio
        :rtype: float
        """
        ticker = yf.Ticker(self.ticker)
        
        deratio = ticker.info
        
        return deratio['debtToEquity']
    
    def _getbeta(self):
        """
        Get the current beta of the given ticker

        :return: beta
        :rtype: float
        """
        ticker = yf.Ticker(self.ticker)
        
        beta = ticker.info
        
        return beta['beta']

    def _get_pe(self):
        """
        Calculates the eps of the given ticker then gets the current price and divides the two to calculate the current price to earnings ratio

        :return: Price to Earnings ratio
        :rtype: float
        """        
        eps = round((self.ins[np.where(self.ins == 'Net Income')[0][0]][1]) / self._sharesoutstanding(), 2)
        
        pe = round((self._getprice()) / eps, 2)
        
        return pe

    def _get_ps(self):
        """
        Calculates the current price to sales ratio using current market value divided by the current total revenue

        :return: Price to Sales ratio
        :rtype: float
        """        
        ps = round((self._getprice() * self._sharesoutstanding()) / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)
        
        return ps
    
    def _get_pb(self):
        """
        Calculates the current price to book ratio using current market value divided by the current total stockholder equity

        :return: Price to Book ratio
        :rtype: float
        """ 
        pb = round((self._getprice() * self._sharesoutstanding()) / self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1], 2)
        
        return pb

    def _get_roc(self):
        """
        Calculates the current return on capital

        :return: Return on capital
        :rtype: float
        """ 
        try:

            bvdebt = self.bsheet[np.where(self.bsheet == 'Short Long Term Debt')[0][0]][1] + self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]

        except:

            try:

                bvdebt = self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]

            except:

                bvdebt = 0

        roc = round(((self.ins[np.where(self.ins == 'Operating Income')[0][0]][1]) * (1 - self.tax_rate)) / (bvdebt + self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1]), 2)
        
        return roc

    def _get_roe(self):
        """
        Calculates the current return on equity

        :return: Return on equity
        :rtype: float
        """
        roe = round((self.ins[np.where(self.ins == 'Net Income')[0][0]][1]) / (self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1]), 2)
        
        return roe

    def _get_grossmargin(self):
        """
        Calculates the current gross margins by dividing gross profit divided by total revenue

        :return: Gross margin
        :rtype: float
        """
        grossmargin = round(self.ins[np.where(self.ins == 'Gross Profit')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)

        return grossmargin

    def _get_netmargin(self):
        """
        Calculates the current net margins by dividing net income divided by total revenue

        :return: Net margin
        :rtype: float
        """
        netmargin = round(self.ins[np.where(self.ins == 'Net Income')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)

        return netmargin

    def _get_operatingmargin(self):
        """
        Calculates the current operating margins by dividing operating income divided by total revenue

        :return: Operating margin
        :rtype: float
        """
        operatingmargin = round(self.ins[np.where(self.ins == 'Operating Income')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)

        return operatingmargin

    def _get_ev(self):
        """
        Calculates the current Enterprise value of the company using the total debt plus the market price minus cash.

        :return: Enterprise values
        :rtype: float
        """
        try:

            bvdebt = self.bsheet[np.where(self.bsheet == 'Short Long Term Debt')[0][0]][1] + self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]

        except:

            try:

                bvdebt = self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]

            except:

                bvdebt = 0

        ev = round((self._getprice() * self._sharesoutstanding()) + bvdebt - self.bsheet[np.where(self.bsheet == 'Cash')[0][0]][1], 2)

        return ev

    def _get_ev_ebitda(self):
        """
        Calculates the current enterprise value to ebitda ratio

        :return: EV/EBITDA ratio
        :rtype: float
        """
        ev_ebitda = round(self._get_ev() / (self.ins[np.where(self.ins == 'Ebit')[0][0]][1] + self.cf[np.where(self.cf == 'Depreciation')[0][0]][1]), 2)

        return ev_ebitda

    def _get_ev_capital(self):
        """
        Calculates the current enterprise value to capital ratio

        :return: EV/Capital ratio
        :rtype: float
        """
        try:

            bvdebt = self.bsheet[np.where(self.bsheet == 'Short Long Term Debt')[0][0]][1] + self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]

        except:

            try:

                bvdebt = self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]

            except:

                bvdebt = 0

        ev = (self._getprice() * self._sharesoutstanding()) + bvdebt - self.bsheet[np.where(self.bsheet == 'Cash')[0][0]][1]

        ev_capital = round(ev / (bvdebt + self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1]), 2)

        return ev_capital

    def _get_ev_sales(self):
        """
        Calculates the current enterprise value to sales ratio

        :return: EV/sales ratio
        :rtype: float
        """
        ev_sales = round((self._get_ev() / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]), 2)

        return ev_sales
    
    def _get_operating_cushion(self):
        """
        Calculates the current operating cushion of the given ticker by subtracting the SG&A/Revenue from the gross margin

        :return: Operating cushion
        :rtype: float
        """
        try:
            try:

                sgapct = self.ins[np.where(self.ins == 'Selling General Administrative')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]

            except:

                sgapct = 0
            
            grossmargin = self.ins[np.where(self.ins == 'Gross Profit')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]
            
            operating_cushion = grossmargin - sgapct
            
            return round(operating_cushion, 2)
        except:
            print('We have to skip this ticker an error was raised')
            pass

    def _get_core_operating_growth(self):
        """
        Calculates the current core operating the growth profile of the given ticker by subtracting the operating cushion from the working capital/revenue percent

        :return: Core operating the growth profile
        :rtype: float
        """
        try:
            operatingcushion = self._get_operating_cushion()
            
            try:

                ar = round(self.bsheet[np.where(self.bsheet == 'Net Receivables')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)

            except:

                ar = 0
            
            try:

                ap = round(self.bsheet[np.where(self.bsheet == 'Accounts Payable')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)

            except:

                ap = 0
            
            try:
                
                inventory = round(self.bsheet[np.where(self.bsheet == 'Inventory')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)
                
            except:
                
                inventory = 0
                
            wc = round(ap - ar - inventory, 2)
            
            cogp = round(wc + operatingcushion, 2)
            
            return cogp
        except:
            print('We have to skip this ticker an error was raised')
            pass

    def _get_zscore(self):
        """
        Calculates the Current modified Altman Z-score by using the formula M-Z-score = 3.25 + 6.56A + 3.26B + 6.72C + 1.05D
        A = (Current Assets - Current Liabilities) / Total Assets
        B = Retained Earnings / Total Assets
        C = EBIT / Total Assets
        D = Book Equity / Total Liabilities

        :return: Altman Z-score
        :rtype: float
        """
        try:
            A = (self.bsheet[np.where(self.bsheet == 'Total Current Assets')[0][0]][1] - self.bsheet[np.where(self.bsheet == 'Total Current Liabilities')[0][0]][1]) / self.bsheet[np.where(self.bsheet == 'Total Assets')[0][0]][1]
            
            B = self.bsheet[np.where(self.bsheet == 'Retained Earnings')[0][0]][1] / self.bsheet[np.where(self.bsheet == 'Total Assets')[0][0]][1]
            
            C = self.ins[np.where(self.ins == 'Ebit')[0][0]][1] / self.bsheet[np.where(self.bsheet == 'Total Assets')[0][0]][1]
            
            D = self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1] / self.bsheet[np.where(self.bsheet == 'Total Liab')[0][0]][1]
            
            zscore = round(3.25 + 6.56*A + 3.26*B + 6.72*C + 1.05*D, 2)
            
            return zscore
        except:
            print('We have to skip this ticker an error was raised')
            pass
        
    def _inputs(self):
        """
        Returns numerous metrics for valuating a company.
        Returns growth rates, discount rates and reinvestment rates used in a discounted cash flow model.

        :return: Metrics for evaluating a company and inputs to discounted cash flow model.
        :rtype: dict
        """
        try:
            bs = super().balancesheet()
            
            cf = super().cashflowstatement()
            
            ins = super().incomestatement()
            
            try:
                
                beta = self._getbeta()
                
                if beta == None:
                    
                    beta = 1
                
                else:
                    
                    beta = beta
                
            except:
                
                beta = 1
            
            """This first portion we calculate corresponds to our Cash Flow/Reinvestments table from the excel sheet Auto DCF
            
            """
            
            try:
                
                stock_buyback = cf[np.where(cf == 'Repurchase Of Stock')[0][0]][1]
                
            except:
                
                stock_buyback = 0
            
            try:
                
                dividend = cf[np.where(cf == 'Dividends Paid')[0][0]][1]

                
            except:
                
                dividend = 0
            
            #de_ratio = self._debttoequity()

            #if de_ratio == None:

            try:
                
                short_term_debt = bs[np.where(bs == 'Short Long Term Debt')[0][0]][1]
                
            except:
                
                short_term_debt = 1

            try:
                
                long_term_debt = bs[np.where(bs == 'Long Term Debt')[0][0]][1]
                
            except:
                
                long_term_debt = 1

            equity = bs[np.where(bs == 'Total Stockholder Equity')[0][0]][1] 
                
            de_ratio = (short_term_debt + long_term_debt) / equity
                            
            #else:

                #de_ratio = int(de_ratio)
                
            unlevered_beta = beta / (1 + (1 - self.tax_rate) * de_ratio)
            
            cost_of_equity_unlevered_beta = self.risk_free_rate + unlevered_beta * self.equity_risk_premium
            
            retained_earnings = bs[np.where(bs == 'Retained Earnings')[0][0]][1]
            
            cash = bs[np.where(bs == 'Cash')[0][0]][1]
            
            cash_t2 = cash = bs[np.where(bs == 'Cash')[0][0]][2]
            
            total_debt = short_term_debt + long_term_debt
            
            try:
                
                short_term_debt_t2 = bs[np.where(bs == 'Short Long Term Debt')[0][0]][2]
                
            except:
                
                short_term_debt_t2 = 0
                
            try:
                
                long_term_debt_t2 = bs[np.where(bs == 'Long Term Debt')[0][0]][2]
                
            except:
                
                long_term_debt_t2 = 0
            
            total_debt_t2 = short_term_debt_t2 + long_term_debt_t2
            
            issue_repayment_debt = total_debt - total_debt_t2
            
            bv_equity = equity
            
            augmented_dividends = (stock_buyback + dividend) * -1
            
            net_income = ins[np.where(ins == 'Net Income')[0][0]][1]
            
            operating_income = ins[np.where(ins == 'Operating Income')[0][0]][1]
            
            revenue = ins[np.where(ins == 'Total Revenue')[0][0]][1]
            
            research_development = ins[np.where(ins == 'Research Development')[0][0]][1]
            
            capex = - 1 * (cf[np.where(cf == 'Capital Expenditures')[0][0]][1])  # Note: we may need to include R & D
            
            depreciation = cf[np.where(cf == 'Depreciation')[0][0]][1]
            
            net_capex = capex - depreciation
            
            current_assets = bs[np.where(bs == 'Total Current Assets')[0][0]][1]

            current_assets_t2 = bs[np.where(bs == 'Total Current Assets')[0][0]][2]
            
            current_liabilities = bs[np.where(bs == 'Total Current Liabilities')[0][0]][1]

            current_liabilities_t2 = bs[np.where(bs == 'Total Current Liabilities')[0][0]][2]
            
            working_capital = current_assets - current_liabilities
            
            change_non_cash_workingcap = (current_assets - current_liabilities - cash) - (current_assets_t2 - current_liabilities_t2 - cash_t2)
            
            total_reinvestment = net_capex + research_development + change_non_cash_workingcap
            
            try:

                new_debt_issued = cf[np.where(cf == 'Net Borrowings')[0][0]][1]

            except:

                new_debt_issued = 0
            
            equity_reinvestment_in_buisness = net_capex + research_development + change_non_cash_workingcap - new_debt_issued  # note compare this formula with the same except swap new_debt_issued with issue_repayment_debt
            
            try:
                
                interest_expense = ins[np.where(ins == 'Interest Expense')[0][0]][1]
                
                if interest_expense == 0:
                    
                    interest_expense  = 1
            
            except:
                
                interest_expense = 1
            
            price = self._getprice()
            
            mv_equity = price * self._sharesoutstanding()
            
            total_stockholder_equity = bs[np.where(bs == 'Total Stockholder Equity')[0][0]][1]
            
            try:
                
                after_tax_cost_of_debt = (-1 * interest_expense) / long_term_debt
            
            except:
                
                after_tax_cost_of_debt = 0
            
            # now we move to discount rates
            
            operating_margin = operating_income / revenue
            
            net_margin = net_income / revenue
            
            wacc = ((total_debt / (total_debt + mv_equity)) * after_tax_cost_of_debt) + ((mv_equity / (total_debt + mv_equity)) * cost_of_equity_unlevered_beta)
            
            cost_of_equity = self.risk_free_rate + beta * (self.equity_risk_premium - self.risk_free_rate)
            
            roc = (operating_income * (1 - self.tax_rate)) / (total_debt + bv_equity)
            
            roe = net_income / bv_equity
            
            roic = (operating_income * (1 - self.tax_rate)) / (total_debt + bv_equity - cash)
            
            # now we move to growth rates
            
            retention_ratio = retained_earnings /  net_income
            
            reinvestment_rate = total_reinvestment / (operating_income * (1 - self.tax_rate))
            
            equity_reinvestment_rate = equity_reinvestment_in_buisness / net_income
            
            dividend_payout_ratio = dividend / net_income
            
            interest_coverage_ratio = operating_income / interest_expense
            
            internal_growth_rate = (roe * retention_ratio) / (1 - roe * retention_ratio)
            
            basic_firm_growth = reinvestment_rate * roc
            
            net_income_next_year = (retained_earnings + bv_equity) * roe
            
            net_income_growth_new_equity = equity_reinvestment_rate * roe
            
            net_income_eps_growth = retention_ratio * roe
            
            growth_rate_operating_income = reinvestment_rate * roc

            growth_rate_operating_income2 = reinvestment_rate * roic
            
            inputs = {
                'Reinvestments' : '------------------------------------------------------------',
                
                'total_reinvestment' : round(total_reinvestment, 2), 'net_capex' : round(net_capex, 2), 'capex' : round(capex, 2), 'change_in_non_cash_workingcap' : round(change_non_cash_workingcap, 2), 'retained_earnings' : round(retained_earnings, 2), 
                
                'equity_reinvestment_in_buisness' : round(equity_reinvestment_in_buisness, 2), 'stock_buyback': round(stock_buyback, 2), 
                
                'Reinvestment Measures' : '----------------------------------------------------',
                
                'retention_ratio' : round(retention_ratio, 2), 'reinvestment_rate' : round(reinvestment_rate, 2), 'equity_reinvestment_rate' : round(equity_reinvestment_rate, 2),

                'Growth Rates' : '------------------------------------------------------------',

                'internal_growth_rate' : round(internal_growth_rate, 2), 'basic_firm_growth' : round(basic_firm_growth, 2),

                'equity_reinvestment_rate x roe' : round(net_income_growth_new_equity, 2), 'retention_ratio x roe' : round(net_income_eps_growth, 2), 'reinvestment_rate x roc' : round(growth_rate_operating_income, 2),

                'reinvestment_rate * roic' : round(growth_rate_operating_income2, 2),
                
                'Discount Rate' : '----------------------------------------------------------',
                
                'unlevered_beta' : round(unlevered_beta, 2), 'beta' : round(beta, 2), 'cost_of_equity_unlevered_beta' : round(cost_of_equity_unlevered_beta, 2), 'after_tax_cost_of_debt' : round(after_tax_cost_of_debt, 2), 'wacc' : round(wacc, 2),
                
                'cost_of_equity' : round(cost_of_equity, 2),

                'Return Measures' : '---------------------------------------------------------',

                'roc' : round(roc, 2), 'roe' : round(roe, 2), 'roic' : round(roic, 2),

                'Misc' : '--------------------------------------------------------------------',

                'dividend_payout_ratio' : round(dividend_payout_ratio, 2), 'interest_coverage_ratio' : round(interest_coverage_ratio, 2), 'debt_equity_ratio' : round(de_ratio, 2),

                'net_income_next_year' : round(net_income_next_year, 2)


            }
            
            return inputs
        except:
            print('We have to skip this stock an error was raised')
            pass