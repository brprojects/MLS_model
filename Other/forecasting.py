#!/usr/bin/env python3
'''
Same as forecasting2.py but for the basic_model_scipy.py parameters
'''
import pandas as pd
import numpy as np

# Load model parameters
parameters = np.load('../Data/parameters.npy', allow_pickle=True)
gamma = parameters[0]
eta = parameters[1]
alpha = parameters[2:23]
beta = parameters[23:]
print(gamma)
print(eta)
print(alpha)
print(beta)

# Import data
df = pd.read_csv('../Data/data.csv')

# Remove data before 06/12/2015 and after 23/10/2016
df.Date = pd.to_datetime(df.Date, dayfirst=True)
df = df.drop(df[(df.Date < '2015-12-07') | (df.Date > '2016-10-23')].index)

# 2016 fixtures
fixtures = df[["Date", "Time", "Home", "Away"]]
fixtures = fixtures.reset_index(drop=True)

# Add two columns to give each team an index from 0:19 (Chivas USA ceased operation in 2014)
teams = ['Chicago Fire', 'Columbus Crew',
        'DC United', 'CF Montreal',
        'New England Revolution', 'New York Red Bulls',
        'New York City', 'Orlando City',
        'Philadelphia Union', 'Toronto FC',
        'Colorado Rapids', 'FC Dallas',
        'Los Angeles Galaxy', 'Portland Timbers',
        'Real Salt Lake', 'San Jose Earthquakes',
        'Seattle Sounders', 'Vancouver Whitecaps',
        'Houston Dynamo', 'Sporting Kansas City']

teams_dict = {}
for num, i in enumerate(teams):
    teams_dict[i] = num

fixtures['home_team'] = fixtures['Home'].map(teams_dict)
fixtures['away_team'] = fixtures['Away'].map(teams_dict)

# Add predicted home and away goals columns
fixtures['predicted_home_goals'] = np.exp(gamma + eta / 2 + alpha[fixtures.home_team] + beta[fixtures.away_team])
fixtures['predicted_away_goals'] = np.exp(gamma - eta / 2 + alpha[fixtures.away_team] + beta[fixtures.home_team])
fixtures = fixtures[["Date", "Time", "Home", "Away", "predicted_home_goals", "predicted_away_goals"]]

# Probabilty of home and away wins
def win_probability(expected_team1_goals, expected_team2_goals):
    sum = 0
    for i in range(10):
        sum1 = 0
        for j in range(i + 1, 10):
            sum1 += expected_team1_goals ** j * np.exp(-expected_team1_goals) / np.math.factorial(j)
        sum += sum1 * (expected_team2_goals ** i * np.exp(-expected_team2_goals) / np.math.factorial(i))
    return sum

fixtures['expected_home_win'] = win_probability(fixtures.predicted_home_goals, fixtures.predicted_away_goals)
fixtures['expected_away_win'] = win_probability(fixtures.predicted_away_goals, fixtures.predicted_home_goals)

# Probability of draw
def draw_probability(expected_team1_goals, expected_team2_goals):
    sum = 0
    for i in range(10):
        sum1 = expected_team1_goals ** i * np.exp(-expected_team1_goals) / np.math.factorial(i)
        sum += sum1 * (expected_team2_goals ** i * np.exp(-expected_team2_goals) / np.math.factorial(i))
    return sum

fixtures['expected_draw'] = draw_probability(fixtures.predicted_home_goals, fixtures.predicted_away_goals)

# Save data
fixtures.to_csv('data_mls_my_predictions.csv')
