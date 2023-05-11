import pandas as pd


class Company:
    def __init__(self,
                 symbol: str,
                 reports: pd.DataFrame):
        self.symbol = symbol
        self.reports = reports
        self.ratios = Company.calculate_ratios(self.reports)

    @staticmethod
    def calculate_ratios(reports: pd.DataFrame):
        ratios = pd.DataFrame(index=reports.index)
        ratios['cosg_ratio'] = (reports['cost_of_revenue'] /
                                reports['revenue'])
        ratios['ebitda_ratio'] = reports['ebitda'] / reports['revenue']
        ratios['d&a_ratio'] = (reports['depreciation_and_amortization'] /
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
        ratios['other_current_liabilities'] = (
                reports['other_current_liabilities'] /
                reports['revenue'])

        return ratios

    def get_last_year(self):
        return max(self.reports.index.to_list())
