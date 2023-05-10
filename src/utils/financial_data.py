import asyncio
import aiohttp

from src.utils.config import FINANCIAL_MODELLING_PREP_API_KEY as FMP_KEY

class FinancialReportType:
    INCOME = 'income-statement'
    BALANCE_SHEET = 'balance-sheet-statement'
    CASH_FLOW = 'cash-flow-statement'


async def get_json_parsed_data(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        data = await response.json()
        return data


async def get_financial_report(session: aiohttp.ClientSession,
                               report_type: FinancialReportType,
                               ticker: str):
    url = (f'https://financialmodelingprep'
           f'.com/api/v3/{report_type}/{ticker}?apikey={FMP_KEY}')
    financial_report = await get_json_parsed_data(session, url)
    return financial_report

