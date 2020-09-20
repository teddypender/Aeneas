#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:51:34 2020

@author: theodorepender
"""
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime as dt
import SocietyCharts

urlPV    = r'https://mappingpoliceviolence.org/s/MPVDatasetDownload.xlsx'
urlWiki  = r'https://en.wikipedia.org/wiki/Race_and_ethnicity_in_the_United_States'
urlUSPop = r'https://www.census.gov/popclock/print.php?component=pop_on_date&image=https://www.census.gov/images/census-logo-whiteBG.png' #r'https://www.census.gov/popclock/'
# ----------------- Data

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
USPopulation = 330310075 /1e6
 
racePopulationEst = {k : USPopulation * (v / 100) for k,v in raceBreakout.items()}

killingsPerRace = pd.DataFrame(df.groupby('Victim\'s race').apply(lambda x : len(x))).rename({0 : 'Count'}, axis = 1).reset_index()
killingsPerRace['KillingsPerMillion'] = [x / racePopulationEst[y] for x,y in zip(killingsPerRace['Count'], killingsPerRace['Victim\'s race'])]

killingsPerRaceTimeSeries = pd.DataFrame(df.groupby(['Victim\'s race','Date of Incident (month/day/year)']).apply(lambda x : len(df[(df['Victim\'s race'] == x['Victim\'s race'].iloc[0]) & (df['Date of Incident (month/day/year)'] <= x['Date of Incident (month/day/year)'].iloc[0])]))).rename({0 : 'Count'}, axis = 1).reset_index()
killingsPerRaceTimeSeries['KillingsPerMillion'] = [x / racePopulationEst[y] for x,y in zip(killingsPerRaceTimeSeries['Count'], killingsPerRaceTimeSeries['Victim\'s race'])]

blackKilling           = [[int(x * 1000),y] for x,y in zip((killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Black']['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Black']['KillingsPerMillion'])]
hispanicKilling        = [[int(x * 1000),y] for x,y in zip((killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Hispanic']['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Hispanic']['KillingsPerMillion'])]
nativeAmericanKilling  = [[int(x * 1000),y] for x,y in zip((killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Native American']['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Native American']['KillingsPerMillion'])]
pacificIslanderKilling = [[int(x * 1000),y] for x,y in zip((killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Pacific Islander']['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Pacific Islander']['KillingsPerMillion'])]
AsianKilling           = [[int(x * 1000),y] for x,y in zip((killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Asian']['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'Asian']['KillingsPerMillion'])]
whiteKilling           = [[int(x * 1000),y] for x,y in zip((killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'White']['Date of Incident (month/day/year)'] - dt.datetime(1970,1,1)).dt.total_seconds(),killingsPerRaceTimeSeries[killingsPerRaceTimeSeries['Victim\'s race'] == 'White']['KillingsPerMillion'])]


lineChartData = SocietyCharts.lineSeriesData.format('Black', blackKilling, 
                             'Hispanic', hispanicKilling,
                             'Native American', nativeAmericanKilling, 
                             'Pacific Islander', pacificIslanderKilling, 
                             'Asian', AsianKilling, 
                             'White', blackKilling)

killingRateByRace = SocietyCharts.lineChartTop + SocietyCharts.lineChartBottom_.format('killingRateByRace', '#FFFFFF', lineChartData, 'Rate of Killing by Race (Per Million)', 300)


fileNames   = ['PoliceBrutalityRateTimeSeries']
htmlStrings = [killingRateByRace]
#write to HTML Files
for file, stringChart in zip(fileNames, htmlStrings):
    with open(file + '.html', "w") as text_file:
        text_file.write(stringChart)




