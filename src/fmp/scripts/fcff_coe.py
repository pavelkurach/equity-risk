import asyncio
import datetime
import logging

import aiohttp
import more_itertools
import pandas as pd

import src.fmp.utils.financial_data as fd
from src.financial_models.dcf import DCF
from src.fmp.financial_models.estimations import CompanyEstimations
from src.utils.index_composition import get_symbols_in_indices

logging.basicConfig(
    filename='../../../logs/fcff_coe.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def get_reports(session: aiohttp.ClientSession,
                      symbol: str) -> pd.DataFrame:
    try:
        reports_raw = await fd.get_combined_reports(
            session=session,
            symbol=symbol,
            years=list(range(2017, 2023)))
        return pd.DataFrame.from_dict(reports_raw).transpose()
    except Exception as exception:
        logger.error(f'symbol: {symbol}, error type: {exception.__class__}, '
                     f'error message: {exception}')
        raise exception


async def get_market_cap(session: aiohttp.ClientSession, symbol: str) -> int:
    try:
        market_cap = await fd.get_market_cap(
            session=session,
            symbol=symbol
        )
        return market_cap
    except Exception as exception:
        logger.error(f'symbol: {symbol}, error type: {exception.__class__}, '
                     f'error message: {exception}')
        raise exception


def calc_implied_coe(symbol: str,
                     reports_df: pd.DataFrame,
                     market_cap: int) -> float:
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


async def generate_reports_and_market_cap_batches(
        list_of_symbols: list[str],
        session: aiohttp.ClientSession) -> list[str, tuple[pd.DataFrame, int]]:
    for batch_of_symbols in more_itertools.batched(list_of_symbols, 5):
        reports_and_market_cap_batch = []
        print(batch_of_symbols)
        for symbol in batch_of_symbols:
            reports_df = await get_reports(session=session, symbol=symbol)
            market_cap = await get_market_cap(session=session, symbol=symbol)
            reports_and_market_cap_batch.append((symbol,
                                                 reports_df,
                                                 market_cap))
        yield reports_and_market_cap_batch
        asyncio.sleep(60)


async def main():
    list_of_symbols = get_symbols_in_indices(indices=['S&P500'])
    async with aiohttp.ClientSession() as session:
        cac40_reports_generator = generate_reports_and_market_cap_batches(
            list_of_symbols=list_of_symbols,
            session=session,
        )
        reports = await anext(cac40_reports_generator)
        for report in reports:
            print(report[0])
            print(report[1])


if __name__ == "__main__":
    asyncio.run(main())
