# Define imports
# from string import punctuation
import string
from collections import Counter
from nltk import bigrams, trigrams
import operator
from matplotlib.pyplot import plot


def preprocess(text) -> list:
    # TODO Exercise 2.2.
    """
    : param text: The text input which you must preprocess by
    removing punctuation and special characters, lowercasing,
    and tokenising

    : return: A list of tokens
    """
    clean = []
    for char in text.lower():
        if char in string.punctuation:
            pass
        else:
            clean.append(char)
    new = "".join(clean)
    tokens = new.split()

    return tokens

def find_ngram_probs(tokens, model='unigram') -> dict:
    # TODO Exercise 2.2
    """
    : param tokens: Pass the tokens to calculate frequencies
    param model: the identifier of the model ('unigram, 'bigram', 'trigram')
    You may modify the remaining function signature as per your requirements

    : return: n-grams and their respective probabilities
    """
    N = len(tokens)
    uni_count = Counter(tokens) # absolute frequency/count of each individual word (=unigram)

    if model=='unigram':
        probs = {k:(v/N) for (k,v) in uni_count.items()}

    bi = [(tokens[len(tokens)-1], tokens[0])] # making sure it's circular - should probs not hardcode this like this..
    bi += [bi for bi in bigrams(tokens)]
    bi_count = Counter(bi) # count of each bigram

    if model=='bigram':
        probs = {k:(v/uni_count[k[0]]) for (k,v) in bi_count.items()}
        
        
    tri = [(tokens[len(tokens)-2], tokens[len(tokens)-1], tokens[0]), (tokens[len(tokens)-1], tokens[0], tokens[1])]
    tri += [tri for tri in trigrams(tokens)]
    tri_counts = Counter(tri) # count of each trigram
    
    if model=='trigram':  
        probs = {k:(v/bi_count[(k[0], k[1])]) for (k,v) in tri_counts.items()}

    return probs


def plot_most_frequent(ngrams) -> None:
    # TODO Exercise 2.2
    """
    : param ngrams: The n-grams and their probabilities
    Your function must find the most frequent ngrams and plot their respective probabilities

    You may modify the remaining function signature as per your requirements
    """

    sort = dict( sorted(ngrams.items(), key=operator.itemgetter(1),reverse=True))
    plot(list(sort.keys())[:20], list(sort.values())[:20])

