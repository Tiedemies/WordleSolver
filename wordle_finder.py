#! /usr/bin/python3.8
import sys

""" WordleFinder finds good matches from the dictionary """
class WordleFinder:
  """ Initialize """
  def __init__(self, dictfile="dict_5.txt", n = 5, hard = True):
    self.dict_ = self.ReadDict(dictfile)
    self.tried_ = set([])
    self.correct_ = {i: False for i in range(n)}
    self.let_correct_ = {}
    self.let_found = {i: set([]) for i in range(n)}
    self.n_ = 5
    self.hard_ = hard

  """ Read dictionary and return it as set of strings """
  def ReadDict(self,dictfile):
    handle = open(dictfile,'r')
    dict = set([])
    for string in handle.readlines():
      dict.add(string.strip())
    return dict
  """ insert a word hint that has 'correct' indices """
  def InsertWord(self, word, correct, found):
    if self.n_ != len(word):
      raise ValueError("Wrong length word") 
    for i in range(len(word)):
      if i in correct and word[i] != correct[i] and self.hard_:
        raise ValueError("Not allowed in hard mode")
