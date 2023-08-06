import pandas as pd
import numpy as np
import datetime

def weekly_season(bootstrap_samples, intervention, predict_df, trend = True):
    prophet_predict = predict_df.copy()
    prophet_predict['weekday_name'] = pd.to_datetime(prophet_predict['ds']).dt.strftime("%A")

    units_week = prophet_predict.groupby('weekday_name').median().weekly
    trend = prophet_predict.trend.median()
    
    day_percentages = prophet_predict.groupby('weekday_name').median().weekly / prophet_predict.groupby('weekday_name').median().weekly.abs().sum() + 1
    start_date = datetime.datetime.strptime(intervention[0], '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(intervention[1], '%Y-%m-%d').date()
    
    period = (end_date - start_date).days + 1
    
    dates = pd.date_range(intervention[0], periods = period, freq = 'D')
    
    results = []
    for sample in bootstrap_samples:

        df = pd.DataFrame({'date': dates, 'value': sample})
        df['weekday_name'] = pd.to_datetime(df['date']).dt.strftime('%A')
        df = pd.merge(df, pd.DataFrame(day_percentages, index=day_percentages.index).reset_index(), on='weekday_name')
        
        if trend:
             df['value_adju'] = (df['value'] * units_week) + trend
        else:
            df['value_adju'] = df['value'] * units_week
        
        new_sample = df.loc[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date)), 'value_adju'].values
        
        results.append(new_sample)
    
    return np.array(results)

def yearly_season(bootstrap_samples, intervention, predict_df, trend = True):
    prophet_predict = predict_df.copy()
    prophet_predict['year_name'] = pd.to_datetime(prophet_predict['ds']).dt.strftime("%Y")

    units_week = prophet_predict.groupby('year_name').median().yearly
    trend = prophet_predict.trend.median()
    
    day_percentages = prophet_predict.groupby('year_name').median().yearly / prophet_predict.groupby('year_name').median().yearly.abs().sum() + 1
    start_date = datetime.datetime.strptime(intervention[0], '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(intervention[1], '%Y-%m-%d').date()
    
    period = (end_date - start_date).days + 1
    
    dates = pd.date_range(intervention[0], periods = period, freq = 'D')
    
    results = []
    for sample in bootstrap_samples:

        df = pd.DataFrame({'date': dates, 'value': sample})
        df['year_name'] = pd.to_datetime(df['date']).dt.strftime('%Y')
        df = pd.merge(df, pd.DataFrame(day_percentages, index=day_percentages.index).reset_index(), on='year_name')
        
        if trend:
             df['value_adju'] = (df['value'] * units_week) + trend
        else:
            df['value_adju'] = df['value'] * units_week
        
        new_sample = df.loc[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date)), 'value_adju'].values
        
        results.append(new_sample)
    
    return np.array(results)