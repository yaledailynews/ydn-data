students <- read.csv("yale_students_s20.csv")
majors <- unique(students$majors)

majors_df <- data.frame(majors)
write.csv(majors_df, "majors.csv")
