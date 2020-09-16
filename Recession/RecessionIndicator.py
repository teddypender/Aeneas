#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:08:09 2020

@author: theodorepender
"""

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import datetime
from fredapi import Fred
import yfinance as yf
import pygsheets

#import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
#from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF



"""
Functionaility

"""

def getFredData(fred_series_ids, primary_dictionary_output):
    
    fred = Fred(api_key='e0e39002ebdae285ab9269213a68ccda')

        
    now = datetime.datetime.now()
    month = now.strftime('%m')
    year = now.year        
    most_recent_date = '{}-{}-07'.format(year, month)
    print('\nGetting data from FRED\'s API as of {}...'.format(most_recent_date))
    
    for series_name in list(fred_series_ids.keys()):
        series_id = fred_series_ids[series_name]
        print('\t|--Getting data for {}({}).'.format(series_name, series_id))
          
        data = fred.get_series(series_id)
        primary_dictionary_output[series_name] = pd.DataFrame(data).rename({0 : series_name}, axis = 1)
        
    #return primary_dictionary_output

def getYahooData(yahoo_series_ids, primary_dictionary_output):
         
    print('\nGetting data from Yahhoo\'s API ...')
    
    for series_name in list(yahoo_series_ids.keys()):
        series_id = yahoo_series_ids[series_name]
        print('\t|--Getting data for {}({}).'.format(series_name, series_id))
         
        data = yf.Ticker(series_id).history(period="max")[['Close']].rename({'Close' : 'S&P_500_Index'}, axis = 1)
        idx = pd.date_range(min(data.index), max(data.index))
        data = data.reindex(idx)
        data.ffill(inplace = True)
        data = data[data.index.day == 1]

        primary_dictionary_output[series_name] = data
        
    #return primary_dictionary_output

            
def initialFeatureEngineering(primary_dictionary_output):

    for k,v in primary_dictionary_output.items():
        # Calculate percentage change in three and twelve months of each data point
        series_3M, series_12M = pd.Series(v[k]), pd.Series(v[k])
        v[k + '_3M']  = ((1 - series_3M.pct_change(3)) ** 4) - 1 
        v[k + '_12M'] = series_12M.pct_change(12) * 100
        
        # Cosnider the spread of treasury 10Y with 5Y and 3Y respectively
        
        
def labelTargets(df):

    NBERRecessions = {'1': {'Begin': '1957-08-01', 'End': '1958-04-01'},
                       '2': {'Begin': '1960-04-01', 'End': '1961-02-01'},
                       '3': {'Begin': '1969-12-01', 'End': '1970-11-01'},
                       '4': {'Begin': '1973-11-01', 'End': '1975-03-01'},
                       '5': {'Begin': '1980-01-01', 'End': '1980-07-01'},
                       '6': {'Begin': '1981-07-01', 'End': '1982-11-01'},
                       '7': {'Begin': '1990-07-01', 'End': '1991-03-01'},
                       '8': {'Begin': '2001-03-01', 'End': '2001-11-01'},
                       '9': {'Begin': '2007-12-01', 'End': '2009-06-01'}}
    
    observations = len(df)
    df['Recession']             = [0] * observations
    df['Recession_in_3mo']      = [0] * observations
    df['Recession_in_6mo']      = [0] * observations
    df['Recession_in_12mo']     = [0] * observations
    df['Recession_in_24mo']     = [0] * observations
    
    for recession in NBERRecessions:
        end_condition = (NBERRecessions[recession]['End'] >= df.index)
        begin_condition = (df.index >= NBERRecessions[recession]['Begin'])
        df.loc[end_condition & begin_condition, 'Recession'] = 1
    
    
    for index in range(0, len(df)):
        if df['Recession'][index] == 1:
            if index >= 24:
                df.loc[df.index[min(index - 3, len(df) - 1)], 'Recession_in_3mo'] = 1
                df.loc[df.index[min(index - 6, len(df) - 1)], 'Recession_in_6mo'] = 1
                df.loc[df.index[min(index - 12, len(df) - 1)], 'Recession_in_12mo'] = 1
                df.loc[df.index[min(index - 24, len(df) - 1)], 'Recession_in_24mo'] = 1
                
            elif index >= 12:
                df.loc[df.index[min(index - 3, len(df) - 1)], 'Recession_in_3mo'] = 1
                df.loc[df.index[min(index - 6, len(df) - 1)], 'Recession_in_6mo'] = 1
                df.loc[df.index[min(index - 12, len(df) - 1)], 'Recession_in_12mo'] = 1

            elif index >= 6:
                df.loc[df.index[min(index - 3, len(df) - 1)], 'Recession_in_3mo'] = 1
                df.loc[df.index[min(index - 6, len(df) - 1)], 'Recession_in_6mo'] = 1
                
            elif index >= 3:
                df.loc[df.index[min(index - 3, len(df) - 1)], 'Recession_in_3mo'] = 1
           
    
            
def threeMonthFeature(df):
    columns = [x for x in df.columns if x[-2:] == '3M']
    targets = ['Recession', 'Recession_in_3mo', 'Recession_in_6mo', 'Recession_in_12mo', 'Recession_in_24mo']    
    return df[columns], df[targets], targets

def twelveMonthFeature(df):
    columns = [x for x in df.columns if x[-3:] == '12M']
    targets = ['Recession', 'Recession_in_3mo', 'Recession_in_6mo', 'Recession_in_12mo', 'Recession_in_24mo']
    return df[columns], df[targets], targets

def allFeatures(df):
    columns = [x for x in df.columns if x[-2:] == '3M'] + [x for x in df.columns if x[-3:] == '12M']
    targets = ['Recession', 'Recession_in_3mo', 'Recession_in_6mo', 'Recession_in_12mo', 'Recession_in_24mo']
    return df[columns], df[targets], targets

def adjustWithTarget(X, y, target):
    if target == 'Recession':
        X_update, y_update = X[:-1], y[:-1]
    elif target == 'Recession_in_3mo':
        X_update, y_update = X[:-3], y[:-3]
    elif target == 'Recession_in_6mo':
        X_update, y_update = X[:-6], y[:-6]
    elif target == 'Recession_in_12mo':
        X_update, y_update = X[:-12], y[:-12]
    elif target == 'Recession_in_24mo':
        X_update, y_update = X[:-24], y[:-24]
    return X_update, y_update




if __name__ == "__main__":
    
    fred_series_ids = {'Non-farm_Payrolls'          : 'PAYEMS',
                        'Civilian_Unemployment_Rate': 'UNRATE',
                        'Effective_Fed_Funds'       : 'FEDFUNDS',
                        'CPI_All_Items'             : 'CPIAUCSL',
                        '10Y_Treasury_Rate'         : 'GS10',
                        '5Y_Treasury_Rate'          : 'GS5',
                        '3_Month_T-Bill_Rate'       : 'TB3MS',
                        'IPI'                       : 'INDPRO'}
    yahoo_series_ids = {'S&P_500_Index'             : '^GSPC'}
    primary_dictionary_output = {}
    secondary_df_output = pd.DataFrame()
    
    
    getFredData(fred_series_ids, primary_dictionary_output)
    getYahooData(yahoo_series_ids, primary_dictionary_output)
    
    initialFeatureEngineering(primary_dictionary_output)
    
    df = pd.concat([primary_dictionary_output[series_name]for series_name in primary_dictionary_output.keys()], axis = 1)
    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    
    labelTargets(df)

    X_threedf, y_threedf, targets = threeMonthFeature(df)
    """
    # ----------- Model Testing ----------- #

    for i in [0,1,2,3]:
        
        target = targets[i]
        
        print('')
        print(target)
        print('')
        
        X_df, y_df = adjustWithTarget(X_threedf, y_threedf, target)
                
        names = [
                "Nearest Neighbors", 
#                 "Linear SVM", "RBF SVM", 
                 "Gaussian Process",
                 "Decision Tree", "Random Forest", 
                 "Neural Net", 
                 "AdaBoost",
#                 "Naive Bayes", "QDA"
                 ]
        
        classifiers = [
            KNeighborsClassifier(3),
#            SVC(kernel="linear", C=0.025),
#            SVC(gamma=2, C=1),
            GaussianProcessClassifier(1.0 * RBF(1.0)),
            DecisionTreeClassifier(max_depth=5),
            RandomForestClassifier(max_depth=5, n_estimators=10, max_features=9),
            MLPClassifier(alpha=0.001, max_iter=10000),
            AdaBoostClassifier()
            ]
        
        
        X, y = np.asarray(X_df), np.asarray(y_df[target])
        
        linearly_separable = (X, y)
        
        datasets = [
                    linearly_separable
                    ]
        
        # iterate over datasets
        for ds_cnt, ds in enumerate(datasets):
            # preprocess dataset, split into training and test part
            X, y = ds
            ss = StandardScaler().fit(X)
            X = ss.transform(X)
            X_True = ss.transform(X_threedf)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4, random_state=42)
        
            # iterate over classifiers
            for name, clf in zip(names, classifiers):
                clf.fit(X_train, y_train)
                score = clf.score(X_test, y_test)
                print(name, score)
                plt.figure(figsize = (10,6))
                plt.title('Binary Recession Predictor Using {0} Model & Target {1} (Score: {2})'.format(name, target, round(score,4)))
                
                plt.plot(X_threedf.index, [x[1] for x in clf.predict_proba(X_True)], label = 'Predicted Proabbility')
                plt.plot(X_threedf.index, clf.predict(X_True), label = ' Binary Prediction')
                    
                plt.plot(X_threedf.index, y_threedf[target], label = 'True')
                plt.ylabel('Binary Recession (1 = Yes, 0 = No)')
                plt.xlabel('Date')
                plt.legend()
    """
    # ----------- Model Running ----------- #
    
    # Choose GaussianProcessClassifier
    
    target = targets[1]
    X_df, y_df = adjustWithTarget(X_threedf, y_threedf, target)

    names = ["Gaussian Process"]
    classifiers = [GaussianProcessClassifier(1.0 * RBF(1.0))]
    
    X, y = np.asarray(X_df), np.asarray(y_df[target])
        
    linearly_separable = (X, y)
    
    datasets = [
                linearly_separable
                ]
    predictedProbability = []
    
    for ds_cnt, ds in enumerate(datasets):
            # preprocess dataset, split into training and test part
            X, y = ds
            ss = StandardScaler().fit(X)
            X = ss.transform(X)
            X_True = ss.transform(X_threedf)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.35, random_state=42)
        
            # iterate over classifiers
            for name, clf in zip(names, classifiers):
                clf.fit(X_train, y_train)
#                predictedProbability.append([x[1] for x in clf.predict_proba(X_True)])
                predictedProbability = [x[1] * 100 for x in clf.predict_proba(X_True)]


    df_Recession_Prediction = pd.DataFrame(index = X_threedf.index, data = predictedProbability, columns = ['Probability of Recession in 3 Months'])
    df_Recession_Prediction.reset_index(inplace = True)
    df_Recession_Prediction.rename({'index' : 'DateTime'}, axis = 1, inplace = True)
    
    
    df_Recession_Prediction_Recent = df_Recession_Prediction[-240:]
    
    #authorization
    gc = pygsheets.authorize(service_file='/Users/theodorepender/Desktop/Midnight-Labs-9d593d26ebe7.json')
    
    #open the google spreadsheet (where 'Recession-Indicator' is the name of my sheet)
    sh = gc.open('Recession-Indicator')
    
    #add worksheets
    #sh.add_worksheet('Sheet3')
    
    #get last update time
    last_update = gc.drive.get_update_time('1Kgn_QkPE58ZetRG_1g0MDpuKdxfpf-WI-8UDxuP4BYw')[0:10].split('-')
    last_update = pd.datetime(int(last_update[0]),int(last_update[1]), int(last_update[2]))
    
    date_time = last_update.strftime("%A, %B %dth")
    
    #select the sheet 
    wks = sh[0]
    wks_recent = sh[1]
    wks_update = sh[2]
    
    #update the sheets with the dataframes. 
    wks.set_dataframe(df_Recession_Prediction,(1,1))
    wks_recent.set_dataframe(df_Recession_Prediction_Recent,(1,1))
    wks_update.update_value('A1', date_time)
    


