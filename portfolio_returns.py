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


# Function calculating return over time period
def return_over_time_period(df, start_date, end_date, summer = True, get_time_weighted_return = True, get_sharpe_ratio = True):
    '''Function return_over_time_period calculates return over given time period, time weighted rate of return as well as sharpe. 
    
    The time period is selected based on given input parameters `start_date` and end_date and makes an investment for all months or excluding summer moths based on the parameter summer. If summer parameter is True we invest in all the months and if not then exclude summer months. If get_time_weighted_return is True the function calculates it. The same way if get_sharpe_ratio parameter is True function calculates it. The default value for both get_time_weighted_return as well as get_sharpe_ratio is True.
    
    The default value for Summer parameter is set to True. 
    The function returns time_weighted_return,total return over a given time period and sharpe ratio.'''

    required_df = df[(df['date_ff_factors'] >= start_date) & (df['date_ff_factors'] < end_date)].reset_index(drop = True)
    # Adding a column which shows $1000 investment monthly or $1333.33 if excluding summer months
    if summer:
        required_df['Investment_Amt'] = 1000
    else:
        summer_months = [6,7,8]
        for i in range(len(required_df)):
            if required_df.loc[i, 'date_ff_factors'].month in summer_months:
                required_df.loc[i,'Investment_Amt'] = 0
            else:
                required_df.loc[i,'Investment_Amt'] = 1333.33

    # Adding a column to show cummilative sum of investment
    required_df['Monthly_Amt_Aggregate'] = required_df['Investment_Amt'].cumsum()

    # Intially setting monthly return 0 for all months
    required_df['Monthly_Return'] = 0
    required_df['Holding_Period_Return'] = 0

    # Calculating monthly return
    for i in range(len(required_df)):
        if i == 0:
            required_df.loc[i, 'Monthly_Return'] = required_df.loc[i, 'Investment_Amt']*(1 + required_df.iloc[i,1] + required_df.iloc[i,4])
            # Checking if time_weighted_return is true
            if get_time_weighted_return:
                if required_df.loc[i, 'Investment_Amt'] == 0:
                    required_df.loc[i, 'Holding_Period_Return'] = 0
                else:
                    required_df.loc[i, 'Holding_Period_Return'] = (required_df.loc[i, 'Monthly_Return'] - required_df.loc[i, 'Investment_Amt'])/required_df.loc[i,'Investment_Amt']
        else:
            required_df.loc[i, 'Monthly_Return'] = (required_df.loc[i, 'Investment_Amt']+required_df.loc[i-1, 'Monthly_Return'])*(1 + required_df.iloc[i,1] + required_df.iloc[i,4])
            
            numerator = (required_df.loc[i, 'Monthly_Return'] - (required_df.loc[i,'Investment_Amt'] + required_df.loc[i-1,'Monthly_Return']))
            denominator = (required_df.loc[i,'Investment_Amt'] + required_df.loc[i-1,'Monthly_Return'])

            if get_time_weighted_return:
                if denominator == 0:
                    required_df.loc[i, 'Holding_Period_Return'] = 0
                else:
                    required_df.loc[i, 'Holding_Period_Return'] = numerator/denominator

    if get_time_weighted_return:            
        time_weighted_return = np.prod(required_df['Holding_Period_Return'].values + 1)
    if get_sharpe_ratio:
        sharpe_ratio = required_df['Mkt-RF'].mean()/required_df['Mkt-RF'].std()
    
    if get_time_weighted_return and get_sharpe_ratio:
        return round(time_weighted_return,3), round(required_df.iloc[-1,-2], 3), round(sharpe_ratio, 3)
    elif get_time_weighted_return and not get_sharpe_ratio:
        return round(time_weighted_return,3), round(required_df.iloc[-1,-2], 3)
    elif get_sharpe_ratio and not get_time_weighted_return:
        return round(required_df.iloc[-1,-2], 3), round(sharpe_ratio, 3)
    else:
        return round(required_df.iloc[-1,-2], 3)
    
# Function for plotting 
def visualization(monthly_returns):   
    '''
    This Function takes in array of monthly_returns and plots distribution as well as the statstical parameters
    ''' 
    fig, ax = plt.subplots(1,1)
    sns.histplot(monthly_returns, kde=True, bins = 50, ax=ax)
    monthly_returns_mean = monthly_returns.mean()
    monthly_returns_median = np.median(monthly_returns)
    monthly_returns_std = monthly_returns.std()
    monthly_returns_95_lower = np.percentile(monthly_returns, 2.5)
    monthly_returns_95_upper = np.percentile(monthly_returns, 97.5)

    y_lims = ax.get_ylim()
    ax.plot(np.zeros(10) + monthly_returns_mean, np.linspace(y_lims[0], y_lims[1], 10), 'r--')
    ax.plot(np.zeros(10) + monthly_returns_median, np.linspace(y_lims[0], y_lims[1], 10), 'g--')
    ax.plot(np.zeros(10) + monthly_returns_95_lower, np.linspace(y_lims[0], y_lims[1], 10), 'y--')
    ax.plot(np.zeros(10) + monthly_returns_95_upper, np.linspace(y_lims[0], y_lims[1], 10), 'y--')

    plt.legend(['Dist', f'Mean: {monthly_returns_mean:.0f}', f'Median: {monthly_returns_median:.0f}'])
    return fig, ax