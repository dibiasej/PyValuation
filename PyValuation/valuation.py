import yfinance as yf
import numpy as np
from PyValuation import ValuationCharts

class Valuation(ValuationCharts):
    """
    Instantiate a Valuation object used to calculate multiple valuation metrics.
    ValuationCharts will be inherited as a child class in order to pull financial data and add chart plotting capabilities.
    Multiple general financial metrics and indicators will be calculated.

    :param ticker: Specific stock ticker.
    :type ticker: str
    """
    def __init__(self, ticker):
        
        super().__init__(ticker)
        
        self.bsheet = super().balancesheet()
        
        self.ins = super().incomestatement()
        
        self.cf = super().cashflowstatement()
        
    def business_summary(self):
        """
        Shows a basic summary of the company being valued.

        :return: Company business summary
        """
        stock = yf.Ticker(self.ticker).info
        
        return stock['longBusinessSummary']
    
    def definitions(self):
        """
        Prints multiple definitions of financial metrics for information purposes.
        """
        print('Operating Cushion: The contribution a $1 increase in revenue has to operating profits')
        
        print('Accounts receivable %: represents the % of every revenue dollar left uncollected from revenue')
        
        print('Acounts payable %: represents the % of every revenue dollar financed by vendors (i.e., paying on credit)')
        
        print('Inventory %: represents the % of every revenue dollar that must be reserved for inventory')
        
        print('Core Operating Growth Profile: The contribution a $1 increase in revenue has to core operating cash flow')
    
    def _get_zscore(self):
        """
        Uses data from financial statements to calculate a modified Altman Z-score.

        :return: Z-score calculated from formula
        :rtype: float
        """
        A = (self.bsheet[np.where(self.bsheet == 'Total Current Assets')[0][0]][1] - self.bsheet[np.where(self.bsheet == 'Total Current Liabilities')[0][0]][1]) / self.bsheet[np.where(self.bsheet == 'Total Assets')[0][0]][1]
        
        B = self.bsheet[np.where(self.bsheet == 'Retained Earnings')[0][0]][1] / self.bsheet[np.where(self.bsheet == 'Total Assets')[0][0]][1]
        
        C = self.ins[np.where(self.ins == 'Ebit')[0][0]][1] / self.bsheet[np.where(self.bsheet == 'Total Assets')[0][0]][1]
        
        D = self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1] / self.bsheet[np.where(self.bsheet == 'Total Liab')[0][0]][1]
        
        zscore = round(3.25 + 6.56*A + 3.26*B + 6.72*C + 1.05*D, 2)
        
        return zscore
    
    def _get_operating_cushion(self):
        """
        Calculates the current operating cushion of the given ticker by subtracting the SG&A/Revenue from the gross margin

        :return: Operating cushion
        :rtype: float
        """
        sgapct = self.ins[np.where(self.ins == 'Selling General Administrative')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]
        
        grossmargin = self.ins[np.where(self.ins == 'Gross Profit')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]
        
        operating_cushion = grossmargin - sgapct
        
        return round(operating_cushion, 2)
    
    def _get_core_operating_growth(self):
        """
        Calculates the current core operating the growth profile of the given ticker by subtracting the operating cushion from the working capital/revenue percent

        :return: Core operating the growth profile
        :rtype: float
        """
        operatingcushion = self._get_operating_cushion()
        
        ar = round(self.bsheet[np.where(self.bsheet == 'Net Receivables')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)
        
        ap = round(self.bsheet[np.where(self.bsheet == 'Accounts Payable')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)
        
        try:
            
            inventory = round(self.bsheet[np.where(self.bsheet == 'Inventory')[0][0]][1] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1], 2)
            
        except:
            
            inventory = 0
            
        wc = round(ap - ar - inventory, 2)
        
        cogp = round(wc + operatingcushion, 2)
        
        return cogp
    
    def credit_score(self):
        """
        Uses the _get_zscore function to retrieve the current Altmans Z-score then prints for comparisons credit scores.

        :return: Altmans Z-score
        :rtype: float
        """
        zscore = self._get_zscore()
        
        print(f"""
        Rating        Mininmum Z-score
        AAA           8.80
        AA            8.40
        A+            8.22
        A             6.94
        A-            6.12
        BBB+          5.80
        BBB           5.75
        BBB-          5.70
        BB+           5.65
        BB            5.52
        BB-           5.07
        B+            4.81
        B             4.03
        B-            3.74
        CCC+          2.84
        CCC           2.57
        CCC-          1.72
        D             0.05
        Credit score: {zscore}
        """)
        
        return zscore
        
    def cogp(self):
        """
        Calculates a make shift financial statement over a 5 year period, ultimately calculating the previous and current core operating growth profile.
        """
        grossmargins = [round(self.ins[np.where(self.ins == 'Gross Profit')[0][0]][i] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][i], 2) for i in range(1, 5)]
        
        sga = [round(self.ins[np.where(self.ins == 'Selling General Administrative')[0][0]][i] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][i], 2) for i in range(1, 5)]
        
        try:

        	ar = [round(self.bsheet[np.where(self.bsheet == 'Net Receivables')[0][0]][i] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][i], 2) for i in range(1, 5)]

        except:

        	ar = [0, 0, 0, 0]
        
        try:

        	ap = [round(self.bsheet[np.where(self.bsheet == 'Accounts Payable')[0][0]][i] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][i], 2) for i in range(1, 5)]

        except:

        	ap = [0, 0, 0, 0]
        
        try:
            
            inventory = [round(self.bsheet[np.where(self.bsheet == 'Inventory')[0][0]][i] / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][i], 2) for i in range(1, 5)]
            
        except:
            
            inventory = [0, 0, 0, 0]
        
        operatingcushion = [round(grossmargins[i] - sga[i], 2) for i in range(0, 4)]
        
        wc = [round(ap[i] - ar[i] - inventory[i], 2) for i in range(0, 4)]
        
        cogp = [round(wc[i] + operatingcushion[i], 2) for i in range(0, 4)]
        
        print("Its important to analyze the change in operating cushion and what causes the change, is SG&A rising/falling, or is Gross Margin rising/falling")
        
        print(f'Gross Margins                             {grossmargins}')
        
        print(f'Less: SG&A                                {sga}')
        
        print(f'------------------------------------------------------------------')
        
        print(f'Operating Cushion                         {operatingcushion}')
        
        print(f'------------------------------------------------------------------')
        
        print(f'Less: Accounts Receivable                 {ar}')
        
        print(f'Les: Inventory                            {inventory}')
        
        print(f'Plus: Accounts Payable                    {ap}')
        
        print(f'------------------------------------------------------------------')
        
        print(f'Working Cap                               {wc}')
        
        print(f'Plus: Operating Cushion                   {operatingcushion}')
        
        print(f'------------------------------------------------------------------')
        
        print(f'Core Operating Growth Profile             {cogp}')
        
    def undervalue_spotting(self):
        """
        Calculates numerous valuation metrics for identifying undervalued companys.
        """
        price = self._getprice()
        
        sharesoutstanding = self._sharesoutstanding()
        
        current_assets = self.bsheet[np.where(self.bsheet == 'Total Current Assets')[0][0]][1]

        current_assets_t2 = self.bsheet[np.where(self.bsheet == 'Total Current Assets')[0][0]][2]
        
        current_liabilities = self.bsheet[np.where(self.bsheet == 'Total Current Liabilities')[0][0]][1]

        current_liabilities_t2 = self.bsheet[np.where(self.bsheet == 'Total Current Liabilities')[0][0]][2]
        
        cash =  self.bsheet[np.where(self.bsheet == 'Cash')[0][0]][1]
        
        cash_t2 =  self.bsheet[np.where(self.bsheet == 'Cash')[0][0]][2]
        
        change_non_cash_workingcap = (current_assets - current_liabilities - cash) - (current_assets_t2 - current_liabilities_t2 - cash_t2)
        
        try:
            
            bvdebt = self.bsheet[np.where(self.bsheet == 'Short Long Term Debt')[0][0]][1] + self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]
            
        except:

            try:

            	bvdebt = self.bsheet[np.where(self.bsheet == 'Long Term Debt')[0][0]][1]
            
            except:

            	bvdebt = 0
            
        eps = round((self.ins[np.where(self.ins == 'Net Income')[0][0]][1] / sharesoutstanding), 2)
        eps2 = round((self.ins[np.where(self.ins == 'Net Income')[0][0]][2] / (sharesoutstanding)), 2)
        
        ev = (price * sharesoutstanding) + bvdebt - cash
        
        pe = round(price / (self.ins[np.where(self.ins == 'Net Income')[0][0]][1] / sharesoutstanding), 2)
        
        eps_g = round(((eps - eps2) / eps2), 2)
        
        pb = round((price * sharesoutstanding) / (self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1]), 2)
        
        roe = round((self.ins[np.where(self.ins == 'Net Income')[0][0]][1]) / (self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1]), 2)
        
        ps = round((price * sharesoutstanding) / (self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]), 2)
        
        net_margin = round((self.ins[np.where(self.ins == 'Net Income')[0][0]][1]) / (self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]), 2)
        
        ev_ebitda = round(ev / (self.ins[np.where(self.ins == 'Ebit')[0][0]][1] + self.cf[np.where(self.cf == 'Depreciation')[0][0]][1]), 2)
        
        reinvestment_rate = round(((-1 * (self.cf[np.where(self.cf == 'Capital Expenditures')[0][0]][1])) - self.cf[np.where(self.cf == 'Depreciation')[0][0]][1] + change_non_cash_workingcap) / (self.ins[np.where(self.ins == 'Ebit')[0][0]][1]), 2)
        
        ev_capital = round(ev / (bvdebt + self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1]), 2)
        
        roc = round(((self.ins[np.where(self.ins == 'Operating Income')[0][0]][1]) * (1 - self.tax_rate)) / (bvdebt + self.bsheet[np.where(self.bsheet == 'Total Stockholder Equity')[0][0]][1]), 2)
        
        ev_sales = round((ev / self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]), 2)
        
        op_margin = round(((self.ins[np.where(self.ins == 'Operating Income')[0][0]][1]) * (1 - self.tax_rate)) / (self.ins[np.where(self.ins == 'Total Revenue')[0][0]][1]), 2)
        
        zscore = self._get_zscore()
        
        print(
        f'Undervalue Spotting')
        
        print(f'P/E Ratio:{pe}     Expected Growth:{eps_g}            We want: Low P/E and a high Expected Growth')
        
        print(f'P/B Ratio:{pb}     ROE:{roe}                         We want: Low P/B and a high ROE')
        
        print(f'P/S Ratio:{ps}     Net Margin:{net_margin}                  We want: Low P/S and a high Net Margin')
        
        print(f'EV/EBITDA:{ev_ebitda}    Reinvestment Rate:{reinvestment_rate}           We want: Low EV/EBITDA and a low Reinvestment Rate')
        
        print(f'EV/CAPITAL:{ev_capital}   ROC:{roc}                         We want: Low EV/CAPITAL and a high ROC')
        
        print(f'EV/SALES:{ev_sales}       Operating Margin:{op_margin}             We want: Low EV/SALES and a high Operating Margin')
        
        print(f'P/B Ratio:{pb}     Altman Z score:{zscore}                  We want: Low P/B and a high Altman Z score')  