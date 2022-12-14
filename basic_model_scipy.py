#!/usr/bin/env python3
'''
This program fits the poisson goal model by MLE of the fitset using
scipy.optimize.minimize

log(lamda) = gamme + eta/2 + alpha[i] + beta[j]
log(mu) = gamme - eta/2 + alpha[i] + beta[j]
'''
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Import data
df = pd.read_csv('./Data/edited_data.csv')

# Add two columns to give each team an index from 0:20
teams = ['Chicago Fire', 'Columbus Crew',
        'DC United', 'CF Montreal',
        'New England Revolution', 'New York Red Bulls',
        'New York City', 'Orlando City',
        'Philadelphia Union', 'Toronto FC',
        'Chivas USA', 'Colorado Rapids',
        'FC Dallas', 'Los Angeles Galaxy',
        'Portland Timbers', 'Real Salt Lake',
        'San Jose Earthquakes', 'Seattle Sounders',
        'Vancouver Whitecaps', 'Houston Dynamo',
        'Sporting Kansas City']

teams_dict = {}
for num, i in enumerate(teams):
    teams_dict[i] = num

df['home_team'] = df['Home'].map(teams_dict)
df['away_team'] = df['Away'].map(teams_dict)


# MLE optimisation for model paramaters
# Function for log-likelihood of home goals
def lik(params):
    gamma = params[0]
    eta = params[1]
    alpha = params[2:23]
    beta = params[23:]
    # print(gamma, eta, alpha, beta)

    L = 0
    for index in range(len(df)):
        lamda = np.exp(gamma + eta / 2 + alpha[df.home_team[index]] + beta[df.away_team[index]])
        x = df.HG[index]
        L += -lamda + np.log(lamda) * x - np.log(np.math.factorial(x))
    print(L)
    return -L

# Funtion for log-likelihood of away goals
def lik2(params):
    gamma = params[0]
    eta = params[1]
    alpha = params[2:23]
    beta = params[23:]
    # print(gamma, eta)

    L = 0
    for index in range(len(df)):
        mu = np.exp(gamma - eta / 2 + alpha[df.away_team[index]] + beta[df.home_team[index]])
        x = df.AG[index]
        L += -mu + np.log(mu) * x - np.log(np.math.factorial(x))

    return -L

# Initialise parameters
initial_guess = [1, 0.5] + 42 * [0]

# Minimize the sum of log-likelihood of home and away goals
result = minimize(lambda y: lik(y) + lik2(y), x0=initial_guess, method='L-BFGS-B')
print(result)
print(result.x)

# Save model parameters
parameters = np.array(result.x)
np.save('./Data/parameters', parameters)
