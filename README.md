# Shopify App Store Keyword Finder
## Introduction
This trawls through the Shopify App Store to find a useful list of keywords from the autocomplete function and then scrapes further data about each keyword providing some invaluable information to App Developers.

It takes two arguments for the starting (-s) and (-e) ending three character strings.  The defaults are aaa and zzz.
```
keywords.py -s bbb -e ddd
```

## Packages Used
We will be using [Progress](https://github.com/verigak/progress) to display the progress of the scrip to the user.

In addition, we wil be using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) to traversing the HTML DOM in process.py.

To install these packages, you should use Python's package installer, pip3.  On the MacOS CLI you can use these commands:
```
pip3 install progress
pip3 install beautifulsoup4
```

## Workings of the Script
* Compiles a list of 3 character strings to submit to app.shopify.com
* 
