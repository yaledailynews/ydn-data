#ggplot theme

library(tidyverse)
library(extrafont)
library(ggthemes)


#Essentially a modification of theme_few(), a very.... elegant? minimal theme
#added the Segoe UI font, which is what maggie and daniel used on the "yales most popular courses" post

theme_ydn <- function(){
  ggthemes::theme_few() + 
    theme(
      text = element_text(size = 16, family = "Segoe UI"), 
      plot.title = element_text(size = 24, face = "bold"), 
      plot.subtitle = element_text(size = 12), 
      panel.border = element_blank(), 
      axis.line = element_line(color = "black"), 
      legend.background = element_rect(fill = "#f4f4f4", linetype = "solid"), 
      legend.key = element_rect(fill = "#f4f4f4"), 
      panel.background = element_rect(fill = "#f4f4f4", color = NA),
      plot.background = element_rect(fill = "#f4f4f4", color = NA),
    ) 
}

scale_ydn <- function(...){
  scale_color_gradient(..., low = "white", high = "#0f4d92")
}



ggplot(iris, aes(x = Sepal.Length, y = Petal.Length, col = Sepal.Width, size = Petal.Width^.2)) + 
  geom_point(alpha = .5) + 
  labs(title = "Sample title to fill up some space", 
       subtitle = "Sample subtitle that is noticeably smaller but still readable") + 
  theme_ydn() + 
  scale_ydn()

class_demands <-  readRDS("cds_archives/merged_demand.RDS") %>% 
  mutate(year = as.numeric(str_sub(dates, -4, -1)), 
         year = ifelse(sem == "01", year, year+.5), 
         demand = as.numeric(str_trim(demand)), 
         dept = word(course_code ,1)) %>% 
  group_by(course_name, year) %>% 
  arrange(course_code, year, desc(demand)) %>% 
  top_n(1, demand) %>% 
  group_by(dept, year) %>% 
  summarise(avg_students = mean(demand, na.rm=T)) 



highest_increase <- class_demands %>% 
  group_by(dept) %>% 
  filter(percent_rank(year) ==0 | percent_rank(year) == 1) %>% 
  mutate(change = avg_students/lag(avg_students)) %>% drop_na(change) %>% 
  arrange(desc(change)) %>% 
  pull(dept) %>% head(8)
depts_of_interest <- class_demands %>% 
  filter(dept %in% c("ER&M", "S&DS", "CGSC", "NSCI"))


courses_plot <- class_demands %>% 
  ggplot(aes(x = year, y = avg_students, group = dept)) + 
  geom_line(alpha = .05) + 
  geom_line(data = depts_of_interest, aes(x = year, y = avg_students, group = dept, color = dept), 
            size = 1) + 
  scale_y_log10() + 
  labs(x = "Year", y = "Students Per Course", color = "Some Subjects \nof Interest", 
       title = "Class Demand Since 2012", 
       subtitle = "This graph yields absolutely no useful information") + 
  theme_ydn()

ggsave("prelim courses plot.png", courses_plot, width = 10, height = 8, dpi = 600)
