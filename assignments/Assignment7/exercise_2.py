import string
import re
from collections import Counter
from typing import List, Tuple

#TODO: Implement
def preprocess(text) -> List:
    '''
    params: text-text corpus
    return: tokens in the text
    '''

    clean = []

    # remove punctuation

    for char in text.lower():
        if char in string.punctuation:
            clean.append(" ")
        else:
            clean.append(char)

    new = "".join(clean)
    tokens = new.split()

    return tokens


class KneserNey:
    def __init__(self, tokens: List[str], N: int, d: float):
        '''
        params: tokens - text corpus tokens
        N - highest order of the n-grams
        d - discounting paramater
        '''
        self.d = d
        self.tokens = tokens
        pass

    def get_n_grams(self, tokens: List[str], n: int) -> List[Tuple[str]]:


        '''

    
        A function that generates n-grams from a given list of tokens.

        :param token: - list of tokens
        :param n: - n


        Returns:
        * n-grams - list of n-grams


        '''

        ngrams = []
        for i in range(len(tokens)-n+1):
            ngram = tuple(tokens[i:i+n])
            ngrams.append(ngram)

        return ngrams


    def starting_with_ngram(self, ngrams, higher_ngrams, n=2):


        '''
        
         A function that determins how many n+1-grams start with a particular n-gram.

        :param ngrams: - list of n-grams
        :param higher_ngrams: - list of n+1-grams (from corpus)
        :param n: - n

        Returns:

        * starting_with_ngram - dict; key: n-gram, value: how many n+1-grams start with that particular n-gram

        '''


        starting_with_ngram = {}
        for n_lower in ngrams:
            temp = 0
            for n_higher in set(higher_ngrams):

                if n ==1 and n_higher[:n] == tuple([n_lower]):
                    temp += 1
                elif n > 1 and n_higher[:n] == tuple(n_lower):
                    temp += 1

            starting_with_ngram[n_lower] = temp

        return starting_with_ngram


    def ending_with_ngram(self, ngrams, higher_ngrams, n=2):

        ''' 

        A function that determins how many n+1-grams end with a particular n-gram.

        :param ngrams: - list of n-grams
        :param higher_ngrams: - list of n+1-grams (from corpus)
        :param n: - n

        Returns:

        * ending_with_ngram - dict; key: n-gram, value: how many n+1-grams end with that particular n-gram

        '''

        ending_with_ngram = {}

        for n_lower in ngrams:
            if n > 1:
                n_lower = list(n_lower)
            temp = 0
            for n_higher in set(higher_ngrams):
                
                n_higher_list = list(n_higher)
                n_higher_list.reverse()
                
                n_higher_slice = n_higher_list[:n]
                n_higher_slice.reverse()

                if n ==1 and n_higher_slice[0] == n_lower:
                    temp += 1
                elif n > 1 and n_higher_slice == n_lower:
                    temp += 1
            if n == 1:
                ending_with_ngram[n_lower] = temp
            else:
                ending_with_ngram[tuple(n_lower)] = temp


        return ending_with_ngram


    def unigram_in_middle_of_trigram(self, unigram, higher_ngrams):


        '''
        
        A function determining how many trigrams have a particular unigram in the second position.

        :param ngrams: - list of n-grams
        :param higher_ngrams: - list of n+1-grams (from corpus)
        :param n: - n

        Returns:

        * uni_in_middle - dict; key: unigram, value: how many trigrams have a particular unigram in the middle

        '''


        uni_in_middle = {}
        for uni in unigram:
            temp = 0
            for trig in higher_ngrams:

                if trig[1] == uni:
                    temp += 1

            uni_in_middle[uni] = temp

        return uni_in_middle



    def get_params(self, trigram) -> None:

        '''


        A function estimating the necessary parameters for calculating the Kneser-Ney probabilities.

        :param trigram: - a trigram whose proability is being determined


        Returns:
        * None

        '''


        preprocessed = self.tokens

        trigs = self.get_n_grams(preprocessed, n=3)
        bigs = self.get_n_grams(preprocessed, n=2)

        counted_trigs = Counter(trigs)
        counted_bigs = Counter(bigs)
        counted_unis = Counter(preprocessed)

        print('|V| =', len(counted_unis.keys()))
        print('N+(**) =', len(counted_bigs.keys()))

        bigram_from_trig = self.get_n_grams(preprocess(trigram), n=2) # list of bigrams made from the given preprocessed trigram
        unigram_from_trig = list(set(preprocess(trigram))) # list of unigrams from the given preprocessed trigram
        prep = self.get_n_grams(preprocess(trigram), n=3)[0] # the trigram in the correct format

        print('N(w1w2w3) = ', counted_trigs[self.get_n_grams(preprocess(trigram), n=3)[0]]) # how many times the trigram appears
        print('N(w1w2) = ', counted_bigs[bigram_from_trig[0]]) # how many times the first two words (bigram) appears in the corpus together

        start_with_big = self.starting_with_ngram(bigram_from_trig, trigs) # how many trigrams start with the bigram
        start_with_uni = self.starting_with_ngram(unigram_from_trig, bigs, n=1) # how many bigrams start with the unigram

        print('N(w1w2*) =', start_with_big)
        print('N(w2*) - unigrams =', start_with_uni)


        end_with_bigs = self.ending_with_ngram(bigram_from_trig, trigs) # how many trigrams end with the bigrams
        end_with_unis = self.ending_with_ngram(unigram_from_trig, bigs, n=1) # how many bigrams end with the unigram

        print('N(*w2w3) =', end_with_bigs)
        print('N(*w3) =', end_with_unis)

        uni_in_middle = self.unigram_in_middle_of_trigram(unigram_from_trig, trigs)
        print('N(*w2*) =', uni_in_middle)

        lam_big = {}
        for b, c in start_with_big.items():
            try:
                lam_big[b] = (self.d / counted_bigs[b]) * c
            except ZeroDivisionError:
                lam_big[b] = 0

        print('lambda - bigrams:', lam_big)

        lam_uni = {}
        for u, c in start_with_uni.items():
            try:
                lam_uni[u] = (self.d / counted_unis[u]) * c
            except ZeroDivisionError:
                lam_uni[u] = 0


        print('lambda - unigrams:', lam_uni)
        print()