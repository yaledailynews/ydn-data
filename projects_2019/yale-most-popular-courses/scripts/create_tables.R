require(readr)
require(dplyr)
require(stringr)
require(tidyr)

setwd("/Users/leonlufkin/Desktop/yale-most-popular-courses/scripts")

# helper functions

unite_code <- function(df) {
	unite(df, code, subject, number, sep = " ", remove = FALSE)
}

separate_code <- function(df) {
	separate(df, code, into = c("subject", "number"), sep = " ", remove = FALSE)
}

separate_designator <- function(df) {
	df %>%
		mutate(number = as.numeric(str_extract(number, "[[:digit:]]+")),
			   designator = str_extract(number, "[:alpha:]"))
}

# read in data

demand <- read_csv("../raw-data/demand.csv") %>%
	mutate(date = as.Date(date, format = "%m/%d"))

courses <- read_csv("../raw-data/courses.csv") %>%
	separate_code() %>%
	separate_designator() %>%
	select(id, code, subject, number, designator, name)

coursetable <- read_csv("../raw-data/coursetable.csv") %>%
	unite_code() %>%
	separate_designator() %>%
	select(code, subject, number, designator, section, times, locations, rating, workload)

# GENERATE TABLE: TOP COURSES

top_ids <- demand %>%
	filter(date == max(date)) %>%
	arrange(desc(count)) %>%
	top_n(20)

top_names <- courses %>%
	filter(number < 500) %>%
	filter(id %in% top_ids$id) %>%
	group_by(id) %>%
	summarize(name = first(name),
			  codes = paste(code, collapse = " / "))

top_courses <- top_ids %>%
	left_join(top_names) %>%
	filter(!is.na(codes)) %>%
	top_n(10)

write_csv(top_courses, "../data/most_shopped.csv")

# GENERATE TABLE: TRENDING

trending_ids <- demand %>%
	filter(date == max(date) - 1 | date == max(date) - 2) %>%
	spread(date, count) %>%
	`colnames<-`(c("id", "yesterday", "today")) %>%
	filter(yesterday >= 3) %>%
	filter(today > 0) %>%
	mutate(change = today - yesterday,
		   absChange = abs(change),
		   pctChange = change / yesterday) %>%
	arrange(desc(absChange)) %>%
	select(id, yesterday, today, change, absChange) %>%
	top_n(20)

trending_names <- courses %>%
	filter(number < 500) %>%
	filter(id %in% trending_ids$id) %>%
	filter(!(id %in% c(2184))) %>%
	group_by(id) %>%
	summarize(name = first(name),
			  codes = paste(code, collapse = " / "))

trending <- trending_ids %>%
	left_join(trending_names) %>%
	filter(!is.na(codes)) %>%
	top_n(10)

write_csv(trending, "../data/trending.csv")

# GENERATE TABLE: SEMINARS

seminars <- coursetable %>%
	# get rid of the 1 HTBAs
	filter(times != "1 HTBA") %>%
	# get the first "word" in the string of times
	mutate(word = stringr::word(times)) %>%
	# the first word must be one letter long (M, T, W, F) or "Th"
	filter(str_length(word) == 1 | word == "Th") %>%
	left_join(demand %>%
			  	filter(date == max(date)) %>%
			  	left_join(courses)) %>%
	# undergrad courses only
	filter(number < 500) %>%
	# these were a lab and Corp Finance (that for some reason only met one a week)
	filter(!(code %in% c("ECON 361", "MCDB 241L", "MCDB 251L", "ENGL 450"))) %>%
	select(code, id, count, name, times) %>%
	group_by(id) %>%
	summarize(name = first(name),
			  codes = paste(code, collapse = " / "),
			  count = first(count),
			  times = first(times)) %>%
	arrange(desc(count)) %>%
	top_n(10, count)

write_csv(seminars, "../data/seminars.csv")
