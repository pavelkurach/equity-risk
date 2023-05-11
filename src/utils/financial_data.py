import datetime

import aiohttp

from src.models.financials import FinancialReportType
from src.models.financials import ModelOfType
from src.utils.config import FINANCIAL_MODELLING_PREP_API_KEY as FMP_KEY
from src.utils.config import FINANCIAL_MODELLING_PREP_URL as FMP_URL


async def get_json_parsed_data(session: aiohttp.ClientSession,
                               url: str) -> list[dict]:
    async with session.get(url) as response:
        data = await response.json()
        return data


async def get_financial_reports(session: aiohttp.ClientSession,
                                report_type: FinancialReportType,
                                ticker: str,
                                years: dict[int]) -> dict[int, object]:
    limit = datetime.date.today().year - min(years) + 1
    url = f'{FMP_URL}/v3/{report_type}/{ticker}?limit={limit}&apikey={FMP_KEY}'
    raw_reports = await get_json_parsed_data(session, url)
    financial_reports = {}
    for raw_report in raw_reports:
        report = ModelOfType[report_type](**raw_report)
        if report.dict()['date'].year in years:
            financial_reports[report.dict()['date'].year] = report
    return financial_reports


async def get_market_cap(session: aiohttp.ClientSession,
                         ticker: str) -> int:
    url = f'{FMP_URL}/v3/market-capitalization/{ticker}?' \
          f'apikey={FMP_KEY}'
    market_cap_data = await get_json_parsed_data(session, url)
    return market_cap_data[0]['marketCap']
