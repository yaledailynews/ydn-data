library(tidyverse)
library(jsonlite)
library(rjson)
fns <- list.files("coursetable raw/", full.names=T) 
coursetable <- map_dfr(fns, function(filename){
  print(filename)
  semester <- str_remove(filename, ".json")
  dt <- jsonlite::fromJSON(filename) %>% #incredibly slow, but reads into R-friendly dataframes
    mutate(year = str_extract(semester, "([0-9]){4}"),
           semester = str_sub(semester, -2, -1))
  
  #json doesn't convert "nicely" to dataframes -- some columns are list columns/dataframes, 
  #so we can't bind_rows() them right away. Reformatting: 
  
  dt_base <- dt %>% select_if(~!is_list(.)) #tidyverse OP
  
  #for my uses i only need the meeting times
  dt <- bind_cols(dt_base, select(dt$times, -by_day))
}) %>% tbl_df()


#some additional formatting once everything has been combined

#rip when r doesn't support recursion past n=1e4
clean_times <- function(t){
  ls <- NULL
  for(i in 1:length(t)) {
    extracted <- str_extract(t[i], "([0-9]){2}\\.([0-9]){2}-([0-9]){2}\\.([0-9]){2}")
    val <- eval(parse(text = extracted))
    ls <- c(ls, val)
  }
  return(ls)
} 

clean_times <- function(t){
  ls <- NULL
  for(i in 1:length(t)) {
    extracted <- str_extract(t[i], "([0-9]){2}\\.([0-9]){2}-([0-9]){2}\\.([0-9]){2}")
    val <- eval(parse(text = extracted))
    ls <- c(ls, val)
  }
  return(ls)
} 


coursetable_new <- coursetable %>% 
  select(year, semester, subject, number, section, times = summary,
         times_expanded = long_summary, everything()) %>%   #reordering and renaming
  mutate(new_times = clean_times(times)) 

saveRDS(coursetable, "coursetable_full.RDS")
