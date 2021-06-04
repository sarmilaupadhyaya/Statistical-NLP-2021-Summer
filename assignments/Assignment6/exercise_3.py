import matplotlib.pyplot as plt
from typing import List
import string


def train_test_split_data(text: List[str], test_size=0.2):
    """ Splits the input corpus in a train and a test set
    :param text: input corpus
    :param test_size: size of the test set, in fractions of the original corpus
    :return: train and test set
    """

    test_split = int(len(text) * test_size)
    train = text[:(len(text)-test_split)]
    test = text[(len(text)-test_split):]


    return train, test


def k_validation_folds(text: List[str], k_folds=10):
    """ Splits a corpus into k_folds cross-validation folds
    :param text: input corpus
    :param k_folds: number of cross-validation folds
    :return: the cross-validation folds
    """
    chunk = len(text) / float(k_folds)
    results = []
    i = 0.0

    while i < len(text):
        results.append(text[int(i):int(i + chunk)])
        i += chunk

    return results


def plot_pp_vs_alpha(pps: List[float], alphas: List[float]):
    """ Plots n-gram perplexity vs alpha
    :param pps: list of perplexity scores
    :param alphas: list of alphas
    """
    plt.figure(figsize=(10, 10), dpi=80)
    plt.plot(alphas,pps)
    plt.xlabel("alphas")
    plt.ylabel("perplexity")
    plt.title("alphas vs perplexity")
    plt.show()



def preprocess(text) -> List:
    """
    preprocess
    """
    clean = []
    # remove punctuation
    for char in text.lower():
        if char.isalnum() == True or char.isspace():
            clean.append(char)
        else:
            pass
    new = "".join(clean)
    tokens = new.split()
    return tokens

