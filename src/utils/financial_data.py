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


async def get_financial_reports(
        session: aiohttp.ClientSession,
        report_type: FinancialReportType,
        ticker: str,
        years: list[int]) -> dict[int, dict[int | str]]:
    limit = datetime.date.today().year - min(years) + 1
    url = f'{FMP_URL}/v3/{report_type.value}/{ticker}?limit={limit}&apikey' \
          f'={FMP_KEY}'
    raw_reports = await get_json_parsed_data(session, url)
    financial_reports = {}
    for raw_report in raw_reports:
        report = ModelOfType[report_type](**raw_report)
        if report.dict()['date'].year in years:
            financial_reports[report.dict()['date'].year] = report.dict()
    return financial_reports


async def get_combined_reports(
        session: aiohttp.ClientSession,
        ticker: str,
        years: list[int]) -> dict[int, dict[int | str]]:
    income_statements = await get_financial_reports(
        session=session,
        report_type=FinancialReportType.INCOME,
        ticker=ticker,
        years=years,
    )
    balance_sheet_statements = await get_financial_reports(
        session=session,
        report_type=FinancialReportType.BALANCE_SHEET,
        ticker=ticker,
        years=years,
    )
    cash_flow_statements = await get_financial_reports(
        session=session,
        report_type=FinancialReportType.CASH_FLOW,
        ticker=ticker,
        years=years,
    )
    combined_reports = {}
    for year in sorted(years):
        combined_reports[year] = {
            **income_statements[year],
            **balance_sheet_statements[year],
            **cash_flow_statements[year],
        }
    return combined_reports


async def get_market_cap(session: aiohttp.ClientSession,
                         ticker: str) -> int:
    url = f'{FMP_URL}/v3/market-capitalization/{ticker}?' \
          f'apikey={FMP_KEY}'
    market_cap_data = await get_json_parsed_data(session, url)
    return market_cap_data[0]['marketCap']
