require(readr)
require(stringr)
require(rvest)
require(purrr)
require(dplyr)
require(magrittr)

fname <- "yale_students.html"

# read everything into html tree
html_tree <- fname %>%
	read_file() %>%
	read_html()

# names are in .student_name h5
names <- html_tree %>%
	html_nodes(".student_name") %>%
	html_nodes("h5") %>%
	html_text() %>%
	str_replace("\\(.*", "") %>% # gets rid of code that plays audio of names
	str_trim()

# years are in .student_year
years <- html_tree %>%
	html_nodes(".student_year") %>%
	html_text()

n <- length(names) # total number of students
odds <- 2 * (1:n) - 1 # odd indices
evens <- 2 * (1:n) # even indices

# res colleges are in ODD .student_info tags
colleges <- html_tree %>%
	html_nodes(".student_info") %>%
	extract(odds) %>%
	html_text()

# all the EVEN .student_info tags contain all of the other information
info <- html_tree %>%
	html_nodes(".student_info") %>%
	extract(evens) %>%
	as.character() %>%
	str_split("<br>")

# emails are always in the first position, unless they don't exist
emails <- info %>% 
	map_chr(1) %>%
	str_replace(., ">\n<", "") %>%
	str_extract(">.*<") %>%
	str_sub(2, -2)

# bdays are always in the last position
bdays <- info %>%
	map_chr(~ .[length(.)]) %>%
	str_replace("</div>", "") %>%
	str_replace("\n", "") %>%
	ifelse(. == "", NA, .)

# majors are always in the second to last pos
majors <- info %>%
	map_chr(~ .[length(.) - 1]) %>%
	str_replace("</div>", "") %>%
	str_replace("\n", "") %>%
	str_replace("&amp;", "&") %>%
	ifelse(str_detect(., "<"), NA, .)

# extract dorm information
dorms <- info %>%
	map(~ .[-c(1, length(.) - 1, length(.))]) %>%
	map_chr(~if(identical(character(0), .[1])) NA else .[1]) %>%
	ifelse(str_detect(., "[:alpha:]+[:alnum:]*-[:alnum:]"), ., NA) %>%
	ifelse(str_detect(., "/"), NA, .)

# extract address info - this is where the bulk of the cleaning has to happen
# I'll comment this a little more later on
address <- info %>%
	map(~ .[-c(1, length(.) - 1, length(.))]) %>%
	map(~if(identical(character(0), .)) NA else .) %>%
	map(~if(!is.na(.) & str_detect(.[1], "[:alpha:]+[:alnum:]*-[:alnum:]")) .[-1] else .) %>%
	map(~if(identical(character(0), .)) NA else .) %>%
	map(~if(!is.na(.x) & str_detect(.[1], "\\d-\\d{4}")) .[-1] else .) %>%
	map(~if(identical(character(0), .)) NA else .) %>%
	map(~str_replace_all(., "/", " ")) %>%
	map(~str_trim(.)) %>%
	map(function(l) {
		if(is.na(l)) return(NA)
		if(length(l) < 2) return(l)
		if(str_detect(l[[2]], "\\d{10}") || str_detect(l[[2]], "\\d{3}-\\d{3}-\\d{4}")) return(l[-(1:2)])
		return(l)
	}) %>%
	map_chr(~paste0(., collapse = " / ")) %>%
	ifelse(str_detect(., "^NA$"), NA, .)

# generate random ids to anonymize data
ids <- sample(100000:200000, n, replace = F)

# at this point let's make a table
students <- data.frame(ids, years, colleges, majors, address)
write_csv(students, "yale_students_s20.csv")
