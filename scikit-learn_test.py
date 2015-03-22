__author__ = 'jbenua'

from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
import numpy as np
from sklearn.svm import NuSVC


def sup_vm(X, y, test):
    clf = svm.SVC()
    clf.fit(X, y)
    print "svm:"
    print test, clf.predict(test)

def nu_svc(X, y, test):
    clf = NuSVC()
    clf.fit(X, y)
    print "nu_svc:"
    print test, clf.predict(test)


def svr(X, y, test):
    clf = svm.SVR()
    clf.fit(X, y)
    print "svr:"
    print test, clf.predict(test)


def nn_centroid(X, y, test):
    clf = NearestCentroid()
    clf.fit(X, y)
    print "nn_centroid:"
    print test, clf.predict(test)


def try_methods(X, Y, test):
    sup_vm(X, Y, test)
    nu_svc(X, Y, test)
    svr(X, Y, test)
    nn_centroid(X, Y, test)


if __name__ == "__main__":
    X1 = [[0, 0], [0.6, 0.3], [1, 1], [2, 2]]
    Y1 = [0, 0, 1, 1]
    tx1 = [[1.3, 0.7]]  # 1

    X2 = [[0, 0], [0.6, 0.3], [1, 1], [2, 2], [0, 2], [2, 3]]
    Y2 = [0, 0, 1, 1, 0, 0]
    tx2 = [[1.3, 0.7]]  # 1

    X3 = [[0, 0], [0.6, 0.3], [1, 1], [2, 2], [0, 2], [2, 3], [1.3, 0.7]]
    Y3 = [0, 0, 1, 1, 0, 0, 0]
    tx3 = [[1.5, 1.5]]  # middle

    X = np.array([[0, 0], [5, 5], [1, 1], [0.5, 0.5]])
    y = np.array([0, 2, 1, 1])
    test1 = [[1, 1]]
    test2 = [[2, 2]]

    try_methods(X1, Y1, tx1)
    try_methods(X2, Y2, tx2)
    try_methods(X, y, test1)
    try_methods(X, y, test2)
    try_methods(X3, Y3, tx3)