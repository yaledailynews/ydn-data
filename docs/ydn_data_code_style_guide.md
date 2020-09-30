Code Style Guide
================
YDN Data Desk
February 16, 2020

This document is a style guide: it will outline common guidelines that
we’ll use to produce efficient, readable, and beautiful code for the YDN
Data Desk. It will be heavily inspired by the [`tidyverse` style
guide](https://style.tidyverse.org/) and [Google’s R Style
Guide](https://google.github.io/styleguide/Rguide.html).

As Hadley Wickham notes on the first page of the style guide:

> All style guides are fundamentally opinionated. Some decisions
> genuinely do make code easier to use (especially matching indenting to
> programming structure), but many decisions are arbitrary. The most
> important thing about a style guide is that it provides consistency,
> making code easier to write because you need to make fewer decisions.

In that vein, **this style guide will evolve as the YDN Data Desk
matures**. We’ll seek to establish a set of rigid yet flexible
conventions that data reporters from all backgrounds will find more
useful than it is constraining, one that allows data reporters to
communicate code with each other while also accomodating for personal
preference.

Questions? Let [Daniel](mailto:daniel.zhao@yale.edu) or
[Maggie](mailto:maggie.nolan@yale.edu) know.

# Naming conventions

## File names

**File names** should be separated with underscores or hyphens, not
spaces. They should stick to letters and numbers, avoiding special
characters. This is particularly important for R Markdown files, since
RStudio will automatically replace space with underscores when knitting
the file.

    # Good
    fit_models.R
    utility_functions.R
    
    # Bad
    fit models.R
    foo.r
    stuff.r

If you have many, many lines of code, considering breaking them up into
separate files. You should prefix the name of teach file with a number:

    00_download.R
    01_explore.R
    ...
    09_model.R
    10_visualize.R

## Object names

**Variable names** should be *nouns*, and use underscores:
`var_name_like_this`

**Function names** should be *verbs*, and use underscores:
`function_name_like_this()`. This is in line the format of function
names in tidyverse.

**Dataframe column names** should be sentence case: \`ColumnNameLikeThis

Never should you name an object with periods. The reasons are twofold:

  - Periods have special meanings in most other programming languages,
    so it’s bad practice in general
  - Periods can get confused with R’s implementation of
    object-orientation, and while we don’t touch R’s S3 objects, it
    eliminates any possibility for confusion

## Descriptive names

All object names should be descriptive, concise, and meaningful. This
means that you should:

  - Avoid naming dataframes as `df`: what does the dataframe contain?
    This reduces confusion when you begin working with several
    dataframes.
  - Avoid naming the mean of a variable as `mean`: consider naming it
    `mean_of_var`, for similar reasons as above.
  - If you’re creating a series of linear regressions, avoid naming them
    `lm1`, `lm2`, and so forth, unless it’s perfectly clear what each
    one represents. Otherwise it forces the reader to find the exact
    line of code where the regression was created to see which
    regression it represents.

For example, if one regression uses the untransformed variables, one
uses logarithmic transformations, and one uses an exponential transform,
consider doing this:

    # Bad
    lm1 <- lm(Income ~ Population, data = census)
    lm2 <- lm(Income ~ log(Population), data = census)
    lm3 <- lm(Income ~ exp(Population), data = census)
    
    # Good
    lm_base <- lm(Income ~ Population, data = census)
    lm_log <- lm(Income ~ log(Population), data = census)
    lm_exp <- lm(Income ~ exp(Population), data = census)

If naming objects concisely is difficult, or if you find yourself trying
to squeeze many different sets of information into the variable name,
you might want to use a list or a dataframe to store your objects. For
example:

    # Bad
    lm_base_00 <- lm(Income ~ Population, data = subset(census, year == 2000))
    lm_base_10 <- lm(Income ~ Population, data = subset(census, year == 2010))
    lm_base_20 <- lm(Income ~ Population, data = subset(census, year == 2020))
    lm_log_00 <- lm(Income ~ log(Population), data = subset(census, year == 2010))
    lm_log_10 <- lm(Income ~ log(Population), data = subset(census, year == 2010))
    lm_log_20 <- lm(Income ~ log(Population), data = subset(census, year == 2010))
    lm_exp_00 <- lm(Income ~ exp(Population), data = subset(census, year == 2020))
    lm_exp_10 <- lm(Income ~ exp(Population), data = subset(census, year == 2020))
    lm_exp_20 <- lm(Income ~ exp(Population), data = subset(census, year == 2020))
    
    # Good
    # todo: fill in example using purrr and tibbles

# Code syntax

## Commas

Every comma should be followed by one space, just like in regular
English. It should never be preceded by a space.

    # Good
    x[, 1]
    
    # Bad
    x[,1]
    x[ ,1]
    x[ , 1]

## Parentheses

Parentheses should not ever be preceded or succeeded by spaces.

    # Good
    mean(x, na.rm = TRUE)
    
    # Bad
    mean (x, na.rm = TRUE)
    mean( x, na.rm = TRUE )
    
    # Depends on preference
    if (TRUE)
    if(TRUE)

The only exception is for a function definition, in which case a space
should follow the final `)`

    # Good
    function(x) {}
    
    # Bad
    function(x){}

# Code layout

## Code width

Code should follow the standard practice of 80 characters wide. RStudio
has a feature to display a line at the 80-character mark; to enable this
option, you can go to Tools \> Global Options \> Code \> Display \>
Check “Show margin”, and make sure “80” is entered in the text box.

## Outline of code

Quoted from Hadley:

Use commented lines of - and = to break up your file into easily
readable chunks.

``` r
# Load data ---------------------------

# Plot data ---------------------------
```

If your script uses add-on packages, load them all at once at the very
beginning of the file. This is more transparent than sprinkling
library() calls throughout your code or having hidden dependencies that
are loaded in a startup file, such as .Rprofile.

# R scripts

## Use case

Primarily for scripting purposes, such as

  - Proessing a batch of .csv files
  - Scraping a website and saving as .csv

# R Markdown

## Use case

Primarily for exploratory purposes, such as

  - Extracting insights from a dataset
  - Sending insight to reporters for comment

## Header

In the YAML header at the top of your R Markdown file, you should
include the document’s title, your name, and the date:

    ---
    title: 'Code Style Guide'
    author: 'Daniel Zhao'
    date: February 16, 2020
    ---

## `R.version`

At the very end of your document, you should always include a code chunk
that includes just one line of code: `R.version`. This will help debug
any compatibility issues that arise when knitting the document in the
future.

``` r
R.version
```

    ##                _                           
    ## platform       x86_64-w64-mingw32          
    ## arch           x86_64                      
    ## os             mingw32                     
    ## system         x86_64, mingw32             
    ## status                                     
    ## major          3                           
    ## minor          6.2                         
    ## year           2019                        
    ## month          12                          
    ## day            12                          
    ## svn rev        77560                       
    ## language       R                           
    ## version.string R version 3.6.2 (2019-12-12)
    ## nickname       Dark and Stormy Night
