import asyncio
import datetime
import logging

import aiohttp
import more_itertools
import numpy as np
import pandas as pd
import pydantic

import src.utils.financial_data as fd
from src.financial_models.dcf import DCF
from src.financial_models.estimations import CompanyEstimations
from src.utils.index_composition import get_symbols_in_indices

logging.basicConfig(
    filename='../logs/fcff_coe.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def find_implied_wacc(session: aiohttp.ClientSession, symbol: str):
    try:
        reports_raw = await fd.get_combined_reports(
            session=session,
            symbol=symbol,
            years=list(range(2017, 2023)))
    except pydantic.ValidationError as e:
        logger.error(f'symbol: {symbol}, error message: {e}')
        raise e
    except KeyError as e:
        logger.error(f'symbol: {symbol}, error type: {e.__class__}, '
                     f'error message: {e}')
        raise e
    market_cap = await fd.get_market_cap(
        session=session,
        symbol=symbol
    )
    reports_df = pd.DataFrame.from_dict(reports_raw).transpose()
    company = CompanyEstimations(
        symbol=symbol,
        reports=reports_df,
        n_years=15,
    )
    dcf = DCF(
        start_date=datetime.date.today(),
        company=company,
        market_cap=market_cap,
    )
    return dcf.calc_implied_coe_from_dcf_to_firm(0.015)


async def main():
    symbol_list = get_symbols_in_indices(indices=['CAC40'])
    implied_coe_list_raw = []
    async with aiohttp.ClientSession() as session:
        for symbol_batch in more_itertools.batched(symbol_list, 50):
            tasks = [asyncio.create_task(find_implied_wacc(
                session=session,
                symbol=symbol,
            )) for symbol in symbol_batch]
            implied_coe_list_raw_batch = await asyncio.gather(
                *tasks,
                return_exceptions=True)
            implied_coe_list_raw.extend(implied_coe_list_raw_batch)
            # print('Loaded batch')
            # time.sleep(60)
    implied_coe_list = list(filter(lambda x: type(x) is np.float64,
                                   implied_coe_list_raw))
    print('Number of symbols: ', len(symbol_list))
    print('Successfully calculated COE for: ', len(implied_coe_list))
    print('Median value : ', np.median(np.array(implied_coe_list)))
    for coe in implied_coe_list_raw:
        if not type(coe) is np.float64:
            print(coe.__class__, coe)


if __name__ == "__main__":
    asyncio.run(main())
