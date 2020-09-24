#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 17:24:50 2020

@author: theodorepender
"""
import pandas as pd
import numpy as np
import chardet    
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

"""
rawdata = open('/Users/theodorepender/Downloads/SCDB_2020_01_justiceCentered_Citation.csv', 'rb').read()
result = chardet.detect(rawdata)
charenc = result['encoding']
print(charenc)
"""

scotusData = 'http://scdb.wustl.edu/_brickFiles/2020_01/SCDB_2020_01_justiceCentered_Citation.csv.zip'

scotusdf = pd.read_csv(scotusData,encoding = 'Windows-1252')

scotusdfCol = scotusdf[['term', 'dateDecision', 'issueArea', 'chief', 'justiceName', 'majority', 'decisionDirection']]
# for information on the featurs go to http://scdb.wustl.edu/_brickFiles/2009_02/SCDB_2009_02_codebook.pdf
# decisionDirection 1 = conservative, 2 = liberal, 3 = unspecifiable: http://supremecourtdatabase.org/documentation.php?var=decisionDirection
# majority http://supremecourtdatabase.org/documentation.php?var=vote
# vote, 1 = voted with majority or plurality, 2 = dissent, 3 =	regular concurrence, 4 =	special concurrence, 5 =	judgment of the Court, 6 =	dissent from a denial or dismissal of certiorari , or dissent from summary affirmation of an appeal, 7 =	jurisdictional dissent, 8 =	justice participated in an equally divided vote

# scotusIssueArea = pd.concat([scotusdfCol[['term', 'justiceName']], pd.get_dummies(scotusdfCol['issueArea']).rename({1.0 : 'Criminal Procedure', 
#                                                                                                                       2.0: 'Civil Rights', 
#                                                                                                                       3.0 : 'First Amendment',
#                                                                                                                       4.0 : 'Due Process',
#                                                                                                                       5.0 : 'Privacy',
#                                                                                                                       6.0 : 'Attorneys',
#                                                                                                                       7.0 : 'Unions',
#                                                                                                                       8.0 : 'Economic Activity',
#                                                                                                                       9.0 : 'Judicial Power',
#                                                                                                                       10.0 : 'Federalism',
#                                                                                                                       11.0 : 'Interstate Relations',
#                                                                                                                       12.0 : 'Federal Taxation',
#                                                                                                                       13.0 : 'Miscellaneous',
#                                                                                                                       14.0 : 'Private Action',}, axis = 1),
#                              pd.get_dummies(scotusdfCol['decisionDirection']).rename({1.0 : 'Conservative', 2.0: 'Liberal', 3.0 : 'Unspecifiable'}, axis = 1)], axis = 1)
#                              #pd.get_dummies(scotusdfCol['justiceName'])], axis = 1)


# rbg = scotusIssueArea[scotusIssueArea.justiceName == 'RBGinsburg']
# X, y = rbg[[x for x in rbg.columns if x not in ['term', 'justiceName', 'Conservative', 'Liberal', 'Unspecifiable']]], rbg['Liberal']
# clf = LogisticRegression(random_state=0).fit(X, y)
# clf.predict(X)

# clf.predict_proba(X)


# clf.score(X, y)



scotusDecision = pd.concat([scotusdfCol[['term','justiceName']],pd.get_dummies(scotusdfCol['decisionDirection']).rename({1.0 : 'Conservative', 2.0: 'Liberal', 3.0 : 'Unspecifiable'}, axis = 1)], axis = 1)
df = scotusDecision.groupby(['term']).sum()[['Conservative', 'Liberal', 'Unspecifiable']].reset_index().sort_values('term')
df.groupby('term').apply(lambda x : x/x.sum(axis = 1).iloc[0])
pd.Series(list(df['Liberal'])) / pd.Series(list(df.sum(axis = 1)))

rob = scotusDecision[scotusDecision.justiceName == 'JGRoberts']
rob200517 = rob[rob.term < 2017]
rob201820 = rob[rob.term >= 2017]

total0517 = rob200517.groupby([True for x in range(len(rob200517))]).sum()
total0517 = total0517 / sum(list(total0517[['Conservative', 'Liberal', 'Unspecifiable']].sum()))


total1820 = rob201820.groupby([True for x in range(len(rob201820))]).sum()
total1820 = total1820 / sum(list(total1820[['Conservative', 'Liberal', 'Unspecifiable']].sum()))
