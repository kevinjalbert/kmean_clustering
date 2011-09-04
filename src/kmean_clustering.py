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

class KMeanClustering():

  """Class that solves the problem of clustering a set of random data points
  into k clusters.

  The process is iterative and visually shown how the clusters convergence on
  the optimal solution.
  """

  def __init__(self):
    """Default constructor.
    """
    pass

  def graph_clusters(self, clusters, centroids):
    """Graphs the clusters and centroids in a scatter plot.

    Args:
      clusters: The clusters and their dataPoints
      centroids: The list of centroids
    """
    colors = ['r', 'b', 'g', 'c', 'm', 'y']
    pyplot.hold(False)
    for i in range(len(centroids)):

      # Split the cluster into x and y values
      x = []
      y = []
      for j in range(len(clusters[i])):
        x.append(clusters[i][j][0])
        y.append(clusters[i][j][1])

      # Graph the clustering
      pyplot.figure(0)
      pyplot.title("K Mean Clustering")
      pyplot.xlabel("X-Coordinate")
      pyplot.ylabel("Y-Coordinate")

      # Plot the clusters
      pyplot.hold(True)
      pyplot.plot(x, y, '.', color=colors[i%6], markersize=3)

      # Plot the centroids
      pyplot.hold(True)
      pyplot.plot(centroids[i][0], centroids[i][1], '.', color='k', markersize=8, alpha=0.6)

      pyplot.draw()

  def graph_RSS(self, allRSS):
    """Graphs the Residual Sum of Squares (RSS) of the clusters in a bar graph.

    Args:
      allRSS: A list of the RSS from the clusters
    """
    # Graph the RSS
    pyplot.figure(1)
    xlocations = numpy.array(range(len(allRSS)))
    pyplot.bar(xlocations, allRSS)
    pyplot.title("RSS of Clusters")
    pyplot.xlabel("Iteration")
    pyplot.ylabel("Value")
    pyplot.draw()

  def points_best_cluster(self, centroids, dataPoint):
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

  def new_centroid(self, cluster):
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

  def configure_clusters(self, centroids, dataPoints):
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
      idealCluster = self.points_best_cluster(centroids, dataPoints[i])
      clusters[idealCluster].append(dataPoints[i])

    return clusters

  def get_cluster_RSS(self, cluster, centroid):
    """Calculates the cluster's Residual Sum of Squares (RSS)

    Args:
      cluster: The list of data points of one cluster
      centroid: The centroid point of the corresponding cluster
    """
    sumRSS = 0
    for i in range(len(cluster)):
      sumRSS += pow(abs(numpy.linalg.norm(cluster[i]-centroid)), 2)
    return sumRSS

  def solve(self, dataPoints, k):
    """Iteratively clusters the dataPoints into the most appropriate cluster
    based on the centroid's distance. Each centroid's position is updated to
    the new mean of the cluster on each iteration. When the RSS doesn't change
    anymore then the best cluster configuration is found.

    Args:
      dataPoints: The set of random data points to be clustered
      k: The number of clusters
    """
    # Create the initial centroids and clusters
    centroids = numpy.random.randn(k, 2)
    clusters = self.configure_clusters(centroids, dataPoints)

    # Loop till algorithm is done
    allRSS = []
    notDone = True
    lastRSS = 0
    while (notDone):
      # Find Residual Sum of Squares of the clusters
      clustersRSS = []
      for i in range(len(clusters)):
        clustersRSS.append(self.get_cluster_RSS(clusters[i], centroids[i]) / len(dataPoints))
      currentRSS = sum(clustersRSS)
      allRSS.append(currentRSS)
      print "RSS", currentRSS

      # See if the kmean algorithm has converged
      if (currentRSS == lastRSS):
        notDone = False
      else:
        lastRSS = currentRSS

      # Update each of the centroids to the new mean location
      for i in range(len(centroids)):
        centroids[i] = self.new_centroid(clusters[i])

      # Reconfigure the clusters to the new centroids
      clusters = self.configure_clusters(centroids, dataPoints)

      self.graph_clusters(clusters, centroids)
    self.graph_RSS(allRSS)

def main():
  """Generate the random points and starts the kmean clustering algorithm.
  """
  # Generate random points
  dataPoints = numpy.random.randn(int(userArgs.points), 2)

  # Enable the graphing
  pyplot.ion()

  # Cluster data using kmean clustering
  kmean = KMeanClustering()
  kmean.solve(dataPoints, int(userArgs.k))

# If this module is ran as main
if __name__ == '__main__':

  # Define the argument options to be parsed
  parser = argparse.ArgumentParser(
      description = 'kmean clustering algorithm <https://github.com/kevinjalbert/kmean_clustering>',
      version = 'kmean_clustering 0.2.0',
      usage = 'python kmean_clustering.py [OPTIONS]')
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

  print "Press any key to exit..."
  raw_input()