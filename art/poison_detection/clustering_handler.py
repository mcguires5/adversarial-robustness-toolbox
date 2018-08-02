from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn.decomposition import FastICA, PCA
from sklearn.cluster import KMeans
import numpy as np


class ClusteringHandler:
    """
    Class in charge of clustering activations by class
    """
    def __init__(self):
        """
        Constructor
        """

    def cluster_activations(self, separated_activations, n_clusters=2, ndims=10, reduce='FastICA',
                            clustering_method='KMeans'):
        """
        Clusters activations and returns two arrays
        1) separated_clusters: where separated_clusters[i] is a 1D array indicating which cluster each datapoint
        in the class has been assigned
        2) separated_reduced_activations: activations with dimensionality reduced using the specified reduce method
        :param separated_activations:  list where separated_activations[i] is a np matrix for the ith class where
        each row corresponds to activations for a given data point
        :type: separated_activations `list`
        :param n_clusters: number of clusters (defaults to 2 for poison/clean)
        :type n_clusters `int`
        :param ndims: number of dimensions to reduce activation to via PCA
        :type ndims `int`
        :param reduce: Method to perform dimensionality reduction, default is FastICA
        :type reduce `str`
        :param clustering_method: Clustering method to use, default is KMeans
        :return: separated_clusters, separated_reduced_activations
        """
        separated_clusters = []
        separated_reduced_activations = []

        if reduce == 'FastICA':
            projector = FastICA(n_components=ndims, max_iter=1000, tol=0.005)
        elif reduce == 'PCA':
            projector = PCA(n_components=ndims)
        else:
            print(reduce + " dimensionality reduction method not supported.")
            return

        if clustering_method == 'KMeans':
            clusterer = KMeans(n_clusters=n_clusters)
        else:
            print(clustering_method + " clustering method not supported.")
            return

        for i, ac in enumerate(separated_activations):
            # apply dimensionality reduction
            n_activations = np.shape(ac)[1]
            if n_activations > ndims:
                reduced_activations = projector.fit_transform(ac)
            else:
                print("Dimensionality of activations = %i less than ndims = %i. Not applying dimensionality "
                      "reduction..." % (n_activations, ndims))
                reduced_activations = ac
            separated_reduced_activations.append(reduced_activations)

            # get cluster assignments
            clusters = clusterer.fit_predict(reduced_activations)

            # clusters = np.array(clusters)

            separated_clusters.append(clusters)

        return separated_clusters, separated_reduced_activations
