import numpy as np
import sklearn

from sklearn.cluster import KMeans

class LlcSpatialPyramidEncoder:
    """
    Class which computes locality-constrained linear codes for a codebook of
    features and a set of features, that have to be encoded. The features must
    be in a spatial pyramid structure. The encoding algorithm is based on Wang
    et als. publication "Locality-constrained Linear Coding for Image
    Classification" (2010 CVPR).

    :author: Joschka Strüber
    """

    def __init__(self, size=None, codebook=None, alpha=1, sigma=1):
        """
        :author: Joschka Strüber
        :param size: int
        The number of features in the codebook.
        :param codebook: ndarray
        Set of features in a matrix, which is a good representation of the
        feature space. Usually, this will be trained based on a larger set of
        features, but a precomputed codebook can be used as well.
        :param alpha: float (default = 1)
        Hyperparameter for regularization, which affects how much choosing
        non-local bases of the codebook is penalized.
        :param sigma: float (default = 1)
        Hyperparameter for regularization, which is used for adjusting the
        weight decay speed of the locality adaptor.
        """
        self.size = size
        self.codebook = codebook
        self.alpha = alpha
        self.sigma = sigma

    def train_codebook(self, features, size=1024):
        """
        Trains a codebook as the cluster centers for a larger set of features.
        k-means is the used clustering algorithm.
        :author: Joschka Strüber
        :param size: unsigned int (default 1024)
        Number of cluster centers for the codebook.
        :param features: ndarray
        ndarray of features, which will be clustered for the codebook.
        :return: None
        """
        # size of codebook must be maximum of number of features and wanted size
        if features.shape[0] >= size:
            self.size = size
        else:
            self.size = features.shape[0]
        k_means_clusters = KMeans(n_clusters=self.size).fit(X=features)
        self.codebook = k_means_clusters.cluster_centers_

    def encode(self, spatial_pyramid, pooling='max', normalization='eucl'):
        """
        Computes a locality-constrained linear code for a spatial pyramid of
        feature vectors based on the classes codebook using the specified
        pooling and normalization methods.
        For each of the 21 spatial bins (level 0: 1, level 1: 4, level 2: 16) a
        pooled and normalized code will be computed. These 21 codes are
        concatenated and returned.

        :author: Joschka Strüber
        :param spatial_pyramid: ndarray
        A spatial pyramid of feature vectors, which is three layers deep. It is
        a nested ndarray of 4 of four array of 4 array each of features. C.f.
        Lazebnik et al.'s publication "Beyond bags of features: spatial pyramid
        matching for recognizing natural scene categories" (2006 CVPR).
        Each of the 16 most inner array holds the features of a level 2 spatial
        bin. A level 1 spatial bin consists of all features of all level 2 bins
        that are part of the same inner array. The level 0 spatial bin consists
        of all features.
        Example:
        [[f0, f1, f2, f3], ..., [f12, f13, f14, f15]]
        The array of features f0 is a level 2 spatial bin, {f0, ..., f3} is a
        level 1 spatial bin and {f0, ..., f15} is the level 0 spatial bin.
        :param pooling: {'max' (default), 'sum'}
        The method used for pooling the locality-constrained linear codes of
        each feature. The supported pooling methods are max pooling (default)
        and sum pooling.
        :param normalization: {'eucl' (default), 'sum'}
        The method used for normalizing the pooled encoding. The euclidean norm
        (default) and sum normalization are supported.
        :return: array of doubles
        The concatenation of the pooled and normalized codes for all 21 spatial
        bins. The first part corresponds to the level 0 bin, followed by level
        1, followed by level 2. In case of an error, None will be returned.
        """
        codes = []

        for level1_spatial_bin in spatial_pyramid:
            for level2_spatial_bin in level1_spatial_bin:
                level2_code = self._encode_spatial_bin(level2_spatial_bin,
                                                       pooling, normalization)
                codes.append(level2_code)

        spm_code = np.concatenate(codes).ravel()
        return spm_code


    def _encode_spatial_bin(self, features, pooling='max',
                            normalization='eucl'):
        """
        Computes the LLC codes for a set of features, pools them with the
        specified pooling method and returns them after normalization.
        """
        return 0

    def _get_llc_code(self, feature):
        """
        Computes a LLC code based on the feature vector and the codebook.
        """

        """
        Broadcast the feature into a matrix that is self.size times the feature.
        Example: feature = [1, 2], self.size = 3.
        Then the result will be:
        [[1, 2],
         [1, 2],
         [1, 2]]
        Use this matrix to center the codebook around the input feature vector.
        """
        centered = self.codebook - np.broadcast_to(feature, (self.size,
                                                             len(feature)))
        cov = np.dot(centered, centered.T)

        llc_code_unnormalized = np.solve 

        return 0

