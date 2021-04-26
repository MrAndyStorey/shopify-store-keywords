#!/usr/bin/env python3
import sys
import string
import re

import argparse

import json
import requests
from bs4 import BeautifulSoup

from progress.bar import Bar

# Allow the user to pass the start and finish of the three-character list via a CLI argument.
# By default it will go from aaa to zzz
parser = argparse.ArgumentParser(description='Processes the input file using Beautiful Soup and then saves the data in the output file.')
parser.add_argument("--input", default="test.txt", type=str, help="Input filename - default = keywords.txt.")
parser.add_argument("--output", default="keyword_data.csv", type=str, help="Output filename - default = keyword_data.csv.")
args = parser.parse_args()

getURL = "https://apps.shopify.com/search?q="
getURL = "https://webhook.site/66d175a7-bfd4-4943-8806-58c0e8510a80?q="

if __name__ == '__main__':
    keywords = []
    # Open the inout file and add all lines to a list    
    with open(args.input, 'r', encoding='utf-8') as input_file:
        keywords = [line.rstrip() for line in input_file]
        input_file.close()

    # Open the output file and loop through each keyword one by one
    with open(args.output, 'w+', encoding='utf-8') as output_file:
        output_file.write('Keyword,Results,Free,Paid,Avg Rating,Avg Reviews,Top 5\n')

        # Showing a progress bar to the user.
        with Bar('Processing ' + str(len(keywords)) + ' keywords.', max=len(keywords)) as bar:

            for keyword in keywords:
                response = requests.get(getURL + keyword)
                if response.status_code == 200:
                    builtString = keyword + ","

                    numResults = re.search("of\s(\d+)\sresults", response.text)
                    if numResults:
                        builtString = builtString + "{},".format(str(numResults[1]))
                    else:
                        builtString = builtString + "0,"

                        
                    avgRating = []
                    avgRevivews = []
                    avgCounter = 0


                    soup = BeautifulSoup(response.text, 'html.parser')

                    #First, lets see the spilt between paid for and free apps - data is contained within id="PriceFilter", inside <li><a><span></span></a></li>
                    for pricingSection in soup.find_all(id="PriceFilter"):
                        priceItem = pricingSection.find_all("span", class_ = "search-filter-group__item-count")
                        if priceItem:
                            builtString = builtString + "{},{},".format(str(priceItem[0].text).strip(),str(priceItem[1].text).strip())
                        else:
                            builtString = builtString + "-,-,"

                    for searchResultItem in soup.find_all("div", class_ = "ui-app-card__review", limit=100):
                        print(str(searchResultItem.find(class_ = "ui-star-rating__rating").text))
                        print(str(searchResultItem.find(class_ = "ui-review-count-summary").text))
                        
                        #avgRating.append()
                        #avgRevivews.append()
                        avgCounter += 1
                                           
                    builtString = builtString + "{},{},".format(str(avgCounter),str(avgCounter))


                    #Finally, find the names of the top 5 apps, we wil separate them with a pipe.
                    for searchResultItem in soup.find_all("h2", class_ = "heading--4 ui-app-card__name", limit=5):
                            builtString = builtString + "{}|".format(str(searchResultItem.text))

                    output_file.write(builtString.rstrip('|') + '\n')

                bar.next()


        output_file.close()

