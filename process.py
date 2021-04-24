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


if __name__ == '__main__':
    keywords = []
    # Open the inout file and add all lines to a list    
    with open(args.input, 'r', encoding='utf-8') as input_file:
        keywords = [line.rstrip() for line in input_file]
        input_file.close()

    # Open the output file and loop through each keyword one by one
    with open(args.output, 'w+', encoding='utf-8') as output_file:
        output_file.write('Keyword,Results,Rating,Top 3\n')

        # Showing a progress bar to the user.
        with Bar('Processing ' + str(len(keywords)) + ' keywords.', max=len(keywords)) as bar:

            for keyword in keywords:
                response = requests.get("https://apps.shopify.com/search?q=" + keyword)
                if response.status_code == 200:
                    builtString = keyword + ","

                    numResults = re.search("of\s(\d+)\sresults", response.text)
                    if numResults:
                        builtString = builtString + str(numResults.group()) + ","
                    else:
                        builtString = builtString + "0,"

                        
                    soup = BeautifulSoup(response.text, 'html.parser')

                
                    output_file.write(builtString + '\n')

                bar.next()


        output_file.close()

