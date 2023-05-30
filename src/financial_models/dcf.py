import datetime
import functools

from scipy.optimize import fsolve

from src.utils.financial_formulas import calc_npv
from models import estimations


class DCF:
    def __init__(
        self,
        symbol: str,
        estimations: estimations.Estimations,
    ):
        self.symbol = symbol
        self.dates = estimations.dates
        self.fcff = estimations.fcff
        self.fcfe = estimations.fcfe
        self.market_cap = estimations.market_cap
        self.enterprise_value = estimations.enterprise_value
        self.total_debt = estimations.total_debt
        self.after_tax_cost_of_debt = estimations.after_tax_cost_of_debt

    def calc_implied_wacc_from_dcf_to_firm(self, growth_rate: float) -> float:
        calc_npv_ = functools.partial(
            calc_npv,
            growth_rate=growth_rate,
            initial_value=-self.enterprise_value,
            cash_flow=self.fcff,
            dates=self.dates,
        )
        implied_wacc = fsolve(calc_npv_, [0.06])[0]
        return implied_wacc

    def calc_implied_coe_from_dcf_to_firm(self, growth_rate: float) -> float:
        wacc = self.calc_implied_wacc_from_dcf_to_firm(growth_rate=growth_rate)
        coe = (
            wacc
            - self.after_tax_cost_of_debt
            * (self.total_debt / self.enterprise_value)
            * self.enterprise_value
            / self.market_cap
        )
        return coe

    def calculate_implied_coe_from_dcf_to_equity(self, growth_rate: float) -> float:
        calc_npv_ = functools.partial(
            calc_npv,
            growth_rate=growth_rate,
            initial_value=-self.market_cap,
            cash_flow=self.fcfe,
            dates=self.dates,
        )
        implied_coe = fsolve(calc_npv_, [0.06])[0]
        return implied_coe
