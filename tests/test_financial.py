import unittest

from models.financial_metrics import (
    calculate_profit_margin,
    calculate_revenue_growth,
    calculate_roa,
    calculate_roe,
    calculate_debt_to_equity,
    calculate_current_ratio,
    calculate_free_cash_flow
)


class TestFinancialAnalysis(unittest.TestCase):

    def test_profit_margin(self):
        self.assertAlmostEqual(
            calculate_profit_margin(1000000, 150000), 15
        )

    def test_revenue_growth(self):
        self.assertAlmostEqual(
            calculate_revenue_growth(1000000, 800000), 25
        )

    def test_roa(self):
        self.assertAlmostEqual(
            calculate_roa(150000, 2000000), 7.5
        )

    def test_roe(self):
        self.assertAlmostEqual(
            calculate_roe(150000, 1200000), 12.5
        )

    def test_debt_to_equity(self):
        self.assertAlmostEqual(
            calculate_debt_to_equity(500000, 1200000),
            0.4166666667
        )

    def test_current_ratio(self):
        self.assertAlmostEqual(
            calculate_current_ratio(600000, 300000), 2
        )

    def test_free_cash_flow(self):
        self.assertEqual(
            calculate_free_cash_flow(200000, 50000),
            150000
        )


if __name__ == "__main__":
    unittest.main()