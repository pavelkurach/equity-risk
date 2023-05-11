import datetime
import enum

from pydantic import BaseModel, Field


class FinancialReportType(enum.Enum):
    INCOME = 'income-statement'
    BALANCE_SHEET = 'balance-sheet-statement'
    CASH_FLOW = 'cash-flow-statement'


class Income(BaseModel):
    date: datetime.date
    symbol: str
    currency: str = Field(alias='reportedCurrency')
    revenue: int
    cost_of_revenue: int = Field(alias='costOfRevenue')
    ebitda: int
    depreciation_and_amortization: int = Field(
        alias='depreciationAndAmortization')
    ebitda_ratio: float = Field(alias='ebitdaratio')
    net_income: int = Field(alias='netIncome')


class BalanceSheet(BaseModel):
    date: datetime.date
    symbol: str
    currency: str = Field(alias='reportedCurrency')
    cash_and_cash_equivalents: int = Field(alias='cashAndCashEquivalents')
    total_debt: int = Field(alias='totalDebt')
    net_debt: int = Field(alias='netDebt')
    total_equity: int = Field(alias='totalEquity')
    # Current assets
    short_term_investments: int = Field(alias='shortTermInvestments')
    net_receivables: int = Field(alias='netReceivables')
    inventory: int
    other_current_assets: int = Field(alias='otherCurrentAssets')
    # Current liabilities
    account_payables: int = Field(alias='accountPayables')
    short_term_debt: int = Field(alias='shortTermDebt')
    tax_payables: int = Field(alias='taxPayables')
    deferred_revenue: int = Field(alias='deferredRevenue')
    other_current_liabilities: int = Field(alias='otherCurrentLiabilities')


class CashFlow(BaseModel):
    date: datetime.date
    symbol: str
    currency: str = Field(alias='reportedCurrency')
    capital_expenditure: int = Field(alias='capitalExpenditure')
    dividends_paid: int = Field(alias='dividendsPaid')
    free_cash_flow: int = Field(alias='freeCashFlow')


ModelOfType = {
    FinancialReportType.INCOME: Income,
    FinancialReportType.BALANCE_SHEET: BalanceSheet,
    FinancialReportType.CASH_FLOW: CashFlow,
}

class CombinedReport(Income, BalanceSheet, CashFlow):
    pass
