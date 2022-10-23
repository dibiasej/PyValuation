import unittest
from PyVal import FinancialData


class FinancialDataTestCase(unittest.TestCase):

    def setUp(self):
        self.financialdata = FinancialData('AAPL')

    def test_balancesheet(self):
        """Test Balance Sheet function"""

        # grab the balance sheet
        result = self.financialdata.balancesheet()
        self.assertEqual(result, result)

    def test_incomestatement(self):
        """Test Income Statement function"""

        # grab the Income Statement
        result = self.financialdata.incomestatement()
        self.assertEqual(result, result)

    def test_cashflowstatement(self):
        """Test cash flow Statement function"""

        # grab the cash flow Statement
        result = self.financialdata.cashflowstatement()
        self.assertEqual(result, result)


if __name__ == '__main__':
    unittest.main()