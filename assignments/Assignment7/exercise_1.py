import numpy as np
from collections import defaultdict
import math

class CountTree():
  def __init__(self, n=4):

      self.ngrams = dict()
  


  def add(self, ngram):

      for i in range(0, len(ngram)):
          each = ngram[i:len(ngram)+1]
          if each in self.ngrams:
              self.ngrams[each] += 1
          else:
              self.ngrams[each] = 1
    

  def get(self, ngram):

      if ngram in self.ngrams:
          return self.ngrams[ngram]
      else:
          for i in range(1, len(ngram)):
              each = ngram[i:len(ngram)+1]
              if self.ngrams.get(each,0) != 0:
                  return self.ngrams[each]
      return 0


  def perplexity(self, ngrams, vocab):
      """
      params:
      ngrams (list) :
      vocab (set) : 
      returns: perplexity value as float
      """
     
      V = len(vocab)
      rf = dict()
      for ngram in ngrams:
          if ngram in rf:
              rf[ngram] += 1
          else:
              rf[ngram] = 1

      rf = {k:v/len(rf) for k,v in rf.items()}
      cf = dict()
      for k,v in rf.items():
          if self.get(k) != 0:
              cp = self.get(k)/self.get(k[1:]) * 0.75
          else:
              cp = V * 0.25
          cf[k] = cp
      
      P = list(cf.values())
      f = list(rf.values())
      pp = np.log2(P) * f 
      pp = 1/(2**pp.sum())
      return pp
     

  def prune(self, k):
      """
      params: k (int): pruning threshold.
      returns: None 

      """


      for kk,v in self.ngrams.items():
          if v<=4:
              pruned = None
              for i in range(1, len(kk)):
                  each = kk[-i:]
                  if pruned is None:
                      if self.ngrams.get(each,0) <= k:
                          self.ngrams[kk] = self.get(each)
                          pruned = self.get(each)
                  else:
                      self.ngrams[each] = pruned 

      
      



