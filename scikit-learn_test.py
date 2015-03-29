__author__ = 'jbenua'

from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.svm import NuSVC
from sklearn import tree


def d_tree(X, y, test):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    print "tree:", clf.predict(test)


def sup_vm(X, y, test):
    clf = svm.SVC()
    clf.fit(X, y)
    print "svm:", clf.predict(test)


def nu_svc9(X, y, test):
    clf = NuSVC(nu=0.9999999999999999)
    clf.fit(X, y)
    print "nu_svc(0.9...9):", clf.predict(test)


def nu_svc1(X, y, test):
    clf = NuSVC(nu=0.000000000000001)
    clf.fit(X, y)
    print "nu_svc(0.0....1):", clf.predict(test)


def nn_centroid(X, y, test):
    clf = NearestCentroid()
    clf.fit(X, y)
    print "nn_centroid:", clf.predict(test)


def try_methods(X, Y, test):
    print "X =", X, "\nY =", Y, "\ntest =", test, "\n"
    sup_vm(X, Y, test)
    nu_svc1(X, Y, test)
    nu_svc9(X, Y, test)
    nn_centroid(X, Y, test)
    d_tree(X, Y, test)
    print "\n"

if __name__ == "__main__":
    X1 = [[0, 0], [0, 2], [2, 2], [2, 0]]
    Y3 = [0, 1, 2, 3]
    tx3 = [[1.000000000000001, 1.000000000000001]]
    try_methods(X1, Y3, tx3)