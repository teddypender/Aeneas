#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:51:34 2020

@author: theodorepender
"""
import numpy as np
import pandas as pd
# from git import Repo
import requests
from bs4 import BeautifulSoup
import datetime as dt
import SocietyCharts
import datetime

# ----------------- URLs ----------------- #
urlPV          = r'https://mappingpoliceviolence.org/s/MPVDatasetDownload.xlsx'
urlWiki        = r'https://en.wikipedia.org/wiki/Race_and_ethnicity_in_the_United_States'
urlUSPop       = r'https://www.census.gov/popclock/print.php?component=pop_on_date&image=https://www.census.gov/images/census-logo-whiteBG.png' #r'https://www.census.gov/popclock/'
urlUSStatePop  = r'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population'
urlUSStateRace = r'https://www.governing.com/gov-data/census/state-minority-population-data-estimates.html' #r'https://worldpopulationreview.com/states/states-by-race'
urlRacePop     = r'https://worldpopulationreview.com/79594026-c853-48bd-a21b-64d49a3273e3'

# ----------------- Mapping ----------------- #
usStateAb = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

columnMap = {
    'Hispanic (of any race)' : 'Hispanic',
    'Non-Hispanic White' : 'White',
       'Non-Hispanic Black' : 'Black', 
       'Non-Hispanic Asian' : 'Asian',
       'Non-Hispanic American Indian' : 'Native American'
    }

# ----------------- Data ----------------- #

websiteText     = requests.get(urlUSStateRace).text
soupPopulation  = BeautifulSoup(websiteText,'lxml')
USPopulationLoc = soupPopulation.findAll('table')[1]
dfStateRacePct  = pd.read_html(str(USPopulationLoc))[0]

dfStateRacePct['State'] = [usStateAb[x] for x in dfStateRacePct['State'] ]

for col in [x for x in dfStateRacePct.columns if x != 'State']:
    dfStateRacePct[col] = [float(x.replace('%', '')) for x in dfStateRacePct[col]]

dfStateRacePct.rename(columnMap, axis = 1, inplace = True)
dfStateRacePct['Pacific Islander'] = 100 - dfStateRacePct.sum(axis = 1)
dfStateRacePct['Unknown race'] = np.nan

df = pd.read_excel(urlPV)

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

killingsPerRaceState = pd.DataFrame(df.groupby(['State','Victim\'s race']).apply(lambda x : len(x))).rename({0 : 'Count'}, axis = 1).reset_index()
killingsPerRaceState['ratePerPctPopulation']        = [x / dfStateRacePct.set_index('State').to_dict()[r][s] if dfStateRacePct.set_index('State').to_dict()[r][s] != 0 else np.nan for x,r,s in zip(killingsPerRaceState['Count'],killingsPerRaceState['Victim\'s race'],killingsPerRaceState['State'])]
killingsPerRaceState['ratePerPctPopulationVsWhite'] = [x / killingsPerRaceState[(killingsPerRaceState['Victim\'s race'] == 'White') & (killingsPerRaceState['State'] == s)]['ratePerPctPopulation'].iloc[0] if len(killingsPerRaceState[(killingsPerRaceState['Victim\'s race'] == 'White') & (killingsPerRaceState['State'] == s)]) > 0 else np.nan for x,s in zip(killingsPerRaceState['ratePerPctPopulation'] , killingsPerRaceState['State'])]

blackKillingsPerRaceState = killingsPerRaceState[killingsPerRaceState['Victim\'s race'] == 'Black'].round(3)

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

blackMultiple           = SocietyCharts.multiple.format(raceMultiples[0], '180', 'rgb(224, 155, 81)')
hispanickMultiple       = SocietyCharts.multiple.format(raceMultiples[1], '90', 'rgb(195, 95, 95)')
nativeAmericanMultiple  = SocietyCharts.multiple.format(raceMultiples[2], '90', 'rgb(195, 95, 95)')
pacificIslanderMultiple = SocietyCharts.multiple.format(raceMultiples[3], '180', 'rgb(224, 155, 81)')
asianMultiple           = SocietyCharts.multiple.format(raceMultiples[4], '90', 'rgb(195, 95, 95)')



blackBbrutalityMapByState = SocietyCharts.honeyCombChartTop + SocietyCharts.honeyCombChartBottom.format('PoliceBrutalityMap', 'Police Brutality Map', SocietyCharts.honeyCombData.format(blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'AL']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'AK']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'AZ']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'AR']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'CA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'CO']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'CT']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'DE']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'DC']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'FL']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'GA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'HI']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'ID']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'IL']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'IN']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'IA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'KS']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'KY']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'LA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'ME']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'MD']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'MA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'MI']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'MN']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'MS']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'MO']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        0,#blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'MT']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'NE']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'NV']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        0,#blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'NH']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'NJ']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'NM']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'NY']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'NC']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        0,#blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'ND']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'OH']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'OK']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'OR']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'PA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'RI']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'SC']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        0,#blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'SD']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'TN']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'TX']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'UT']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        0,#blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'VT']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'VA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'WA']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'WV']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'WI']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                        0#blackKillingsPerRaceState[blackKillingsPerRaceState['State'] == 'WY']['ratePerPctPopulationVsWhite'].iloc[0], 
                                                                                                                                                                                       ))




lastUpdated      = SocietyCharts.lastUpdated.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M%p"))



fileNames   = ['lastUpdated', 'PoliceBrutalityRateTimeSeries', 'blackRateMultiple', 'hispanicRateMultiple', 'nativeAmericanRateMultiple', 'pacificIslanderRateMultiple', 'asianRateMultiple', 'blackBrutalityMap']
htmlStrings = [lastUpdated, killingRateByRace, blackMultiple, hispanickMultiple, nativeAmericanMultiple, pacificIslanderMultiple, asianMultiple, blackBbrutalityMapByState]
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
