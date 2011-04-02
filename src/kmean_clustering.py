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
import copy

userArgs = None

class kmeanClustering():

  """Class that solves the problem of clustering a set of random data points
  into k clusters.

  The process is iterative and visually shown how the clusters convergence on
  the optimal solution.
  """

  def __init__(self):
    pass

  def graph(self, clusters, centroids):
    """Graphs the clusters and centroids in a matplotlib plot.

    Args:
      clusters: The clusters and their dataPoints
      centroids: The list of centroids
    """
    colors = ['r', 'b', 'g', 'c', 'm', 'y']
    markers = ['.', ',', 'x', '+', '_', '|']
    pyplot.hold(False)
    for i in range(len(centroids)):

      # Split the cluster into x and y values
      x = []
      y = []
      for j in range(len(clusters[i])):
        x.append(clusters[i][j][0])
        y.append(clusters[i][j][1])

      # Plot the clusters
      pyplot.hold(True)
      pyplot.plot(x, y, markers[i%6], color=colors[i%6])

      # Plot the centroids
      pyplot.hold(True)
      pyplot.plot(centroids[i][0], centroids[i][1], '*', color='black', markersize=10, alpha=0.3)
      pyplot.draw()

  def pointsBestCluster(self, centroids, dataPoint):
    """Takes the dataPoint and find the centroid index that it is closest too.

    Args:
      centroids: The list of centroids
      dataPoint: The dataPoint that is going to be determined which centroid it
        is closest too
    """

    closestCentroid = None
    leastDistance = None
    for i in range(len(centroids)):
      distance = numpy.linalg.norm(dataPoint-centroids[i])
      if (distance < leastDistance or leastDistance == None):
        closestCentroid = i
        leastDistance = distance
    return closestCentroid

  def newCentroid(self, cluster):
    """Finds the new centroid location given the cluster of data points. The
    mean of all the data points is the new location of the centroid.

    Args:
      cluster: A single cluster of data points, used to find the new centroid
    """

    # Split the cluster into x and y values
    x = []
    y = []
    for i in range(len(cluster)):
      x.append(cluster[i][0])
      y.append(cluster[i][1])

    return [numpy.mean(x), numpy.mean(y)]

  def configureClusters(self, centroids, dataPoints):
    """Creates a new configuration of clusters for the given set of dataPoints
    and centroids.

    Args:
      centroids: The list of centroids
      dataPoints: The set of random data points to be clustered

    Return:
        The set of new cluster configurations around the centroids
    """

    # Create the empty clusters
    clusters = []
    for i in range(len(centroids)):
      cluster = []
      clusters.append(cluster)

    # For all the dataPoints, place them in initial clusters
    for i in range(int(userArgs.points)):
      idealCluster = self.pointsBestCluster(centroids, dataPoints[i])
      clusters[idealCluster].append(dataPoints[i])

    return clusters

  def getMovement(self, centroids, lastCentroids):
    """Calculates the sum of the movements between the last centroid position
    to that of the new centroid positions.

    Args:
      centroid: The list of the current centroids
      lastCentroids: The list of the previous centroids

    Return:
      The sum of the total movement between the last centroids to that of the
        new centroids
    """

    # Sum of distance between corresponding centroids
    movement = 0
    for i in range(len(centroids)):
      movement += numpy.linalg.norm(centroids[i]-lastCentroids[i])
    return movement

  def solve(self, dataPoints, k):
    """Iteratively clusters the dataPoints into the most appropriate cluster
    based on the centroid's distance. Each centroid's position is updated to
    the new mean of the cluster on each iteration. When no movement is detected
    the best cluster configuration is found.

    Args:
      dataPoints: The set of random data points to be clustered
      k: The number of clusters
    """

    # Create the initial centroids and clusters
    centroids = numpy.random.randn(k, 2)
    clusters = self.configureClusters(centroids, dataPoints)

    # Loop till no more movement
    movement = True
    while (movement):
      lastCentroids = copy.copy(centroids)

      # Update each of the centroids to the new mean location
      for i in range(len(centroids)):
        centroids[i] = self.newCentroid(clusters[i])

      centroidMovement = self.getMovement(centroids, lastCentroids)
      print "Movement", centroidMovement

      if (centroidMovement == 0):
        movement = False
      else:
        lastCentroidtMovement = centroidMovement

      clusters = self.configureClusters(centroids, dataPoints)
      self.graph(clusters, centroids)

def main():
  """Generate the random points and starts the kmean clustering algorithm.
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