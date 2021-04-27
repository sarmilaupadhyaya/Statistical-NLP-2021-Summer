# QUESTION: Can we use external packages? (i presume we can since they also used some lol)

from nltk import FreqDist
import matplotlib.pyplot as plt
from matplotlib.pyplot import loglog

def analysis(name, data):
	
	""" 
	 Plot Zipfian distribution of words + true Zipfian distribution. Compute MSE.

  	:param name: title of the graph
  	:param data: list of words
  
  	"""
	
# 	  NOTE: just Zipfian dist, needs "true Zipfian dist" + MSE

	freq = FreqDist(data)                # freq - frequency distribution
	sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)   # sorted_freq - frequency distribution sorted by values in descending order
	freq_values = [i[1] for i in sorted_freq]
	x = [i for i in range(1, (len(freq_values) + 1))]   # x - sequence of numbers from 1 to the # of tokens  
	plt.loglog(x, freq_values, "bo")
	plt.title("Log plot - {}".format(name))
	plt.show()

  
#   print("TODO", name)
