
import unittest

from models.financial_interpreter import (
    interpret_metric,
    generate_interpretations
)


class TestFinancialInterpreter(unittest.TestCase):

    def test_negative_profit_margin(self):
        result = interpret_metric("profit_margin", -5)
        self.assertIn("net loss", result)

    def test_revenue_decline(self):
        result = interpret_metric("revenue_growth", -10)
        self.assertIn("declined", result)

    def test_low_current_ratio(self):
        result = interpret_metric("current_ratio", 0.8)
        self.assertIn("liabilities exceed", result)

    def test_positive_free_cash_flow(self):
        result = interpret_metric("free_cash_flow", 100000)
        self.assertIn("positive free cash flow", result)

    def test_missing_data(self):
        result = interpret_metric("roa", None)
        self.assertIn("Insufficient data", result)

    def test_generate_interpretations(self):
        company = {
            "profit_margin": 15,
            "revenue_growth": 10,
            "roa": 8,
            "roe": 12,
            "debt_to_equity": 0.6,
            "current_ratio": 1.5,
            "free_cash_flow": 100000
        }

        results = generate_interpretations(company)
        self.assertEqual(len(results), 7)


if __name__ == "__main__":
    unittest.main()