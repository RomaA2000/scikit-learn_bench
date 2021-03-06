# Copyright (C) 2020 Intel Corporation
#
# SPDX-License-Identifier: MIT

import argparse
from bench import (
    parse_args, measure_function_time, load_data, print_output, accuracy_score
)
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

parser = argparse.ArgumentParser(
    description='scikit-learn kNN classifier benchmark')

parser.add_argument('--n-neighbors', default=5, type=int,
                    help='Number of neighbors to use')
parser.add_argument('--weights', type=str, default='uniform',
                    help='Weight function used in prediction')
parser.add_argument('--method', type=str, default='brute',
                    help='Algorithm used to compute the nearest neighbors')
parser.add_argument('--metric', type=str, default='euclidean',
                    help='Distance metric to use')
params = parse_args(parser)

# Load generated data
X_train, X_test, y_train, y_test = load_data(params)
params.n_classes = len(np.unique(y_train))

# Create classification object
knn_clsf = KNeighborsClassifier(n_neighbors=params.n_neighbors,
                                weights=params.weights,
                                algorithm=params.method,
                                metric=params.metric)

knn_clsf.fit(X_train, y_train)
# Time predict
time, yp = measure_function_time(knn_clsf.predict, X_test, params=params)

acc = 100 * accuracy_score(yp, y_test)

columns = ('batch', 'arch', 'prefix', 'function', 'threads', 'dtype', 'size',
           'n_neighbors', 'n_classes', 'time')

print_output(library='sklearn', algorithm='knn_classification',
             stages=['prediction'], columns=columns, params=params,
             functions=['knn_clsf.predict'], times=[time], accuracies=[acc],
             accuracy_type='accuracy[%]', data=[X_test], alg_instance=knn_clsf)
