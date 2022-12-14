#!/usr/bin/env python3
'''
This program fits the improved poisson goal model, which now accounts for
seasonality, by MLE of the fitset

log(lamda) = gamme + eta/2 + alpha[i] + beta[j] + seasonality
log(mu) = gamme - eta/2 + alpha[i] + beta[j]
'''
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Import data
df = pd.read_csv('./Data/edited_data.csv')

# Checking for seasonality in the data by sorting all data by MM-DD
df.Date = pd.to_datetime(df.Date)
df['Seasonality'] = df['Date'].dt.strftime('%m-%d')
df['Seasonality'] = '2000-' + df['Seasonality']
df.Seasonality = pd.to_datetime(df.Seasonality) - pd.datetime(2000, 3, 1)
df.Seasonality = df['Seasonality'].dt.days.astype('int16')

# Concatenate home and away goals, this time including a seasonality parameter
# only for home goals
goal_model_data = pd.concat([df[['Home', 'Away', 'HG', 'Seasonality']].assign(home=1/2).rename(
    columns={'Home': 'team', 'Away': 'opponent', 'HG': 'goals'}),
    df[['Away', 'Home', 'AG']].assign(home=-1/2).rename(
    columns={'Away': 'team', 'Home': 'opponent', 'AG': 'goals'})])

# Fit the parameters of the poisson distribution to the data
goals_model = smf.glm(formula="goals ~ home + team + opponent + Seasonality", data=goal_model_data,
                family=sm.families.Poisson()).fit()
print(goals_model.summary())

# Save the model
goals_model.save("./Data/improved_goals_model")
