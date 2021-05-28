from typing import Dict, List
import matplotlib.pyplot as plt

def plot_pp(pps: Dict):
    """ Plots perplexity vs n for all languages in the corpus

    :param pps: dictionary with langs as keys and lists of perplexity scores as values
    """
    for j in range(0, len(list(pps.values())[0])):
        color = ['red', 'blue', 'green', 'pink']
        plt.figure(figsize=(10, 10), dpi=80)
        for i, (lang, pp) in enumerate(pps.items()): 
            lables = ['unigram']
            plt.plot(lables, [pp[j]], 'o', color=color[i])
        plt.legend(pps.keys())
        plt.title("Perplexity for " + str(j+1) + "gram model")
        plt.show()




def plot_pp_vs_alpha(pps: List[float], alphas: List[float]):
    """ Plots n-gram perplexity vs alpha
    :param pps: list of perplexity scores
    :param alphas: list of alphas
    """
    plt.figure(figsize=(10, 10), dpi=80)
    plt.plot(alphas,pps)
    plt.show()
