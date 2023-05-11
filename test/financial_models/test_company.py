import pytest
from src.financial_models.company import Company
import pandas as pd
import numpy as np

def test_calculate_ratios():
    reports = pd.read_csv('ai_pa_reports.csv', index_col=0)
    ratios = pd.read_csv('ai_pa_ratios.csv', index_col=0)
    calculated_ratios = Company.calculate_ratios(reports)
    assert np.max(np.abs((ratios-calculated_ratios))) < 1.e-3
