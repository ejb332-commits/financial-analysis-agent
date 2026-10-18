
import csv
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

from models.financial_interpreter import generate_interpretations


METRICS = {
    "Profit Margin": ("profit_margin", "%"),
    "Revenue Growth": ("revenue_growth", "%"),
    "Return on Assets": ("roa", "%"),
    "Return on Equity": ("roe", "%"),
    "Debt-to-Equity": ("debt_to_equity", "x"),
    "Current Ratio": ("current_ratio", "x"),
    "Free Cash Flow": ("free_cash_flow", "$")
}


def safe_calculate(function, *values):
    if any(value is None for value in values):
        return None

    try:
        return function(*values)
    except ZeroDivisionError:
        return None


def format_result(value, unit):
    if value is None:
        return "N/A"

    if unit == "$":
        return f"${value:,.2f}"

    return f"{value:.2f}{unit}"


def analyze_company(symbol):
    data = get_company_data(symbol)

    company = {
        "ticker": symbol,
        "name": data["company"],
        "source": data["source"],
        "fiscal_year_end": data["fiscal_year_end"],
        "previous_fiscal_year_end": data[
            "previous_fiscal_year_end"
        ],
        "retrieved_at": data["retrieved_at"]
    }

    calculations = {
        "profit_margin": (
            calculate_profit_margin,
            data["revenue"],
            data["profit"]
        ),
        "revenue_growth": (
            calculate_revenue_growth,
            data["revenue"],
            data["previous_revenue"]
        ),
        "roa": (
            calculate_roa,
            data["profit"],
            data["assets"]
        ),
        "roe": (
            calculate_roe,
            data["profit"],
            data["equity"]
        ),
        "debt_to_equity": (
            calculate_debt_to_equity,
            data["total_debt"],
            data["equity"]
        ),
        "current_ratio": (
            calculate_current_ratio,
            data["current_assets"],
            data["current_liabilities"]
        ),
        "free_cash_flow": (
            calculate_free_cash_flow,
            data["operating_cash_flow"],
            data["capital_expenditures"]
        )
    }

    for key, (function, *values) in calculations.items():
        company[key] = safe_calculate(function, *values)

    return company


def print_analysis(companies):
    for company in companies:
        print(f"\n{company['name']} ({company['ticker']})")
        print("-" * 45)

        print(f"Fiscal year-end: {company['fiscal_year_end']}")
        print(f"Data source: {company['source']}")
        print(f"Retrieved: {company['retrieved_at']}")

        for label, (key, unit) in METRICS.items():
            print(
                f"{label}: {format_result(company[key], unit)}"
            )

        print("\nFINANCIAL INTERPRETATION")
        print("-" * 45)

        for interpretation in generate_interpretations(company):
            print(interpretation)


def compare_companies(companies):
    lines = ["COMPANY COMPARISON", "-" * 45]

    for label, (key, unit) in METRICS.items():
        available = [
            company for company in companies
            if company[key] is not None
        ]

        if not available:
            lines.append(f"{label}: No available data")
            continue

        if key == "debt_to_equity":
            best = min(available, key=lambda c: c[key])
            comparison = "Lowest"
        else:
            best = max(available, key=lambda c: c[key])
            comparison = "Highest"

        lines.append(
            f"{comparison} {label}: {best['name']} "
            f"({format_result(best[key], unit)})"
        )

    print("\n" + "\n".join(lines))
    return lines


def save_results(companies, comparison_lines):
    folder = "results/real_companies"
    os.makedirs(folder, exist_ok=True)

    csv_path = f"{folder}/financial_data.csv"

    fields = [
        "ticker",
        "name",
        "source",
        "fiscal_year_end",
        "previous_fiscal_year_end",
        "retrieved_at"
    ] + [
        key for key, unit in METRICS.values()
    ]

    with open(csv_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(companies)

    report_path = f"{folder}/financial_report.txt"

    with open(report_path, "w") as file:
        file.write("REAL COMPANY FINANCIAL ANALYSIS\n")
        file.write("=" * 45 + "\n\n")

        for company in companies:
            file.write(
                f"{company['name']} ({company['ticker']})\n"
            )
            file.write(
                f"Fiscal year-end: {company['fiscal_year_end']}\n"
            )
            file.write(f"Source: {company['source']}\n")
            file.write(f"Retrieved: {company['retrieved_at']}\n")
            file.write("-" * 45 + "\n")

            for label, (key, unit) in METRICS.items():
                file.write(
                    f"{label}: "
                    f"{format_result(company[key], unit)}\n"
                )

            file.write("\nFINANCIAL INTERPRETATION\n")

            for interpretation in generate_interpretations(company):
                file.write(interpretation + "\n")

            file.write("\n")

        file.write("\n".join(comparison_lines))
        file.write("\n\n")
        file.write(
            "Interpretations use illustrative thresholds "
            "and are not investment recommendations.\n"
        )
        file.write(
            "Financial periods may differ between companies.\n"
        )

    print(f"\nData saved: {csv_path}")
    print(f"Report saved: {report_path}")


def generate_charts(companies):
    folder = "results/real_companies"
    os.makedirs(folder, exist_ok=True)

    for label, (key, unit) in METRICS.items():
        available = [
            company for company in companies
            if company[key] is not None
        ]

        if not available:
            continue

        names = [company["ticker"] for company in available]
        values = [company[key] for company in available]

        plt.figure(figsize=(8, 5))
        plt.bar(names, values)
        plt.title(f"{label} Comparison")
        plt.xlabel("Company")
        plt.ylabel(f"{label} ({unit})")
        plt.axhline(0, linewidth=0.8)
        plt.tight_layout()

        filepath = f"{folder}/{key}_chart.png"

        plt.savefig(filepath)
        plt.close()

        print(f"Chart saved: {filepath}")


def main():
    user_input = input(
        "Enter stock tickers separated by commas "
        "(example: AAPL, MSFT, NVDA): "
    )

    tickers = [
        ticker.strip().upper()
        for ticker in user_input.split(",")
        if ticker.strip()
    ]

    if not tickers:
        print("No tickers entered.")
        return

    companies = []

    for symbol in tickers:
        try:
            print(f"\nRetrieving {symbol}...")
            company = analyze_company(symbol)
            companies.append(company)
        except Exception as error:
            print(f"Could not analyze {symbol}: {error}")

    if not companies:
        print("No company data retrieved.")
        return

    print_analysis(companies)
    comparison_lines = compare_companies(companies)
    save_results(companies, comparison_lines)
    generate_charts(companies)


if __name__ == "__main__":
    main()