
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf


def get_statement_value(statement, possible_names, period):
    if statement.empty or period not in statement.columns:
        return None

    for name in possible_names:
        if name in statement.index:
            value = statement.loc[name, period]

            if isinstance(value, pd.Series):
                value = value.iloc[0]

            if pd.notna(value):
                return float(value)

    return None


def get_company_data(ticker_symbol):
    ticker_symbol = ticker_symbol.upper()
    ticker = yf.Ticker(ticker_symbol)

    financials = ticker.financials
    balance_sheet = ticker.balance_sheet
    cash_flow = ticker.cashflow

    if financials.empty:
        raise ValueError(
            f"No income statement available for {ticker_symbol}"
        )

    if balance_sheet.empty or cash_flow.empty:
        raise ValueError(
            f"Missing balance sheet or cash flow statement "
            f"for {ticker_symbol}"
        )

    common_periods = (
        set(financials.columns)
        & set(balance_sheet.columns)
        & set(cash_flow.columns)
    )

    if not common_periods:
        raise ValueError(
            f"No matching annual reporting periods for {ticker_symbol}"
        )

    current_period = max(common_periods)

    earlier_periods = [
        period
        for period in financials.columns
        if period < current_period
    ]

    previous_period = (
        max(earlier_periods) if earlier_periods else None
    )

    def income(names, period=current_period):
        return get_statement_value(financials, names, period)

    def balance(names):
        return get_statement_value(
            balance_sheet, names, current_period
        )

    def cash(names):
        return get_statement_value(
            cash_flow, names, current_period
        )

    capex = cash(["Capital Expenditure"])

    if capex is not None:
        capex = abs(capex)

    previous_revenue = (
        income(["Total Revenue"], previous_period)
        if previous_period is not None
        else None
    )

    return {
        "company": ticker_symbol,
        "ticker": ticker_symbol,
        "source": "Yahoo Finance via yfinance",
        "fiscal_year_end": current_period.strftime("%Y-%m-%d"),
        "previous_fiscal_year_end": (
            previous_period.strftime("%Y-%m-%d")
            if previous_period is not None
            else None
        ),
        "retrieved_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "revenue": income(["Total Revenue"]),
        "previous_revenue": previous_revenue,
        "profit": income([
            "Net Income",
            "Net Income Common Stockholders"
        ]),
        "assets": balance(["Total Assets"]),
        "equity": balance([
            "Stockholders Equity",
            "Total Equity Gross Minority Interest"
        ]),
        "total_debt": balance(["Total Debt"]),
        "current_assets": balance(["Current Assets"]),
        "current_liabilities": balance(["Current Liabilities"]),
        "operating_cash_flow": cash(["Operating Cash Flow"]),
        "capital_expenditures": capex
    }