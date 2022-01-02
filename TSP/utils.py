"""
For defining utility/helper methods
"""
import numpy
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    coordinates_array = numpy.array(locations)
    dist_array = pdist(coordinates_array, 'cityblock')
    dist_matrix = squareform(dist_array)
    return dist_matrix
