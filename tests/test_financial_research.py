import copy
import unittest

from financial_research import _calculate, detect_anomalies, verify_calculations


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.raw_a = dict(revenue=100.0, net_income=10.0, assets=200.0, equity=100.0,
                          debt=40.0, current_assets=60.0, current_liabilities=30.0,
                          operating_cash_flow=20.0, capital_expenditures=-5.0)
        self.raw_b = dict(revenue=120.0, net_income=30.0, assets=220.0, equity=110.0,
                          debt=45.0, current_assets=66.0, current_liabilities=33.0,
                          operating_cash_flow=10.0, capital_expenditures=-15.0)
        self.history = {'periods': [
            {'fiscal_year_end': '2023-12-31', 'raw': self.raw_a,
             'metrics': _calculate(self.raw_a, None)},
            {'fiscal_year_end': '2024-12-31', 'raw': self.raw_b,
             'metrics': _calculate(self.raw_b, self.raw_a['revenue'])},
        ]}

    def test_profit_margin_and_capex_sign(self):
        metrics = _calculate(self.raw_a, None)
        self.assertEqual(metrics['profit_margin_pct'], 10.0)
        self.assertEqual(metrics['free_cash_flow_usd'], 15.0)

    def test_growth(self):
        self.assertEqual(self.history['periods'][1]['metrics']['revenue_growth_pct'], 20.0)

    def test_anomalies(self):
        alerts = detect_anomalies(self.history)
        self.assertTrue(any(a['metric'] == 'profit_margin_pct' for a in alerts))
        self.assertTrue(any(a['metric'] == 'free_cash_flow_usd' for a in alerts))

    def test_verification_passes(self):
        self.assertTrue(verify_calculations(self.history)['passed'])

    def test_verification_detects_tampering(self):
        modified = copy.deepcopy(self.history)
        modified['periods'][1]['metrics']['profit_margin_pct'] = 99
        self.assertFalse(verify_calculations(modified)['passed'])

    def test_missing_inputs(self):
        row = dict(self.raw_a, equity=0, net_income=None)
        result = _calculate(row, None)
        self.assertIsNone(result['return_on_equity_pct'])
        self.assertIsNone(result['profit_margin_pct'])


if __name__ == '__main__':
    unittest.main()
