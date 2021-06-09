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
      """
     
      V = len(vocab)
      rf = dict()
      for ngram in ngrams:
          if ngram in rf:
              rf[ngram] += 1
          else:
              rf[ngram] = 1

      rf = {k:v/len(rf) for k,v in rf.items() if k in self.ngrams}
      cf = { k:self.ngrams[k]/self.ngrams[k[1:]] for k,v in rf.items() }
      
      P = list(cf.values())
      f = list(rf.values())
      pp = np.log2(P) * f
      pp = 1/(2**pp.sum()) * 0.75 + V * 0.25
      return pp
      
  def prune(self, k):

      for kk,v in self.ngrams.items():
          if v<=4:
              for i in range(1, len(kk)):
                  each = kk[i:len(kk)+1]
                  if self.ngrams.get(each,0) >= k:
                      self.ngrams[kk] = k


