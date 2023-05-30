from pydantic import BaseModel
import datetime


class Estimations(BaseModel):
    dates: list[datetime.date]
    fcff: list[float]
    fcfe: list[float]
    enterprise_value: float
    market_cap: float
    total_debt: float
    risk_free_rate: float
    after_tax_cost_of_debt: float
