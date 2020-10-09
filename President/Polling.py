#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 20:02:28 2020

@author: theodorepender
"""
import pandas as pd
import numpy as np
from scipy.stats import beta, binom, norm, skewnorm
import scipy.stats as st
import datetime
from dateutil import parser
import seaborn as sns
import matplotlib.pyplot as plt


fivethirtyeightPollsURL           = 'https://projects.fivethirtyeight.com/polls-page/president_polls.csv'
pollsterRatingsURL                = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/pollster-ratings.csv'
fivethirtyeightHistoricalPollsURL = 'https://raw.githubusercontent.com/fivethirtyeight/data/master/polls/pres_pollaverages_1968-2016.csv'
# cycle, state, pollster_id, pollster, fte_grade, sample_size, population, start_date, end_date, election_date, answer, candidate_party, pct
class Poll:
    def __init__(self, row):
        self.cycle           = row.cycle
        self.state           = row.state
        self.pollster_id     = row.pollster_id
        self.pollster        = row.pollster
        self.fte_grade       = row.fte_grade
        self.sample_size     = row.sample_size
        self.population      = row.population
        self.start_date      = row.start_date
        self.end_date        = row.end_date
        self.election_date   = row.election_date
        self.canswerycle     = row.answer
        self.candidate_party = row.candidate_party
        self.pct             = row.pct
        
    def marginOfError(self, q = 0.975):
        
        """
        The general formula for the margin of error for a sample proportion (if certain conditions are met) is
            
        ME = z * (((p * (1 - p)) / n) ** 0.5),

        where p is the sample proportion, n is the sample size, and z is the appropriate z*-value for your desired level of confidence.
        
        Inputs:
        ----------
            p, float: between 0 and 1, the variable is set to a default of 0.95 and describes the level of confidence you're looking for
                    Python calculates left/lower-tail probabilities by default. If you want to determine the density points where
                    95% of the distribution is included, you have to take another approach so you must change the interval by half the distances 
                    because of the two tails. Therefore 0.95 becomes 0.975.
                    
        Output:
        ---------
            me, float: between 0 and 1. For example, a poll might state that there is a 95% confidence interval of 0.488 and 0.526. 
            That means if the poll is repeated using the same techniques, 95% of the time the true population parameter (parameter vs. statistic)
            will fall within the interval estimates (i.e. between 0.488 and 0.526) 95% of the time.
        """
            
        z             = st.norm.ppf(q)
        n             = self.sample_size
        p             = self.pct / 100

        me            = z * (((p * (1 - p)) / n) ** 0.5)
        
        return me
    
    def standardError(self):
        
        """
        The main fact that polling is based on is: there's a 95% chance in a random sample of size n that p^ will be in the range p ± 2sigma.
        I.e., that p and p ^ are within 2sigma of each other, and thus, using s to estimate sigma, we expect there to be a 95% chance that p is in
        the range p^ ± 2s, no matter how big N is (as long as N is not too small). We call ±2s the "margin of error".
        
        Inputs:
        --------
        
        Outputs:
        --------
            se, float: between 0 and 1. An estimate for the standard deviation of the poll.
        
        """
        
        p = self.pct / 100
        n = self.sample_size
        
        se = (p * (1-p) / n) ** 0.5
        
        return se
    
    def mean(self):
        
        return self.pct
    
    def variance(self):
        
        n = self.sample_size
        p = self.pct / 100
        
        var = n * p * (1 - p)
        
        return var
    
    def standardDeviation(self, t = 'pct'):
        
        return self.variance() ** 0.5
    
    def confidenceRange(self, q = 0.95):
        """
        

        Parameters
        ----------
        q : TYPE, optional
            DESCRIPTION. The default is 0.95. which deescribes the confidence level of a one tailed distribution. So q = 0.95 means 90% confidence interval,
            if q = 0.975 then that is the 95% confidence limit (becasue 1 - ((1-q) * 2) = confidence interval)

        Returns
        -------
        None.

        """
        
        stdDev   = self.standardDeviation()
        m        = self.mean() / 100 * self.sample_size
        noStdDev = st.norm.ppf(q)
        
        lowerBound = m - (stdDev * noStdDev)
        upperBound = m + (stdDev * noStdDev)
        
        return (lowerBound / self.sample_size, upperBound /  self.sample_size)
    
    def normalDistribution(self, sampleSize = 100000):
        """
        Inputs
        -------
        n = number of trials
        k = number of successes
        p = probability of success
        

        Returns
        -------
        str
            DESCRIPTION.

        """
        
        return np.random.normal(loc = self.mean() / 100, scale = self.standardDeviation() / self.sample_size, size = sampleSize)
    
    def normalDistpdf(self):
        lst = np.linspace(0, 1, 1000)
        normalpdf = [st.norm.pdf(x, loc = self.mean() / 100, scale = self.standardDeviation() / self.sample_size) for x in lst]
        
        return normalpdf

def statePoll(state, presidentdf, date = datetime.datetime(2020, 11, 4)):
    
    statePollingDEM    = presidentdf[(presidentdf.state == state) & (presidentdf.candidate_party == 'DEM') & (presidentdf.end_date <= date)]
    statePollObjDEM    = [Poll(i) for i in [statePollingDEM.iloc[n] for n in range(len(statePollingDEM))]] 
    
    statePollingREP    = presidentdf[(presidentdf.state == state) & (presidentdf.candidate_party == 'REP') & (presidentdf.end_date <= date)]
    statePollObjREP    = [Poll(i) for i in [statePollingREP.iloc[n] for n in range(len(statePollingREP))]]
    
    dfPollsDEM = pd.DataFrame([poll.normalDistpdf() for poll in statePollObjDEM], index = [poll.end_date for poll in statePollObjDEM]).sort_index(ascending = True)
    dfPollsREP = pd.DataFrame([poll.normalDistpdf() for poll in statePollObjREP], index = [poll.end_date for poll in statePollObjREP]).sort_index(ascending = True)

    return dfPollsDEM, dfPollsREP, statePollObjDEM, statePollObjDEM, statePollObjREP

def rollingTimeSeries(statePollObjDEM, statePollObjREP, q = 0.9, w = 21):
    
    repMean  = pd.Series([poll.mean() for poll in statePollObjREP[::-1]]).rolling(w).mean()
    repLower = pd.Series([poll.confidenceRange(q)[0]*100 for poll in statePollObjREP[::-1]]).rolling(w).mean()
    repUpper = pd.Series([poll.confidenceRange(q)[1]*100 for poll in statePollObjREP[::-1]]).rolling(w).mean()
    demMean  = pd.Series([poll.mean() for poll in statePollObjDEM[::-1]]).rolling(w).mean()
    demLower = pd.Series([poll.confidenceRange(q)[0]*100 for poll in statePollObjDEM[::-1]]).rolling(w).mean()
    demUpper = pd.Series([poll.confidenceRange(q)[1]*100 for poll in statePollObjDEM[::-1]]).rolling(w).mean()
    
    return repMean, repLower, repUpper, demMean, demLower, demUpper
    
def simulateElection(dfPollsDEM, dfPollsREP, state):
    demWeights = dfPollsDEM.mean() / dfPollsDEM.mean().sum()
    repWeights = dfPollsREP.mean() / dfPollsREP.mean().sum()
    demSimulation = np.random.choice(np.linspace(0, 1, 1000), p = demWeights, size = 10000)    
    repSimulation = np.random.choice(np.linspace(0, 1, 1000), p = repWeights, size = 10000)   
    
    demVotesMean, demVotes10, demVotes90 = np.mean(demSimulation), np.quantile(demSimulation, 0.1), np.quantile(demSimulation, 0.9)
    repVotesMean, repVotes10, repVotes90 = np.mean(repSimulation), np.quantile(repSimulation, 0.1), np.quantile(repSimulation, 0.9)
    
    demWinList = [1 if x > y else 0 for x,y in zip(demSimulation, repSimulation)]
    demWin = sum(demWinList) / len(demWinList) * 100
    print('Probability Democrats Win {0} = {1}%'.format(state, demWin))
    
    return demWin, 100 - demWin, demVotesMean, demVotes10, demVotes90, repVotesMean, repVotes10, repVotes90

if __name__ == '__main__': 
    print('main')

    

    # ----------- Import Data ----------- #
    
    
    pollsterRatingsdf   = pd.read_csv(pollsterRatingsURL)
    pollratingsDict     = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], pollsterRatingsdf['Mean-Reverted Advanced Plus Minus'])}
    pollratingsDictBias = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], [x if type(x) == str else '0 0' for x in pollsterRatingsdf['Bias']])}
    pollratingsDictErro = {k : v for k,v in zip(pollsterRatingsdf['Pollster Rating ID'], pollsterRatingsdf['Simple Expected Error'])}
    stateCorrection     = {'Maine CD-1' : 'ME-1', 'Maine CD-2' : 'ME-2', 'Nebraska CD-1' : 'NE-1', 'Nebraska CD-2' : 'NE-2', 'Nebraska CD-3' : 'NE-3'}
    
    presidentHistory  = pd.read_csv(fivethirtyeightHistoricalPollsURL)
    presidentHistory  = presidentHistory[presidentHistory['cycle'].isin([2016, 2012, 2008, 2004, 2000])][['timestamp', 'cycle', 'state', 'candidate_name', 'pct_estimate']].rename({'pct_estimate' : 'pct'}, axis = 1)
    demCandidates = ['Barack Obama', 'Hillary Rodham Clinton', 'Al Gore', 'John Kerry']
    repCandidates = ['Donald Trump', 'Mitt Romney', 'John McCain', 'George W. Bush']
    presidentHistory['candidate_party'] = ['DEM' if x in demCandidates else 'REP' if x in repCandidates else 'IND' for x in presidentHistory['candidate_name']]
    
    presidentdf                    = pd.read_csv(fivethirtyeightPollsURL)
    presidentdf['number_people']   = (presidentdf['pct'] / 100) * presidentdf['sample_size']
    presidentdf['date_difference'] = [(datetime.datetime.today() - parser.parse(x)).days + 1 for x in presidentdf['end_date']]
    presidentdf                    = presidentdf[(presidentdf.cycle == 2020) & (presidentdf.date_difference < 365) & (presidentdf.race_id != 7781)]
    presidentdf                    = presidentdf[presidentdf.candidate_party.isin(['DEM', 'REP'])]
    presidentdf['end_date']        = [parser.parse(x) for x in presidentdf['end_date']]
    


    # ----------- Create Poll Class ----------- #
    everythingList = []
    for state in sorted([x for x in presidentdf.state.unique() if type(x) == str]):
    # state = 'Florida'
        dfPollsDEM, dfPollsREP, statePollObjDEM, statePollObjDEM, statePollObjREP = statePoll(state, presidentdf)
        demWin, repWin, demVotesMean, demVotes10, demVotes90, repVotesMean, repVotes10, repVotes90 = simulateElection(dfPollsDEM, dfPollsREP, state)
        everythingList.append([state, demWin, repWin, demVotesMean, demVotes10, demVotes90, repVotesMean, repVotes10, repVotes90])









    

    
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

