###########################
#     YDN Data Desk       #
#     Sports - Sarah      #
# Exploring prelim csv    #
###########################

# load in csv
setwd('C:/Users/sarah/OneDrive/Documents/Data Desk/')
master <- read.csv('athletic_master.csv')
summary(master)

# load libraries
library(dplyr, ggplot2)

# turn leave into binary indicator
master <- master%>%
  mutate(leave_binary = ifelse(leave==FALSE,0,1))

# renaming  "Men" to "Male" in gender column
print(unique(master$gender))
master$gender <-gsub("Men", "Male", master$gender)

# exploring relationship between gender and leave of absence
gender_explore <- master%>%
  group_by(gender)%>%
  summarise(percent_leave = mean(leave_binary), sample_size=n())

print(gender_explore) # this shows the percent of male, female, and coed athletes
# who took a leave this year

write.csv(gender_explore, 'gender_explore_updated.csv')


# exploring relationship between team and leave of absence
team_explore <- master%>%
  group_by(team)%>%
  summarise(percent_leave = mean(leave_binary), team_size=n())%>%
  arrange(desc(percent_leave))

print(team_explore) 

write.csv(team_explore, 'team_explore_updated.csv')

# exploring relationship between year and loa
master <- master%>%
  mutate(year_actual = ifelse(year=='2022'&leave==TRUE, '2021',
                              ifelse(year=='2023'&leave==TRUE, '2022',
                                     ifelse(year=='2024'&leave==TRUE, '2023',year))))
  

year_explore <- master%>%
  group_by(year_actual)%>%
  summarise(percent_leave = mean(leave_binary), sample_size = n())

print(year_explore)

write.csv(year_explore, 'year_explore_updated.csv')

# exploring relationships between season and loa

# creating bar plots
# gender
gender_plot <- ggplot(gender_explore, aes(gender,percent_leave))+
  geom_col(width=0.6, aes(fill=gender))+
  labs(title='Percent of Athletes Taking Leave by Gender', x='gender', y='percent')
gender_plot
ggsave('gender_plot_updated.png')

# year
year_plot <- ggplot(year_explore, aes(year_actual, percent_leave))+
  geom_col(aes(fill=year_actual))+
  labs(title='Percent of Athletes Taking Leave by Year', x='Class Year', y='Percent')
year_plot

ggsave('year_plot_updated.png')

#team as function of size
team_plot <- ggplot(team_explore, aes(team_size, percent_leave))+
  geom_point()+
  #geom_smooth(method = "lm", se=FALSE)+
  labs(title='Percent of Athletes Taking Leave by Size of Team', x='Team Size', y='Percent')

team_plot

ggsave('team_plot_updated_nolm.png')

# explore sports seasons
# fall sports = Soccer, Cross-country, Field Hockey, Volleyball, Football
# winter sports = Swim & Dive, Hockey, Gymnastics, Basketball, Fencing, Squash

master <- mutate(master, season=ifelse((team=='mens_crosscountry')|(team=='mens_soccer')|
                                        (team=='womens_soccer')|(team=='womens_field_hockey')|
                                        (team=='womens_volleyball')|(team=='football'),'Fall',
                                      ifelse((team=='womens_basketball')|(team=='mens_basketball')|
                                               (team=='womens_swimming_diving')|(team=='mens_fencing')|
                                               (team=='womens_squash')|(team=='womens_gymnastics')|
                                               (team=='womens_fencing')|(team=='mens_hockey')|(team=='mens_squash')|
                                               (team=='mens_swimming')|(team=='womens_icehockey'),'Winter', 'Spring')))

season_explore <- master%>%
  group_by(season)%>%
  summarise(percent_leave = mean(leave_binary), sample_size=n())

print(season_explore) 

season_explore$season <- factor(season_explore$season,levels = c("Fall", "Winter", "Spring"))

season_plot <- ggplot(season_explore, aes(season,percent_leave))+
  geom_col(width=0.6, aes(fill=season))+
  labs(title='Percent of Athletes Taking Leave by Season', x='Sport Season', y='Percent')

season_plot

ggsave('season_plot_updated.png')
