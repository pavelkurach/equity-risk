import pytest
import datetime

from src.utils import financial_formulas as ff


def test_calc_xnpv():
    values = list(map(lambda x: float(x), [10, 8, 5, 14, 7]))
    dates = [datetime.date(year, 6, 30) for year in range(2023, 2028)]
    assert (ff.calc_xnpv(0.05, values=values, dates=dates) - 40) < 0.01
