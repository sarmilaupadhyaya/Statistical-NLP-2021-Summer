from typing import List, Dict
import string
#Add imports

def preprocess(text) -> List:

    clean = []

    # remove punctuation

    for char in text.lower():
        if char in string.punctuation:
            pass
        else:
            clean.append(char)
    new = "".join(clean)

    tokens = new.split()

    return tokens


def train_test_split_data(text:List, test_size:float=0.1):

    test_split = int(len(text) * test_size)
    train = text[:(len(text)-test_split)]
    test = text[(len(text)-test_split):]


    return train, test


def get_oov_rates(train:List, test:List) -> List:
    return []


def plot_oov_rates(oov_rates:Dict) -> None:
    pass