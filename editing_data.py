#!/usr/bin/env python3
'''
This program removes data from after the 2015 season and appends a column
indicating in which conference each team plays
'''
import pandas as pd
from datetime import datetime

# Import data
df = pd.read_csv('./Data/data.csv')

# Remove data after 06/12/2015
df.Date = pd.to_datetime(df.Date, dayfirst=True)
df = df.drop(df[df.Date > '2015-12-06'].index)

# Add column indicating which conference teams are part of
Eastern = ['Chicago Fire', 'Columbus Crew',
        'DC United', 'CF Montreal',
        'New England Revolution', 'New York Red Bulls',
        'New York City', 'Orlando City',
        'Philadelphia Union', 'Toronto FC']
Western = ['Colorado Rapids', 'FC Dallas',
        'Los Angeles Galaxy', 'Portland Timbers',
        'Real Salt Lake', 'San Jose Earthquakes',
        'Seattle Sounders', 'Vancouver Whitecaps']

# Teams who changed from Eastern to Western conference in 2015
Mix = ['Houston Dynamo', 'Sporting Kansas City']

conference_dict = {}
for i in Eastern:
    conference_dict[i] = 'Eastern'
for i in Western:
    conference_dict[i] = 'Western'

# Add conference columns to the dataframe
df['home_conference'] = df['Home'].map(conference_dict)
df['away_conference'] = df['Away'].map(conference_dict)
df = df.fillna(0)

# Accounting for team whos changed conference
def conference_mixed(row, h_a):
    if row['{0}_conference'.format(h_a)] == 0 and row['Date'] < datetime.strptime('2015-01-01', '%Y-%m-%d'):
        return 'Eastern'
    if row['{0}_conference'.format(h_a)] == 0 and row['Date'] > datetime.strptime('2015-01-01', '%Y-%m-%d'):
        return 'Western'
    else:
        return row['{0}_conference'.format(h_a)]

df['home_conference'] = df.apply(conference_mixed, h_a='home', axis=1)
df['away_conference'] = df.apply(conference_mixed, h_a='away', axis=1)

# save edited data
df.to_csv('./Data/edited_data.csv')
