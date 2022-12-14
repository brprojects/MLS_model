#!/usr/bin/env python3
'''
Create Eastern and Western confernce results tables for the 2016 season where
the goals scored in each fixture follows a poisson distribution with a lamda
calculated in forecasting2.py
Then check how often LA Galaxy finish top 2 in their confernce
'''
import pandas as pd
import numpy as np
from tabulate import tabulate

# Import data
fixtures = pd.read_csv('./Data/data_mls_my_predictions2.csv')

# Clubs class from which the table is created
class clubs:
    def __init__(self, club, points, goals_for, goals_against, conference, wins, draws, losses):
        self.club = club
        self.points = points
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.conference = conference
        self.wins = wins
        self.draws = draws
        self.losses = losses

    # Relevant data required for the actual results table
    def summary(self):
        return [self.club, self.wins, self.draws, self.losses,
                self.goals_for, self.goals_against,
                self.goals_for - self.goals_against, self.points]

# Teams in each conference
Eastern = ['Chicago Fire', 'Columbus Crew',
        'DC United', 'CF Montreal',
        'New England Revolution', 'New York Red Bulls',
        'New York City', 'Orlando City',
        'Philadelphia Union', 'Toronto FC']
Western = ['Colorado Rapids', 'FC Dallas',
        'Los Angeles Galaxy', 'Portland Timbers',
        'Real Salt Lake', 'San Jose Earthquakes',
        'Seattle Sounders', 'Vancouver Whitecaps',
        'Houston Dynamo', 'Sporting Kansas City']

# Run a simulation of the 2016 season based on goal model probabilities
def mls_simulation():
    # Add all clubs to a dictionary with their confernece declared
    clubs_dict = {}
    for i in Eastern:
        clubs_dict[i] = clubs(i, 0, 0, 0, 'E', 0, 0, 0)
    for i in Western:
        clubs_dict[i] = clubs(i, 0, 0, 0, 'W', 0, 0, 0)

    # Add points, goals and results to clubs based on their results, which
    # are based on their poisson distributed goals
    for game_id in range(len(fixtures)):
        home_goals = np.random.poisson(fixtures.predicted_home_goals[game_id])
        away_goals = np.random.poisson(fixtures.predicted_away_goals[game_id])
        clubs_dict[fixtures.Home[game_id]].goals_for += home_goals
        clubs_dict[fixtures.Home[game_id]].goals_against += away_goals
        clubs_dict[fixtures.Away[game_id]].goals_for += away_goals
        clubs_dict[fixtures.Away[game_id]].goals_against += home_goals
        if home_goals > away_goals:
            clubs_dict[fixtures.Home[game_id]].points += 3
            clubs_dict[fixtures.Home[game_id]].wins += 1
            clubs_dict[fixtures.Away[game_id]].losses += 1
        elif away_goals > home_goals:
            clubs_dict[fixtures.Away[game_id]].points += 3
            clubs_dict[fixtures.Home[game_id]].losses += 1
            clubs_dict[fixtures.Away[game_id]].wins += 1
        else:
            clubs_dict[fixtures.Home[game_id]].points += 1
            clubs_dict[fixtures.Away[game_id]].points += 1
            clubs_dict[fixtures.Home[game_id]].draws += 1
            clubs_dict[fixtures.Away[game_id]].draws += 1

    # Create both conference tables
    East_table = []
    West_table = []
    for i in clubs_dict.keys():
        if clubs_dict[i].conference == 'E':
            East_table.append(clubs_dict[i].summary())
        else:
            West_table.append(clubs_dict[i].summary())

    # Sort tables by points, goal difference, goals for and then alphabetically
    East_table.sort(key=lambda x: x[0])
    West_table.sort(key=lambda x: x[0])
    East_table.sort(key=lambda x: (x[7], x[6], x[4]), reverse=True)
    West_table.sort(key=lambda x: (x[7], x[6], x[4]), reverse=True)

    return East_table, West_table

# Return better formatted table
def pretty_table(East_table, West_table):
    West_result = tabulate(West_table, headers=('Team', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Points'), tablefmt='fancy_grid', showindex=range(1, 11))
    East_result = tabulate(East_table, headers=('Team', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Points'), tablefmt='fancy_grid', showindex=range(1, 11))
    return East_result, West_result

# Run 2016 MLS simulation and print results table
East_table, West_table = mls_simulation()
East_result, West_result = pretty_table(East_table, West_table)
print(East_result)
print(West_result)

# Simulation to see how many times LA Galaxy finishes top two in their
# conference out of 10^4 runs
LA_Galaxy_top_two = 0
for i in range(10_000):
    East_table, West_table = mls_simulation()
    if West_table[0][0] == 'Los Angeles Galaxy' or West_table[1][0] == 'Los Angeles Galaxy':
        LA_Galaxy_top_two += 1
    if (i+1) % 500 == 0:
        print(f'{i+1} simulations complete')
print(LA_Galaxy_top_two)
