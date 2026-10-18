
from data.real_company_data import get_company_data

from models.financial_metrics import (
    calculate_profit_margin,
    calculate_revenue_growth,
    calculate_roa,
    calculate_roe,
    calculate_debt_to_equity,
    calculate_current_ratio,
    calculate_free_cash_flow
)


def safe_calculate(function, *values):
    if any(value is None for value in values):
        return None

    try:
        return function(*values)
    except ZeroDivisionError:
        return None


def format_result(value, unit="%"):
    if value is None:
        return "N/A"

    if unit == "$":
        return f"${value:,.2f}"

    return f"{value:.2f}{unit}"


def analyze_company(symbol):
    print(f"\nRetrieving financial data for {symbol}...")

    data = get_company_data(symbol)

    print(f"\nFinancial Analysis: {data['company']}")
    print("-" * 45)

    metrics = {
        "Profit Margin": (
            calculate_profit_margin,
            (data["revenue"], data["profit"]),
            "%"
        ),
        "Revenue Growth": (
            calculate_revenue_growth,
            (data["revenue"], data["previous_revenue"]),
            "%"
        ),
        "Return on Assets": (
            calculate_roa,
            (data["profit"], data["assets"]),
            "%"
        ),
        "Return on Equity": (
            calculate_roe,
            (data["profit"], data["equity"]),
            "%"
        ),
        "Debt-to-Equity": (
            calculate_debt_to_equity,
            (data["total_debt"], data["equity"]),
            "x"
        ),
        "Current Ratio": (
            calculate_current_ratio,
            (data["current_assets"], data["current_liabilities"]),
            "x"
        ),
        "Free Cash Flow": (
            calculate_free_cash_flow,
            (
                data["operating_cash_flow"],
                data["capital_expenditures"]
            ),
            "$"
        )
    }

    for name, (function, values, unit) in metrics.items():
        result = safe_calculate(function, *values)

        print(f"{name}: {format_result(result, unit)}")


def main():
    tickers = ["AAPL", "MSFT", "NVDA"]

    for symbol in tickers:
        try:
            analyze_company(symbol)
        except Exception as error:
            print(f"Unable to analyze {symbol}: {error}")


if __name__ == "__main__":
    main()