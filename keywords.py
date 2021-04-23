
#!/usr/bin/env python3
import requests
import sys
import getopt
import time
import string
from progress.bar import Bar


if __name__ == ‘__main__’:

  # By default it will go from aaa to zzz, but lets allow two parameters to be passed to the script to specifiy a start and end.
  charStarts = "aaa"
  charEnds = "zzz"

  try:
    opts, args = getopt.getopt(argv,"s:e:",["ifile=","ofile="])

  except getopt.GetoptError:
    print 'keywords.py -starts <three-characters: aaa> -ends <three-characters: zzz>'
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-s", "--starts"):
      charStarts = arg
    elif opt in ("-e", "--ends"):
      charEnds = arg

  # First, build a list of strings for the script to attempt to retrieve KWs.  
  # Three character chars is the minimum that the xxx will accept.
  letters = string.ascii_lowercase
  if charEnds > charStarts:
    builtArray=([''.join([a,b,c]) for a in letters for b in letters for c in letters if a+b+c >= charStarts and a+b+c <= charEnds])
    print(len(builtArray))

  # Due to a web request for each list element, this will take some time, so lets show the user a progress bar
  with Bar('Processing...') as bar:
      for i in range(100):
          sleep(0.02)
          bar.next()

