import pandas as pd

from src.financial_models.company import Company


class CompanyEstimations(Company):
    def __init__(self,
                 symbol: str,
                 reports: pd.DataFrame,
                 n_years: int):
        super.__init__(symbol, reports)
        self.n_years = n_years
        self.years = sorted(list(
            range(self.get_last_year() + 1,
                  self.get_last_year() + self.n_years + 2)))
        self.estimations = CompanyEstimations.make_estimations(
            reports=self.reports,
            years=self.years,
        )

    @staticmethod
    def make_estimations(reports: pd.DataFrame,
                         years: list[int]) -> pd.DataFrame:
        estimations = pd.DataFrame(index=pd.Index(years))
        estimations['revenue'] = CompanyEstimations.estimate_revenue(
            reports=reports,
            years=years,
        )

    @staticmethod
    def estimate_revenue(reports: pd.DataFrame,
                         years: list[int]) -> pd.Series:
        growth_rate = reports['revenue'].pct_change().mean()
        past_revenue = reports.loc[years[0] - 1, 'revenue']
        revenue_est = pd.Series(index=pd.Index(years), name='revenue')
        revenue_est[years[0]] = past_revenue
        for year in years[1:]:
            revenue_est[year] = revenue_est[year - 1] * (1 + growth_rate)
        return revenue_est
