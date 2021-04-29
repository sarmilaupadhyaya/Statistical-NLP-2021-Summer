import matplotlib.pyplot as plt
from matplotlib.pyplot import loglog
import numpy as np

def analysis(name, data):
    """ 
     Plot Zipfian distribution of words + true Zipfian distribution. Compute MSE.

      :param name: title of the graph
      :param data: list of words

      """
    counts = [(word, data.count(word) / len(data)) for word in set(data)] 
    sorted_freq = sorted(counts, key = lambda x: x[1], reverse=True)
    rank = range(1,len(sorted_freq)+1)
    freq_list = [tup[1] for tup in sorted_freq]
    # ideal = [sorted_freq[0][1]/r for r in rank]

    denom = sum([1/r for r in rank])

    ideal = [(1/r)/denom for r in rank]

    mse = ((np.array(ideal) - np.array(freq_list))**2).mean()


    plt.loglog(rank, freq_list, "bo")
    plt.loglog(rank, ideal, "r")
    plt.title("Log plot - {}".format(name))
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.show()

    print(f"MSE, {name} = {mse}")
