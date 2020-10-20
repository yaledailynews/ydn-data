# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

#print("hello world")


yc_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/yc_loa.csv")
# full_loa = [full_yc[i][0] for i in range(full_yc.iloc[:,0]) if full_yc[i][2]]
# print(full_yc.iloc[:,0])

# print(full_yc.at[0, "full_name"])

yc_loa = yc_full[yc_full["leave"]]
# print(yc_loa)
# print(yc_loa["full_name"])
# print(yc_loa.at[213,"full_name"])



# print(fencing_full["Names"])
# print(type(fencing_full["Names"]))
# print(fencing_full["Names"].item("Jonah Cho"))

# print("Jonah Cho" in yc_loa["full_name"])

# print(fencing_loa_bool)
# print(type(fencing_loa_bool))

#fencing (coed)
fencing_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/fencing_roster.csv")
fencing_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in fencing_full["Names"]])
del fencing_full['Unnamed: 0']
fencing_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/fencing_roster_loa.csv")

#football
football_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/football_roster.csv")
football_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in football_full["Names"]])
del football_full['Unnamed: 0']
football_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/football_roster_loa.csv")

#golf (coed)
golf_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/golf_roster.csv")
golf_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in golf_full["Names"]])
del golf_full['Unnamed: 0']
golf_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/golf_roster_loa.csv")

#lacrosse (coed)
lacrosse_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/lacrosse_roster.csv")
lacrosse_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in lacrosse_full["Names"]])
del lacrosse_full['Unnamed: 0']
lacrosse_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/lacrosse_roster_loa.csv")

#mens cross country
men_cc_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/men_cc_roster.csv")
men_cc_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in men_cc_full["Names"]])
del men_cc_full['Unnamed: 0']
men_cc_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/men_cc_roster_loa.csv")

#men_hockey
men_hockey_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/men_hockey_roster.csv")
men_hockey_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in men_hockey_full["Names"]])
del men_hockey_full['Unnamed: 0']
men_hockey_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/men_hockey_roster_loa.csv")

#men_soccer
men_soccer_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/men_soccer_roster.csv")
men_soccer_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in men_soccer_full["Names"]])
del men_soccer_full['Unnamed: 0']
men_soccer_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/men_soccer_roster_loa.csv")

#men_squash
men_squash_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/men_squash_roster.csv")
men_squash_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in men_squash_full["Names"]])
del men_squash_full['Unnamed: 0']
men_squash_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/men_squash_roster_loa.csv")

#sailing (coed)
sailing_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/sailing_roster.csv")
sailing_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in sailing_full["Names"]])
del sailing_full['Unnamed: 0']
sailing_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/sailing_roster_loa.csv")

#swimming (coed)
swimming_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/swimming_roster.csv")
swimming_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in swimming_full["Names"]])
del swimming_full['Unnamed: 0']
swimming_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/swimming_roster_loa.csv")

#tennis (coed)
tennis_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/tennis_roster.csv")
tennis_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in tennis_full["Names"]])
del tennis_full['Unnamed: 0']
tennis_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/tennis_roster_loa.csv")

#track (coed)
track_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/track_roster.csv")
track_full.insert(2, "leave", [name in list(yc_loa["full_name"]) for name in track_full["Names"]])
del track_full['Unnamed: 0']
track_full.to_csv("/Users/davidpeng/Desktop/YDN/loa/track_roster_loa.csv")






# football_full = pd.read_csv("/Users/davidpeng/Desktop/YDN/football_roster.csv")

# football_loa_bool = [name in yc_loa for name in football_full["Names"]]


####

# full_loa = []
# for i in range(len(full_yc.iloc[:,0])):
#     if full_yc.at[i,"leave"] == True:
#         # print("true!")
#         full_loa.append(full_yc.at[i,"full_name"])
# print(len(full_loa))
        

# print(full_loa)

# def taking_loa (name):
#     if name in full_loa.iloc[:,0]:
#         return True
#     else:
#         return False

# print(taking_loa ())

# def check_team (team_csv):
#     team_members = pd.read_csv(team_csv).iloc[:,1]
#     #print(team_members)
#     return [taking_loa(x) for x in team_members]
# for (i in range(1,length()))

# print(check_team ("/Users/davidpeng/Desktop/YDN/football.csv"))

# pd.read_csv(team_csv).iloc[:,0]
# [taking_loa(x) for x in team_members]

# (print (taking_loa ("Klara Aastroem")))