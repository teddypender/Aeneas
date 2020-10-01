#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 07:36:24 2020

@author: theodorepender
"""
import pandas as pd
import numpy as np
from scipy.stats import beta, binom, norm, skewnorm
import datetime
from dateutil import parser
# import scipy.stats as stats
# import SenateForecastCharts
import matplotlib.pyplot as plt
import PresidentialCharts
import collections

fivethirtyeightzip   = 'https://projects.fivethirtyeight.com/polls-page/president_polls.csv'
pollsterRatings      = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/pollster-ratings.csv'
senateMakeupurl      = 'https://en.wikipedia.org/wiki/List_of_current_United_States_senators'
presedentialStateurl = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/polls/pres_pollaverages_1968-2016.csv'

senateBreakoutFull = pd.read_html(senateMakeupurl)[4][['State', 'Senator', 'Party.1', 'Term up']]

pollsterRatingsdf   = pd.read_csv(pollsterRatings)
pollratingsDict     = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], pollsterRatingsdf['Mean-Reverted Advanced Plus Minus'])}
pollratingsDictBias = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], [x if type(x) == str else '0 0' for x in pollsterRatingsdf['Bias']])}
pollratingsDictErro = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], pollsterRatingsdf['Simple Expected Error'])}
cycleRating         = {2016 : 1, 2012 : 2, 2008 : 3, 2004 : 4, 2000 : 5}
stateCorrection     = {'Maine CD-1' : 'ME-1', 'Maine CD-2' : 'ME-2', 'Nebraska CD-1' : 'NE-1', 'Nebraska CD-2' : 'NE-2', 'Nebraska CD-3' : 'NE-3'}

presidentHistory  = pd.read_csv(presedentialStateurl)
presidentHistory  = presidentHistory[presidentHistory['cycle'].isin([2016, 2012, 2008, 2004, 2000])][['timestamp', 'cycle', 'state', 'candidate_name', 'pct_estimate']].rename({'pct_estimate' : 'pct'}, axis = 1)
# presidentHistory  = presidentHistory[['timestamp', 'cycle', 'state', 'candidate_name', 'pct_estimate']].rename({'pct_estimate' : 'pct'}, axis = 1)
# senatedfAll['weight']          = [1 for x in range(len(senatedfAll))]
demCandidates = ['Barack Obama', 'Hillary Rodham Clinton', 'Al Gore', 'John Kerry']
repCandidates = ['Donald Trump', 'Mitt Romney', 'John McCain', 'George W. Bush']
presidentHistory['candidate_party'] = ['DEM' if x in demCandidates else 'REP' if x in repCandidates else 'IND' for x in presidentHistory['candidate_name']]
presidentHistory['rate']            = [cycleRating[c] for c in presidentHistory['cycle']]

presidentdf                    = pd.read_csv(fivethirtyeightzip)
presidentdf['number_people']   = (presidentdf['pct'] / 100) * presidentdf['sample_size']
presidentdf['date_difference'] = [(datetime.datetime.today() - parser.parse(x)).days + 1 for x in presidentdf['end_date']]
presidentdf                    = presidentdf[(presidentdf.cycle == 2020) & (presidentdf.date_difference < 365) & (presidentdf.race_id != 7781)]
presidentdf                    = presidentdf[presidentdf.candidate_party.isin(['DEM', 'REP'])]
presidentdf['end_date']        = [parser.parse(x) for x in presidentdf['end_date']]

# Adjust Polls
df           = presidentdf
df['weight'] = [min(df['date_difference']) / x for x in df['date_difference']]
df['bias']   = [pollratingsDictBias[p] if p in pollratingsDictBias.keys() else '0 0' for p in df['pollster_rating_id']]
df['bias']   = [['DEM', float(x.split()[1])] if x.split()[0] == 'D' else ['REP', float(x.split()[1])] if x.split()[0] == 'R' else ['0', '0'] for x in df['bias']]
df['pct']    = [x - y[1] if y[0] == pa else x for x,y,pa in zip(df['pct'], df['bias'], df['candidate_party'])]
df['stdDev'] = [pollratingsDictErro[p] if p in pollratingsDictErro.keys() else np.mean([x for x in pollratingsDictErro.values()]) for p in df['pollster_rating_id']]
   
dfPolls = df
dfPolls['state']  = [x if x not in stateCorrection.keys() else stateCorrection[x] for x in dfPolls['state']]
dflikelihoodMean  = pd.DataFrame(dfPolls.groupby(['candidate_party', 'state']).apply(lambda x : sum(x.pct * x.weight) / x.weight.sum())).rename({0 : 'likelihoodEstimateMean'}, axis = 1).reset_index()
dflikelihoodStDev = pd.DataFrame(dfPolls.groupby(['candidate_party', 'state']).apply(lambda x : x.stdDev.mean())).rename({0 : 'likelihoodEstimateStd'}, axis = 1).reset_index()


electoralCollege = {'Alaska': 3,'Alabama': 9,'Arkansas': 6,'Arizona': 11,
                    'California': 55,'Colorado': 9,'Connecticut': 7,'District of Columbia': 3,'Delaware': 3,
                    'Florida': 29,'Georgia': 16,'Hawaii': 4,'Iowa': 6,'Idaho': 4,'Illinois': 20,
                    'Indiana': 11,'Kansas': 6,'Kentucky': 8,'Louisiana': 8,'Massachusetts': 11,
                    'Maryland': 10,'Maine': 2,'ME-1': 1, 'ME-2' : 1,
                    'Michigan': 16,'Minnesota': 10,'Missouri': 10,
                    'Mississippi': 6,'Montana': 3,'North Carolina': 15,'North Dakota': 3,
                    'Nebraska': 2,'NE-1' : 1, 'NE-2' : 1, 'NE-3' : 1,
                    'New Hampshire': 4,'New Jersey': 14,'New Mexico': 5,
                    'Nevada': 6,'New York': 29,'Ohio': 18,'Oklahoma': 7,'Oregon': 7,
                    'Pennsylvania': 20,'Rhode Island': 4,'South Carolina': 9,'South Dakota': 3,
                    'Tennessee': 11,'Texas': 38,'Utah': 6,'Virginia': 13,'Vermont': 3,
                    'Washington': 12,'Wisconsin': 10,'West Virginia': 5,'Wyoming': 3}

stateList = sorted(presidentHistory.state.unique())

# ---------------------------------- Create Distributions ---------------------------------- #

def stateDistributionWeights(stateList, dfPolls, presidentHistory, dflikelihoodMean, dflikelihoodStDev, model, n_steps):
    listOfDistributions = []
    for k in stateList:
        State = k
        # prior = pd.DataFrame(presidentHistory[presidentHistory.state == State].groupby('candidate_party').apply(lambda x : sum(x.pct * (1 / (x.cycle ** 2)))), columns = ['pct']).reset_index()
        # prior['pct'] = prior['pct'] / prior['pct'].sum() * 100
        factorUp = 0.5
        priorHistory   = presidentHistory[presidentHistory.state == State].groupby('candidate_party').apply(lambda x : sum(x.pct * (1 / (x.rate ** 2))) / sum(1 / (x.rate ** 2))).reset_index()
        priorThisCycle = dfPolls[(dfPolls.state == State) & (dfPolls.date_difference >= 0)].groupby('candidate_party')['pct'].mean().reset_index()
        
        if len(priorThisCycle) < 2:
            prior = priorHistory.rename({0 : 'pct'}, axis = 1)
        else:
            prior = pd.merge(priorThisCycle, priorHistory, on = 'candidate_party').rename({'pct' : 'recent', 0 : 'past'}, axis = 1)
            prior['diff'] = abs(prior['recent'] - prior['past'])
            weights = (prior['diff'] / prior['diff'].sum())
            prior['pct'] = (prior['recent'] * weights) + (prior['past'] * (1-weights)) 
            prior = prior[['candidate_party', 'pct']]
        
        #with a beta prior distribution we have two parameters a and B, a = the number of successes and B is the number of failures
        try:
            demSuccessPrior, demSuccessLikelihood, demSuccessLikelihoodStdev = prior[prior.candidate_party == 'DEM']['pct'].iloc[0], dflikelihoodMean[(dflikelihoodMean.candidate_party == 'DEM') & (dflikelihoodMean.state == State)]['likelihoodEstimateMean'].iloc[0], dflikelihoodStDev[(dflikelihoodStDev.candidate_party == 'DEM') & (dflikelihoodStDev.state == State)]['likelihoodEstimateStd'].iloc[0]
            repSuccessPrior, repSuccessLikelihood, repSuccessLikelihoodStdev = prior[prior.candidate_party == 'REP']['pct'].iloc[0], dflikelihoodMean[(dflikelihoodMean.candidate_party == 'REP') & (dflikelihoodMean.state == State)]['likelihoodEstimateMean'].iloc[0], dflikelihoodStDev[(dflikelihoodStDev.candidate_party == 'REP') & (dflikelihoodStDev.state == State)]['likelihoodEstimateStd'].iloc[0]
        except:
             demSuccessPrior, demSuccessLikelihood, demSuccessLikelihoodStdev = prior[prior.candidate_party == 'DEM']['pct'].iloc[0], prior[prior.candidate_party == 'DEM']['pct'].iloc[0], dflikelihoodStDev[(dflikelihoodStDev.candidate_party == 'DEM')]['likelihoodEstimateStd'].mean()
             repSuccessPrior, repSuccessLikelihood, repSuccessLikelihoodStdev = prior[prior.candidate_party == 'REP']['pct'].iloc[0], prior[prior.candidate_party == 'REP']['pct'].iloc[0], dflikelihoodStDev[(dflikelihoodStDev.candidate_party == 'REP')]['likelihoodEstimateStd'].mean()

        # totalTrials = prior[prior.candidate_party.isin(['DEM', 'REP'])]['pct'].sum()            
        lst         = np.linspace(0, 1, n_steps)
        
        if model == 'Bayesian':
            demPrior           = [beta(demSuccessPrior, repSuccessPrior).pdf(i) for i in lst]
            demLikelihood      = [norm(loc = demSuccessLikelihood / 100, scale =  demSuccessLikelihoodStdev / 100).pdf(i) for i in lst]
            demLikelihoodShift = [factorUp * (max(demLikelihood) - x) for x in demLikelihood]    
            demLikelihood2     = [x + y for x,y in zip(demLikelihood, demLikelihoodShift)]
            approachFactor     = [norm(loc = demSuccessLikelihood / 100, scale =  demSuccessLikelihoodStdev / 100).pdf(demSuccessLikelihood / 100) * abs((demSuccessLikelihood / 100) - x) for x in lst]
            approachFactor     = [1 - (x / max(approachFactor)) for x in approachFactor]
            demLikelihood      = [x * (y ** 2) for x,y in zip(demLikelihood2, approachFactor)]
            demPosterior       = np.multiply(demPrior, demLikelihood)
            
            repPrior           = [beta(repSuccessPrior, demSuccessPrior).pdf(i) for i in lst]
            repLikelihood      = [norm(loc = repSuccessLikelihood / 100, scale =  repSuccessLikelihoodStdev / 100).pdf(i) for i in lst]
            repLikelihoodShift = [factorUp * (max(repLikelihood) - x) for x in repLikelihood]    
            repLikelihood2     = [x + y for x,y in zip(repLikelihood, repLikelihoodShift)]
            approachFactor     = [norm(loc = repSuccessLikelihood / 100, scale =  repSuccessLikelihoodStdev / 100).pdf(repSuccessLikelihood / 100) * abs((repSuccessLikelihood / 100) - x) for x in lst]
            approachFactor     = [1 - (x / max(approachFactor)) for x in approachFactor]
            repLikelihood      = [x * (y ** 2) for x,y in zip(repLikelihood2, approachFactor)]
            repPosterior       = np.multiply(repPrior, repLikelihood)
            
            # plt.plot(demPosterior, color = 'red')
            # plt.plot(repPosterior, color = 'blue')
            
            
            listOfDistributions.append([State, demPosterior, repPosterior])
        else:
            demLikelihood = [norm(loc = demSuccessLikelihood / 100, scale =  demSuccessLikelihoodStdev / 100).pdf(i) for i in lst] #[binom(1000,i).pmf(k = int(demSuccessLikelihood * 10)) for i in lst]
            repLikelihood = [norm(loc = repSuccessLikelihood / 100, scale =  repSuccessLikelihoodStdev / 100).pdf(i) for i in lst] #[binom(1000,i).pmf(k = int(repSuccessLikelihood * 10)) for i in lst]
            
            listOfDistributions.append([State, demLikelihood, repLikelihood])
            
        demList, repList = np.random.choice(lst, 100000, p=demPosterior/sum(demPosterior)), np.random.choice(lst, 100000, p=repPosterior/sum(repPosterior))
        demVotesMean, demVotesLower, demVotes, demVotesUpper = np.mean(demList), pd.Series(demList).quantile(0.25) * 100,  pd.Series(demList).quantile(0.50) * 100,  pd.Series(demList).quantile(0.75) * 100
        repVotesMean, repVotesLower, repVotes, repVotesUpper = np.mean(repList), pd.Series(repList).quantile(0.25) * 100,  pd.Series(repList).quantile(0.50) * 100,  pd.Series(repList).quantile(0.75) * 100
        demWinList = [1 if x > y else 0 for x,y in zip(np.random.choice(demList, 100000), np.random.choice(repList, 100000))]
        demWinProbability = sum(demWinList) / len(demWinList)
        repWinProbability = 1 - demWinProbability
        
        print('State: {2} \nDem Win = {0} \nRep Win = {1}'.format(demWinProbability, repWinProbability, k))
        print('Democrat Vote Share,',demVotesMean / (demVotesMean + repVotesMean) * 100)
        print('Republican Vote Share,',repVotesMean / (demVotesMean + repVotesMean) * 100)
        print(" ")
        
    
    weightsdf = pd.DataFrame(listOfDistributions, columns = ['State', 'DEMPos', 'REPPos'])
    
    return weightsdf
        

# ---------------------------------- Run Simulations ---------------------------------- #
def electoralCollegeFn(stateWinningProbdf):
    demElectoralCollege = 0
    repElectoralCollege = 0
    
    for i in range(len(stateWinningProbdf)):
        state = stateWinningProbdf['State'].iloc[i]
        dem   = stateWinningProbdf['DemWin'].iloc[i]
        rep   = stateWinningProbdf['RepWin'].iloc[i]
        if dem > rep:
            demElectoralCollege += electoralCollege[state]
        else:
            repElectoralCollege += electoralCollege[state]
            
    print(" ")
    print('Democrats win {0} Electoral College Votes'.format(demElectoralCollege))
    print('Republicans win {0} Electoral College Votes'.format(repElectoralCollege))
        
    return demElectoralCollege, repElectoralCollege

def simulateElection(weightsdf, stateList, runs, n_steps, electoralCollege):
    stateWinningProbabilities = []
    lst = np.linspace(0, 1, n_steps)

    for k in [x for x in stateList if x in electoralCollege.keys()]:
        # print(k)
        demPosterior, repPosterior = weightsdf[weightsdf.State == k]['DEMPos'].iloc[0], weightsdf[weightsdf.State == k]['REPPos'].iloc[0]
        
        plt.plot(demPosterior)
        plt.plot(repPosterior)
        
        demList, repList = np.random.choice(lst, runs, p=demPosterior/sum(demPosterior)), np.random.choice(lst, runs, p=repPosterior/sum(repPosterior))
        demVotesMean, demVotesLower, demVotes, demVotesUpper, demVotesStd = np.mean(demList) * 100, pd.Series(demList).quantile(0.25) * 100,  pd.Series(demList).quantile(0.50) * 100,  pd.Series(demList).quantile(0.75) * 100, np.std(demList) * 100
        repVotesMean, repVotesLower, repVotes, repVotesUpper, repVotesStd = np.mean(repList) * 100, pd.Series(repList).quantile(0.25) * 100,  pd.Series(repList).quantile(0.50) * 100,  pd.Series(repList).quantile(0.75) * 100, np.std(repList) * 100
        
        demWinList = [1 if x > y else 0 for x,y in zip(np.random.choice(demList, 10000), np.random.choice(repList, 10000))]
        demWinProbability = sum(demWinList) / len(demWinList)
        repWinProbability = 1 - demWinProbability
        
        demVoteShare = demVotesMean / (demVotesMean + repVotesMean) * 100
        repVoteShare = repVotesMean / (demVotesMean + repVotesMean) * 100
        
        # plt.plot(demPosterior, color = 'blue')
        # plt.plot(repPosterior, color = 'red')
        
        stateWinningProbabilities.append([k, demWinProbability, demVotesMean, demVotesLower, demVotes, demVotesUpper, repWinProbability, repVotesMean, repVotesLower, repVotes, repVotesUpper, demVoteShare, repVoteShare, demVotesStd, repVotesStd])
        
    stateWinningProbdf = pd.DataFrame(stateWinningProbabilities, columns = ['State', 'DemWin', 'demVotesMean', 'demVotesLower', 'demVotes', 'demVotesUpper', 'RepWin', 'repVotesMean', 'repVotesLower', 'repVotes', 'repVotesUpper', 'demVoteShare', 'repVoteShare', 'demVotesStd', 'repVotesStd'])
    
    return stateWinningProbdf[['State', 'DemWin', 'RepWin', 'demVoteShare', 'repVoteShare', 'demVotesMean', 'repVotesMean', 'demVotesStd', 'repVotesStd']]

def simulateElectoralCollege(stateWinningProbdf, presidentHistory, weightsdf, stateList, nSimulations, n_steps, electoralCollege):
    
    stateWinsSim, demWinProbSim = [], []

    for i in range(len(stateWinningProbdf)):
        state        = stateWinningProbdf['State'].iloc[i]
        dem, dstd    = stateWinningProbdf['demVotesMean'].iloc[i], stateWinningProbdf['demVotesStd'].iloc[i]
        rep, rstd    = stateWinningProbdf['repVotesMean'].iloc[i], stateWinningProbdf['repVotesStd'].iloc[i]
        
        # priorHistory = presidentHistory[presidentHistory.state == state].groupby('candidate_party').apply(lambda x : sum(x.pct * (1 / (x.rate ** 2))) / sum(1 / (x.rate ** 2))).reset_index().rename({0 : 'pct'}, axis = 1)
        priorHistory = presidentHistory.groupby('candidate_party').apply(lambda x : sum(x.pct * (1 / (x.rate ** 2))) / sum(1 / (x.rate ** 2))).reset_index().rename({0 : 'pct'}, axis = 1)
        demHistory   = priorHistory[priorHistory.candidate_party == 'DEM']['pct'].iloc[0]
        repHistory   = priorHistory[priorHistory.candidate_party == 'REP']['pct'].iloc[0]
        
        demSkew = 0 #((dem * 1) - (demHistory * 1))
        repSkew = 0 if dem > rep else 1 #((rep * 1) - (repHistory * 1)) 
        
        # demscaled  = dem / (dem + rep) * 100
        # repscaled  = rep / (dem + rep) * 100
        # demHscaled = demHistory / (demHistory + repHistory) * 100
        # repHscaled = repHistory / (demHistory + repHistory) * 100
        
        # demSkew = (demscaled * 1.0) - (demHscaled * 1.0) #florida 1.07
        # repSkew = (repscaled * 1.0) - (repHscaled * 1.0)
    
        demVoteSim = skewnorm.rvs(demSkew, loc = dem, scale = dstd, size = nSimulations) + np.random.normal(0, 5, nSimulations)
        repVoteSim = skewnorm.rvs(repSkew, loc = rep, scale = rstd, size = nSimulations) + np.random.normal(0, 5, nSimulations)
        
        # plt.figure(figsize = (10,6))
        # plt.title(state)
        # sns.distplot(demVoteSim)
        # sns.distplot(repVoteSim, color = 'red')
        
        demWinList = [1 if x > y else 0 for x,y in zip(np.random.choice(demVoteSim, 10000), np.random.choice(repVoteSim, 10000))]
        print('Dem Win: {0}'.format(state), sum(demWinList) / len(demWinList) * 100)
        stateWinsSim.append(demWinList)
        demWinProbSim.append([state, sum(demWinList) / len(demWinList) * 100])
        
    simulationsdf = pd.DataFrame(stateWinsSim, index = stateWinningProbdf['State'])
    demWinProb = pd.DataFrame(demWinProbSim, columns = ['State', 'DemWin'])

    electoralCollegeOutcomes = []
    for col in simulationsdf.columns:
        demElectoralCollege = 0
        repElectoralCollege = 0
        series = simulationsdf[col]
        for n,j in enumerate(series):
            state = series.index[n]
            if j == 1:
                demElectoralCollege += electoralCollege[state]
            else:
                repElectoralCollege += electoralCollege[state]
        electoralCollegeOutcomes.append([demElectoralCollege, repElectoralCollege])
                

    return electoralCollegeOutcomes, simulationsdf, demWinProb.sort_values('DemWin')

def tippingPointStates(electoralCollegeOutcomes, simulationsdf, stateWinningProbdf):

    electoralDF = pd.DataFrame(electoralCollegeOutcomes, columns = ['DEM', 'REP']).T
    stateTippers = []
    for col in simulationsdf.columns:
        series = simulationsdf[col]
        demEC, repEC = electoralDF[col].iloc[0], electoralDF[col].iloc[1]
        for n,j in enumerate(series):
            state = series.index[n]
            ec = max(demEC, repEC)
            if ec - electoralCollege[state] < 270:
                stateTippers.append(state)
                
    dfCounts = pd.DataFrame(pd.Series(stateTippers).value_counts()).rename({0 : 'Count'}, axis = 1)
    dfCounts['relativeOutcome'] = [x * min(stateWinningProbdf[stateWinningProbdf.State == y]['DemWin'].iloc[0], (100 - stateWinningProbdf[stateWinningProbdf.State == y]['DemWin'].iloc[0])) for x,y in zip(dfCounts['Count'], dfCounts.index)]
    # dfCounts['relativeOutcome'] = [x * min(stateWinningProbdf[stateWinningProbdf.State == y]['DemWin'].iloc[0], (stateWinningProbdf[stateWinningProbdf.State == y]['RepWin'].iloc[0])) for x,y in zip(dfCounts['Count'], dfCounts.index)]
    dfCounts['probabilityTip']  = dfCounts['relativeOutcome'] / dfCounts['relativeOutcome'].sum() * 100
    
    dfCounts = dfCounts.sort_values('probabilityTip', ascending = False)
    
    return dfCounts


# ---------------------------------- Main ---------------------------------- #
n_steps      = 100
nSimulations = 10000
runs         = 10000
model        = 'Bayesian'

weightsdf          = stateDistributionWeights(stateList, dfPolls, presidentHistory, dflikelihoodMean, dflikelihoodStDev, model, n_steps)
stateWinningProbdf = simulateElection(weightsdf, stateList, runs, n_steps, electoralCollege)

electoralCollegeOutcomes, simulationsdf,demWinProb        = simulateElectoralCollege(stateWinningProbdf, presidentHistory, weightsdf, stateList, nSimulations, n_steps, electoralCollege)
demLowerBoundEC, demMedianEC, demUpperBoundEC, demMeanEC  = pd.Series([x[0] for x in electoralCollegeOutcomes]).quantile(0.10), pd.Series([x[0] for x in electoralCollegeOutcomes]).quantile(0.50), pd.Series([x[0] for x in electoralCollegeOutcomes]).quantile(0.90), pd.Series([x[0] for x in electoralCollegeOutcomes]).mean()
repLowerBoundEC, repMedianEC, repUpperBoundEC, repMeanEC  = pd.Series([x[1] for x in electoralCollegeOutcomes]).quantile(0.10), pd.Series([x[1] for x in electoralCollegeOutcomes]).quantile(0.50), pd.Series([x[1] for x in electoralCollegeOutcomes]).quantile(0.90), pd.Series([x[1] for x in electoralCollegeOutcomes]).mean()

demChanceOfWinning = sum([1 if x[0] >= 270 else 0 for x in electoralCollegeOutcomes]) / len(electoralCollegeOutcomes)
repChanceOfWinning = sum([1 if x[1] >= 270 else 0 for x in electoralCollegeOutcomes]) / len(electoralCollegeOutcomes)

tippingPointStatesdf  = tippingPointStates(electoralCollegeOutcomes, simulationsdf, demWinProb)
words                 = [[x,y] if len(x.split()) == 1 else [x.split()[0] + ' ' + x.split()[1], y] for x,y in zip(tippingPointStatesdf.index[:10], tippingPointStatesdf['probabilityTip'][:10])]
wordCorpus            = [[x[0] for a in range(int(x[1]))] for x in words]
wordCorpus            = [a for b in wordCorpus for a in b]
wordCorpusL           = [wordCorpus[x] + '-' for x in range(len(wordCorpus))]
wordsMap              = str({k : collections.Counter(wordCorpus)[k] for k in [x[0] for x in words]})

wordCloudD = ''
for i in wordCorpusL:
    wordCloudD += i
wordCloudD = wordCloudD[:-1]

electoralDF      = pd.DataFrame(electoralCollegeOutcomes, columns = ['DEM', 'REP'])
presDemSort      = sorted(electoralDF['DEM'].unique())
presRepSort      = sorted(electoralDF['REP'].unique())
totalSeats       = [x for x in range(min(min(presRepSort), min(presDemSort)), max(max(presRepSort), max(presDemSort)))]
demProbabilities = {k : len(electoralDF[electoralDF.DEM == k]) / len(electoralDF) for k in totalSeats}
repProbabilities = {k : len(electoralDF[electoralDF.REP == k]) / len(electoralDF) for k in totalSeats}

lastUpdated      = PresidentialCharts.lastUpdated.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M%p"))

demWinPercentage = PresidentialCharts.demWinPct.format(demChanceOfWinning * 100)
repWinPercentage = PresidentialCharts.repWinPct.format(repChanceOfWinning * 100)

demExpectedEC    = PresidentialCharts.demMeanSeats.format(demMedianEC)
repExpectedEC    = PresidentialCharts.repMeanSeats.format(repMedianEC)

dem10thEC, dem90thEC = PresidentialCharts.demNthSeats.format(demLowerBoundEC), PresidentialCharts.demNthSeats.format(demUpperBoundEC)
rep10thEC, rep90thEC = PresidentialCharts.repNthSeats.format(repLowerBoundEC), PresidentialCharts.repNthSeats.format(repUpperBoundEC)

ChartTest        = PresidentialCharts.wordChart + PresidentialCharts.wordChartData.format(wordCloudD, wordsMap, max([collections.Counter(wordCorpus)[k] for k in [x[0] for x in words]])) + PresidentialCharts.wordChartBottom
demHistogram     = PresidentialCharts.histogramChartTop + PresidentialCharts.histogramChartBottom_.format('DemHistogram', [str(k) for k in demProbabilities.keys()], [v * 100 for v in demProbabilities.values()], '#3F52B9')
repHistogram     = PresidentialCharts.histogramChartTop + PresidentialCharts.histogramChartBottom_.format('RepHistogram', [str(k) for k in repProbabilities.keys()], [v * 100 for v in repProbabilities.values()], '#DE3947')


tippingPointStatesdfTable = tippingPointStatesdf.reset_index().rename({'index' : 'State', 'probabilityTip' : 'Tipping Point Probability'}, axis = 1).set_index(['State'])[['Tipping Point Probability']].iloc[0:11]

tippingPointStatesdfTable = tippingPointStatesdfTable.to_html(index = True)
firstEdit = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>"""
firstReplace = """<table cellpadding="0" cellspacing="1" border="0" class="heat-map" id="heat-map-3">
        <thead>
          <tr>
            <th class="first">"""
            
secondEdit = """</th>
      <th>Tipping Point Probability"""
secondReplace = """</th>
            <th class="last">Tipping Point Probability"""
            
thirdEdit = """<thead>
          <tr>
            <th class="first"></th>
            <th class="last">Tipping Point Probability</th>
    </tr>
    <tr>
      <th>State</th>
      <th></th>
    </tr>"""

thirdReplace = """<thead>
          <tr>
            <th class="first">State</th>
            <th class="last">Tipping Point Probability (%)</th>
    </tr>"""

tippingPointStatesdfTable = tippingPointStatesdfTable.replace(firstEdit, firstReplace)
tippingPointStatesdfTable = tippingPointStatesdfTable.replace(secondEdit, secondReplace)
tippingPointStatesdfTable = tippingPointStatesdfTable.replace(thirdEdit, thirdReplace)


fileNames   = ['lastUpdated', 'wordCloud', 'demHistogram', 'repHistogram', 'demExpectedEC', 'repExpectedEC', 'demWinPercentage', 'repWinPercentage', 'dem10thEC', 'dem90thEC', 'rep10thEC', 'rep90thEC']
htmlStrings = [lastUpdated, ChartTest, demHistogram, repHistogram, demExpectedEC, repExpectedEC, demWinPercentage, repWinPercentage, dem10thEC, dem90thEC, rep10thEC, rep90thEC]

#write to HTML Files
for file, stringChart in zip(fileNames, htmlStrings):
    with open(file + '.html', "w") as text_file:
        text_file.write(stringChart)





