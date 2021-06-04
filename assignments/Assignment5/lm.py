from collections import Counter
from copy import deepcopy
import numpy as np
from typing import List


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
        return tokens


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


def relative_frequencies(tokens:List, model:int=1) -> dict:
    """
    Should compute the relative n-gram frequencies of the test set of the corpus.
    :param tokens: the tokenized test set
    :param model: the identifier of the model ('unigram, 'bigram', 'trigram')
    :return: a dictionary with the ngrams as keys and the relative frequencies as values
    """
    relative_freqs= []

    for i in range(1, model+1):
        relative_freq = dict()
        if i ==1:
            ngram_tokens = tokens.copy()
        elif i == 2:
            ngram_tokens = ngram_generator(tokens)
        elif i == 3:
            ngram_tokens = ngram_generator(tokens, n=3)

        N = len(ngram_tokens)
        freqs = custom_counter(ngram_tokens)

        relative_freqs.append({k:v/N for k,v in freqs.items()})
    return relative_freqs



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
        self.test_rfs = relative_frequencies(test_tokens, N)
        self.lm = self.find_ngram_probs()


    def update_vocab(self,train_counts, test_counts) -> dict:
        """
        function that adds unseen test word in the test corpus as count 0
        :param train_counts: dictionary containing ngram pair as key and its count as value for train corpus.
        :param test_counts: dictionary containing ngram pair as key and its count as value for test corpus.
        
        : return updated dictionary adding the unseen test ngrams.
        """

        for k,v in test_counts.items():
            if k not in train_counts:
                train_counts[k] = 0
                
        return train_counts

    
    def find_ngram_probs(self) -> list:
        """

        : return: n-grams and their respective probabilities
        """
        probs = []
        for i in range(1, self.N+1):
            ngrams_train = [bi for bi in ngram_generator(self.train_tokens, n=i)]
            ngrams_test = [bi for bi in ngram_generator(self.test_tokens, n=i)]
            count_train = custom_counter(ngrams_train)
            count_test = custom_counter(ngrams_test)
            unsmoothened_count = self.update_vocab(count_train, count_test)
            smoothened_count = self.lidstone_smoothing(unsmoothened_count)

            if i==1:
                N = sum(list(unsmoothened_count.values()))
                smoothened_N = sum(list(smoothened_count.values()))
                probs.append({k:smoothened_count[k]/smoothened_N for k,v in unsmoothened_count.items()})
                previous_unsmoothened_count = unsmoothened_count.copy()
                v_prev = len(smoothened_count)
            else:
                temp_probs = dict()
                
                for pair in ngrams_test:
                    if i == 2:
                        set_prev = pair[0]
                    else:
                        set_prev = tuple(list(pair)[:-1])
                    temp_probs[pair] = smoothened_count[pair]/(self.alpha*v_prev + previous_unsmoothened_count[set_prev])

                previous_unsmoothened_count = unsmoothened_count.copy()
                probs.append(temp_probs)
        return probs

    
    def perplexity(self) -> list:
        """ returns the perplexity of the language model for n-grams with n=n """

        pps = []
        for lm,ref in zip(self.lm, self.test_rfs):
            P = np.array([lm[k] for k in list(ref.keys())])
            f = np.array(list(ref.values()))
            pp = np.log2(P) * f
            pps.append(1/(2**pp.sum()))
        return pps


    def lidstone_smoothing(self, unsmoothened_count: dict) -> dict:
        """ applies lidstone smoothing on train counts

        :param unsmoothened_count: the unsmoothed counts
        :return: the smoothed counts
        """

        return {key: (value + self.alpha) for key,value in unsmoothened_count.items()}
if __name__ == "__main__":
    train_tokens = ["I", "am", "a", "man", "not", "a", "mouse", "and", "also", "not", "a", "dog"]
    test_tokens = ["I", "am", "a", "cow", "not", "a", "horse"]

    LM = LanguageModel(train_tokens, test_tokens, N=3, alpha=1)
    pp = LM.perplexity()
    print(pp)



