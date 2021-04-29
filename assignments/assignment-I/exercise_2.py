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
  
  stick_lengths = [stick_length**B for stick_length in stick_lengths]
  ideal_zipf = [stick_lengths[0]/i for i in range(1,len(stick_lengths)+1)]
  fig, ax = plt.subplots(figsize=(8,8))
  ax.set_xscale("log", basex=2)
  ax.set_yscale("log", basey=2)
  ax.plot(stick_lengths, label = "stick length")
  ax.plot(ideal_zipf, label="ideal zipfs law")
  ax.legend(loc="upper right")
  plt.xlabel("Rank")
  plt.ylabel("Stick Length")
  ax.title.set_text('Stick Length and Ideal Zipfs Plot for alpha {} and B {}'.format(alpha, B))
