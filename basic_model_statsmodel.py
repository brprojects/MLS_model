#!/usr/bin/env python3
'''
This program fits the poisson goal model by MLE of the fitset using statsmodels

log(lamda) = gamme + eta/2 + alpha[i] + beta[j]
log(mu) = gamme - eta/2 + alpha[i] + beta[j]
'''
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Import data
df = pd.read_csv('./Data/edited_data.csv')

# Concatenate home and away goals, assigning weighting of eta to each
goal_model_data = pd.concat([df[['Home', 'Away', 'HG']].assign(home=1/2).rename(
    columns={'Home': 'team', 'Away': 'opponent', 'HG': 'goals'}),
    df[['Away', 'Home', 'AG']].assign(home=-1/2).rename(
    columns={'Away': 'team', 'Home': 'opponent', 'AG': 'goals'})])

# Fit the parameters of the poisson distribution to the data
goals_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
                family=sm.families.Poisson()).fit()
print(goals_model.summary())

# Save the model
goals_model.save("./Data/goals_model")
