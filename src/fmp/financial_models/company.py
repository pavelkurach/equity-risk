import pandas as pd

from src.utils.financial_ratios import calculate_ratios


class Company:
    def __init__(self,
                 symbol: str,
                 reports: pd.DataFrame,
                 tax_rate: float = 0.27):
        self.symbol = symbol
        self.reports = reports
        self.ratios = calculate_ratios(self.reports)

    def get_last_year(self):
        return max(self.reports.index.to_list())

    def calc_cost_of_equity(self):
        return self.ratios['interest_ratio'].mean()


def calc_change_in_wc(reports: pd.DataFrame) -> pd.Series:
    years = sorted(reports.index.to_list())
    wc = (
            reports['short_term_investments'] +
            reports['net_receivables'] +
            reports['inventory'] +
            reports['other_current_assets'] -
            reports['account_payables'] -
            reports['short_term_debt'] -
            reports['tax_payables'] -
            reports['deferred_revenue'] -
            reports['other_current_liabilities']
    )
    change_in_wc = pd.Series(index=reports.index,
                             name='change_in_wc')
    for year in years[1:]:
        change_in_wc[year] = wc[year] - wc[year - 1]
    return change_in_wc
