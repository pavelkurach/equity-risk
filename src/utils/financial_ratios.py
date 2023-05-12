import pandas as pd


def calculate_ratios(reports: pd.DataFrame):
    ratios = pd.DataFrame(index=reports.index)
    ratios['cosg_ratio'] = (reports['cost_of_revenue'] /
                            reports['revenue'])
    ratios['ebitda_ratio'] = reports['ebitda'] / reports['revenue']
    ratios['da_ratio'] = (reports['depreciation_and_amortization'] /
                           reports['revenue'])
    ratios['capex_ratio'] = (reports['capital_expenditure'] /
                             reports['revenue'])

    # Current assets
    ratios['short_term_investments_ratio'] = (
            reports['short_term_investments'] /
            reports['revenue'])
    ratios['receivables_ratio'] = (
            reports['net_receivables'] /
            reports['revenue'])
    ratios['inventory_ratio_cogs'] = (
            reports['inventory'] /
            reports['cost_of_revenue'])
    ratios['other_current_assets_ratio'] = (
            reports['other_current_assets'] /
            reports['revenue'])

    # Current liabilities
    ratios['payables_ratio_cogs'] = (
            reports['account_payables'] /
            reports['cost_of_revenue'])
    ratios['short_term_debt_ratio'] = (
            reports['short_term_debt'] /
            reports['revenue'])
    ratios['tax_payables_ratio'] = (
            reports['tax_payables'] /
            reports['revenue'])
    ratios['deferred_revenue_ratio'] = (
            reports['deferred_revenue'] /
            reports['revenue'])
    ratios['other_current_liabilities_ratio'] = (
            reports['other_current_liabilities'] /
            reports['revenue'])

    return ratios
