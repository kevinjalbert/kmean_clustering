""" Script that drives the kmean algorithm after parsing the user parameters.

The user inputed parameters are used to customize the kmean algorithm's
parameters. The progress of the convergence of the optimal clustering is shown 
in each iteration using pyplot.
"""
import numpy
import matplotlib
matplotlib.use('GTKAgg') # For linux gtk
from matplotlib import pyplot
import argparse

userArgs = None

class kmeanClustering():

  """Class that solves the problem of clustering a set of random data points
  into k clusters.

  The process is iterative and visually shown how the clusters convergence on
  the optimal solution.
  """

  def solve(self, dataPoints, k):
    """Iteratively clusters the dataPoints into the most appropriate cluster
    based on the centroid's distance. Each centroid's position is updated to the
    new mean of the cluster on each iteration. When no movement is detected the
    best cluster configuration is found.

    Attributes:
      dataPoints: The set of random data points to be clustered
      k: The number of clusters
    """
    pass

def main():
  """Generate the random points and initialize the data structures to hold the
  cluster, centroids, and data points.
  """

  # Generate random points
  dataPoints = numpy.random.randn(int(userArgs.points), 2)

  # Enable the graphing
  pyplot.ion()

  # Cluster data using kmean clustering
  kmean = kmeanClustering()
  kmean.solve(dataPoints, int(userArgs.k))

# If this module is ran as main
if __name__ == '__main__':

  # Define the argument options to be parsed
  parser = argparse.ArgumentParser(
      description = 'kmean clustering algorithm <https://github.com/kevinjalbert/kmean_clustering>',
      version = 'kmean_clustering 0.1.0',
      usage = 'python kmean_clustering.py [OPTIONS]')
  parser.add_argument(
      '--verbose',
      action='store_true',
      default=False,
      dest='verbose',
      help='Displays additional information during execution')
  parser.add_argument(
      '-k',
      action='store',
      default=3,
      dest='k',
      help='Number of k clusters [Default=3]')
  parser.add_argument(
      '--points',
      action='store',
      default=100,
      dest='points',
      help='Number of random points [Default=100]')

  # Parse the arguments passed from the shell
  userArgs = parser.parse_args()

  main()