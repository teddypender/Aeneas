#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 08:43:51 2020

@author: theodorepender
"""
import pandas as pd
import numpy as np
# from scipy.stats import binom
import datetime
from dateutil import parser
import scipy.stats as stats
import SenateForecastCharts

fivethirtyeightzip   = 'https://projects.fivethirtyeight.com/polls-page/senate_polls.csv'
pollsterRatings      = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/pollster-ratings.csv'
senateMakeupurl      = 'https://en.wikipedia.org/wiki/List_of_current_United_States_senators'
presedentialStateurl = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/polls/pres_pollaverages_1968-2016.csv'
partyDict            = {'Republican' : 'REP', 'Democratic' : 'DEM', 'Independent[a]' : 'DEM'}

senateBreakout     = pd.read_html(senateMakeupurl)[0]
senateBreakoutFull = pd.read_html(senateMakeupurl)[4][['State', 'Senator', 'Party.1', 'Term up']]
senateBreakoutFull['Term_up'] = [x.split()[0] for x in senateBreakoutFull['Term up']]
senateBreakoutFull['candidate_party'] = [partyDict[p] for p in senateBreakoutFull['Party.1']]

pollsterRatingsdf   = pd.read_csv(pollsterRatings)
pollratingsDict     = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], pollsterRatingsdf['Mean-Reverted Advanced Plus Minus'])}
pollratingsDictBias = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], [x if type(x) == str else '0 0' for x in pollsterRatingsdf['Bias']])}
pollratingsDictErro = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], pollsterRatingsdf['Simple Expected Error'])}

senatedfAll                    = pd.read_csv(presedentialStateurl)
senatedfAll                    = senatedfAll[senatedfAll['cycle'].isin([2016])][['timestamp', 'state', 'candidate_name', 'pct_estimate']].rename({'pct_estimate' : 'pct'}, axis = 1)
senatedfAll['weight']          = [1 for x in range(len(senatedfAll))]
senatedfAll['candidate_party'] = ['DEM' if x == 'Hillary Rodham Clinton' else 'REP' if x == 'Donald Trump' else 'IND' for x in senatedfAll['candidate_name']]

senatedf                    = pd.read_csv(fivethirtyeightzip)
senatedf['number_people']   = (senatedf['pct'] / 100) * senatedf['sample_size']
senatedf['date_difference'] = [(datetime.datetime.today() - parser.parse(x)).days + 1 for x in senatedf['end_date']]
senatedf                    = senatedf[(senatedf.cycle == 2020) & (senatedf.date_difference < 365) & (senatedf.race_id != 7781)]
senatedf                    = senatedf[senatedf.candidate_party.isin(['DEM', 'REP'])]
senatedf['end_date']        = [parser.parse(x) for x in senatedf['end_date']]

# ---------------------------------- Create Prior Distribution ---------------------------------- #

def skew_norm_pdf(nSimulations, e=0, w=1, a=0):
    # adapated from:
    # http://stackoverflow.com/questions/5884768/skew-normal-distribution-in-scipy
    x = np.linspace(0,100,nSimulations * 10) 
    t = (x-e) / w
    p = 2.0 * w * stats.norm.pdf(t) * stats.norm.cdf(a*t)
    return p, x


def simulateSenate(senatedf, senatedfAll, pollratingsDict, pollratingsDictBias, pollratingsDictErro, normalPolls = True, nSimulations = 10000):
    
    matrixOfForecasts = []
    
    dfpriorMeanAll  = pd.DataFrame(senatedfAll.groupby(['candidate_party', 'state']).apply(lambda x : x.pct.mean())).rename({0 : 'PriorEstimateMean'}, axis = 1).reset_index()
    dfpriorStdAll   = pd.DataFrame(senatedfAll.groupby(['candidate_party', 'state']).apply(lambda x : x.pct.std())).rename({0 : 'PriorEstimateStd'}, axis = 1).reset_index()
    
    for i in range(len(senateBreakoutFull)):
        incumbParty = senateBreakoutFull['candidate_party'].iloc[i]
        senateState = senateBreakoutFull['State'].iloc[i]
        senator     = senateBreakoutFull['Senator'].iloc[i]
        print(i, incumbParty, senateState, senator)
        
        if senateBreakoutFull['Term_up'].iloc[i] == '2020':
            ridList     = list(senatedf[senatedf.state == senateState]['race_id'].unique())
            
            if len(ridList) == 0:
   
                demPFMean, repPFMean = dfpriorMeanAll[(dfpriorMeanAll.candidate_party == 'DEM') & (dfpriorMeanAll.state == senateState)]['PriorEstimateMean'].iloc[0], dfpriorMeanAll[(dfpriorMeanAll.candidate_party == 'REP') & (dfpriorMeanAll.state == senateState)]['PriorEstimateMean'].iloc[0]
                demPFStd, repPFStd   = dfpriorStdAll[(dfpriorStdAll.candidate_party == 'DEM') & (dfpriorStdAll.state == senateState)]['PriorEstimateStd'].iloc[0], dfpriorStdAll[(dfpriorStdAll.candidate_party == 'REP') & (dfpriorStdAll.state == senateState)]['PriorEstimateStd'].iloc[0]
                
                muDem, muRep = demPFMean, repPFMean
                # demList, repList = np.random.gumbel(muDem, demPFStd, nSimulations), np.random.gumbel(muRep, repPFStd, nSimulations)
                demList, repList = np.random.normal(muDem, demPFStd, nSimulations), np.random.normal(muRep, repPFStd, nSimulations)
                
                if incumbParty == 'DEM':
                    incumbWins = ['DEM' if x > y else 'REP'for x,y in zip(demList, repList)]
                else:
                    incumbWins = ['REP' if x > y else 'DEM'for x,y in zip(repList, demList)]
                
            else:
                if len(ridList) > 1:
                    df = senatedf[senatedf.race_id.isin(ridList)]
                    df['lastname'] = [x.split()[-1] for x in df['candidate_name']]
                    rid = df[df['lastname'] == senator.split()[-1]].race_id.iloc[0]
                # elif XXXXX: consider when the sitting senator is not up for relection and there are two seats open
                else:
                    rid = ridList[0]

                if len(senatedf[senatedf.race_id == rid]) > 3:
                    df           = senatedf[senatedf.race_id == rid]
                    df['weight'] = [min(df['date_difference']) / x for x in df['date_difference']]
                    df['bias']   = [pollratingsDictBias[p] if p in pollratingsDictBias.keys() else '0 0' for p in df['pollster_rating_id']]
                    df['bias']   = [['DEM', float(x.split()[1])] if x.split()[0] == 'D' else ['REP', float(x.split()[1])] if x.split()[0] == 'R' else ['0', '0'] for x in df['bias']]
                    df['pct']    = [x - y[1] if y[0] == pa else x for x,y,pa in zip(df['pct'], df['bias'], df['candidate_party'])]
                    df['stdDev'] = [pollratingsDictErro[p] if p in pollratingsDictErro.keys() else np.mean([x for x in pollratingsDictErro.values()]) for p in df['pollster_rating_id']]
                    df['pctMu']  = [np.mean(np.random.gumbel(mu, stdDev, 10000)) for mu, stdDev in zip(df['pct'], df['stdDev'])]
                    dfpriorMean = pd.DataFrame(df.groupby(['candidate_party', 'race_id', 'state']).apply(lambda x : sum(x.pct * x.weight) / x.weight.sum())).rename({0 : 'PriorEstimateMean'}, axis = 1).reset_index()
                    dfpriorSkew  = pd.DataFrame(df.groupby(['candidate_party', 'race_id', 'state']).apply(lambda x : stats.skew(x.pct) * 0)).rename({0 : 'PriorEstimateSkew'}, axis = 1).reset_index()
                    # dfpriorMean  = pd.DataFrame(df.groupby(['candidate_party', 'race_id', 'state']).apply(lambda x : x.pct.mean())).rename({0 : 'PriorEstimateMean'}, axis = 1).reset_index()
                    dfpriorStd   = pd.DataFrame(df.groupby(['candidate_party', 'race_id', 'state']).apply(lambda x : x.stdDev.mean() * 1)).rename({0 : 'PriorEstimateStd'}, axis = 1).reset_index()
                    
                    demPFMean, repPFMean = dfpriorMean[dfpriorMean.candidate_party == 'DEM']['PriorEstimateMean'].iloc[0], dfpriorMean[dfpriorMean.candidate_party == 'REP']['PriorEstimateMean'].iloc[0]
                    demPFStd, repPFStd   = dfpriorStd[dfpriorStd.candidate_party == 'DEM']['PriorEstimateStd'].iloc[0], dfpriorStd[dfpriorStd.candidate_party == 'REP']['PriorEstimateStd'].iloc[0]
                    demPFSkew, repPFSkew = dfpriorSkew[dfpriorSkew.candidate_party == 'DEM']['PriorEstimateSkew'].iloc[0], dfpriorSkew[dfpriorSkew.candidate_party == 'REP']['PriorEstimateSkew'].iloc[0]

                    if normalPolls == True:
                        muDem, muRep = demPFMean, repPFMean
                    else:
                        muDem, muRep = demPFMean, repPFMean #demLHMean, repLHMean #fix this
                else:
                    # Poll Narrowing
                    days_to_election = [(parser.parse(x) - datetime.datetime.today()).days for x in senatedf['election_date']]
                    narrowing = 0 # = 3percent difference / 2 people
                    narrowingFromNow = narrowing * ((365 - days_to_election[0]) / 365)
                    
                    demPFMean, repPFMean = dfpriorMeanAll[(dfpriorMeanAll.candidate_party == 'DEM') & (dfpriorMeanAll.state == senateState)]['PriorEstimateMean'].iloc[0], dfpriorMeanAll[(dfpriorMeanAll.candidate_party == 'REP') & (dfpriorMeanAll.state == senateState)]['PriorEstimateMean'].iloc[0]
                    demPFStd, repPFStd   = dfpriorStdAll[(dfpriorStdAll.candidate_party == 'DEM') & (dfpriorStdAll.state == senateState)]['PriorEstimateStd'].iloc[0], dfpriorStdAll[(dfpriorStdAll.candidate_party == 'REP') & (dfpriorStdAll.state == senateState)]['PriorEstimateStd'].iloc[0]
                    
                    if demPFMean > repPFMean:
                        repPFMean += narrowingFromNow
                        demPFMean -= narrowingFromNow
                    else:
                        demPFMean += narrowingFromNow
                        repPFMean -= narrowingFromNow   
                    
                    #
                    
                    muDem, muRep = demPFMean, repPFMean
                    
                # demList, repList = np.random.gumbel(muDem, demPFStd, nSimulations), np.random.gumbel(muRep, repPFStd, nSimulations)
                
                demp, xdem, = skew_norm_pdf(nSimulations, e=muDem, w=demPFStd, a=demPFSkew)
                repp, xrep = skew_norm_pdf(nSimulations, e=muRep, w=repPFStd, a=repPFSkew)
                demList, repList = np.random.choice(xdem, nSimulations, p=demp/sum(demp)), np.random.choice(xrep, nSimulations, p=repp/sum(repp))
                
                
                if incumbParty == 'DEM':
                    incumbWins = ['DEM' if x > y else 'REP'for x,y in zip(demList, repList)]
                    # print(incumbWins.count('DEM') / len(incumbWins)) 
                else:
                    incumbWins = ['REP' if x > y else 'DEM'for x,y in zip(repList, demList)]
                    # print(incumbWins.count('REP') / len(incumbWins)) 
                    
        else:
            incumbWins = [incumbParty for x in range(0, nSimulations)]
                        
        matrixOfForecasts.append(incumbWins)
        
        simulationsDataFrame = pd.DataFrame(matrixOfForecasts)
        simulationsDataFrame = pd.concat([senateBreakoutFull[['State', 'Senator', 'candidate_party']], simulationsDataFrame], axis = 1)
        
        listOfSimulationdfs = []
        for col in [x for x in simulationsDataFrame.columns if x not in ['State', 'Senator', 'candidate_party']]:
            simulation = pd.DataFrame(simulationsDataFrame[col].value_counts()).T
            listOfSimulationdfs.append(simulation)
            
        dataFrameOfSimulations = pd.concat(listOfSimulationdfs)
    return dataFrameOfSimulations, simulationsDataFrame

    
def createResults(senateResults, simulationsDataFrame):
    senateResults['tuple']              = [(x,y) for x,y in zip(senateResults['DEM'], senateResults['REP'])]
    senateResultsTuples                 = pd.DataFrame(senateResults['tuple'].value_counts()).reset_index().rename({'index' : 'breakdown'}, axis = 1)
    senateResultsTuples['probability']  = senateResultsTuples['tuple'] / senateResultsTuples['tuple'].sum() * 100
    senateResultsTuples['Democrat']     = [x[0] for x in senateResultsTuples['breakdown']]
    senateResultsTuples['Republican']   = [x[1] for x in senateResultsTuples['breakdown']]
    senateResultsTuples.sort_values('Democrat', inplace = True)
    
    senDemSort = senateResults['DEM'].unique()
    senDemSort.sort()
    
    senRepSort = senateResults['REP'].unique()
    senRepSort.sort()
    
    totalSeats = [x for x in range(min(min(senRepSort), min(senDemSort)), max(max(senRepSort), max(senDemSort)))]
    
    demProbabilities = {k : len(senateResults[senateResults.DEM == k]) / len(senateResults) for k in totalSeats}
    repProbabilities = {k : len(senateResults[senateResults.REP == k]) / len(senateResults) for k in totalSeats}
    
    demExpSeats, dem10thSeats, dem90thSeats = senateResults.mean()[['DEM']].iloc[0], senateResults.quantile([0.1])[['DEM']].iloc[0][0], senateResults.quantile([0.9])[['DEM']].iloc[0][0]
    repExpSeats, rep10thSeats, rep90thSeats = senateResults.mean()[['REP']].iloc[0], senateResults.quantile([0.1])[['REP']].iloc[0][0], senateResults.quantile([0.9])[['REP']].iloc[0][0]
    
    probabilityDemControl = senateResultsTuples[senateResultsTuples.Democrat > 50].probability.sum()
    probabilityRepControl = senateResultsTuples[senateResultsTuples.Republican >= 50].probability.sum()
    
    winsList = []
    for i,row in simulationsDataFrame.iterrows():
        results = list(row[[x for x in simulationsDataFrame.columns if x not in ['State', 'Senator', 'candidate_party']]])
        demWins = results.count('DEM') / len(results) * 100
        repWins = results.count('REP') / len(results) * 100
        winsList.append([demWins, repWins])
        
    stateWinningProbability = pd.concat([simulationsDataFrame[['State', 'Senator', 'candidate_party']], pd.DataFrame(winsList, columns = ['DEM Win', 'REP Win'])], axis = 1)

    return demProbabilities, repProbabilities, demExpSeats, dem10thSeats, dem90thSeats, repExpSeats, rep10thSeats, rep90thSeats, probabilityDemControl, probabilityRepControl, stateWinningProbability

def runModelTimeSeries(senatedf, senatedfAll, pollratingsDict, pollratingsDictBias, pollratingsDictErro, normalPolls = True, nSimulations = 100, nDaysBack = 30):
    results = []
    for i in range(0,nDaysBack):
        from_date = max(senatedf['end_date']) - datetime.timedelta(i)
        print("Running Model as of {0}".format(from_date))
        senateResults, simulationsDataFrame = simulateSenate(senatedf, senatedfAll, pollratingsDict, pollratingsDictBias, pollratingsDictErro, nSimulations = 100)
        _, _, demExpSeats, dem10thSeats, dem90thSeats, repExpSeats, rep10thSeats, rep90thSeats, probabilityDemControl, probabilityRepControl, _ = createResults(senateResults, simulationsDataFrame)
        results.append([from_date, demExpSeats, dem10thSeats, dem90thSeats, repExpSeats, rep10thSeats, rep90thSeats, probabilityDemControl, probabilityRepControl])
    
    ModelTimeSeries = pd.DataFrame(results, columns = ['Modeldate', 'demExpSeats', 'dem10thSeats', 'dem90thSeats', 'repExpSeats', 'rep10thSeats', 'rep90thSeats', 'probabilityDemControl', 'probabilityRepControl'])
    return ModelTimeSeries


senateResults, simulationsDataFrame = simulateSenate(senatedf, senatedfAll, pollratingsDict, pollratingsDictBias, pollratingsDictErro, normalPolls = True, nSimulations = 10000)

demProbabilities, repProbabilities, demExpSeats, dem10thSeats, dem90thSeats, repExpSeats, rep10thSeats, rep90thSeats, probabilityDemControl, probabilityRepControl, stateWinningProbability = createResults(senateResults, simulationsDataFrame)

ModelTimeSeries = runModelTimeSeries(senatedf, senatedfAll, pollratingsDict, pollratingsDictBias, pollratingsDictErro, nSimulations = 1000, nDaysBack = 60)

# ------------------------------- Write Charts ------------------------------- #

lastUpdated = SenateForecastCharts.lastUpdated.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M%p"))

demWinPercentage = SenateForecastCharts.demWinPct.format(probabilityDemControl)
repWinPercentage = SenateForecastCharts.repWinPct.format(probabilityRepControl)

demExpectedSeats = SenateForecastCharts.demMeanSeats.format(demExpSeats)
repExpectedSeats = SenateForecastCharts.repMeanSeats.format(repExpSeats)

dem10thSeats, dem90thSeats = SenateForecastCharts.demNthSeats.format(dem10thSeats), SenateForecastCharts.demNthSeats.format(dem90thSeats)
rep10thSeats, rep90thSeats = SenateForecastCharts.repNthSeats.format(rep10thSeats), SenateForecastCharts.repNthSeats.format(rep90thSeats)

demHistogram     = SenateForecastCharts.histogramChartTop + SenateForecastCharts.histogramChartBottom_.format('DemHistogram', [str(k) for k in demProbabilities.keys()], [v * 100 for v in demProbabilities.values()], '#3F52B9')
repHistogram     = SenateForecastCharts.histogramChartTop + SenateForecastCharts.histogramChartBottom_.format('RepHistogram', [str(k) for k in repProbabilities.keys()], [v * 100 for v in repProbabilities.values()], '#DE3947')

demTimSeriesProb = [[int(x * 1000),y] for x,y in zip((ModelTimeSeries['Modeldate'][8:] - datetime.datetime(1970,1,1)).dt.total_seconds(),ModelTimeSeries['probabilityDemControl'].rolling(7).mean()[8:])][::-1]
repTimSeriesProb = [[int(x * 1000),y] for x,y in zip((ModelTimeSeries['Modeldate'][8:] - datetime.datetime(1970,1,1)).dt.total_seconds(),ModelTimeSeries['probabilityRepControl'].rolling(7).mean()[8:])][::-1]

lineChartDataProbControl = SenateForecastCharts.lineSeriesData.format('Democrats', demTimSeriesProb, 'Republicans', repTimSeriesProb)
senateProbControlChart   = SenateForecastCharts.lineChartTop + SenateForecastCharts.lineChartBottom_.format('probabilityControl', '#FFFFFF', lineChartDataProbControl, 'Probability of Winning Senate', 100, 'Date.UTC({0}, {1}, {2})'.format(min(ModelTimeSeries['Modeldate'] + datetime.timedelta(8)).year, min(ModelTimeSeries['Modeldate'] + datetime.timedelta(8)).month - 1, min(ModelTimeSeries['Modeldate'] + datetime.timedelta(8)).day))

fileNames   = ['lastUpdated', 'demWinPercentage', 'repWinPercentage', 'demHistogram', 'repHistogram', 'demExpectedSeats', 'repExpectedSeats', 'dem10thSeats', 'dem90thSeat', 'rep10thSeats', 'rep90thSeats', 'lineChartDataProbControl']
htmlStrings = [lastUpdated, demWinPercentage, repWinPercentage, demHistogram, repHistogram, demExpectedSeats, repExpectedSeats, dem10thSeats, dem90thSeats, rep10thSeats, rep90thSeats, senateProbControlChart]

#write to HTML Files
for file, stringChart in zip(fileNames, htmlStrings):
    with open(file + '.html', "w") as text_file:
        text_file.write(stringChart)



