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
    self.pos_ = [a for a  in self.dict_]
    self.freq_ = {}
    self.sug_ = 0

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
    self.sug_ = 0

  """ update the set of words that would be feasible given
      current information """
  def UpdatePossibleWords(self):
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
    for r in removed:
      if not r in self.pos_:
        continue
      self.pos_.remove(r)

  """ Report the number of words left in dictionary """
  def NumLeft(self):
    return len(self.pos_)
  
  """ Helper function to calculate residual frequency table """
  def UpdateFreqTable(self):
    self.freq_ = {}
    for word in self.pos_:
      for i,ltr in enumerate(word):
        if self.correct_[i]:
          if not ltr in self.freq_:
            self.freq_[ltr] = 0
          continue
        if not ltr in self.freq_:
          self.freq_[ltr] = 1
        else:
          self.freq_[ltr] += 1
    
  def SortPos(self):
    ckey = lambda string: sum([self.freq_[ltr] for ltr in set(string) ])
    self.pos_.sort(key=ckey,reverse=True)

  """ Come up with the suggestion for next word """
  def SuggestWord(self):
    self.UpdateFreqTable()
    self.SortPos()
    togo = self.pos_[self.sug_]
    self.sug_+=1
    return togo


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
  sgt = W.SuggestWord()
  print("To start, I suggest: ")
  print(sgt)
  while True:
    print("Enter word or write 0 if you need a new word:")
    word = InputWord()    
    if word == "0":
      sgt = W.SuggestWord()
      print ("In that case, I suggest:")
      print(sgt)
      continue
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

    
