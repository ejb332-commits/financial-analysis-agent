
def interpret_metric(metric, value):
    if value is None:
        return "Insufficient data for interpretation."

    if metric == "profit_margin":
        if value < 0:
            return "The company is reporting a net loss."
        elif value < 10:
            return "The company has a relatively low net profit margin."
        elif value < 20:
            return "The company has a moderate net profit margin."
        else:
            return "The company has a high net profit margin."

    elif metric == "revenue_growth":
        if value < 0:
            return "Revenue declined compared with the previous period."
        elif value < 10:
            return "Revenue is growing at a relatively slow rate."
        elif value < 20:
            return "Revenue is growing at a moderate rate."
        else:
            return "Revenue is growing rapidly."

    elif metric == "roa":
        if value < 0:
            return "The company is generating a negative return on assets."
        elif value < 5:
            return "The company has a relatively low return on assets."
        elif value < 10:
            return "The company has a moderate return on assets."
        else:
            return "The company has a high return on assets."

    elif metric == "roe":
        if value < 0:
            return "The company has a negative return on equity."
        elif value < 10:
            return "The company has a relatively low return on equity."
        elif value < 20:
            return "The company has a moderate return on equity."
        else:
            return "The company has a high return on equity."

    elif metric == "debt_to_equity":
        if value < 0:
            return "Negative equity may make this ratio difficult to interpret."
        elif value < 0.5:
            return "The company has relatively low financial leverage."
        elif value < 1.5:
            return "The company has moderate financial leverage."
        else:
            return "The company has relatively high financial leverage."

    elif metric == "current_ratio":
        if value < 1:
            return "Current liabilities exceed current assets."
        elif value < 2:
            return "Current assets exceed current liabilities."
        else:
            return "Current assets are at least twice current liabilities."

    elif metric == "free_cash_flow":
        if value < 0:
            return "The company has negative free cash flow."
        elif value == 0:
            return "The company has zero free cash flow."
        else:
            return "The company generates positive free cash flow."

    return "No interpretation available."


def generate_interpretations(company):
    interpretations = []

    metrics = [
        "profit_margin",
        "revenue_growth",
        "roa",
        "roe",
        "debt_to_equity",
        "current_ratio",
        "free_cash_flow"
    ]

    for metric in metrics:
        value = company.get(metric)
        interpretation = interpret_metric(metric, value)

        readable_name = metric.replace("_", " ").title()

        interpretations.append(
            f"{readable_name}: {interpretation}"
        )

    return interpretations