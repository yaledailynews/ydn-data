library(tidyverse)
library(tidytext)
library(readr)
library(plotly)

afinn <- get_sentiments("afinn")
bing <- get_sentiments("bing")
nrc <- get_sentiments("nrc")

RESCOs <- c("TD", "JE", "Davenport", "Grace Hopper", "Ezra Stiles", "Saybrook", "Silliman", "Benjamin Franklin", "Pierson", "Branford", "Pauli Murray", "Berkeley", "Trumbull", "Morse")

data <- readxl::read_xlsx("data/Email Data.xlsx") %>% 
  mutate(Extra = as.logical(Extra), `Target Class Years` = ifelse(`Target Class Years` == "All", "First-years, Sophomores, Juniors, Seniors", `Target Class Years`)) %>%
  mutate(`First-years` = grepl("First-years", `Target Class Years`), Sophomores = grepl("Sophomores", `Target Class Years`), Juniors = grepl("Juniors", `Target Class Years`), Seniors = grepl("Seniors", `Target Class Years`)) %>% dplyr::select(-`Target Class Years`) %>%
  arrange(Date) %>% mutate(Email = paste(Subject, Sender, format(Date, "%m/%d/%Y"), sep = ", "))
data$ADMIN <- !(data$Sender %in% RESCOs)
df <- data %>% dplyr::select(ADMIN, Date, Text) %>% unnest_tokens(input = Text, output = word, token = "words") %>% group_by(ADMIN) %>% count(word, sort = T) %>% ungroup %>%
  group_by(word) %>% mutate(n_ADMIN = sum(n * ADMIN), n_HOCs = sum(n * !ADMIN)) %>% mutate(p_ADMIN = n_ADMIN / sum(n), p_HOCs = n_HOCs / sum(n)) %>% ungroup %>%
  dplyr::select(-c(n, ADMIN)) %>% distinct() 
TOTAL_ADMIN <- sum(df$n_ADMIN)
TOTAL_HOCs <- sum(df$n_HOCs)
df <- df %>% anti_join(stop_words, by = c("word" = "word")) %>% mutate(n = n_ADMIN + n_HOCs)

#####################
## EMPIRICAL BAYES ##
#####################
hyper.param <- df %>% filter(n > 10) %>% # filter words with 3 or more mentions
  dplyr::select(p_ADMIN) %>% as_vector() %>% unname() %>% fitdistrplus::fitdist(distr = "beta", method = "mme")
df$n_ADMIN_EB <- df$n_ADMIN + hyper.param$estimate[1]
df$n_HOCs_EB <- df$n_HOCs + hyper.param$estimate[2]
df <- df %>% mutate(rate_ADMIN = 25000*n_ADMIN/TOTAL_ADMIN, rate_HOCs = 25000*n_HOCs/TOTAL_HOCs, 
                    rate_ADMIN_EB = 25000*n_ADMIN_EB/TOTAL_ADMIN, rate_HOCs_EB = 25000*n_HOCs_EB/TOTAL_HOCs,
                    rate_total_EB = 25000*(n_ADMIN_EB+n_HOCs_EB)/(TOTAL_ADMIN+TOTAL_HOCs)) %>% 
  mutate(rate_ratio = rate_ADMIN/rate_HOCs, rate_ratio_EB = rate_ADMIN_EB/rate_HOCs_EB) %>%
  mutate(group_HOCs_admin = ifelse(rate_ratio > 1, "Admin", "HOCs"), 
         id = row_number())

topN_words <- c("continue", "assignments", "widespread", "strong", "limited", "message", "continue", "safe", "returning", "academic", "courtyard",
                  "strict", "crisis", "campus", "health", "students", "zoom", "public", "testing", "quarantine", "gatherings", "spread",
                  "professional", "activities", "experience", "move", "senior", "2020", "mask", "crisis", "unable", "responsibility", "common", "remote",
                  "participate", "communities", "asymptomatic", "city", "parties", "virus", "families", "violate", "virtual",
                  "holiday", "symptoms", "society", "belongings", "traditions", "leadership", "obstacles", "successful", "decompress", "school", "travel",
                  "time", "continue", "covid", "health", "students", "community", "college", "staff", "fall", "semester", "research", "life", "faculty",
                  "distancing", "questions", "hall", "time", "connecticut", "guidelines", "test", "athletics", "vaccination", "vaccine", "quarantine",
                  "collge", "athletics", "information", "questions", "life", "academic", "distancing", "final", "compact", "drop", "mental")
topN_words <- unique(topN_words)
df_topN <- df %>% filter(word %in% topN_words) %>% arrange(abs(log(rate_ratio_EB))) %>% #group_by(group_HOCs_admin) %>% slice(which(row_number() %% round(n()/50) == 1)) %>% sample_frac() %>% ungroup() %>%
  mutate(color_range = log(rate_ratio)) %>% 
  mutate(color_range = ifelse(color_range == Inf, 3, ifelse(color_range == -Inf, -3, color_range))) %>%
  mutate(color_range_scale = ifelse(color_range>0, color_range/max(color_range), color_range/abs(min(color_range))))
df_topN %>% select(-c(n_ADMIN, n_HOCs, n_ADMIN_EB, n_HOCs_EB, rate_ADMIN_EB, rate_HOCs_EB, p_ADMIN, p_HOCs)) %>%
  write.csv("data/word_list_odds_topN.csv", row.names = F)

get_sentences_with_word <- function(word, sentences) sentences[as.vector(sapply(sentences, function(sentence) any(sapply(unlist(str_split(sentence, pattern = "[-, ]+")), function(testword) tolower(testword) == tolower(word)))))]
get_text_with_word <- function(word) apply(data[,c("Sender", "Text", "Email")], 1, function(x) list(sender = ifelse(x[1] %in% RESCOs, "HOCs", "Admin"), email=x[3], sentences=get_sentences_with_word(word=word, sentences=unlist(str_split(x[2], pattern = "[-.!?]")))))

topN_quotes <- df_topN$word %>% lapply(get_text_with_word) %>% lapply(function(emails) emails[ !unlist(lapply(emails, function(x) identical(x$sentences, character(0)) )) ] )
names(topN_quotes) <- df_topN$word
max_sentences_per_word <- 5

topN_quotes_cutoff <- lapply(topN_quotes, function(l) {
  l <- l[sample(1:length(l))]
  out_l_index <- c()
  count_admin <- count_HOCs <- 0
  for (i in 1:length(l)) {
    email <- l[[i]]
    sentences <- email$sentences
    email$sentences <- sentences[sample(1:length(sentences))][1:min(5,length(sentences))]
    l[[i]] <- email
    
    flag <- F
    if (email$sender == "Admin") {
      count_admin <- count_admin + 1
      if (count_admin > max_sentences_per_word) flag <- T
    } else {
      count_HOCs <- count_HOCs + 1
      if (count_HOCs > max_sentences_per_word) flag <- T
    }
    
    out_l_index <- if (flag) c(out_l_index, F) else c(out_l_index, T)
  }
  return(l[out_l_index])
})

topN_json <- jsonlite::toJSON(topN_quotes_cutoff, pretty = TRUE, auto_unbox = TRUE)
sink("data/topN_quotes.json")
cat(topN_json)
sink()


