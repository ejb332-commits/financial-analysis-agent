
# Financial Analysis — Equations

This document explains the financial formulas implemented
in the Financial Analysis Agent.

## 1. Profit Margin

Formula:

Profit Margin = (Net Income / Revenue) × 100

Python implementation:

```python
def calculate_profit_margin(revenue, profit):
    return (profit / revenue) * 100
```

Example:

- Revenue = $1,000,000
- Net Income = $150,000

Profit Margin = (150,000 / 1,000,000) × 100 = 15%

Interpretation:

The company earns $0.15 in net income for every $1
of revenue.

## 2. Revenue Growth

Formula:

Revenue Growth = ((Current Revenue - Previous Revenue)
                  / Previous Revenue) × 100

Python implementation:

```python
def calculate_revenue_growth(current_revenue, previous_revenue):
    return ((current_revenue - previous_revenue)
            / previous_revenue) * 100
```

Example:

- Current Revenue = $1,000,000
- Previous Revenue = $800,000

Revenue Growth = ((1,000,000 - 800,000) / 800,000) × 100
               = 25%

Interpretation:

The company's revenue increased by 25% compared
with the previous period.

## 3. Return on Assets (ROA)

Formula:

ROA = (Net Income / Total Assets) × 100

Python implementation:

```python
def calculate_roa(profit, assets):
    return (profit / assets) * 100
```

Example:

- Net Income = $150,000
- Total Assets = $2,000,000

ROA = (150,000 / 2,000,000) × 100 = 7.5%

Interpretation:

The company generates $0.075 of net income
for each dollar of assets.

## 4. Return on Equity (ROE)

Formula:

ROE = (Net Income / Shareholders' Equity) × 100

Python implementation:

```python
def calculate_roe(profit, equity):
    return (profit / equity) * 100
```

Example:

- Net Income = $150,000
- Shareholders' Equity = $1,200,000

ROE = (150,000 / 1,200,000) × 100 = 12.5%

Interpretation:

The company generates $0.125 of net income
for every dollar of shareholders' equity.

## 5. Model Assumptions

- Profit is treated as net income.
- Financial values are assumed to be in the same currency.
- Reporting periods are assumed to be comparable.
- Assets and equity use the balances provided in the CSV,
  rather than average balances.
- All denominators are assumed to be nonzero.

See ASSUMPTIONS.md for further details.

## 6. Future Equations

Future versions may introduce:

- Current Ratio
- Debt-to-Equity Ratio
- Free Cash Flow
- Price-to-Earnings (P/E) Ratio
- Discounted Cash Flow (DCF) Valuation


## 7. Debt-to-Equity Ratio

Formula:

Debt-to-Equity = Total Debt / Shareholders' Equity

Python implementation:

    def calculate_debt_to_equity(total_debt, equity):
        return total_debt / equity

Example:

- Total Debt = $500,000
- Shareholders' Equity = $1,200,000

Debt-to-Equity = 500,000 / 1,200,000 = 0.42

Interpretation:

The company has approximately $0.42 of debt for
every $1 of shareholders' equity.

A higher ratio generally indicates greater financial
leverage, although appropriate levels vary by industry.

## 8. Current Ratio

Formula:

Current Ratio = Current Assets / Current Liabilities

Python implementation:

    def calculate_current_ratio(current_assets, current_liabilities):
        return current_assets / current_liabilities

Example:

- Current Assets = $600,000
- Current Liabilities = $300,000

Current Ratio = 600,000 / 300,000 = 2.00

Interpretation:

The company has $2 of current assets for every $1
of current liabilities.

This provides a basic indication of short-term liquidity.

## 9. Free Cash Flow

Formula:

Free Cash Flow = Operating Cash Flow - Capital Expenditures

Python implementation:

    def calculate_free_cash_flow(operating_cash_flow, capital_expenditures):
        return operating_cash_flow - capital_expenditures

Example:

- Operating Cash Flow = $200,000
- Capital Expenditures = $50,000

Free Cash Flow = 200,000 - 50,000 = $150,000

Interpretation:

The company generates $150,000 of cash after
subtracting capital expenditures from operating cash flow.

## Additional Limitations

- Debt-to-equity uses total debt, not total liabilities.
- Current ratio does not measure the quality or liquidity
  of individual current assets.
- Free cash flow is calculated before financing activities.
- Higher ratios are not universally better.
- Comparisons should consider industry and business models.
