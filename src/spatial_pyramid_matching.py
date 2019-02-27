import cv2
from sklearn.svm import LinearSVC

from src.feature_extraction import FeatureExtraction
from src.llc_spatial_pyramid_encoding import LlcSpatialPyramidEncoder
from src.segment import segment


if __name__ == '__main__':
    # load data, assign labels and split into test and training data

    # segment the images to get only the regions of interest with animals

    # select random images from every category to get features to train the
    # codebook
    sift = cv2.xfeatures2d.SIFT_create()
    extractor = FeatureExtraction(sift)

    # extract dense features from every image for encoding

    # encode all training and test images

    # save LLC codes and labels in arrays for training and prediction
    training_codes = None
    testing_codes = None
    training_labels = None
    testing_labels = None

    # train an SVM with linear kernel
    classifier = LinearSVC()
    classifier.fit(training_codes, training_labels)

    # use test images for verification
    result = classifier.score(testing_codes, testing_labels)
    print("The mean accuracy of the classification was: {}".format(result))

