
# Agentic Financial Research System

An AI-powered financial research agent built with Python, Groq, and Yahoo Finance. The system retrieves financial statements, calculates financial metrics, identifies unusual trends, and generates reproducible research reports.

Unlike a traditional chatbot that primarily generates responses, this application uses **LLM tool calling** to decide when to retrieve and analyze financial data. Financial calculations are performed by deterministic Python functions rather than the language model.

## Features

### 1. Autonomous Tool Calling
- Uses GPT-OSS-20B through the Groq API.
- Allows the language model to select financial analysis tools based on a user's question.
- Supports multi-step investigations involving multiple companies.
- Executes financial calculations through Python functions.

### 2. Historical Financial Analysis
- Retrieves available annual financial statements using Yahoo Finance.
- Analyzes up to four annual reporting periods, depending on data availability.
- Calculates financial metrics including:
  - Profit margin
  - Revenue growth
  - Return on assets (ROA)
  - Return on equity (ROE)
  - Debt-to-equity ratio
  - Current ratio
  - Free cash flow

### 3. Financial Anomaly Detection
Automatically identifies potentially unusual financial developments, including:

- Significant changes in profit margins.
- Sharp changes in revenue growth.
- Negative free cash flow.
- Certain balance-sheet warning signs.

Anomalies are identified using predefined rules and thresholds. These flags indicate changes worth investigating, not necessarily financial problems.

### 4. Financial Calculation Verification
- Recalculates financial metrics to check their consistency.
- Detects inconsistencies between stored and recomputed values.
- Includes automated tests for calculation and verification logic.

**Current limitation:** The system verifies financial calculations but does not yet independently validate every numerical or qualitative claim in the language model's final response.

### 5. Reproducible Research Reports
Each historical investigation saves:

- A Markdown research report.
- A JSON file containing financial data and analysis results.
- Company identifiers and reporting periods.
- Financial metrics and anomaly findings.
- Available source information.

Reports are stored in:

`results/research/`

Saved snapshots make it possible to inspect the inputs and calculations used in a particular investigation. Re-fetching live data later may produce different results because financial data can be updated or restated.

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application and financial calculations |
| Groq API | Hosted language model inference and tool calling |
| GPT-OSS-20B | Financial question interpretation and tool selection |
| yfinance | Retrieval of public-company financial statements |
| Pandas | Financial data processing |
| Matplotlib | Financial visualizations |
| python-dotenv | Environment variable management |
| unittest | Automated testing |
| Git | Version control |

## How It Works

```text
User asks a financial question
              |
              v
       GPT-OSS-20B
              |
              v
    Selects a financial tool
              |
              v
    Python executes the tool
              |
              v
    Retrieves financial data
              |
              v
  Calculates financial metrics
              |
              v
   Detects unusual changes
              |
              v
   Saves reproducible reports
              |
              v
  Returns results to the model
              |
              v
   AI generates an explanation
```

The model does not execute Python code directly. Instead, it requests a tool call through the Groq API. The Python application validates the request, executes the corresponding function, and returns the results to the model.

## Project Structure

```text
financial-analysis-agent/
|
|-- ai_agent.py
|-- analyze_real_companies.py
|-- financial_research.py
|-- evaluate_agent.py
|-- main.py
|
|-- config/
|   |-- analysis_rules.md
|
|-- data/
|   |-- companies.csv
|   |-- real_company_data.py
|
|-- models/
|   |-- financial_metrics.py
|   |-- financial_interpreter.py
|
|-- tests/
|   |-- test_financial.py
|   |-- test_interpreter.py
|   |-- test_financial_research.py
|
|-- results/
|   |-- real_companies/
|   |-- research/
|
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- .env
```

The `.env` file is stored locally and must not be committed to GitHub.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/financial-analysis-agent.git
cd financial-analysis-agent
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install dependencies

Make sure Python 3 is installed.

```bash
python3 -m pip install -r requirements.txt
```

Ensure the Groq SDK is installed:

```bash
python3 -m pip install groq
```

### 3. Configure your API key

Create a `.env` file in the project's root directory:

```env
GROQ_API_KEY=your_api_key_here
```

Obtain an API key from Groq Cloud.

Never commit your API key or `.env` file to a public repository.

## Usage

Start the AI financial research agent:

```bash
python3 ai_agent.py
```

Example questions:

```text
Compare Apple's and Microsoft's profitability.
```

```text
Analyze NVIDIA's financial performance over
the last four available annual periods.
```

```text
Investigate unusual changes in Mondelez's
profit margins and free cash flow.
```

```text
Compare NVIDIA and Mondelez over the last
four available years and identify financial anomalies.
```

The agent determines which available financial tools to request and uses their results to generate an explanation.

### Other Analysis Modes

Run the original financial analysis application:

```bash
python3 main.py
```

Run the real-company financial analysis script:

```bash
python3 analyze_real_companies.py
```

## Testing

Run the financial research evaluation suite:

```bash
python3 evaluate_agent.py
```

Run the project's unit tests:

```bash
python3 -m unittest discover -s tests -v
```

The research evaluation currently includes tests for:

- Revenue growth calculations.
- Profit margin calculations.
- Capital expenditure sign handling.
- Missing financial inputs.
- Financial anomaly detection.
- Detection of inconsistent financial calculations.

The initial research evaluation suite contains six deterministic tests.

These tests validate Python financial logic. They do not measure language model reasoning accuracy or guarantee that every generated conclusion is correct.

## Data Sources and Limitations

Financial statements are retrieved using `yfinance`, an unofficial interface to Yahoo Finance data.

Important limitations:

- Historical annual data availability varies by company.
- Some financial statement fields may be missing.
- Companies can have different fiscal year-end dates.
- Financial figures may be revised or restated.
- Industry differences can make direct ratio comparisons misleading.
- Anomaly detection uses heuristic thresholds rather than statistical proof of abnormality.
- The language model may generate interpretations that are not fully supported by the retrieved financial data.

The application is intended for financial research, education, and software engineering experimentation. It is not a substitute for professional investment advice.

## Future Improvements

### AI Claim Verification
Require model-generated numerical claims to reference specific calculated metrics, then verify those claims programmatically before including them in final reports.

### SEC Filing Integration
Retrieve original SEC filings and link financial conclusions to supporting source documents.

### Expanded Financial Analysis
Introduce additional historical metrics, industry comparisons, and financial risk indicators.

### Model Evaluation
Compare multiple language models on tool-calling reliability, financial accuracy, unsupported claims, and response time.

## Project Goals

This project explores how large language models can be integrated with deterministic financial calculations and external data sources to create reliable, specialized AI applications.

The primary engineering goals are:

1. Build an agent capable of selecting and using financial tools.
2. Separate language-model reasoning from numerical computation.
3. Analyze historical financial performance and detect unusual trends.
4. Preserve financial evidence and research outputs for inspection.
5. Improve reliability through automated testing and verification.

## Disclaimer

This project is for educational and research purposes only. Financial information may be incomplete or inaccurate, and AI-generated interpretations should be independently reviewed before being used for investment decisions.