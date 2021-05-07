# Define imports
import string
import operator
import matplotlib.pyplot as plt


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


def preprocess(text) -> list:
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

    # bi = [(tokens[len(tokens)-1], tokens[0])] # making sure it's circular - should probs not hardcode this like this..
    bi = [bi for bi in ngram_generator(tokens, n=2)]
    bi_count = custom_counter(bi) # count of each bigram

    if model=='bigram':
        probs = {k:(v/uni_count[k[0]]) for (k,v) in bi_count.items()}
        
        
    # tri = [(tokens[len(tokens)-2], tokens[len(tokens)-1], tokens[0]), (tokens[len(tokens)-1], tokens[0], tokens[1])]
    tri = [tri for tri in ngram_generator(tokens, n=3)]
    tri_counts = custom_counter(tri) # count of each trigram
    
    if model=='trigram':  
        probs = {k:(v/bi_count[(k[0], k[1])]) for (k,v) in tri_counts.items()}

    return probs


def plot_most_frequent(ngrams, prev=None, model=None) -> None:
    """
    : param ngrams: The n-grams and their probabilities
    Your function must find the most frequent ngrams and plot their respective probabilities

    You may modify the remaining function signature as per your requirements
    """

    if model=='unigrams':
        sort = dict(sorted(ngrams.items(), key=operator.itemgetter(1),reverse=True))
       

    else:
	    with_most_freq_uni = {el:v for (el,v) in ngrams.items() if el[:-1] == prev}    
	    sort = dict(sorted(with_most_freq_uni.items(), key=operator.itemgetter(1),reverse=True))

	    
    x_k = [str(el) for el in list(sort.keys())[:20]]
    y_v = list(sort.values())[:20]
    plt.plot(x_k, y_v)
    plt.xticks(rotation=90)
    plt.show()

    if model=='unigrams':
        return tuple([list(sort.keys())[0]])
    else:
        return list(sort.keys())[0]







