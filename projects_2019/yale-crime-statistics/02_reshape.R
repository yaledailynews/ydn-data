require(readr)
require(tidyr)
require(dplyr)
require(stringr)

crime <- read_csv("yale_crime_merged_2018.csv")

reshaped <- crime %>% 
	spread(Location, Number) %>% 
	mutate(`On-campus non-student housing` = `On campus` - `On campus student housing facilities`) %>%
	rename(`On-campus student housing` = `On campus student housing facilities`) %>%
	select(-one_of("<NA>", "On campus")) %>%
	gather("Location", "Number", -1:-6) %>%
	mutate(Location = str_replace_all(Location, "Student housing facilities", "On-campus student housing"),
		   Category = str_replace_all(Category, "Vawa", "VAWA")) %>%
	group_by(Year, Institution, Campus, `Institution Size`, Category, Subcategory, Location) %>%
	summarize(Number = sum(Number, na.rm = TRUE))

write_csv(reshaped, "yale_crime_merged.csv")