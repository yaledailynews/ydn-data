#a version of the CDS scraper in R
library(rvest)
library(tidyverse)
library(magrittr)

subjects <- read_html('https://ivy.yale.edu/course-stats/') %>% 
  html_nodes("#subjectCode option") %>% html_text() %>% 
  str_split("-", n =2) %>% unlist() %>% str_trim()

subjects <- data.frame(codes = subjects[seq(3, length(subjects), 2)], 
                       names = subjects[seq(4, length(subjects), 2)],
                       stringsAsFactors = F)



get_semester_data <- function(semester){
  dates <- read_html(paste0("https://ivy.yale.edu/course-stats/?termCode=", semester, "&subjectCode=AMTH")) %>% 
    html_nodes("table table") %>% html_nodes("td") %>% html_text() %>% 
    str_subset("/") %>% str_trim()
  #rip nested loops
  courses <- map_dfr(subjects$codes, function(subject){
    time <- system.time({
      page <- paste0('https://ivy.yale.edu/course-stats/?termCode=', semester, 
                     "&subjectCode=", str_replace(subject, "&", "%26")) %>% 
        read_html() 
      
      
      containers <- page %>% html_nodes("div#content div table tbody tr") %>% 
        extract(!unlist(map(html_attrs(.), is_empty)))
      
      subject_data <- map_dfr(containers, function(container){
        
        full_code <- container %>% html_nodes("td a") %>% html_text()  %>% str_remove_all(";") %>% str_trim() %>% 
          str_subset(".+") 
        code <- full_code %>% str_split("/") %>% unlist() %>% 
          str_subset(subject) %>% extract(1)
        name <- container %>% html_nodes("td span") %>% html_text() %>% str_remove_all(";") %>% str_trim() %>% 
          str_subset(".+")
        demand <- html_nodes(container, "td.trendCell") %>% html_text() 
        
        assembled_data <- data.frame(aliases = full_code, course_code = code, 
                                     course_name = name, demand = demand, dates = dates,
                                     stringsAsFactors = F)
        return(assembled_data)
      })
      
    })
    
    print(paste("Scraped", str_sub(semester, 1,4), subject, "in", round(time[3], 2), "seconds" ))
    return(subject_data)
  })
  saveRDS(courses, paste0("cds_archives/", semester, ".RDS"))
  return(courses) 
}

semesters <- c("201103", 
               unlist(map(2012:2019, function(x) paste0(x, "0", c(1,3)))),
               "202001")
full_dataset <- map_dfr(semesters, get_semester_data)


full_dataset <- map_dfr(list.files("cds_archives/", full.names = T, pattern = "([0-9]){4}"),                         function(filename){
                          readRDS(filename) %>% 
                            reduce(bind_rows) %>% 
                            mutate(dates = paste0(dates, "/", 
                                                  str_extract(filename, "([0-9]){4}")), 
                                   sem = str_extract(str_extract(filename, 
                                                                 "([0-9]){2}.RDS"),
                                                     "([0-9]){2}")) 
                          }
                        )
saveRDS(tbl_df(full_dataset), "cds_archives/merged_demand.RDS")
