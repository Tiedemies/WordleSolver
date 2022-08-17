#! /usr/bin/python3.8

from random import choice
from wordle_finder import *

def color(str,n):
  #white for not correct
  if n == 0:
    cc = "\033[1;37m"
  ## Green for correct
  elif n == 1:
    cc = "\033[1;32m"
  ## Yellow for somewhere
  elif n == 2:
    cc = "\033[1;33m"
  else:
    cc = "\033[0;37m"
  return cc+str


class WordleEngine(WordleFinder):
  def __init__(self, dict="dict_5.txt", n=5, hard = True):
    super().__init__(dict,n,hard)
    self.correct_word_ = None
    self.letter_count = {}
  def NewWord(self):
    self.correct_word_ = choice(list(self.dict_))
    self.tried_words_ = set([])
    self.failed_letters_ = set([])
    self.correct_ = {i: None for i in range(self.n_)}
    self.let_correct_ = {}
    self.let_found_ = {i: set([]) for i in range(self.n_)}
    self.contain_letters_ = {}
    self.letter_count = {ltr: 0 for ltr in self.correct_word_}
    for ltr in self.correct_word_:
      self.letter_count[ltr]+=1
    
  def Guess(self,word):
    if (self.CheckWord(word)):
      return False
    toprint = ""
    if word == self.correct_word_:
      toprint += color(word,1) + color("",3)
      print (toprint)
      return True
    wcount = {a:self.letter_count[a] for a in self.letter_count}
    correct = []
    found = []
    for i in range(self.n_):
      if word[i] == self.correct_word_[i]:
        wcount[word[i]] -= 1
        correct.append(i)
    for i in range(self.n_):
      if word[i] == self.correct_word_[i]:
        toprint += color(word[i],1)
      elif word[i] in self.correct_word_ and wcount[word[i]] > 0:
        wcount[word[i]] -= 1
        toprint += color(word[i],2)
        found.append(i)
      else:
        toprint += color(word[i],0)
    self.InsertWord(word,correct, found)
    toprint += color("",3)
    return toprint
  
if __name__ == "__main__":
  print(" Welcome to the game. Try to guess the 5-letter word.")
  print(" White is wrong letter, yellow is correct letter in the wrong place and green is correct letter in correct place")
  W = WordleEngine()
  W.NewWord()
  while True:
    print("Enter your guess:")
    word = InputWord()
    erms = W.CheckWord(word)
    if erms:
      print(erms)
      continue    
    rs = W.Guess(word)
    if rs and rs != True:
      print(rs)
    elif rs == True:
      print(color("end",3))
      break

    print("Failed letters: " + str(W.failed_letters_))
