from Bio import SeqIO
from collections import Counter
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import math
import re





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



def get_nucleotides(location):

    nucleotides = ''
    with open(location, 'r') as handle:
        for record in SeqIO.parse(handle, "fasta"):
            nucleotides += record.seq

    return nucleotides



def sample_records(genome_loc: Path, genome_red_loc: Path, num_records: int):
    """ Samples n reads from a fasta file and saves them to a new file.

    :param genome_loc: path to the unreduced file
    :param genome_red_loc: path to the reduced file
    :num_records: number of reads to sample
    """
    sequence = SeqIO.parse(genome_loc.absolute(), 'fasta')
    sequence = list(sequence)

    genome_red_loc.touch()
    handle = genome_red_loc.open('w')
    
    for _ in range(num_records):
        index = np.random.randint(len(sequence))
        SeqIO.write(sequence[index], handle, 'fasta')
    

def get_k_mers(genome_red_loc: Path, k: int, remove_seq_error: bool = False) -> List[str]:
    """ Samples k-mers from a fasta file (preferrably the reduced one).
        See also https://en.wikipedia.org/wiki/K-mer
    :param genome_loc: path to the fasta file
    :param k: length of of the n-mer
    :param remove_seq_error: bool value to remove the error "N" or not.
    :return: a list of n-mers
    """

    nucleo = get_nucleotides(genome_red_loc).upper()

    if remove_seq_error:
        nucleo = nucleo._data.replace("N", "")
    kmers = []
    for i in range(len(nucleo)-k+1):
        current_kmer = tuple(nucleo[i:i+k])
        kmers.append(current_kmer)

    return kmers



def get_k_mers_24(genome_red_loc: Path, k: int, tandem_repeats=False) -> List[str]:
    """ Samples k-mers from a fasta file (preferrably the reduced one), but this time 
        only for tandem repeat regions or non tandem repeat regions.

    :param genome_loc: path to the fasta file
    :param k: length of of the n-mer
    :param tandem_repeats: get only tandem repeats or non-tandem repeats
    :return: a list of n-mers
    """
    nucleo = get_nucleotides(genome_red_loc)
    kmers = []
    if not tandem_repeats:
        nucleo = re.findall('[A-Z]', nucleo._data)
    else:
        nucleo = re.findall('[a-z]', nucleo._data)

    for i in range(len(nucleo)-k+1):
        current_kmer = tuple(nucleo[i:i+k])
        kmers.append(current_kmer)

    return kmers



def k_mer_statistics(genome_red_loc: Path, K: int, delta=1.e-10, remove_seq_error = False) -> Tuple:
    """ Calculates relative k-mer frequencies and conditional k-mer probabilities 
        on the provided fasta file.

    :param genome_red_loc: path to the fasta file
    :param K: upper bound of the k of k-mers
    :param delta: threshold for probability mass loss, defaults to 2.e-10
    :param remove_seq_error: bool value to remove the error "N" or not.
    :return: lists of relative frequencies and conditional probabilities
    """
    prev_re_freqs = None
    total_rel_freqs = []
    total_cond_prob = []
    for k in range(1,K+1):

        k_grams = get_k_mers(genome_red_loc, k, remove_seq_error)
        abs_freqs = custom_counter(k_grams)
        N = sum(abs_freqs.values())
        relative_freqs = {k: v/N for k, v in abs_freqs.items()}

        try:
            assert abs(1 - sum(relative_freqs.values())) <= delta
            print("K-mers relative frequency for k = " + str(k) +" has probability mass loss acceptable")
        except:
            print("K-mers relative frequency for k = " + str(k) +" do not have probability mass loss acceptable")


        if prev_re_freqs is None:
            conditional_probs = relative_freqs.copy()
        else:
            conditional_probs = {p:(v/prev_re_freqs[tuple(list(p)[0:(k-1)])]) for p,v in relative_freqs.items()} 
        prev_re_freqs = relative_freqs
        total_rel_freqs.append(relative_freqs)
        total_cond_prob.append(conditional_probs)

    return total_rel_freqs, total_cond_prob





def k_mer_statistics_24(genome_red_loc: Path, K: int, tandem_repeats=False, delta=1.e-10) -> Tuple:
    """ Calculates relative k-mer frequencies and conditional k-mer probabilities 
        on the provided fasta file, but this time only for tandem repeat regions 
        or non tandem repeat regions.

    :param genome_red_loc: path to the fasta file
    :param K: upper bound of the k of k-mers
    :param tandem_repeats: get only tandem repeats or non-tandem repeats
    :param delta: threshold for probability mass loss, defaults to 1.e-10
    :return: lists of relative frequencies and conditional probabilities
    """
    prev_re_freqs = None
    total_rel_freqs = []
    total_cond_prob = []
    for k in range(1,K+1):

        k_grams = get_k_mers_24(genome_red_loc, k, tandem_repeats)
        abs_freqs = custom_counter(k_grams)
        N = sum(abs_freqs.values())
        relative_freqs = {k: v/N for k, v in abs_freqs.items()}

        try:
            assert abs(1 - sum(relative_freqs.values())) <= delta
            print("K-mers relative frequency for k = " + str(k) +" has probability mass loss acceptable")
        except:
            print("K-mers relative frequency for k = " + str(k) +" do not have probability mass loss acceptable")

        if prev_re_freqs is None:
            conditional_probs = relative_freqs.copy()
        else:
            conditional_probs = {p:(v/prev_re_freqs[tuple(list(p)[0:(k-1)])]) for p,v in relative_freqs.items()}
        prev_re_freqs = relative_freqs
        total_rel_freqs.append(relative_freqs)
        total_cond_prob.append(conditional_probs)

    return total_rel_freqs, total_cond_prob



def conditional_entropy(rel_freqs: Dict, cond_probs: Dict) -> float:
    """ Calculates the conditional entropy of a corpus given by relative k-mer frequencies
        and conditional k-mer probabilities

    :param rel_freqs: (a dictionary of) relative frequencies
    :param cond_probs: (a dictionary of) conditional probabilities
    :return: the conditional entropy of the corpus
    """

    values = zip(rel_freqs.values(), cond_probs.values())
    to_sum = []
    for el in values:
        to_sum.append(el[0] * math.log(el[1],2))


    return -sum(to_sum)




def plot_k_mers(rel_freqs: List[Dict], n=10, k=5, title=""):
    """ Plots n most frequent k-mers vs. their frequency.

    :param rel_freqs: the list of relative frequency dicts
    :param n: the number of most frequent k-mers to plot
    :param k: the k of k-mers
    :params title: title for the plot
    """
    colors = ["red", "blue", "orange", "purple", "yellow"]
    
    for k, v in enumerate(rel_freqs):

        sorted_freqs = dict(sorted(v.items(), key=lambda item: item[1], reverse=True))
        plt.loglog(range(0, len(sorted_freqs)), sorted_freqs.values(),'o', colors[k])
    
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.figure(figsize=(10, 10), dpi=80)
    plt.show()







def plot_conditional_entropies(H_ks:List[float], title):
    """ Plots conditional entropy vs. k-mer length

    :param H_ks: the conditional entropy scores
    :params title: title for the plot
    """
    xax = range(1,21)
    plt.plot(xax, H_ks, 'bo')
    plt.title(title)
    plt.xticks(xax)
    plt.xlabel("K-mer")
    plt.ylabel("Conditional entropy")
    plt.show()

