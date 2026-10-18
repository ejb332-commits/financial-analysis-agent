"""Historical financial research, deterministic checks, and reproducible artifacts."""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results' / 'research'

ROWS = {
    'revenue': ('Total Revenue', 'Operating Revenue'),
    'net_income': ('Net Income', 'Net Income Common Stockholders'),
    'assets': ('Total Assets',),
    'equity': ('Stockholders Equity', 'Total Equity Gross Minority Interest', 'Common Stock Equity'),
    'debt': ('Total Debt', 'Long Term Debt'),
    'current_assets': ('Current Assets',),
    'current_liabilities': ('Current Liabilities',),
    'operating_cash_flow': ('Operating Cash Flow', 'Cash Flow From Continuing Operating Activities'),
    'capital_expenditures': ('Capital Expenditure', 'Capital Expenditures'),
}


def _number(frame, names, period):
    if frame is None or frame.empty:
        return None
    for name in names:
        if name in frame.index and period in frame.columns:
            value = frame.loc[name, period]
            if isinstance(value, pd.Series):
                value = value.iloc[0]
            if pd.notna(value):
                try:
                    value = float(value)
                    return value if math.isfinite(value) else None
                except (TypeError, ValueError):
                    pass
    return None


def _ratio(numerator, denominator, percentage=False):
    if numerator is None or denominator is None or denominator == 0:
        return None
    value = numerator / denominator * (100 if percentage else 1)
    return round(value, 4) if math.isfinite(value) else None


def _calculate(row, previous_revenue):
    revenue = row['revenue']
    profit = row['net_income']
    op_cf = row['operating_cash_flow']
    capex = row['capital_expenditures']
    return {
        'profit_margin_pct': _ratio(profit, revenue, True),
        'revenue_growth_pct': _ratio(revenue - previous_revenue, previous_revenue, True)
            if revenue is not None and previous_revenue is not None else None,
        'return_on_assets_pct': _ratio(profit, row['assets'], True),
        'return_on_equity_pct': _ratio(profit, row['equity'], True),
        'debt_to_equity': _ratio(row['debt'], row['equity']),
        'current_ratio': _ratio(row['current_assets'], row['current_liabilities']),
        'free_cash_flow_usd': round(op_cf - abs(capex), 2)
            if op_cf is not None and capex is not None else None,
    }


def fetch_history(ticker: str, years: int = 4) -> dict:
    """Yahoo Finance commonly exposes up to ~4 annual periods; never invent earlier ones."""
    ticker = ticker.strip().upper()
    if not ticker or not ticker.replace('.', '').replace('-', '').isalnum() or len(ticker) > 15:
        raise ValueError('Invalid ticker symbol')
    if not isinstance(years, int) or not 2 <= years <= 4:
        raise ValueError('years must be an integer from 2 to 4')

    import yfinance as yf
    stock = yf.Ticker(ticker)
    income = stock.financials
    balance = stock.balance_sheet
    cashflow = stock.cashflow
    if any(frame is None or frame.empty for frame in (income, balance, cashflow)):
        raise ValueError(f'Missing annual statements for {ticker}')

    common = sorted(set(income.columns) & set(balance.columns) & set(cashflow.columns))
    if not common:
        raise ValueError(f'No matching fiscal-year columns for {ticker}')
    # Build chronologically, using an extra income period for earliest growth if present.
    common = common[-years:]
    records = []
    for period in common:
        row = {}
        for field, names in ROWS.items():
            statement = income if field in ('revenue', 'net_income') else (
                balance if field in ('assets', 'equity', 'debt', 'current_assets', 'current_liabilities') else cashflow
            )
            row[field] = _number(statement, names, period)
        older = sorted(p for p in income.columns if p < period)
        previous_revenue = _number(income, ROWS['revenue'], older[-1]) if older else None
        records.append({
            'fiscal_year_end': pd.Timestamp(period).date().isoformat(),
            'raw': row,
            'previous_revenue': previous_revenue,
            'metrics': _calculate(row, previous_revenue),
        })
    return {
        'ticker': ticker,
        'source': 'Yahoo Finance annual financial statements via yfinance',
        'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
        'periods': records,
        'limitations': [
            'Yahoo Finance may provide fewer than four aligned annual periods.',
            'Statement labels, restatements, units, and availability may vary by company.',
            'Fiscal years may not align across different companies.',
            'Ratios with missing inputs or zero denominators are null.',
            'Negative equity can make ROE and debt-to-equity misleading.',
        ],
    }


def detect_anomalies(history: dict) -> list[dict]:
    """Transparent screening thresholds, not investment recommendations."""
    alerts = []
    periods = history['periods']
    for previous, current in zip(periods, periods[1:]):
        a, b = previous['metrics'], current['metrics']
        for key, threshold in (('profit_margin_pct', 5), ('revenue_growth_pct', 15)):
            x, y = a.get(key), b.get(key)
            if x is not None and y is not None and abs(y - x) >= threshold:
                alerts.append({
                    'metric': key, 'from_period': previous['fiscal_year_end'],
                    'to_period': current['fiscal_year_end'],
                    'previous': x, 'current': y,
                    'change': round(y - x, 4),
                    'rule': f'absolute change >= {threshold} percentage points',
                })
    for current in periods:
        b = current['metrics']
        fcf = b.get('free_cash_flow_usd')
        if fcf is not None and fcf < 0:
            alerts.append({
                'metric': 'free_cash_flow_usd', 'period': current['fiscal_year_end'],
                'current': fcf, 'rule': 'negative annual free cash flow',
            })
        equity = current['raw'].get('equity')
        if equity is not None and equity <= 0:
            alerts.append({
                'metric': 'equity', 'period': current['fiscal_year_end'],
                'current': equity, 'rule': 'nonpositive shareholders equity',
            })
    return alerts


def verify_calculations(history: dict) -> dict:
    """Recompute every stored metric from recorded raw inputs, independently of the LLM."""
    failures = []
    periods = history['periods']
    for i, period in enumerate(periods):
        # Prefer the recorded prior income-statement year; older fixtures can
        # fall back to the preceding aligned period.
        prior_revenue = period.get('previous_revenue', periods[i - 1]['raw']['revenue'] if i > 0 else None)
        expected = _calculate(period['raw'], prior_revenue)
        for key, actual in period['metrics'].items():
            computed = expected[key]
            if (actual is None) != (computed is None) or (
                actual is not None and not math.isclose(actual, computed, rel_tol=1e-8, abs_tol=1e-3)
            ):
                failures.append({'period': period['fiscal_year_end'], 'metric': key,
                                 'stored': actual, 'recomputed': computed})
    return {'passed': not failures, 'checked_periods': len(periods), 'failures': failures,
            'scope': 'Stored numeric metrics; does not verify LLM prose or Yahoo Finance accuracy'}


def save_research(history: dict) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    alerts = detect_anomalies(history)
    verification = verify_calculations(history)
    payload = {'history': history, 'anomalies': alerts, 'verification': verification}
    canonical = json.dumps(payload, sort_keys=True, allow_nan=False)
    digest = hashlib.sha256(canonical.encode()).hexdigest()[:12]
    stem = f"{history['ticker']}_{digest}"
    json_path = OUT / f'{stem}.json'
    report_path = OUT / f'{stem}.md'
    json_path.write_text(json.dumps(payload, indent=2, allow_nan=False), encoding='utf-8')

    lines = [f"# Financial research: {history['ticker']}", '',
             f"Source: {history['source']}",
             f"Retrieved (UTC): {history['retrieved_at_utc']}",
             f"Verification: {'PASS' if verification['passed'] else 'FAIL'}", '',
             '## Annual metrics', '',
             '| Fiscal year end | Profit margin % | Revenue growth % | ROE % | Current ratio | FCF (USD) |',
             '|---|---:|---:|---:|---:|---:|']
    def fmt(value):
        return 'N/A' if value is None else f'{value:,.2f}'
    for period in history['periods']:
        m = period['metrics']
        lines.append('| ' + ' | '.join([
            period['fiscal_year_end'], fmt(m['profit_margin_pct']),
            fmt(m['revenue_growth_pct']), fmt(m['return_on_equity_pct']),
            fmt(m['current_ratio']), fmt(m['free_cash_flow_usd'])
        ]) + ' |')
    lines += ['', '## Screening flags (rule-based, not investment advice)', '']
    lines += [f"- {json.dumps(a, sort_keys=True)}" for a in alerts] or ['- No flags triggered.']
    lines += ['', '## Limitations', '']
    lines += [f'- {x}' for x in history['limitations']]
    lines += ['', '## Audit record', '', f'- JSON snapshot: `{json_path.name}`',
              f'- Snapshot hash prefix: `{digest}`',
              '- Numerical verification checks the recorded ratios, not the accuracy of the source or AI narrative.']
    report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return {'json_file': str(json_path), 'report_file': str(report_path),
            'verification': verification, 'anomalies': alerts,
            'periods_available': len(history['periods'])}


def investigate_company(ticker: str, years: int = 4) -> dict:
    history = fetch_history(ticker, years)
    artifacts = save_research(history)
    return {'ticker': history['ticker'], 'source': history['source'],
            'retrieved_at_utc': history['retrieved_at_utc'],
            'periods': history['periods'], 'limitations': history['limitations'],
            **artifacts}
