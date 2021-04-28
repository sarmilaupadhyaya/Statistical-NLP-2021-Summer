import math
import numpy as np
from numpy.random import Generator, PCG64
import matplotlib.pyplot as plt

G = Generator(PCG64())

def stick_breaking(n:int,alpha:float) -> np.ndarray:
  """
  Draws n samples from a stick-breaking process with beta distribution intensity alpha.

  :param n: number of samples
  :param alpha: intensity parameter of the beta distribution
  :returns: stick lengths
  """
  betas = G.beta(a=alpha, b=1.0, size=n)
  betas[1:] *= np.cumprod(1-betas[:-1])
  weights = np.sort(betas)[::-1]
  return weights

def plot_stick_lengths(stick_lengths:np.array,
		       alpha:float,
		       B:int) -> None:
  """
  Plots -log2(sticks)
  :param sticks: list of stick lenghts
  """
  sticks = [-B * math.log2(stick_length) for stick_length in stick_lengths]
  fig = plt.figure()
  ax = fig.subplots()
  ax.loglog(sticks)
  plt.xlabel("Rank")
  plt.ylabel("Stick Length (log2)")
  plt.show()
