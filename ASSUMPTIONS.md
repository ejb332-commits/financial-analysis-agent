
# Financial Analysis Model — Assumptions

## 1. Data Source

The project currently uses fictional financial data stored in
`data/companies.csv`.

The dataset contains three example companies:
- Company A
- Company B
- Company C

All financial values are illustrative and do not represent
actual publicly traded companies.

## 2. Financial Data

The model assumes that:

- Revenue represents total revenue for the current period.
- Previous revenue represents revenue from the preceding period.
- Profit represents net income for the current period.
- Assets represent total assets.
- Equity represents total shareholders' equity.
- All monetary values are expressed in the same currency.
- All companies use comparable reporting periods.

## 3. Financial Calculations

The model calculates four financial metrics:

### Profit Margin

Profit Margin = (Net Income / Revenue) × 100

This measures how much profit a company generates
for each dollar of revenue.

### Revenue Growth

Revenue Growth = ((Current Revenue - Previous Revenue) /
Previous Revenue) × 100

This measures the percentage change in revenue
between two periods.

### Return on Assets (ROA)

ROA = (Net Income / Total Assets) × 100

This measures profitability relative to total assets.

### Return on Equity (ROE)

ROE = (Net Income / Shareholders' Equity) × 100

This measures profitability relative to shareholders' equity.

## 4. Simplifying Assumptions

- The model uses the supplied asset and equity balances,
  rather than average balances over the reporting period.
- The CSV contains complete and correctly formatted data.
- Revenue, previous revenue, assets, and equity are nonzero.
- Financial metrics are compared without adjusting for
  differences in industry, company size, or accounting methods.
- The company with the highest value for a metric is identified,
  but is not necessarily the best company or investment.

## 5. Limitations

- The program does not verify financial statements.
- The model does not account for debt levels or cash flow.
- It does not calculate investment valuation metrics.
- It does not incorporate market conditions.
- It does not currently generate AI-based recommendations.

## 6. Future Improvements

Future versions may include:

- Real financial statement data
- Additional financial ratios
- Industry-specific comparisons
- Data validation and error handling
- AI-generated financial analysis

## Version 2.5 — Additional Assumptions

The model now includes debt, liquidity, and cash flow analysis.

### Debt-to-Equity

- Total debt represents interest-bearing debt.
- Equity represents shareholders' equity.
- Equity is assumed to be nonzero.
- Lower leverage is not automatically better.

### Current Ratio

- Current assets are assets expected to be converted
  into cash or consumed within the operating cycle.
- Current liabilities are obligations due within the
  operating cycle or one year, as applicable.
- Current liabilities are assumed to be nonzero.

### Free Cash Flow

- Operating cash flow is obtained from operating activities.
- Capital expenditures are entered as positive amounts.
- Free cash flow equals operating cash flow minus
  capital expenditures.

### Data and Comparison Assumptions

- All data remains fictional.
- Financial values use comparable reporting periods.
- The program assumes complete, correctly formatted CSV data.
- Company rankings are descriptive and do not constitute
  investment recommendations.
- The model does not yet validate missing values,
  zero denominators, or inconsistent financial statements.
