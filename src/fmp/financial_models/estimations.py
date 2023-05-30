# type: ignore
import pandas as pd

from src.fmp.financial_models.company import Company


def estimate_revenue(reports: pd.DataFrame, years: list[int]) -> pd.Series:
    growth_rate = reports['revenue'].pct_change().mean()
    past_revenue = reports.loc[years[0] - 1, 'revenue']
    revenue_est = pd.Series(index=pd.Index(years), name='revenue')
    revenue_est[years[0]] = past_revenue
    for year in years[1:]:
        revenue_est[year] = revenue_est[year - 1] * (1 + growth_rate)
    return revenue_est


def estimate_ebitda(
        revenue: pd.Series, ratios: pd.DataFrame, years: list[int]
) -> pd.Series:
    ebitda_ratio_mean = ratios['ebitda_ratio'].mean()
    ebitda_est = pd.Series(index=pd.Index(years), name='ebitda')
    for year in years:
        ebitda_est[year] = revenue[year] * ebitda_ratio_mean
    return ebitda_est


def estimate_da(
        revenue: pd.Series, ratios: pd.DataFrame, years: list[int]
) -> pd.Series:
    da_ratio_mean = ratios['da_ratio'].mean()
    da_est = pd.Series(index=pd.Index(years),
                       name='depreciation_and_amortization')
    for year in years:
        da_est[year] = revenue[year] * da_ratio_mean
    return da_est


def estimate_capex(
        revenue: pd.Series, ratios: pd.DataFrame, years: list[int]
) -> pd.Series:
    capex_ratio_mean = ratios['capex_ratio'].mean()
    capex_est = pd.Series(index=pd.Index(years), name='capital_expenditure')
    for year in years:
        capex_est[year] = revenue[year] * capex_ratio_mean
    return capex_est


def estimate_change_in_wc(
        revenue: pd.Series, ratios: pd.DataFrame, past_wc: int,
        years: list[int]
) -> pd.Series:
    # Current assets
    short_term_investments_ratio_mean = ratios[
        'short_term_investments_ratio'].mean()
    receivables_ratio_mean = ratios['receivables_ratio'].mean()
    inventory_ratio_mean = ratios['inventory_ratio'].mean()
    other_current_assets_ratio_mean = ratios[
        'other_current_assets_ratio'].mean()
    # Current liabilities
    payables_ratio_mean = ratios['payables_ratio'].mean()
    short_term_debt_ratio_mean = ratios['short_term_debt_ratio'].mean()
    tax_payables_ratio_mean = ratios['tax_payables_ratio'].mean()
    deferred_revenue_ratio_mean = ratios['deferred_revenue_ratio'].mean()
    other_current_liabilities_ratio_mean = ratios[
        'other_current_liabilities_ratio'
    ].mean()

    change_in_wc_est = pd.Series(index=pd.Index(years), name='change_in_wc')
    previous_wc = past_wc
    for year in years:
        current_assets = revenue[year] * (
                short_term_investments_ratio_mean
                + receivables_ratio_mean
                + other_current_assets_ratio_mean
                + inventory_ratio_mean
        )
        current_liabilities = revenue[year] * (
                short_term_debt_ratio_mean
                + tax_payables_ratio_mean
                + deferred_revenue_ratio_mean
                + other_current_liabilities_ratio_mean
                + payables_ratio_mean
        )
        current_wc = current_assets - current_liabilities
        change_in_wc_est[year] = current_wc - previous_wc
        previous_wc = current_wc
    return change_in_wc_est


def make_estimations(
        reports: pd.DataFrame,
        ratios: pd.DataFrame,
        years: list[int],
        tax_rate: float = 0.27,
) -> pd.DataFrame:
    last_year = min(years) - 1
    estimations = pd.DataFrame(index=pd.Index(years))
    estimations['revenue'] = estimate_revenue(
        reports=reports,
        years=years,
    )
    estimations['ebitda'] = estimate_ebitda(
        revenue=estimations['revenue'],
        ratios=ratios,
        years=years,
    )
    estimations['depreciation_and_amortization'] = estimate_da(
        revenue=estimations['revenue'],
        ratios=ratios,
        years=years,
    )
    estimations['capital_expenditure'] = estimate_capex(
        revenue=estimations['revenue'],
        ratios=ratios,
        years=years,
    )
    past_wc = (
            reports.loc[last_year, 'short_term_investments']
            + reports.loc[last_year, 'net_receivables']
            + reports.loc[last_year, 'inventory']
            + reports.loc[last_year, 'other_current_assets']
            - reports.loc[last_year, 'account_payables']
            - reports.loc[last_year, 'short_term_debt']
            - reports.loc[last_year, 'tax_payables']
            - reports.loc[last_year, 'deferred_revenue']
            - reports.loc[last_year, 'other_current_liabilities']
    )
    estimations['change_in_wc'] = estimate_change_in_wc(
        revenue=estimations['revenue'],
        ratios=ratios,
        past_wc=past_wc,
        years=years,
    )
    estimations['nopat'] = (
                                   estimations['ebitda'] - estimations[
                               'depreciation_and_amortization']
                           ) * (1 - tax_rate)
    estimations['free_cash_flow'] = (
            estimations['nopat']
            + estimations['depreciation_and_amortization']
            - estimations['change_in_wc']
            + estimations['capital_expenditure']
    )
    return estimations


class CompanyEstimations(Company):
    def __init__(
            self, symbol: str, reports: pd.DataFrame, n_years: int,
            tax_rate: float = 0.27
    ):
        super().__init__(symbol, reports)
        self.n_years = n_years
        self.years = sorted(
            list(
                range(self.get_last_year() + 1,
                      self.get_last_year() + self.n_years + 2)
            )
        )
        self.tax_rate = tax_rate
        self.estimations = make_estimations(
            reports=self.reports,
            ratios=self.ratios,
            years=self.years,
            tax_rate=tax_rate,
        )
