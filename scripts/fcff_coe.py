import asyncio
import datetime

import aiohttp
import numpy as np
import pandas as pd

import src.utils.financial_data as fd
from src.financial_models.dcf import DCF
from src.financial_models.estimations import CompanyEstimations
from src.utils.index_composition import get_symbols_in_indices


async def find_implied_wacc(session: aiohttp.ClientSession, symbol: str):
    reports_raw = await fd.get_combined_reports(
        session=session,
        symbol=symbol,
        years=list(range(2017, 2023)))
    if reports_raw is None:
        return None
    market_cap = await fd.get_market_cap(
        session=session,
        symbol=symbol
    )
    reports_df = pd.DataFrame.from_dict(reports_raw).transpose()
    company = CompanyEstimations(
        symbol=symbol,
        reports=reports_df,
        n_years=5,
    )
    dcf = DCF(
        start_date=datetime.date.today(),
        company=company,
        market_cap=market_cap,
    )
    return dcf.calc_implied_coe_from_dcf_to_firm(0.015)


async def main():
    symbol_list = get_symbols_in_indices(indices=['CAC40'])
    implied_coe_list = []
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(find_implied_wacc(
            session=session,
            symbol=symbol,
        )) for symbol in symbol_list]
        implied_coe_list_raw = await asyncio.gather(*tasks,
                                                    return_exceptions=True)
    implied_coe_list = list(filter(lambda x: type(x) is np.float64,
                                   implied_coe_list_raw))
    print('Number of symbols: ', len(symbol_list))
    print('Successfully calculated COE for: ', len(implied_coe_list))
    for coe in implied_coe_list:
        if type(coe) is np.float64:
            print(coe)


if __name__ == "__main__":
    asyncio.run(main())
