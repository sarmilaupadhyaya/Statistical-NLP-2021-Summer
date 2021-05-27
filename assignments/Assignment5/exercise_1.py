from typing import List, Dict
from collections import Counter
import matplotlib.pyplot as plt

#Add imports

def preprocess(text) -> List:

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


def train_test_split_data(text:List, test_size:float=0.1):

    test_split = int(len(text) * test_size)
    train = text[:(len(text)-test_split)]
    test = text[(len(text)-test_split):]


    return train, test


def get_oov_rates(train:List, test:List) -> List:
    
    counted = sorted(Counter(train).items(), key=lambda item: item[1], reverse=True)
    vocab = [el[0] for el in counted[:15000]]
    print(len(vocab))
    all_oovs = []

    for i in range(1000,len(vocab),1000):
        
        unseen = [token for token in test if token not in vocab[:i]]
        
        oov = (len(unseen) / len(test)) * 100
        
        all_oovs.append(oov)

    return all_oovs


def plot_oov_rates(oov_rates:Dict) -> None:
    
    color = ['red', 'blue', 'green', 'pink']
    lengths = [8108, 15000, 14556, 15000]
    plt.figure(figsize=(10, 7), dpi=80)
    for ind, el in enumerate(oov_rates.values()):
        plt.loglog(range(1000, lengths[ind], 1000), sorted(el, reverse=True), color=color[ind], marker='o')
    plt.legend(oov_rates.keys())
    plt.xticks(range(1000, 15000, 1000), ['1k', '2k', '3k', '4k', '5k', '6', '7k', '8k', '9k', '10k', '11k', '12k', '13k', '14k'])
    plt.show()