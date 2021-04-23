# Shopify App Store Keyword Finder
## Introduction
This trawls through the Shopify App Store to find a useful list of keywords from the autocomplete function and then scrapes further data about each keyword providing some invavuable information to App Developers.

It takes two arguments for the starting (-s) and (-e) ending three character strings.  The defaults are aaa and zzz.
```
keywords.py -s bbb -e ddd
```

## Packages Used
We will be using [Progress](https://github.com/verigak/progress) to display the progress of the scrip to the user.
To install Progress, you should use Python's package installer, pip3.  On the MacOS CLI you can use these commands:
```
pip3 install progress
```

## Workings of the Script
* Compiles a list of 3 character strings to submit to app.shopify.com
* 
