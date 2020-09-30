require(readr)
require(dplyr)
require(tidyr)
require(stringr)

# download full data from here: https://ope.ed.gov/campussafety/#/customdata/search
# select all years and all categories, except "Fire Statistics at bottom

# set working directory
setwd("C:/Users/Daniel/Google Drive/Areas/YDN Data Desk/Projects/Yale Crime Statistics")

# read all the files in the /data folder
files <- list.files(paste0(getwd(), "/data/"))

# read in one data file, convert to tidy format
read_data_file <- function(file_name) {
	df <- read_csv(paste0("data/", file_name))
	
	# some dataframes are empty, we only want those aren't
	if((ncol(df) > 1) & (nrow(df) > 0)) {
		# the filename is of the format category_location_moreSpecficWords.csv
		# we want to get this info into a column so that we have it when we merge the csvs
		# first, we clean the title
		file_name_cleaned <- file_name %>%
			str_replace(".csv", "") %>%
			str_replace_all("_", " ") %>%
			str_to_sentence()
		
		# for "arrests", the category is the first word, and location is everything else after
		# for all else, category is first two words, and locatiton is everything else
		if(stringr::word(file_name_cleaned) == "Arrests") {
			category <- "Arrests"
			location <- stringr::word(file_name_cleaned, 2, -1) %>% str_to_sentence()
		} else {
			category <- stringr::word(file_name_cleaned, 1, 2)
			location <- stringr::word(file_name_cleaned, 3, -1) %>% str_to_sentence()
		}
		
		# gather into tidy format and do some cleaning
		df %>%
			select(-one_of("Unitid", "Campus ID")) %>%
			gather("Subcategory", "Number", -1:-4) %>%
			mutate(Category = category,
				   Location = location,
				   Number = ifelse(is.na(Number), 0, Number)) %>%
			# We have a lot of very detailed categories, but nearly all of them say "0",
			#   so we filter them out. All of them happen to have " - ", which makes it
			#   easy, EXCEPT we want info on forcible and nonforcible sex offenses,
			#   which have a " - ", so we don't filter those out.
			filter((!str_detect(Subcategory, " - ")) | 
				   	Subcategory == "Sex offenses - Forcible" |
				   	Subcategory == "Sex offenses - Non-forcible") %>%
			select(Year = `Survey year`,
				   Institution = `Institution name`,
				   Campus = `Campus Name`,
				   `Institution Size`, Category, Location, Subcategory, everything())
	} else NULL
}

# read in all files into list, merge them together
crime <- files %>%
	lapply(read_data_file) %>%
	dplyr::bind_rows()

# save to csv
write_csv(crime, "yale_crime_merged.csv")

# what are the unique categories of numbers we have to fill in?
write_csv(crime %>% select(Category, Location, Subcategory) %>% unique(), "to_fill_in.csv")