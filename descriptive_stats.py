#!/usr/bin/env python3
'''
This program calculates the different home advantage for each conference
and plots the home advantage, home goals and away goals against time to find
seasonality in the data
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Import data
df = pd.read_csv('./Data/edited_data.csv')

# Count number of games where teams aren't in the same conference
count = len(df[df.home_conference != df.away_conference])
# print(count)
# print(len(df))

# Consider only matches between teams in the same conference
df2 = df.drop(df[df.home_conference != df.away_conference].index)

# Count (Home Wins : Away Wins : Draws) for each conference
Western_results = {'H': 0, 'A': 0, 'D': 0}
Eastern_results = {'H': 0, 'A': 0, 'D': 0}

for i in ['Eastern', 'Western']:
    for r in ['H', 'A', 'D']:
        if i == 'Western':
            Western_results[r] += len(df2[(df2.Res == r) & (df2.home_conference == i)])
        if i == 'Eastern':
            Eastern_results[r] += len(df2[(df2.Res == r) & (df2.home_conference == i)])

# print both win dictionaries and the home advantage of each conference
print(Western_results, Eastern_results)
print((Western_results['H'] * 3 + Western_results['D']) / (Western_results['A'] * 3 + Western_results['D']))
print((Eastern_results['H'] * 3 + Eastern_results['D']) / (Eastern_results['A'] * 3 + Eastern_results['D']))

# Checking for seasonality in the data by sorting all data by MM-DD
df.Date = pd.to_datetime(df.Date)
df['MM_DD'] = df['Date'].dt.strftime('%m-%d')
df['MM_DD'] = '2000-' + df['MM_DD']
df.MM_DD = pd.to_datetime(df.MM_DD)

fig, ax = plt.subplots(3, 1)

# Convert dates to numbers so can plot a trendline
x = mdates.date2num(df.MM_DD)

# Ploting home win, draw, away win against time
df['Res_num'] = df['Res'].apply(lambda x: -1 if x == 'A' else (1 if x == 'H' else 0))
y = df.Res_num
ax[0].scatter(x, y, s=20)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax[0].plot(x, p(x), "r--")

ax[0].set_xlabel('Date (DD-MM)')
ax[0].set_ylabel('Results')
ax[0].set_xticks([11018, 11064, 11110, 11157, 11204, 11251, 11298])
ax[0].set_xticklabels(['02-03', '17-04', '02-06', '19-07', '04-09', '21-10', '07-12'])
ax[0].set_yticks([1, 0, -1])
ax[0].set_yticklabels(['H', 'D', 'A'])

# Plotting home goals against time
y = df.HG
ax[1].scatter(x, y, s=20)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax[1].plot(x, p(x), "r--")

ax[1].set_xlabel('Date (DD-MM)')
ax[1].set_ylabel('Home Goals')
ax[1].set_xticks([11018, 11064, 11110, 11157, 11204, 11251, 11298])
ax[1].set_xticklabels(['02-03', '17-04', '02-06', '19-07', '04-09', '21-10', '07-12'])

# Plotting away goals against time
y = df.AG
ax[2].scatter(x, y, s=20)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax[2].plot(x, p(x), "r--")

ax[2].set_xlabel('Date (DD-MM)')
ax[2].set_ylabel('Away Goals')
ax[2].set_xticks([11018, 11064, 11110, 11157, 11204, 11251, 11298])
ax[2].set_xticklabels(['02-03', '17-04', '02-06', '19-07', '04-09', '21-10', '07-12'])

plt.show()
