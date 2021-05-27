from collections import Counter
from copy import deepcopy
import numpy as np
from typing import List
from utils import relative_frequencies, find_ngram_probs


def ngram_generator(tokens:list, n=2) -> list:

    """
     : param tokens: list of strings from which you have to get word pairs.

    : return: A list of tuples of ngrams
    
    """
    if n==2:
        return list(zip(tokens[-1:]+tokens[:-1], tokens))
    elif n==3:
        return list(zip(tokens[-2:]+tokens[:-2],tokens[-1:]+tokens[:-1], tokens))
    else:
        return []


def custom_counter(items:list) -> dict:
    """
      : param items: list of word pairs or words depending upon the model.

    : return: dictionary containing the count of word pair or words.
    """

    items_count = dict()

    for item in items:
        if item in items_count:
            items_count[item] += 1
        else:
            items_count[item] = 1
    return items_count


def relative_frequencies(tokens:List, model=1) -> dict:
    """
    Should compute the relative n-gram frequencies of the test set of the corpus.
    :param tokens: the tokenized test set
    :param model: the identifier of the model ('unigram, 'bigram', 'trigram')
    :return: a dictionary with the ngrams as keys and the relative frequencies as values
    """
    relative_freq = dict()

    if model == 2:
        tokens = ngram_generator(tokens)
    elif model == 3:
        tokens = ngram_generator(tokens, n=3)

    N = len(tokens)
    freqs = custom_counter(tokens)

    return {k:v/N for k,v in freqs.items()}



class LanguageModel:
    
    def __init__(self, train_tokens: List[str], test_tokens: List[str], N: int, alpha: float, epsilon=1.e-10):
        """ 
        :param train_tokens: list of tokens from the train section of your corpus
        :param test_tokens: list of tokens from the test section of your corpus
        :param N: n of the highest-order n-gram model
        :param alpha: pseudo count for lidstone smoothing
        :param epsilon: threshold for probability mass loss, defaults to 1.e-10
        """
        self.N = N
        self.alpha = alpha
        self.train_tokens = train_tokens
        self.test_tokens = test_tokens
        self.test_rfs = relative_frequencies(test_tokens)
        self.lm = self.find_ngram_probs()


    def update_vocab(self,train_ngrams, test_counts):
        """

        """

        for test_count in test_counts:
            if test_count not in train_counts:
                self.train_counts[test_count] = 0
        return train_counts

    
    def find_ngram_probs(self) -> dict:
        """
        : param tokens: Pass the tokens to calculate frequencies
        param model: the identifier of the model (1,2,3)
        You may modify the remaining function signature as per your requirements

        : return: n-grams and their respective probabilities
        """

        uni_count_train = custom_counter(self.train_tokens) # absolute frequency/count of each individual word (=unigram)
        uni_count_test = custom_counter(self.test_tokens)
        uni_unsmoothened_count = update_vocab(uni_count_train, uni_count_test)

        if self.N==1:
            uni_smoothened_count = lidstone_smoothing(uni_unsmoothened_count) 
            N = sum(list(uni_unsmoothened_count.values()))
            uni_smoothened_N = sum(list(uni_smoothened_count.values())) * self.alpha + N
            probs = {k:v/uni_smoothened_N for k,v in uni_smoothened_N.items()}
        else:
            bi_count_train = [bi for bi in ngram_generator(self.train_tokens, n=2)]
            bi_count_test = [bi for bi in ngram_generator(self.train_tokens, n=2)]
            bi_unsmoothened_count = update_vocab(bi_count_train, bi_count_test)

            if self.N==2:
                bi_smoothened_count = lidstone_smoothing(bi_unsmoothened_count)

                probs = dict()
                for pair,value in bi_smoothened_count.items():
                    v = [1 for k,v in bi_smoothened_count.items() if k[0] == pair[0]]
                    probs[pair] = value/(self.alpha*v + uni_unsmoothened_count[pair[0]])
 
            elif self.N == 3:
                tri_count_train = [tri for tri in ngram_generator(self.train_tokens, n=3)]
                tri_count_test = [tri for tri in ngram_generator(self.train_tokens, n=3)]
                tri_unsmoothened_count = update_vocab(tri_count_train, tri_count_test)

                tri_smoothened_count = lidstone_smoothing(tri_unsmoothened_count)

                probs = dict()
                for pair,value in tri_smoothened_count.items():
                    v = [1 for k,v in tri_smoothened_count.items() if (k[0] == pair[0] and k[1] == pair[1])]
                    probs[pair] = value/(self.alpha*v + bi_unsmoothened_count[(pair[0],pait[1])])

        return probs

    
    def perplexity(self, n: int):
        """ returns the perplexity of the language model for n-grams with n=n """

        P = np.array([self.lm[k] for k in self.test_rfs.keys()])
        f = np.array(list(self.test_rfs.values()))
        pp = np.log2(P) * f
        return pp


    def lidstone_smoothing(self, unsmoothened_count: dict):
        """ applies lidstone smoothing on train counts

        :param unsmoothened_count: the unsmoothed counts
        :return: the smoothed counts
        """

        return {key: (value + self.alpha) for key,value in unsmoothened_count.items()}

        
