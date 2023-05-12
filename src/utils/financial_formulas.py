import datetime


class NonPositiveTVException(Exception):
    pass


def calc_xnpv(rate: float,
              values: list[float],
              dates: list[datetime.date]):
    today = min(dates)
    return sum(
        [
            value / (1.0 + rate) ** ((date - today).days / 365.0)
            for value, date in zip(values, dates)
        ]
    )


def calc_npv(
        rate: float,
        growth_rate: float,
        initial_value: float,
        cash_flow: list[float],
        dates: list[datetime.date]) -> float:
    if cash_flow[-1] <= 0:
        raise NonPositiveTVException
    terminal_value = cash_flow[-1] * (1 + growth_rate) / (rate - growth_rate)
    return calc_xnpv(
        rate=rate,
        values=[initial_value, *cash_flow, terminal_value],
        dates=dates,
    )


def calc_xduration(rate: float,
                   values: list[float],
                   dates: list[datetime.date]):
    today = min(dates)
    return sum(
        [
            ((date - today).days / 365.0)
            * value
            / (1.0 + rate) ** ((date - today).days / 365.0)
            for value, date in zip(values[1:], dates[1:])
        ]
    ) / (-values[0])


def calc_duration(
        rate: float,
        growth_rate: float,
        initial_value: float,
        cash_flow: list[float],
        dates: list[datetime.date]) -> float:
    if cash_flow[-1] <= 0:
        raise NonPositiveTVException
    terminal_value = cash_flow[-1] * (1 + growth_rate) / (rate - growth_rate)
    return calc_xduration(
        rate=rate,
        values=[initial_value, *cash_flow, terminal_value],
        dates=dates,
    )

