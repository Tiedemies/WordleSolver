#! /usr/bin/python3.8

""" Filters the dictionary for 5-letter words """
from curses.ascii import isalpha, islower


def filter(filename):
  handle = open(filename, 'r')
  dict = []
  for string in handle.readlines():
    word = string.strip()
    if word.isalpha() and len(word) == 5 and word.islower():
      dict.append(word)
  return dict

if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2:
    filename = "dict.txt"
  else:
    filename = sys.argv[1]
  dict = filter(filename)
  if len(sys.argv) < 3:
    outfile = "dict_5.txt"
  else:
    outfile = sys.argv[2]
  f = open(outfile,'w')
  for string in dict:
    f.write(string + '\n')
  print("Wrote " + str(len(dict)) + " words.")

    