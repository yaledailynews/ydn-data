###########################
#     YDN Data Desk       #
#     Sports - Sarah      #
# Exploring prelim csv    #
###########################

# load in csv
setwd('C:/Users/sarah/OneDrive/Documents/Data Desk')
master <- yale_athletics_master2021
summary(master)

# load libraries
library(dplyr, ggplot2)

# turn leave into binary indicator
master <- master%>%
  mutate(leave_binary = ifelse(leave==FALSE,0,1))

# exploring relationship between gender and leave of absence
gender_explore <- master%>%
  group_by(gender)%>%
  summarise(percent_leave = mean(leave_binary), n=n())

print(gender_explore) # this shows that 46 percent of male athletes took leaves and 
                      # 34 percent of female athletes took leaves

write.csv(gender_explore, 'C:/Users/sarah/OneDrive/Documents/Data Desk/gender_explore.csv')


# exploring relationship between team and leave of absence
team_explore <- master%>%
  group_by(team)%>%
  summarise(percent_leave = mean(leave_binary), n=n())%>%
  arrange(desc(percent_leave))

print(team_explore) 

write.csv(team_explore, 'C:/Users/sarah/OneDrive/Documents/Data Desk/team_explore.csv')

# exploring relationship between year and loa
year_explore <- master%>%
  group_by(year)%>%
  summarise(percent_leave = mean(leave_binary), sample_size = n())

print(year_explore)

write.csv(year_explore, 'C:/Users/sarah/OneDrive/Documents/Data Desk/year_explore.csv')

# exploring relationships between season and loa
