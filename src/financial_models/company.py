from src.models.financials import ReportsCombined


class Company:
    def __init__(self,
                 reports: list[ReportsCombined]):
        self.reports = sorted(reports,
                              key=lambda report: report.date.year)
