#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:51:34 2020

@author: theodorepender
"""
import numpy as np
import pandas as pd
from git import Repo
import requests
from bs4 import BeautifulSoup
import datetime as dt
import SocietyCharts

# ----------------- URLs ----------------- #
urlPV          = r'https://mappingpoliceviolence.org/s/MPVDatasetDownload.xlsx'
urlWiki        = r'https://en.wikipedia.org/wiki/Race_and_ethnicity_in_the_United_States'
urlUSPop       = r'https://www.census.gov/popclock/print.php?component=pop_on_date&image=https://www.census.gov/images/census-logo-whiteBG.png' #r'https://www.census.gov/popclock/'
urlUSStatePop  = r'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population'
urlUSStateRace = r'https://www.governing.com/gov-data/census/state-minority-population-data-estimates.html'

# ----------------- Data ----------------- #

websiteText     = requests.get(urlUSPop).text
soupPopulation  = BeautifulSoup(websiteText,'lxml')
USPopulationLoc = soupPopulation.find('span',{'class':'pop-count'})

df          = pd.read_excel(urlPV)


#Wikipedia Source: urlWiki 
raceBreakout = {'White' : 63.4,
                'Hispanic' : 15.3,
                'Black' : 13.4,
                'Asian' : 5.9,
                'Native American' : 1.3,
                'Pacific Islander' : 0.2,
                'Two or More' : 2.7,
                'Unknown race' : np.nan}

#Google Source: 
USPopulation = 330310075 / 1e6
 
racePopulationEst = {k : USPopulation * (v / 100) for k,v in raceBreakout.items()}

killingsPerRace = pd.DataFrame(df.groupby('Victim\'s race').apply(lambda x : len(x))).rename({0 : 'Count'}, axis = 1).reset_index()
killingsPerRace['KillingsPerMillion'] = [x / racePopulationEst[y] for x,y in zip(killingsPerRace['Count'], killingsPerRace['Victim\'s race'])]

killingsPerRaceTimeSeries = pd.DataFrame(df.groupby(['Victim\'s race','Date of Incident (month/day/year)']).apply(lambda x : len(df[(df['Victim\'s race'] == x['Victim\'s race'].iloc[0]) & (df['Date of Incident (month/day/year)'] <= x['Date of Incident (month/day/year)'].iloc[0])]))).rename({0 : 'Count'}, axis = 1).reset_index()
killingsPerRaceTimeSeries['KillingsPerMillionCumulative'] = [x for x,y in zip(killingsPerRaceTimeSeries['Count'], killingsPerRaceTimeSeries['Victim\'s race'])]
killingsPerRaceTimeSeries['KillingsPerMillion'] = [x / racePopulationEst[y] for x,y in zip(killingsPerRaceTimeSeries['Count'], killingsPerRaceTimeSeries['Victim\'s race'])]

blackPerMillionTimeSeries = killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Black'].set_index('Date of Incident (month/day/year)')
idx = pd.date_range(min(blackPerMillionTimeSeries.index), dt.datetime.today())
blackPerMillionTimeSeries = blackPerMillionTimeSeries.reindex(idx, fill_value=np.nan).ffill().reset_index().rename({'index' : 'Date of Incident (month/day/year)'}, axis = 1)

hispanicPerMillionTimeSeries = killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Hispanic'].set_index('Date of Incident (month/day/year)')
idx = pd.date_range(min(hispanicPerMillionTimeSeries.index), dt.datetime.today())
hispanicPerMillionTimeSeries = hispanicPerMillionTimeSeries.reindex(idx, fill_value=np.nan).ffill().reset_index().rename({'index' : 'Date of Incident (month/day/year)'}, axis = 1)

nativeAmericanPerMillionTimeSeries = killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Native American'].set_index('Date of Incident (month/day/year)')
idx = pd.date_range(min(nativeAmericanPerMillionTimeSeries.index), dt.datetime.today())
nativeAmericanPerMillionTimeSeries = nativeAmericanPerMillionTimeSeries.reindex(idx, fill_value=np.nan).ffill().reset_index().rename({'index' : 'Date of Incident (month/day/year)'}, axis = 1)

pacificIslanderPerMillionTimeSeries = killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Pacific Islander'].set_index('Date of Incident (month/day/year)')
idx = pd.date_range(min(pacificIslanderPerMillionTimeSeries.index), dt.datetime.today())
pacificIslanderPerMillionTimeSeries = pacificIslanderPerMillionTimeSeries.reindex(idx, fill_value=np.nan).ffill().reset_index().rename({'index' : 'Date of Incident (month/day/year)'}, axis = 1)

asianPerMillionTimeSeries = killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Asian'].set_index('Date of Incident (month/day/year)')
idx = pd.date_range(min(asianPerMillionTimeSeries.index), dt.datetime.today())
asianPerMillionTimeSeries = asianPerMillionTimeSeries.reindex(idx, fill_value=np.nan).ffill().reset_index().rename({'index' : 'Date of Incident (month/day/year)'}, axis = 1)

whitePerMillionTimeSeries = killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'White'].set_index('Date of Incident (month/day/year)')
idx = pd.date_range(min(whitePerMillionTimeSeries.index), dt.datetime.today())
whitePerMillionTimeSeries = whitePerMillionTimeSeries.reindex(idx, fill_value=np.nan).ffill().reset_index().rename({'index' : 'Date of Incident (month/day/year)'}, axis = 1)

blackKillingCumulative           = [[int(x * 1000),y] for x,y in zip((blackPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),blackPerMillionTimeSeries['KillingsPerMillionCumulative'])]
hispanicKillingCumulative        = [[int(x * 1000),y] for x,y in zip((hispanicPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),hispanicPerMillionTimeSeries['KillingsPerMillionCumulative'])]
nativeAmericanKillingCumulative  = [[int(x * 1000),y] for x,y in zip((nativeAmericanPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),nativeAmericanPerMillionTimeSeries['KillingsPerMillionCumulative'])]
pacificIslanderKillingCumulative = [[int(x * 1000),y] for x,y in zip((pacificIslanderPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),pacificIslanderPerMillionTimeSeries['KillingsPerMillionCumulative'])]
AsianKillingCumulative           = [[int(x * 1000),y] for x,y in zip((asianPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),asianPerMillionTimeSeries['KillingsPerMillionCumulative'])]
whiteKillingCumulative           = [[int(x * 1000),y] for x,y in zip((whitePerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),whitePerMillionTimeSeries['KillingsPerMillionCumulative'])]

blackKilling           = [[int(x * 1000),y] for x,y in zip((blackPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),blackPerMillionTimeSeries['KillingsPerMillion'])]
hispanicKilling        = [[int(x * 1000),y] for x,y in zip((hispanicPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),hispanicPerMillionTimeSeries['KillingsPerMillion'])]
nativeAmericanKilling  = [[int(x * 1000),y] for x,y in zip((nativeAmericanPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),nativeAmericanPerMillionTimeSeries['KillingsPerMillion'])]
pacificIslanderKilling = [[int(x * 1000),y] for x,y in zip((pacificIslanderPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),pacificIslanderPerMillionTimeSeries['KillingsPerMillion'])]
AsianKilling           = [[int(x * 1000),y] for x,y in zip((asianPerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),asianPerMillionTimeSeries['KillingsPerMillion'])]
whiteKilling           = [[int(x * 1000),y] for x,y in zip((whitePerMillionTimeSeries['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),whitePerMillionTimeSeries['KillingsPerMillion'])]

raceMultiples          = [round(x[-1][1] / whiteKilling[-1][1], 2) for x in [blackKilling, hispanicKilling, nativeAmericanKilling, pacificIslanderKilling, AsianKilling]]

lineChartData = SocietyCharts.lineSeriesData.format('Black', blackKillingCumulative, 
                                                    'Hispanic', hispanicKillingCumulative,
                                                    'Native American', nativeAmericanKillingCumulative, 
                                                    'Pacific Islander', pacificIslanderKillingCumulative, 
                                                    'Asian', AsianKillingCumulative, 
                                                    'White', whiteKillingCumulative)

killingRateByRace       = SocietyCharts.lineChartTop + SocietyCharts.lineChartBottom_.format('killingRateByRace', '#FFFFFF', lineChartData, 'Rate of Killing by Race (Per Million)', max(killingsPerRaceTimeSeries['KillingsPerMillionCumulative'] * 1.1))
blackMultiple           = SocietyCharts.multiple.format(raceMultiples[0])
hispanickMultiple       = SocietyCharts.multiple.format(raceMultiples[1])
nativeAmericanMultiple  = SocietyCharts.multiple.format(raceMultiples[2])
pacificIslanderMultiple = SocietyCharts.multiple.format(raceMultiples[3])
asianMultiple           = SocietyCharts.multiple.format(raceMultiples[4])



brutalityMapByState = SocietyCharts.honeyCombChartTop + SocietyCharts.honeyCombChartBottom.format('PoliceBrutalityMap', 'Police Brutality Map', SocietyCharts.honeyCombData.format('Name'))



fileNames   = ['PoliceBrutalityRateTimeSeries', 'blackRateMultiple', 'hispanicRateMultiple', 'nativeAmericanRateMultiple', 'pacificIslanderRateMultiple', 'asianRateMultiple', 'brutalityMap']
htmlStrings = [killingRateByRace, blackMultiple, hispanickMultiple, nativeAmericanMultiple, pacificIslanderMultiple, asianMultiple, brutalityMapByState]
#write to HTML Files
for file, stringChart in zip(fileNames, htmlStrings):
    with open(file + '.html', "w") as text_file:
        text_file.write(stringChart)


# https://stackoverflow.com/questions/41836988/git-push-via-gitpython
# PATH_OF_GIT_REPO = r'path\to\your\project\folder\.git'  # make sure .git folder is properly configured
# COMMIT_MESSAGE = 'comment from python script'

# def git_push():
#     try:
#         repo = Repo(PATH_OF_GIT_REPO)
#         repo.git.add(update=True)
#         repo.index.commit(COMMIT_MESSAGE)
#         origin = repo.remote(name='origin')
#         origin.push()
#     except:
#         print('Some error occured while pushing the code')    

# git_push()
