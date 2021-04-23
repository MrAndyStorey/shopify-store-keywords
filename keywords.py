import sys
import getopt

import time

import string
letters = string.ascii_lowercase

from progress.bar import progressBar


def main(argv):

  # By default it will go from aaa to zzz, but lets allow two parameters to be passed to the script to specifiy a start and end.
  charStarts = "ccc"
  charEnds = "ddd"
  try:
    opts, args = getopt.getopt(argv,"s:e:",["starts=","ends="])
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
  if charEnds > charStarts:
    timeStart = time.perf_counter()
    builtArray=([''.join([a,b,c]) for a in letters for b in letters for c in letters if a+b+c >= charStarts and a+b+c <= charEnds])
    timeEnd = time.perf_counter()
    print(f"Concatenation: {timeStart - timeEnd:0.4f} seconds")

  print(len(builtArray))

  # Due to a web request for each list element, this will take some time, so lets show the user a progress bar
  with progressBar('Processing...') as bar:
      for i in range(100):
          sleep(0.02)
          bar.next()
          
if __name__ == "__main__":
   main(sys.argv[1:])
