#!/usr/bin/env python3
'''
This program applies the improved goal model on the 2016 MLS season to find
expected home and away goals. Then it uses those probabilities to find the
expected home win, draw and away win probabilities
'''
import pandas as pd
import statsmodels.api as sm
from scipy.stats import poisson

# Load in the model
goals_model = sm.load('./Data/improved_goals_model')

# Import data
df = pd.read_csv('./Data/data.csv')

# Remove data before 06/12/2015 and after 23/10/2016
df.Date = pd.to_datetime(df.Date, dayfirst=True)
df = df.drop(df[(df.Date < '2015-12-07') | (df.Date > '2016-10-23')].index)

# Create new dataframe for 2016 fixtures
fixtures = df[["Date", "Time", "Home", "Away"]]
fixtures = fixtures.reset_index(drop=True)

# Convert dates to all be the same year so only difference is MM-DD
# then convert to number of days from 01/03/2000 so can find a correlation
fixtures.Date = pd.to_datetime(fixtures.Date)
fixtures['Seasonality'] = fixtures['Date'].dt.strftime('%m-%d')
fixtures['Seasonality'] = '2000-' + fixtures['Seasonality']
fixtures.Seasonality = pd.to_datetime(fixtures.Seasonality) - pd.datetime(2000, 3, 1)
fixtures.Seasonality = fixtures['Seasonality'].dt.days.astype('int16')

# Return expected number of home and away goals, then from that work out the
# corresponding home win, draw and away win probabilities
def forecast(model, home_team, away_team, seasonality):
    predicted_home_goals = goals_model.predict(pd.DataFrame(data={'team': home_team,
                            'opponent': away_team, 'home': 1/2, 'Seasonality': seasonality}, index=[1])).values[0]
    predicted_away_goals = goals_model.predict(pd.DataFrame(data={'team': away_team,
                            'opponent': home_team, 'home': -1/2, 'Seasonality': 0}, index=[1])).values[0]

    # Probabilty of home wins, draws and away wins
    expected_home_win = 0
    expected_draw = 0
    expected_away_win = 0
    for i in range(11):
        for j in range(11):
            if i > j:
                expected_home_win += poisson.pmf(i, predicted_home_goals) * poisson.pmf(j, predicted_away_goals)
            elif j > i:
                expected_away_win += poisson.pmf(i, predicted_home_goals) * poisson.pmf(j, predicted_away_goals)
            elif i == j:
                expected_draw += poisson.pmf(i, predicted_home_goals) * poisson.pmf(j, predicted_away_goals)
    return predicted_home_goals, predicted_away_goals, expected_home_win, expected_draw, expected_away_win


# Add predicted home and away goals and expected home win, draw and away win columns
fixtures['predicted_home_goals'], fixtures['predicted_away_goals'], fixtures['expected_home_win'], fixtures['expected_draw'], fixtures['expected_away_win'] = 0, 0, 0, 0, 0
for i in range(len(fixtures)):
    fixtures.predicted_home_goals[i], fixtures.predicted_away_goals[i], fixtures.expected_home_win[i], fixtures.expected_draw[i], fixtures.expected_away_win[i] = forecast(goals_model, fixtures.Home[i], fixtures.Away[i], fixtures.Seasonality[i])

# Save data
fixtures.to_csv('./Data/data_mls_my_predictions2.csv')
