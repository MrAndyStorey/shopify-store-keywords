#!/usr/bin/env python3
import sys
import time
import string

import argparse

import json
import requests
import csv

from progress.bar import Bar

# Allow the user to pass the start and finish of the three-character list via a CLI argument.
# By default it will go from aaa to zzz
parser = argparse.ArgumentParser(description='Two optional arguments (start & end) can be passed with three-letter values.')
parser.add_argument("--start", default="ada", type=str, help="Start of the three-letter character list - default = 'aaa'.")
parser.add_argument("--end", default="aea", type=str, help="End of the three-letter character list - default = 'zzz'.")
args = parser.parse_args()


if __name__ == '__main__':

  charStarts = args.start
  charEnds = args.end

  requestHeaders = {'content-type': 'application/json', 'accept-encoding': 'gzip, deflate, br', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}

  keywords = []

  csv_file_location = 'keywords.txt'


  # First, build a list of strings for the script to attempt to retrieve KWs.  
  # Three character chars is the minimum that the apps.shopify.com/search/autocomplete will accept.
  letters = string.ascii_lowercase
  if charEnds >= charStarts:
    builtArray=([''.join([a,b,c]) for a in letters for b in letters for c in letters if a+b+c >= charStarts and a+b+c <= charEnds])

    # Due to a web request for each list element, this will take some time, so lets show the user a progress bar
    with Bar('Processing ' + str(len(builtArray)) + ' items.', max=len(builtArray)) as bar:
      for threeChars in builtArray:
        response = requests.get("https://apps.shopify.com/search/autocomplete?max_results=standard&q=" + threeChars + "&st_source=autocomplete&v=2")
        # response = requests.get("https://webhook.site/66d175a7-bfd4-4943-8806-58c0e8510a80", headers=requestHeaders)

        if response.status_code == 200:
          searches = response.json()
          
          for item in searches["searches"]:
            keywords.append(item["name"])

        bar.next()

    with open(csv_file_location, 'w+', encoding='utf-8') as output_file:
      output_file.write('\n'.join(keywords))
      output_file.close()
    
  else:
    print('The passed arguments --end must be after the --start.  You gave {} and {}.'.format(charStarts, charEnds))
