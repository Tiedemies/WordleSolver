#! /usr/bin/python3.8
import sys

""" WordleFinder finds good matches from the dictionary """
class WordleFinder:
  """ Initialize """
  def __init__(self, dictfile="dict_5.txt", n = 5, hard = True):
    self.dict_ = self.ReadDict(dictfile)
    self.tried_words_ = set([])
    self.failed_letters_ = set([])
    self.correct_ = {i: None for i in range(n)}
    self.let_correct_ = {}
    self.let_found_ = {i: set([]) for i in range(n)}
    self.contain_letters_ = {}
    self.n_ = 5
    self.hard_ = hard
    self.pos_ = []

  """ Read dictionary and return it as set of strings """
  def ReadDict(self,dictfile):
    handle = open(dictfile,'r')
    dict = set([])
    for string in handle.readlines():
      dict.add(string.strip())
    return dict
  """ Checks if a word can be tried, return None if OK """
  def CheckWord(self,word):
    if self.n_ != len(word):
      return "Wrong length"
    if word in self.tried_words_:
      return "Already tried" 
    for i in range(len(word)):
      if self.correct_[i] and word[i] != self.correct_[i] and self.hard_:
        return "Wrong letter not allowed in hard mode"
      if word[i] in self.let_found_[i] and self.hard_:
        return "Repeated attempt of wrong place"
      if self.hard_ and word[i] in self.failed_letters_:
        return "Failed letter retry"
    if not word in self.dict_:
      return "Not in dictionary"
    return None

  """ insert a word hint that has 'correct' indices """
  def InsertWord(self, word, correct, found):
    erms = self.CheckWord(word)
    if erms:
      raise ValueError()
    self.tried_words_.add(word)
    self.contain_letters_ = {}
    for i in range(len(word)):
      if i in correct:
        self.correct_[i] = word[i]
        if not word[i] in self.contain_letters_:
          self.contain_letters_[word[i]] = 1
        else:
          self.contain_letters_[word[i]] += 1
      elif i in found:
        self.let_found_[i].add(word[i])
        if not word[i] in self.contain_letters_:
          self.contain_letters_[word[i]] = 1
        else:
          self.contain_letters_[word[i]] += 1
      else:
        self.failed_letters_.add(word[i])
    self.UpdatePossibleWords()

  """ update the set of words that would be feasible given
      current information """
  def UpdatePossibleWords(self):
    if len(self.pos_) == 0:
      ## Copy the dictioary
      self.pos_ = set([word for word in self.dict_])
    ## Next rule out everything that does not match. 
    removed = []
    for word in self.pos_:
      lettercount = {a: self.contain_letters_[a] for a in self.contain_letters_}
      for i,ltr in enumerate(word):
        if self.correct_[i] and self.correct_[i] != ltr:
          removed.append(word)
          break
        if ltr in self.failed_letters_:
          removed.append(word)
          break
        if ltr in self.let_found_[i]:
          removed.append(word)
          break
        if ltr in lettercount:
          lettercount[ltr] -= 1
      for a in lettercount:
        if lettercount[a] > 0:
          removed.append(word)
    self.pos_.difference_update(removed)
  """ Report the number of words left in dictionary """
  def NumLeft(self):
    return len(self.pos_)

  """ Come up with the suggestion for next word """
  def SuggestWord(self):
  ## Just pick a random word
    if len(self.pos_) > 0:
      return self.pos_.pop()
    else:
      return False

def InputWord():
  return input().strip()
def InputIndexList():
  thelist = []
  y = input()
  for strn in y.split():
    thelist.append(int(strn))
  return thelist

if __name__ == "__main__":
  W = WordleFinder()
  while True:
    print("Enter word:")
    word = InputWord()    
    erms = W.CheckWord(word)
    if erms:
      print(erms)
      continue
    print("Enter correct indices separated by white space:")
    correct = InputIndexList()
    print("Enter indices of found letters: ")
    found = InputIndexList()
    W.InsertWord(word,correct,found)
    sgt = W.SuggestWord()
    if sgt:
      print("Number of words left: ")
      print(W.NumLeft())
      print("I would suggest you next try: ")
      print(sgt)
    else:
      print("No more words left.")
      break

    
