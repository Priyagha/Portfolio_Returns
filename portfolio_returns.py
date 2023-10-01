# Importing required libraries
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import getFamaFrenchFactors as gff
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

# Defining Required Functions

# Function Calculating End Date
def calculate_end_date(start_date, years = 30):
    '''
    calculates the end date given start_date as a positional parameter and years as an optional parameter and returns end_date as datetime object.
    '''
    end_date = start_date + relativedelta(years = years)
    return end_date
