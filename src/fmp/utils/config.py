import os

from dotenv import load_dotenv

load_dotenv()

FINANCIAL_MODELLING_PREP_API_KEY = os.getenv(
    'FINANCIAL_MODELLING_PREP_API_KEY')

FINANCIAL_MODELLING_PREP_URL = 'https://financialmodelingprep.com/api'
