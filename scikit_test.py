from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import tree


class Learn(object):
    def test(self, X, Y, test):
        t = [self.sup_vm(X, Y, test),
             self.nn_centroid(X, Y, test),
             self.d_tree(X, Y, test)]
        print "\n"
        return t

    def d_tree(self, X, y, test):
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, y)
        t = clf.predict(test)
        print "tree:", t
        return t

    def sup_vm(self, X, y, test):
        clf = svm.SVC()
        clf.fit(X, y)
        t = clf.predict(test)
        print "svm:", t
        return t

    def nn_centroid(self, X, y, test):
        clf = NearestCentroid()
        clf.fit(X, y)
        t = clf.predict(test)
        print "nn_centroid:", t
        return t

    def try_methods(self, X, Y, test):
        # print "X =", X, "\nY =", Y, "\ntest =", test, "\n"
        self.sup_vm(X, Y, test)
        self.nn_centroid(X, Y, test)
        self.d_tree(X, Y, test)
        print "\n"

if __name__ == "__main__":
    a = Learn()
    X1 = [[0, 0], [0, 2], [2, 2], [2, 0]]
    Y3 = [0, 1, 2, 3]
    tx3 = [[1.000000000000001, 1.000000000000001]]  # - dtree
    a.try_methods(X1, Y3, tx3)
    X2 = [[0, 0], [0, 2], [2, 2], [2, 0]]
    Y2 = [0, 1, 0, 1]
    tx2 = [[1, 1]]
    a.try_methods(X2, Y2, tx2)  # - nn_centroid
    a.try_methods([[0, 0], [1, 1]], [0, 1], [[2., 2.]])
