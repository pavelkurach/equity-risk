import datetime
import functools

from scipy.optimize import fsolve

from src.financial_models.estimations import CompanyEstimations
from src.utils.financial_formulas import calc_npv


class DCF:
    def __init__(self,
                 start_date: datetime.date,
                 company: CompanyEstimations,
                 market_cap: int,
                 enterprise_value: int = None):
        self.start_date = start_date
        self.company = company
        self.market_cap = market_cap
        if not enterprise_value is None:
            self.enterprise_value = enterprise_value
        else:
            self.enterprise_value = self.market_cap + company.reports[
                'net_debt'].tail(1).iloc[0]

    def calc_implied_wacc_from_dcf_to_firm(self,
                                           growth_rate: float) -> float:
        initial_value = -self.enterprise_values
        fcff = [initial_value, *self.company.estimations['free_cash_flow']]
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
