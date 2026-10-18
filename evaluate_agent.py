"""Offline deterministic evaluation; no Groq credits or live market data needed."""
import unittest

if __name__ == '__main__':
    print('Running reproducible financial calculation, anomaly, and verification tests...')
    suite = unittest.defaultTestLoader.discover('tests', pattern='test_financial_research.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f'\nPassed: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}')
    print('Scope: deterministic Python logic only. This is NOT a benchmark of LLM factual accuracy,')
    print('tool-choice reliability, or a comparison against ChatGPT.')
    raise SystemExit(0 if result.wasSuccessful() else 1)
