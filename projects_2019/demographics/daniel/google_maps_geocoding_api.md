Google Maps Geocoding API
================
Daniel Zhao
February 25, 2020

Full API reference:
<https://developers.google.com/maps/documentation/geocoding/intro#geocoding>

The API is pretty easy to use, and the code below should be pretty
self-explanatory.

``` r
library(httr)
knitr::opts_chunk$set(cache = T, message = F)

# function to simplify string concatenation
`%+%` <- function(a, b) paste0(a, b)

# Daniel's API key for Google Maps - please don't share
api_key <- "AIzaSyC13iWxQlr78Xibu25HrkP6nnBSatRWcrM"

# obtains coordinates for one address term
get_coords <- function(addr, key) {
    base <- "https://maps.googleapis.com/maps/api/geocode/json?address="
    
    url <- base %+% gsub(" ", "+", addr) %+% "&key=" %+% key
    
    r <- GET(url)
    
    lat <- content(r)$results[[1]]$geometry$location$lat
    lng <- content(r)$results[[1]]$geometry$location$lng
    
    c(lat, lng)
}
```

Some test calls:

``` r
get_coords("Bronx, New York City", api_key)
```

    ## [1]  40.84478 -73.86483

``` r
get_coords("Dubai, United Arab Emirates", api_key)
```

    ## [1] 25.20485 55.27078

``` r
get_coords("189 Elm St, New Haven, CT", api_key)
```

    ## [1]  41.30980 -72.92739
