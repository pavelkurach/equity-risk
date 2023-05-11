from src.models.financials import ReportsCombined


class Company:
    def __init__(self,
                 reports: list[ReportsCombined]):
        self.reports: dict[int, ReportsCombined] = \
            {report.year: report for report in reports}
        self.years = sorted(reports.keys())
