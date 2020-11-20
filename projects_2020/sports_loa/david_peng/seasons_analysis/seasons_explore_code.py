#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# """
# Created on Mon Nov  2 15:12:35 2020

# @author: davidpeng
# """

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


master_roster = pd.read_csv("/Users/davidpeng/Desktop/YDN/analysis/yale_athletics_master2021_modi.csv")

# Fall: Soccer Cross-country Field Hockey Volleyball Football 
# Winter: Swim & Dive Hockey Gymnastics Basketball Fencing Squash 
# Spring: Lacrosse Rowing/Crew Golf Track/(Cross Country) Sailing Softball Baseball Tennis


# I manually separated the womens 'track and field' and 'cross country' teams

# Fall: Soccer Cross-country Field Hockey Volleyball Football 
fall_teams = ['womens_soccer','mens_soccer', 'womens_fieldhockey','womens_volleyball','football',
              'mens_crosscountry','womens_crosscountry']
# Winter: Swim & Dive Hockey Gymnastics Basketball Fencing Squash 
winter_teams = ['mens_swimming','womens_swimming_diving','womens_icehockey','mens_hockey','womens_gymnastics',
                'mens_basketball','womens_basketball','womens_fencing','mens_fencing','womens_squash','mens_squash']
# Spring: Lacrosse Rowing/Crew Golf Track Sailing Softball Baseball Tennis
spring_teams = ['womens_lacrosse','mens_lacrosse','womens_crew','mens_heavyweight_crew','mens_lightweight_crew',
                'womens_golf','mens_golf','mens_track','womens_track_field','sailing','womens_softball',
                'mens_baseball','womens_tennis','mens_tennis']


master_roster.insert(8,'season','')

# del master_roster['Unnamed: 8']
# del master_roster['Unnamed: 9']


for i, row in master_roster.iterrows():
    if master_roster.loc[i,'team'] in fall_teams:
        master_roster.loc[i,'season'] = 'fall'        
    elif master_roster.loc[i,'team'] in winter_teams:
        master_roster.loc[i,'season'] = 'winter'
    else:
        master_roster.loc[i,'season'] = 'spring'

fall = master_roster.loc[master_roster['season']=='fall'].reset_index(drop=True)
leave_fall = list(fall['leave']).count(True) / len(fall)
# print(leave_fall)
# print(len(fall))
# fall.to_csv("/Users/davidpeng/Desktop/YDN/analysis/fall_data.csv")

winter = master_roster.loc[master_roster['season']=='winter'].reset_index(drop=True)
leave_winter = list(winter['leave']).count(True) / len(winter)
# print(leave_winter)
# print(len(winter))

spring = master_roster.loc[master_roster['season']=='spring'].reset_index(drop=True)
leave_spring = list(spring['leave']).count(True) / len(spring)
# print(leave_spring)
# print(len(spring))


# mens_bball = winter.loc[winter['team']=='mens_basketball'].reset_index(drop=True)
# leave_mens_bball = list(mens_bball['leave']).count(True) / len(mens_bball)
# print(leave_mens_bball)


# master_roster.to_csv("/Users/davidpeng/Desktop/YDN/analysis/yale_athletics_master2021_seasons.csv")


# Use to put into a CSV #

# seasons = {'season': ['Fall','Winter','Spring'],
#            'percent_leave': [leave_fall,leave_winter,leave_spring],
#            'sample_size': [len(fall),len(winter),len(spring)]}

# s_explore = pd.DataFrame(seasons, columns = ['Season','percent_leave','sample_size'])
# seasons_explore.to_csv("/Users/davidpeng/Desktop/YDN/analysis/season_explore.csv")


sns.set_style('dark')
# plt.style.use('fivethirtyeight')

# Use to Graph #
# data_for_plt = [leave_fall,leave_winter,leave_spring]
data_for_plt = [i * 100 for i in [leave_fall,leave_winter,leave_spring]]
# print(data_for_plt)

s_explore = pd.DataFrame({'percent_leave': data_for_plt}, 
                         index = ['Fall','Winter','Spring'])

ax = s_explore.plot(kind='bar',rot=0)#,color='aqua')
# plt.xticks( horizontalalignment='center')

plt.title('Athletes Taking Leave by Sports Season (%)')
plt.xlabel('Sports Season')
plt.ylabel('% on Leave')
plt.tight_layout()
ax.set_yticks(np.arange(0,50,5))
ax.grid(axis='y')
# plt.show()

plt.savefig("/Users/davidpeng/Desktop/YDN/analysis/seasons_explore.png",dpi=200, bbox_inches='tight')


