Extracting information from the JSON
================
Daniel Zhao
February 24, 2020

Use `fromJSON()` from the `rjson` package

``` r
require(rjson)
```

    ## Loading required package: rjson

``` r
# Replace with the path to the JSON file on your computer
# Use relative paths if possible
# The following should work automatically if you're cloning the Git repo
ct <- rjson::fromJSON(file = "../coursetable.json")
```

`ct` is a list, and each element of the list is itself another list.
Each element of `ct` represents one course.

``` r
str(ct)
ct[[1]]
str(ct[[1]])
str(ct[[1]]$evaluations)
ct[[2]]$long_title
```

Extracting simple variables: use `sapply()` (look this up on Google).
`sapply()` attempts to convert a list to a numeric or string if
possible, and in this case, it is possible

``` r
titles <- sapply(ct, function(x) x$long_title)
head(titles)
```

    ## [1] "Foundations of Accounting and Valuation"                                                 
    ## [2] "“We Interrupt this Program:  The Multidimensional Histories of Queer and Trans Politics”"
    ## [3] "The Rise and Fall of Atlantic Slavery"                                                   
    ## [4] "Sickness and Health in African American History"                                         
    ## [5] "Caribbean Baseball: A Cultural History"                                                  
    ## [6] "Afro-Modernism in the Twentieth Century"

Now, we try for a more complex variable. There are `NULL` values in the
ratings, so `sapply()` continues to return a list

``` r
ratings <- sapply(ct, function(x) x$average$same_both$rating)
head(ratings, 20)
```

    ## [[1]]
    ## [1] 3.43
    ## 
    ## [[2]]
    ## NULL
    ## 
    ## [[3]]
    ## [1] 3.82
    ## 
    ## [[4]]
    ## [1] 4.99
    ## 
    ## [[5]]
    ## NULL
    ## 
    ## [[6]]
    ## [1] 3
    ## 
    ## [[7]]
    ## NULL
    ## 
    ## [[8]]
    ## [1] 4.5
    ## 
    ## [[9]]
    ## [1] 4.3
    ## 
    ## [[10]]
    ## [1] 4.9
    ## 
    ## [[11]]
    ## [1] 4.2
    ## 
    ## [[12]]
    ## NULL
    ## 
    ## [[13]]
    ## [1] 3.63
    ## 
    ## [[14]]
    ## NULL
    ## 
    ## [[15]]
    ## NULL
    ## 
    ## [[16]]
    ## NULL
    ## 
    ## [[17]]
    ## [1] 3.84
    ## 
    ## [[18]]
    ## NULL
    ## 
    ## [[19]]
    ## [1] 4.54
    ## 
    ## [[20]]
    ## [1] 4.65

To solve this problem, we need to write a function that will return `NA`
instead of `NULL` any time there’s a `NULL`.

``` r
extract_rating <- function(x) {
    r <- x$average$same_both$rating
    if(!is.null(r)) return(r)
    else return(NA)
}

ratings <- sapply(ct, extract_rating)
head(ratings, 20)
```

    ##  [1] 3.43   NA 3.82 4.99   NA 3.00   NA 4.50 4.30 4.90 4.20   NA 3.63   NA   NA
    ## [16]   NA 3.84   NA 4.54 4.65
