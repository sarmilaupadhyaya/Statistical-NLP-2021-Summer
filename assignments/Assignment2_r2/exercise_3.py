import random
import numpy as np
from typing import Dict, List
from exercise_2 import preprocess
import matplotlib.pyplot as plt


def ngram_generator(tokens:List, n=2):

    """

    """
    if n==2:
        return list(zip(tokens[-1:]+tokens[:-1], tokens))
    elif n==3:
        return list(zip(tokens[-2:]+tokens[:-2],tokens[-1:]+tokens[:-1], tokens))
    else:
        return []


def Counter(items:List) -> dict:
    """

    """

    items_count = dict()

    for item in items:
        if item in items_count:
            items_count[item] += 1
        else:
            items_count[item] = 1
    return items_count


def train_test_split(corpus:List, test_size:float) -> (List, List):
    """
    Should split a corpus into a train set of size len(corpus)*(1-test_size)
    and a test set of size len(corpus)*test_size.
    :param text: the corpus, i. e. a list of strings
    :param test_size: the size of the training corpus
    :return: the train and test set of the corpus
    """
    #not sure if I can shuffle the data using random package
    random.shuffle(corpus)
    split_index = int(len(corpus) * (1-test_size))
    return corpus[:split_index], corpus[split_index:]


def relative_frequencies(tokens:List, model='unigram') -> dict:
    """
    Should compute the relative n-gram frequencies of the test set of the corpus.
    :param tokens: the tokenized test set
    :param model: the identifier of the model ('unigram, 'bigram', 'trigram')
    :return: a dictionary with the ngrams as keys and the relative frequencies as values
    """
    relative_freq = dict()

    if model == "bigram":
        tokens = ngram_generator(tokens)
    elif model == "trigram":
        tokens = ngram_generator(tokens, n=3)

    N = len(tokens)
    freqs = Counter(tokens)

    return {k:v/N for k,v in freqs.items()}


def pp(lm:Dict, rfs:Dict) -> float:
    """
    Should calculate the perplexity score of a language model given the relative
    frequencies derived from a test set.
    :param lm: the language model (from exercise 2)
    :param rfs: the relative frequencies
    :return: a perplexity score
    """
    
    P = np.array([lm[k] for k in rfs.keys()])
    f = np.array(list(rfs.values()))
    pp = np.log2(P) *f
    return 1/(2**pp.sum())


def plot_pps(pps:List) -> None:
    """
    Should plot perplexity value vs. language model
    :param pps: a list of perplexity scores
    :return:
    """
    labels = ['unigram', 'bigram', 'trigram']
    plt.plot(labels, pps, 'bo')
    plt.show()
