#!/usr/bin/env python3
'''
This program creates a table of all teams in the MLS sorted on their
expected points in the 2016 season which is based on the win probabilities
calculated in forecasting2.py.
This expected points table is compared to the actual results table to
calculate the RMS error
'''
import pandas as pd
import numpy as np
from tabulate import tabulate

# Import data
fixtures = pd.read_csv('./Data/data_mls_my_predictions2.csv')

# Uncomment if using data_mls_simset_predictions as it rename columns
# fixtures = fixtures.rename(columns={"expected_team1_win": "expected_home_win", "expected_draw": "expected_draw", "expected_team2_win": "expected_away_win", "expected_team1_goals": "predicted_home_goals", "expected_team2_goals": "predicted_away_goals"})

# Import actual 2016 results
actual_results = pd.read_csv('./Data/data.csv')

# Remove data before 06/12/2015 and after 23/10/2016
actual_results.Date = pd.to_datetime(actual_results.Date, dayfirst=True)
actual_results = actual_results.drop(actual_results[(actual_results.Date < '2015-12-07') | (actual_results.Date > '2016-10-23')].index)
actual_results = actual_results.reset_index()

# Clubs class from which the table is created
class clubs:
    def __init__(self, club, points, goals_for, goals_against):
        self.club = club
        self.points = points
        self.goals_for = goals_for
        self.goals_against = goals_against

    def summary(self):
        return [self.club, self.goals_for, self.goals_against, self.points]

# List of teams, note that Montreal is stored under two seperate names beacuse
# data_mls_simset_predictions refers to them as 'Montreal Impact'
teams = ["Chicago Fire", "Columbus Crew",
        "DC United", "CF Montreal", "Montreal Impact",
        "New England Revolution", "New York Red Bulls",
        "New York City", "Orlando City",
        "Philadelphia Union", "Toronto FC",
        "Colorado Rapids", "FC Dallas",
        "Los Angeles Galaxy", "Portland Timbers",
        "Real Salt Lake", "San Jose Earthquakes",
        "Seattle Sounders", "Vancouver Whitecaps",
        "Houston Dynamo", "Sporting Kansas City"]

# Create instance of clubs class for each team
clubs_dict = {}
for i in teams:
    clubs_dict[i] = clubs(i, 0, 0, 0)

actual_dict = {}
for i in teams:
    actual_dict[i] = clubs(i, 0, 0, 0)

# Add points and goals to clubs based on expected results
for game_id in range(len(fixtures)):
    clubs_dict[fixtures.Home[game_id]].points += 3 * fixtures.expected_home_win[game_id] + fixtures.expected_draw[game_id]
    clubs_dict[fixtures.Home[game_id]].goals_for += fixtures.predicted_home_goals[game_id]
    clubs_dict[fixtures.Home[game_id]].goals_against += fixtures.predicted_away_goals[game_id]
    clubs_dict[fixtures.Away[game_id]].points += 3 * fixtures.expected_away_win[game_id] + fixtures.expected_draw[game_id]
    clubs_dict[fixtures.Away[game_id]].goals_for += fixtures.predicted_away_goals[game_id]
    clubs_dict[fixtures.Away[game_id]].goals_against += fixtures.predicted_home_goals[game_id]

# Add points and goals to clubs based on actual results
for game_id in range(len(actual_results)):
    actual_dict[actual_results.Home[game_id]].goals_for += actual_results.HG[game_id]
    actual_dict[actual_results.Home[game_id]].goals_against += actual_results.AG[game_id]
    actual_dict[actual_results.Away[game_id]].goals_for += actual_results.AG[game_id]
    actual_dict[actual_results.Away[game_id]].goals_against += actual_results.HG[game_id]
    if actual_results.HG[game_id] > actual_results.AG[game_id]:
        actual_dict[actual_results.Home[game_id]].points += 3
    elif actual_results.HG[game_id] < actual_results.AG[game_id]:
        actual_dict[actual_results.Away[game_id]].points += 3
    elif actual_results.HG[game_id] == actual_results.AG[game_id]:
        actual_dict[actual_results.Home[game_id]].points += 1
        actual_dict[actual_results.Away[game_id]].points += 1

# Create expected table
table = []
for i in clubs_dict.keys():
    table.append(clubs_dict[i].summary())

# Sort based on points
table.sort(key=lambda x: x[3], reverse=True)

# Create actual table
table2 = []
for i in actual_dict.keys():
    table2.append(actual_dict[i].summary())

# Sort based on points
table2.sort(key=lambda x: x[3], reverse=True)

# Calculate root-mean-squared error of goals for, goals against and Points
# between expected results from the model and the actual results

# Uncomment if using data_mls_simset_predictions as this accounts for differnt
# name of Montreal team
# clubs_dict['CF Montreal'] = clubs_dict['Montreal Impact']

del clubs_dict['Montreal Impact']
del actual_dict['Montreal Impact']
GF_error = 0
GA_error = 0
Points_error = 0
for team in clubs_dict:
    Points_error += (clubs_dict[team].points - actual_dict[team].points)**2
    GF_error += (clubs_dict[team].goals_for - actual_dict[team].goals_for)**2
    GA_error += (clubs_dict[team].goals_against - actual_dict[team].goals_against)**2

# print RMS errors
print(np.sqrt(Points_error / 20))
print(np.sqrt(GF_error / 20))
print(np.sqrt(GA_error / 20))

# Print results tables
print(tabulate(table, headers=('Team', 'Goals For', 'Goals Against', 'Points'), tablefmt='fancy_grid', showindex=range(1, 22)))
print(tabulate(table2, headers=('Team', 'Goals For', 'Goals Against', 'Points'), tablefmt='fancy_grid', showindex=range(1, 22)))
