#!/usr/bin/env python3
import sys
import string
import re
import csv

import argparse

import json
import requests
from bs4 import BeautifulSoup

from progress.bar import Bar

# Allow the user to pass the start and finish of the three-character list via a CLI argument.
# By default it will go from aaa to zzz
parser = argparse.ArgumentParser(description='Processes the input file using Beautiful Soup and then saves the data in the output file.')
parser.add_argument("--input", default="/Users/andystorey/shopify-store-keywords/keywords.txt", type=str, help="Input filename - default = keywords.txt.")
parser.add_argument("--output", default="/Users/andystorey/shopify-store-keywords/keyword_data.csv", type=str, help="Output filename - default = keyword_data.csv.")
args = parser.parse_args()

getURL = "https://apps.shopify.com/search?q="
#getURL = "https://webhook.site/66d175a7-bfd4-4943-8806-58c0e8510a80?q="

topXLimit = 3

requestHeaders = {'content-type': 'application/json', 'accept-encoding': 'gzip, deflate, br', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}

if __name__ == '__main__':
    keywords = []
    # Open the inout file and add all lines to a list    
    with open(args.input, 'r', encoding='utf-8') as input_file:
        keywords = [line.rstrip() for line in input_file]
        input_file.close()

    # Open the output file and loop through each keyword one by one
    with open(args.output, 'w+', encoding='utf-8') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Keyword', 'Results', 'Free', 'Paid', 'Avg-Rating', 'Avg-Reviews', 'Top-' + str(topXLimit)])

        # Showing a progress bar to the user.
        with Bar('Processing ' + str(len(keywords)) + ' keywords.', max=len(keywords)) as bar:

            for keyword in keywords:
                response = requests.get(getURL + keyword)
                if response.status_code == 200:
                    avgRating = []
                    avgReviews = []
                    
                    builtResults = "0"
                    builtFree = "0"
                    builtPaid = "0"
                    builtAvgRating = "0"
                    builtAvgReviews = "0"
                    builtTopX = ""

                    #Count the total number of results.  
                    numResults = re.search("of\s(\d+)\sresults", response.text)
                    if numResults:
                        builtResults = "{}".format(str(numResults[1]))
                    else:
                        builtResults = "0"
                    
                    #Create an object, passing the HTML text
                    soup = BeautifulSoup(response.text, 'html.parser')

                    #First, lets see the spilt between paid for and free apps - data is contained within id="PriceFilter", inside <li><a><span></span></a></li>
                    for pricingSection in soup.find_all(id="PriceFilter"):
                        priceItem = pricingSection.find_all("span", class_ = "search-filter-group__item-count")
                        if priceItem:
                            builtFree = "{}".format(str(priceItem[0].text).strip())
                            builtPaid = "{}".format(str(priceItem[1].text).strip())
                        else:
                            builtFree = "-"
                            builtPaid = "-"

                    #Now find out the average number of stars each app has (avgRating) and a count of all the reviews (avgReviews)
                    for searchResultItem in soup.find_all("div", class_ = "ui-app-card__review", limit=100):
                        if searchResultItem.find(class_ = "ui-star-rating__rating"):
                            searchRatings = re.search("([0-9].[0-9])", searchResultItem.find(class_ = "ui-star-rating__rating").text)
                            if searchRatings:
                                avgRating.append(float(searchRatings[1]))

                        if searchResultItem.find(class_ = "ui-review-count-summary"):
                            searchReviews = re.search("(\d+)", searchResultItem.find(class_ = "ui-review-count-summary").text)
                            if searchReviews:
                                avgReviews.append(int(searchReviews[1]))

                    if len(avgRating) > 0:
                        builtAvgRating = "{}".format(round(sum(avgRating) / len(avgRating),2))
                        
                    if len(avgReviews) > 0:
                        builtAvgReviews = "{}".format(round(sum(avgReviews) / len(avgReviews),0))

                    #Find the names of the top X apps, we wil separate them with a pipe.
                    for searchResultItem in soup.find_all("h2", class_ = "heading--4 ui-app-card__name", limit=topXLimit):
                            builtTopX = builtTopX + "{}|".format(str(searchResultItem.text))

                    # Write the data for this row to the csv file.
                    csv_writer.writerow([keyword, builtResults, builtFree, builtPaid, builtAvgRating, builtAvgReviews, builtTopX.rstrip('|')])
                bar.next()
        output_file.close()
