Technical Setup
================
### YDN Data Desk
**Updated 9/29/20**

Welcome to the YDN Data Desk\! The purpose of this document is to help
you get started with the technical tools we plan to be using. By making
sure everyone’s devices are set up as similarly as possible, we can
reduce the chances of compatibility issues across computers and
collaborators.

We’ve tried to make the instructions below as extensive as possible, but
if anything is unclear or if any of the instructions aren’t working, you
should reach out to Darwin and Ashley as soon as possible.

# R Setup

Much of our data manipulation and analysis work will be conducted using
**R**, in large part because it’s the language most commonly used at
Yale. R itself is a programming language, which means that like any
other language (Java, Python, C++), you’ll need to have appropriate
software installed to interpret code. Most R users also choose to use
**RStudio**, an *integrated development environment* (IDE) that makes
programming in R much more efficient by providing features that monitor
the state of variables, autocomplete code, highlighting errors, and
more. Finally, the **tidyverse** is a set of R packages that streamline
common data manipulation tasks.

(As of September 29, 2020, the latest stable release of R is 4.0.2 “Taking off Again”)

## Installing R

**Everyone should have R and R Studio installed on their computers.** If
you do, you can skip this section; if you don’t already, follow these
steps:

**Windows**

  - [Go to this page](https://cloud.r-project.org/bin/windows/base/)
  - Click on “Download R 4.0.2 for Windows”
  - Once the installer downloads, open it and complete the steps
  - Finally, install R Studio: go to [this
    page](https://rstudio.com/products/rstudio/download/#download),
    click the big blue button that says “Download RStudio for Windows”,
    and follow the instructions
  - Open R Studio. In the console, type `install.packages("tidyverse")`

**Mac**

  - [Go to this page](https://cloud.r-project.org/bin/macosx/)
  - Click on “R-4.0.2.pkg”
  - Once the installer downloads, open it and complete the steps
  - Finally, install R Studio: go to [this
    page](https://rstudio.com/products/rstudio/download/#download),
    click the big blue button that says “Download RStudio for Mac”, and
    follow the instructions
  - Open R Studio. In the console, type `install.packages("tidyverse")`

## Updating R

Since we expect many of you will already have R and RStudio installed on
your computer from previous classes and projects, we also want to make
sure that everyone is using the same version of R. Please be sure to go
through the steps corresponding to your system (either Mac or Windows),
which are provided below for your convenience:

**Windows**

  - Install the `installr` package by calling
    `install.packages("installr")`
  - Call the `updateR()` function by typing `installr::updateR()`
  - Click “Yes” in all the menus that pop up. One of the popups will
    “recommend” that you use the R GUI to update R instead of doing so
    within RStudio; you can safely ignore this popup.
  - The popups will then offer to help you copy and update old packages;
    make sure you click “Yes”.

**Mac**

The process for updating R on Mac is the same as the process for freshly
installing R:

  - Go to [this page](https://cloud.r-project.org/bin/macosx/)
  - Find a blue link labeled “R-4.0.2.pkg”, and click it.
  - Click the file once it’s finished downloading to install it, and
    follow through the setup process.

## Updating R packages

Finally, make sure you update all of your packages by going into RStudio
\> Tools \> Check for Package Updates. A small menu should pop up with
all of the packages for which there are newer versions. You don’t need
to update all of your packages (it can take awhile), but if you see
these packages listed:

  - `dplyr`
  - `knitr`
  - `rmarkdown`
  - `tidyr`
  - `tidyselect`
  - `tidyverse`

you should check the box next to them and click “Install Updates”.

# Python Setup

We don’t be using Python nearly as extensively in our work, and will
strive to consolidate as much of our work in R as possible. That said,
we anticipate that we still use Python because:

  - Python is popular, especially in industry
  - While R is better for data analysis, Python is better for scripting
    (automating repetitive) tasks
  - Certain tools are more developed in Python than they are in R, such
    as web scraping and machine learning

Because of this, **you have the option of installing Python now or
installing Python only once your project calls for it**. Whenever you
choose to install Python, please follow the instructions below.

## Background

Like R, Python is a programming language that reads and interprets code
that you write. This means that you must install both the language
itself and some form of integrated development environment (IDE) that
makes programming tasks more efficient. Unlike R, however, there are
many more options for IDEs that are commonly used. They range in
complexity from basic text editors that include additional programming,
auto-complete, and terminal functionality (Atom, VS Code, Sublime) to
full-featured environments that monitor variable states and help you
manage complex file structures (Visual Studio, Eclipse).

While you can feel free to choose any IDE, there are two that I
recommend:

  - **Visual Studio Code** because it is a lightweight, customizable IDE
    that’s also flexible for other languages we might use for the Data
    Desk, namely HTML/CSS/JavaScript
  - **Jupyter Notebook** (which isn’t technically an IDE) because it
    allows you to see code and output in one place; it’s essentially the
    Python analog for R Markdown
  - **Spyder** is a much more full-powered IDE; it’s essentially a
    parallel of R Studio, but for Python

While Python wasn’t designed for data science, it’s become incredibly
popular for data science, and people have come up with customized
installations that included exactly what you need to use Python for data
science: it’s called **Anaconda**. Installing Anaconda will install the
core Python functionality, Visual Studio Code, Jupyter Notebook, and
data science packages (`pandas`, etc.) for Python all at once.

**While going through Anacaonda and everything is *technically* the best way to set everything up, I just install packages on my system environment and use virtual environments if needed for other projects. This is not good practice but it works and I'm too lazy to switch. So basically... you do you.** - Interjection from Darwin

## Installing Anaconda

On both **Mac** and **Windows**, follow these steps if you’ve never
installed Anaconda before (including if you’ve only installed vanilla
Python):

  - Go to this [page](https://www.anaconda.com/distribution)
  - Scroll down to “Windows” and “macOS”, and click your operating
    system
  - Click the “Download” buttom next to “Python 3.7”
  - Once the download is complete, open the file and complete the
    installation process, accepting all default options

On **Windows**, you should also then do the following:

  - Open the Start menu and type “path”
  - Click the first option that comes up, which should say “Edit the
    system environment variables”
  - In the window that pops up, click “Environment Variables”
  - Under “User variables”, double-click the row that says “Path” under
    “Variable”
  - Press the “New” button, and paste in `C:\ProgramData\Anaconda3`.
    Press enter. Click “Move Up” until the row moves to the very top.
  - Repeat the above step, but for `C:\ProgramData\Anaconda3\Scripts`
    and for `C:\ProgramData\Anaconda3\Library\bin`

If you’re having issue using pandas or numpy (as I did with a fresh
Anaconda3 installation), try these steps:

  - Make sure you have all three locations above added to your PATH
    variables
  - Open Command Prompt as administrator
  - Enter `pip uninstall numpy` and `pip uninstall pandas`
  - Enter `pip install numpy` and `pip install pandas`

## Updating Anaconda

If you’ve previously installed Anaconda, you will likely have older
versions of Python, Anaconda, and `numpy` or `pandas`. For now, it’s
most important that you update Anaconda, `numpy`, and `pandas`; we’ll
provide more complete instructions later.

Open Command Prompt (Windows) or Terminal (Mac) **as an administrator**
by right-clicking and clicking "Run as administrator. Then, type in
these two commands and hit enter, one-by-one:

    conda update conda
    conda update pandas

You should make absolutely sure that you have `pandas` 1.0.0 or later,
as `pandas` recently went through some pretty big changes to core
functions and we want to reduce the likelihood of encountering
compatibility issues. You can check the version of `pandas` that you
have installed by typing `pip list` in Command Prompt or Terminal, and
scrolling down to `pandas`.

Don’t worry if any of this doesn’t work for now. Since we likely won’t
be using Python immediately (except for scraping), it’s not too likely
we’ll run into issues between versions, so we can iron out these issues
later.

# GitHub setup

If you’ve ever worked on a group project that has involved some sort of
coding, you’ve probably found that sharing code is always a hassle. For
smaller projects, it’s viable to have each team member handle a specific
portion of the project, and send around some code files as necessary.
For larger projects, however, this quickly gets unwieldy, especially as
the number of files and the number of collaborators increases.

GitHub is a platform for sharing code, collaborating on code, and
tracking versions of code. If you’re a computer science major and work
on side projects, you’re probably already familiar with GitHub, but
GitHub tends to be used less often in statistics and data science (and
certainly not in the Yale Statistics & Data Science department, unless
you’re currently taking S&DS 262).

A technical note, for those interested: *GitHub* is built on *Git*,
which is the version control system that does the hard work of comparing
files and tracking changes. GitHub is an open-source platform that uses
Git and provides an online interface and community for sharing files.
GitHub is the most popular version control platform that utilizes Git,
but you may find some employers using different Git clients separate
from GitHub.

We'll be using GitHub to store all of our work and changes. If you don't already 
have one, you should create a GitHub account and read up on how it works. Links to resources
will be provided in the Teams.

The following instructions will tell you how to obtain GitHub and the student developer pack which gives you some cool free perks. However these perks are completely optional and all you need is just a functional GitHub account. 

**You can simply create an account on the website and you will be all set.** 

However if you would like, you can follow the instructions below to get the student developer pack.

## If you don’t have a GitHub account and want the developer pack

1.  Go to the [GitHub homepage](https://github.com/)
2.  Type in a username, your Yale email, and a password to create an
    account. Note that GitHub allows you to change the primary email
    associated with your account, so if you don’t have a GitHub account
    right now, it’s best to create your account with your Yale email,
    then change it down the road.
3.  Complete the sign-up and verification process. (You’ll likely have
    to click a verification link in your email.)
4.  Make sure you’re signed into GitHub, then go to [GitHub for
    Education](https://education.github.com/benefits), and click “Get
    benefits” at the top right
5.  Follow the directions to request access. Choose your Yale email when
    prompted.
6.  You’ll have a to wait between a few hours and a few days, and you’ll
    be notified when your account is approved
7.  Message Daniel and Maggie once you’ve completed these steps (no need
    to wait for student access to go through) with your GitHub username
    (not email)

## If you have a GitHub account, but don’t have the Student Developer Pack 

1.  Make sure you’re signed in, and go to [Profile \> Settings \>
    Emails](https://github.com/settings/emails)
2.  Add your Yale address under “Add email address”; you’ll have to
    confirm your email via a link sent to your email
3.  Go to [GitHub for Education](https://education.github.com/benefits),
    and click “Get benefits” at the top right
4.  Follow the directions to request access. Choose your Yale email when
    prompted.
5.  You’ll have a to wait between a few hours and a few days, and you’ll
    be notified when your account is approved
6.  Message Daniel and Maggie once you’ve completed these steps (no need
    to wait for student access to go through), with your GitHub username
    (not email)

## Conclusion
Once you have GitHub / `r` / `python` (if you anticipate on using it) set up, great! There will be some links in the teams to other resources that would be useful to know.