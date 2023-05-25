import datetime
import functools

from scipy.optimize import fsolve

from src.fmp.financial_models.estimations import CompanyEstimations
from src.utils.financial_formulas import calc_npv


class DCF:
    def __init__(self,
                 start_date: datetime.date,
                 company: CompanyEstimations,
                 market_cap: int,
                 enterprise_value: int | None = None):
        self.start_date = start_date
        self.company = company
        self.market_cap = market_cap
        if not enterprise_value is None:
            self.enterprise_value = enterprise_value
        else:
            self.enterprise_value = self.market_cap + company.reports[
                'net_debt'].tail(1).iloc[0]
        self.total_debt = company.reports[
            'total_debt'].tail(1).iloc[0]

    def calc_implied_wacc_from_dcf_to_firm(self,
                                           growth_rate: float) -> float:
        initial_value = -self.enterprise_value
        fcff = self.company.estimations['free_cash_flow'].to_list()
        years = self.company.estimations.index.to_list()
        final_year = years[-1]
        dates = list(map(lambda year: datetime.date(year, 6, 30), years))
        if self.start_date.month > dates[0].month:
            dates[0] = self.start_date
        dates = [self.start_date, *dates, datetime.date(final_year, 12, 31)]
        calc_npv_ = functools.partial(
            calc_npv,
            growth_rate=growth_rate,
            initial_value=initial_value,
            cash_flow=fcff,
            dates=dates
        )
        implied_wacc = fsolve(calc_npv_, [0.06])[0]
        return implied_wacc

    def calc_implied_coe_from_dcf_to_firm(self,
                                          growth_rate: float) -> float:
        wacc = self.calc_implied_wacc_from_dcf_to_firm(growth_rate=growth_rate)
        after_tax_cost_of_debt = self.company.calc_cost_of_equity() * (
                1 - self.company.tax_rate
        )
        coe = (wacc - after_tax_cost_of_debt * (
                self.total_debt / self.enterprise_value
        ) * self.enterprise_value / self.market_cap)
        return coe
