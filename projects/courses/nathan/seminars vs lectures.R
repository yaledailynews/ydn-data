#analyzing seminar enrollment 

library(tidyverse)
library(plotly)
dt <- readRDS("cds_archives/merged_demand.RDS") %>% 
  mutate(demand = as.numeric(str_trim(demand)),
         year = str_extract(dates, "([0-9]){4}")) %>% 
  distinct(dates, demand, course_name, year, sem, aliases) %>% 
  filter(aliases != "DISR 999")

highest <- dt %>% group_by(year, sem, aliases) %>% 
  top_n(1, wt = demand) %>% 
  distinct(demand, course_name, year, sem, aliases) %>% 
  ungroup %>% 
  mutate(sem = case_when(sem == "03" ~ paste("Fall", year),
                         sem == "01" ~ paste("Spring", year)))

map(unique(highest$sem), function(semester){
  demand_dist <- highest %>% filter(sem == semester) %>% 
    ggplot(aes(x = demand)) + 
    geom_histogram(bins = 50) + 
    lims(y = c(0, 200)) + 
    scale_x_log10(limits = c(1, 1200)) + 
    theme_bw()
  
  ggsave(paste0("plots/", semester, ".png"), demand_dist, 
         width = 9, height = 7)
})


