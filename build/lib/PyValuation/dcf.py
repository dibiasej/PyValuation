from PyValuation import FinancialData
import numpy as np
import yfinance as yf
import numpy_financial as npf

class DCF(FinancialData):
    """
    Instantiate a discounted cash flow model for valuating a company.
    FinancialData will be inherited as a child class in order to pull financial statements and data.
    Growth rates are calculated and used ot project out cash flows.
    The intrinsic value of a company is calculated based on projected cash flows, discount rates and growth rates

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
        
        super().__init__(ticker, tax_rate = .28, risk_free_rate = .04, equity_risk_premium = 0.12)
                
        self.ins = super().incomestatement()
        
        self.cf = super().cashflowstatement()
        
    def formulas_info(self):
        """
        Print statement to show formulas used is calculating different forms of cash flow
        """
        #if formula == 'cash flow':
        print(
        """
        The formulas used for current cash flows are:

        ebitda = Ebit + Depreciation

        cashflow = Total Cash From Operating Activities

        free cash flow = Total Cash From Operating Activities + Capital Expenditures

        free cash flow to equity = Total Cash From Operating Activities + Capital Expenditures + Net Borrowings

        free cash flow to the firm = Total Cash From Operating Activities + Capital Expenditures + Interest Expense

        """)
        
    def current_cashflows(self):
        """
        Pull data from financial statements and calculate current and previous 4 years ebitda, cash flow, free cash flow, free cash flow to equity and free cash flow to the firm.

        :return: Numpy array of multiple cash flows
        :rtype: np.array
        """     
        try:
            
            net_borrowings = self.cf[np.where(self.cf == 'Net Borrowings')[0][0]]
            
        except:
            
            print('There are no Net Borrowings')
            
            net_borrowings = np.array(['net borrowings', 0, 0, 0, 0], dtype=object)
        
        ebitda = (self.cf[np.where(self.cf == 'Depreciation')[0][0]] + self.ins[np.where(self.ins == 'Ebit')[0][0]]).tolist()
        
        cashflow = (self.cf[np.where(self.cf == 'Total Cash From Operating Activities')[0][0]]).tolist()
                
        freecashflow = (self.cf[np.where(self.cf == 'Total Cash From Operating Activities')[0][0]] + self.cf[np.where(self.cf == 'Capital Expenditures')[0][0]]).tolist()
                
        fcfe = (self.cf[np.where(self.cf == 'Total Cash From Operating Activities')[0][0]] + self.cf[np.where(self.cf == 'Capital Expenditures')[0][0]] + net_borrowings).tolist()
        
        fcff = (self.cf[np.where(self.cf == 'Total Cash From Operating Activities')[0][0]] + self.cf[np.where(self.cf == 'Capital Expenditures')[0][0]] + self.ins[np.where(self.ins == 'Interest Expense')[0][0]]).tolist()
        
        ebitda[0], cashflow[0], freecashflow[0], fcfe[0], fcff[0] = 'EBITDA', 'CF', 'FCF', 'FCFE', 'FCFF'
        
        cashflowarr = [ebitda, cashflow, freecashflow, fcfe, fcff]
               
        return cashflowarr    

    def growth_rates(self):
        """
        Use current_cashflows function to calculate the rate at which the cash flow metrics change year over year.

        :return: Numpy array of year over year growth rates.
        :rtype: np.array 
        """
        cashflow = self.current_cashflows()
        
        for i in cashflow:
            metric = i[0]   
            i = i[1:][::-1]
            i = [round((i[f] - i[f - 1]) / i[f - 1], 2) for f in range(1, len(i))]
            print(f'{metric} growth over the last 3 years is {i}')
            
    def projected_cashflows(self):
        """
        Projects out cash flows based on multiple user inputs including discount rates and growth rates.

        :return: Cash flows projected out to 5 years
        :rtype: np.array
        """
        wacc = float(input('Enter the WACC'))
        
        cost_of_equity = float(input('Enter the Cost of Equity, Either Unlevered or Levered Beta'))
        
        cf_growth_rate = float(input('Enter a CF Growth Rate'))
        
        fcf_growth_rate = float(input('Enter a FCF Growth Rate'))
        
        fcfe_growth_rate = float(input('Enter a FCFE Growth Rate'))
        
        fcff_growth_rate = float(input('Enter a FCFF Growth Rate'))
        
        cfdf = self.current_cashflows()
        
        cf = [cfdf[1][1]]
        fcf = [cfdf[2][1]]
        fcfe = [cfdf[3][1]]
        fcff = [cfdf[4][1]]
        for i in range(5):

            cf.append(round((cf[i] * (1 + cf_growth_rate)), 2))
            fcf.append(round((fcf[i] * (1 + fcf_growth_rate)), 2))
            fcfe.append(round((fcfe[i] * (1 + fcfe_growth_rate)), 2))
            fcff.append(round((fcff[i] * (1 + fcff_growth_rate)), 2))
            
        print(f'Projected cash flow over the next five years is {cf}')
        print(f'Projected free cash flow over the next five years is {fcf}')
        print(f'Projected cash flow to equity over the next five years is {fcfe}')
        print(f'Projected cash flow to the firm over the next five years is {fcff}')
        

 
    def intrinsic_value(self, freecashflowequity = 0, freecashflowtofirm = 0):
        """
        Individual company intrinsic value calculation.

        :param: freecashflowequity: Optional free cash flow to equity to project.
        :type freecashflowequity: int

        :param: freecashflowtofirm: Optional free cash flow to firm to project.
        :type freecashflowtofirm: int

        :return: Intrinsic value using free cash flow to equity and free cash flow to the firm.
        :rtype: dict
        """
        wacc = float(input('Enter the WACC'))
        
        cost_of_equity = float(input('Enter the Cost of Equity, Either Unlevered or Levered Beta'))
        
        fcfe_growth_rate = float(input('Enter a FCFE Growth Rate'))
        
        fcff_growth_rate = float(input('Enter a FCFF Growth Rate'))
        
        print("If current cash flows are negative you may want to enter a personal one using freecashflowequity and freecashflowtofirm as parameters")
        
        cfdf = self.current_cashflows()
        
        sharesoutstanding = super()._sharesoutstanding()
        
        if freecashflowequity == 0:
            
            fcfe = [cfdf[3][1]]
            
        else:
            
            fcfe = [freecashflowequity]
        
        if freecashflowtofirm == 0:
        
            fcff = [cfdf[4][1]]
            
        else:
            
            fcff = [freecashflowtofirm]
        
        for i in range(5):

            fcfe.append((fcfe[i] * (1 + fcfe_growth_rate)))
            fcff.append((fcff[i] * (1 + fcff_growth_rate)))
        
        fcfe_npv = npf.npv(cost_of_equity, fcfe)
                
        fcff_npv = npf.npv(wacc, fcff)

        intinsic_fcff = ((((fcff[5] * (1.02)) / (wacc - .02)) / (1 + wacc) ** 5) + fcff_npv) / sharesoutstanding
        
        intinsic_fcfe = ((((fcff[5] * (1.02)) / (cost_of_equity - .02)) / (1 + cost_of_equity) ** 5) + fcfe_npv) / sharesoutstanding
    
        return {'FCFF' : round(intinsic_fcff, 2), 'FCFE' : round(intinsic_fcfe, 2)}
    
    

    def outside_spread(self, freecashflowequity = 0, freecashflowtofirm = 0):
        """
        Individual company intrinsic value calculation using multiple growth rates in order to create a upper and lower bound on the possible values of the company.

        :param: freecashflowequity: Optional free cash flow to equity to project.
        :type freecashflowequity: int
        
        :param: freecashflowtofirm: Optional free cash flow to firm to project.
        :type freecashflowtofirm: int

        :return: Intrinsic value using free cash flow to equity and free cash flow to the firm.
        :rtype: dict
        """ 
        inputs = self._inputs()
                
        wacc = inputs['wacc']

        cost_of_equity = inputs['cost_of_equity']
        
        fcff_growth_rate = [.1, .35, .55, .7]
        
        fcfe_growth_rate = [.1, .35, .55, .7]
        
        cfdf = self.current_cashflows()
        
        sharesoutstanding = super()._sharesoutstanding()
        
        fcfe_spread = []
        
        fcff_spread = []
        
        for i, j in zip(fcfe_growth_rate, fcff_growth_rate):
            if freecashflowequity == 0:
            
                fcfe = [cfdf[3][1]]
            
            else:
            
                fcfe = [freecashflowequity]
        
            if freecashflowtofirm == 0:
        
                fcff = [cfdf[4][1]]
            
            else:
            
                fcff = [freecashflowtofirm]
                    
            for t in range(5):

                fcfe.append((fcfe[t] * (1 + i)))
                fcff.append((fcff[t] * (1 + j)))

            fcfe_npv = npf.npv(cost_of_equity, fcfe)
                        
            fcff_npv = npf.npv(wacc, fcff)
            
            intinsic_fcff = ((((fcff[5] * (1.028)) / (wacc - .02)) / (1 + wacc) ** 5) + fcff_npv) / sharesoutstanding

            intinsic_fcfe = ((((fcff[5] * (1.028)) / (cost_of_equity - .02)) / (1 + cost_of_equity) ** 5) + fcfe_npv) / sharesoutstanding
            
            fcfe_spread.append(round(intinsic_fcfe, 2))
            
            fcff_spread.append(round(intinsic_fcff, 2))
            
        return {'fcff Outside spread': fcff_spread, 'fcfe Outside spread' : fcfe_spread}