def calculate_profit_margin(revenue, profit):
    return (profit / revenue) * 100


def calculate_revenue_growth(current_revenue, previous_revenue):
    return ((current_revenue - previous_revenue) / previous_revenue) * 100


def calculate_roa(profit, assets):
    return (profit / assets) * 100


def calculate_roe(profit, equity):
    return (profit / equity) * 100


def calculate_debt_to_equity(total_debt, equity):
    return total_debt / equity


def calculate_current_ratio(current_assets, current_liabilities):
    return current_assets / current_liabilities


def calculate_free_cash_flow(operating_cash_flow, capital_expenditures):
    return operating_cash_flow - capital_expenditures