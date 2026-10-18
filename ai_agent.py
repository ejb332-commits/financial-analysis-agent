"""Groq tool-calling financial agent: latest ratios + auditable historical research."""
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from analyze_real_companies import analyze_company, METRICS, format_result
from financial_research import investigate_company

MODEL = 'openai/gpt-oss-20b'
ROOT = Path(__file__).resolve().parent
MAX_ROUNDS = 6


def get_company_financials(ticker):
    ticker = ticker.strip().upper()
    if not ticker or len(ticker) > 15 or not ticker.replace('.', '').replace('-', '').isalnum():
        return {'error': 'Invalid ticker'}
    company = analyze_company(ticker)
    return {
        'company': company['name'], 'ticker': company['ticker'],
        'source': company['source'], 'fiscal_year_end': company['fiscal_year_end'],
        'retrieved_at': company['retrieved_at'],
        'metrics': {label: format_result(company[key], unit)
                    for label, (key, unit) in METRICS.items()},
    }


TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'get_company_financials',
            'description': 'Get the latest annual financial ratios for a public company. Use for current annual ratio comparisons.',
            'parameters': {
                'type': 'object',
                'properties': {'ticker': {'type': 'string', 'description': 'Stock ticker, e.g. AAPL'}},
                'required': ['ticker'], 'additionalProperties': False,
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'investigate_company',
            'description': ('Retrieve up to four aligned annual fiscal periods, calculate ratios and trends, '
                            'screen for anomalies, independently verify stored calculations, and save an auditable report. '
                            'Use for historical trends, warning signs, changes over time, or evidence-backed research.'),
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {'type': 'string', 'description': 'Stock ticker, e.g. MSFT'},
                    'years': {'type': 'integer', 'minimum': 2, 'maximum': 4,
                              'description': 'Requested annual periods, 2 to 4; defaults to 4'},
                },
                'required': ['ticker'], 'additionalProperties': False,
            },
        },
    },
]


def execute_tool(name, args):
    if not isinstance(args, dict):
        return {'error': 'Tool arguments must be an object'}
    ticker = args.get('ticker')
    if name not in {'get_company_financials', 'investigate_company'}:
        return {'error': f'Unknown tool: {name}'}
    if not isinstance(ticker, str):
        return {'error': 'ticker must be a string'}
    try:
        if name == 'get_company_financials':
            return get_company_financials(ticker)
        years = args.get('years', 4)
        if type(years) is not int or years not in (2, 3, 4):
            return {'error': 'years must be an integer from 2 to 4'}
        return investigate_company(ticker, years)
    except Exception as exc:
        return {'error': f'{type(exc).__name__}: {exc}', 'ticker': ticker}


def run_agent(question):
    load_dotenv(ROOT / '.env')
    key = os.getenv('GROQ_API_KEY')
    if not key:
        print('Missing GROQ_API_KEY in .env')
        return
    client = Groq(api_key=key)
    rules = ROOT / 'config' / 'analysis_rules.md'
    system_text = rules.read_text(encoding='utf-8') if rules.exists() else (
        'You are a careful financial research assistant. Use tools for company-specific figures. '
        'Do not invent data. Cite fiscal periods and sources. Explain limitations.'
    )
    messages = [{'role': 'system', 'content': system_text},
                {'role': 'user', 'content': question}]
    for step in range(MAX_ROUNDS):
        print(f'\nAgent step {step + 1}...')
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS,
            tool_choice='auto', temperature=0.2, max_completion_tokens=1800,
        )
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))
        if not message.tool_calls:
            print('\nFINANCIAL ANALYSIS\n' + '=' * 50)
            print(message.content or 'No response returned.')
            return
        for call in message.tool_calls:
            name = call.function.name
            try:
                args = json.loads(call.function.arguments or '{}')
            except (ValueError, TypeError):
                args = None
            print(f'Tool requested: {name} {args}')
            result = execute_tool(name, args)
            if 'error' in result:
                print('Tool error:', result['error'])
            else:
                print('Tool completed.')
                if result.get('report_file'):
                    print('Saved report:', result['report_file'])
                    print('Saved data:', result['json_file'])
            messages.append({
                'role': 'tool', 'tool_call_id': call.id, 'name': name,
                'content': json.dumps(result, allow_nan=False),
            })
    print('\nAgent stopped at the step limit. Try a narrower question.')


if __name__ == '__main__':
    print('FINANCIAL RESEARCH AGENT\n' + '=' * 50)
    question = input('\nAsk a financial question: ').strip()
    if question:
        try:
            run_agent(question)
        except Exception as exc:
            print(f'Groq/API error: {exc}')
    else:
        print('No question entered.')
