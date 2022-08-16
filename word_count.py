#! /usr/bin/python3.8

import sys

def letterfreq(filename):
  handle = open(filename,'r')
  dict = {}
  for string in handle.readlines():
    found = {}
    for ltr in string.strip():
      if ltr in found:
        continue
      if not ltr in dict:
        dict[ltr] = 1
      else:
        dict[ltr] += 1
      found[ltr] = True
  return {k: v for k, v in sorted(dict.items(), key = lambda item: item[1], reverse=True)}

if __name__ == "__main__":
  if len(sys.argv) < 2:
    filename = "dict_5.txt"
  else:
    filename = sys.argv[1]
  dict = letterfreq(filename)
  for k in dict:
    print (k + ": " + str(dict[k]))
  