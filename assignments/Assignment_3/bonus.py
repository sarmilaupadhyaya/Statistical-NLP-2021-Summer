from typing import List
import math


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


def find_ngram_probs(tokens, model='unigram') -> dict:
    """
    : param tokens: Pass the tokens to calculate frequencies
    param model: the identifier of the model ('unigram, 'bigram', 'trigram')
    You may modify the remaining function signature as per your requirements
    : return: n-grams and their respective probabilities
    """
    N = len(tokens)
    uni_count = custom_counter(tokens) # absolute frequency/count of each individual word (=unigram)

    if model=='unigram':
        probs = {k:(v/N) for (k,v) in uni_count.items()}

    bi = [bi for bi in ngram_generator(tokens, n=2)]
    bi_count = custom_counter(bi) # count of each bigram

    if model=='bigram':
        probs = {k:(v/uni_count[k[0]]) for (k,v) in bi_count.items()}
        
        
    tri = [tri for tri in ngram_generator(tokens, n=3)]
    tri_counts = custom_counter(tri) # count of each trigram
    
    if model=='trigram':  
        probs = {k:(v/bi_count[(k[0], k[1])]) for (k,v) in tri_counts.items()}

    return probs

def dkl(P:List[float], Q:List[float]) -> float:
    """
    Calculates the Kullback-Leibler-Divergence of two probability distributions
    :param P: the ground truth distribution
    :param Q: the estimated distribution
    :return: the DKL of the two distribution, in bits
    """
    to_sum = []
    jedan = zip(P.values(),Q.values())
    for el in jedan:
        to_sum.append(el[1] * math.log((el[1]/el[0]))) # D_KL(Q1 || P1) = sum(q_i*log(q_i/p_i))


    return sum(to_sum)
