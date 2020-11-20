# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 21:21:51 2020

@author: Ben Wonderlin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read in master csv and yales.io leave data
df = pd.read_csv("yale_athletics_master2021_ver_2.csv")
all_students = pd.read_csv("yc_loa.txt")

# math
num_athletes = len(df.index)
num_athletes_leave = len(df[df["leave"] == True])

num_all = len(all_students.index)
num_all_leave = len(all_students[all_students["leave"] == True])

num_non_athlete = num_all - num_athletes
num_non_athlete_leave = num_all_leave - num_athletes_leave

percent_non_athlete_leave = num_non_athlete_leave / num_non_athlete
overall_average = np.mean(all_students["leave"])

# pandas shenanigans

df["international"] = df["international"].apply(lambda s: s == True)

percent_international_leave = np.mean(df[df["international"] == True]["leave"])
percent_non_international_leave = np.mean(df[df["international"] == False]["leave"])

# matplotlib shenanigans

plt.rcParams['font.family'] = "serif"
plt.rcParams["figure.figsize"] = (8, 5)        
plt.style.use("seaborn")

fig = plt.figure(figsize = (6,6))
ax = fig.add_axes([0,0,1,1])
ax.set_ylabel("% on Leave of Absence")
ax.set_xlabel("")
ax.axhline(y = overall_average, linewidth = 3, color = "black", linestyle = "--")

categories = ["Non-Athletes", "International Athletes", "Non-International Athletes"]
percents = [percent_non_athlete_leave, percent_international_leave, percent_non_international_leave]
ax.bar(categories, percents)

plt.show()



