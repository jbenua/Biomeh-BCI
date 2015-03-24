__author__ = 'user'
from emotiv import Emotiv
from sklearn import svm

class User(object):
    def __init__(self):
        self.userid = -1
        self.username = ""
        self.current_session_raw = []
        self.prev_tags = []
        self.prev_data = []

    def print_all_info(self):
        print "id: ", self.userid
        print "name: " + self.username
        print "current raw: ", self.current_session_raw
        print "previous tags: ", self.prev_tags
        print "previous sessions: ", self.prev_data

    def read_data(self):
        try:
            a = Emotiv()
            self.current_session_raw = a.setupWin()
        except Exception as err:
            a.device.close()
            print "Error reading raw data! "
            for t in err.args:
                print t

    def fill_info(self, db, name, pswd):
        self.username = name
        get_id = "SELECT id FROM users WHERE username='" + self.username + "' AND passwd='" + pswd+"'"
        u_id = db.execute_sql(get_id)
        for i in u_id:
            self.userid = i[0]
        get_tags = "SELECT tag_id, raw_id FROM sessions WHERE user_id = '" + str(self.userid) + "'"
        tags = db.execute_sql(get_tags)
        for i in tags:
            get_raw_t = "SELECT f3, fc6, p7, t8, f7, f8, t7, p8, af4, f4, af3, o2, o1, fc5, x, y, unknown from raw " +\
                "WHERE id = '" + str(i[1]) + "'"
            each_tag = db.execute_sql(get_raw_t)
            temp = []
            for j in each_tag:
                for a in j:
                    temp.append(a)
            self.prev_data.append(temp)
            self.prev_tags.append(i[0])

    def detect(self, db):
        # test
        self.current_session_raw = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #
        if self.current_session_raw!=[]:
            # maybe change the method
            clf = svm.SVC()
            clf.fit(self.prev_data, self.prev_tags)
            a = clf.predict(self.current_session_raw)
            print "svm:", clf.predict(self.current_session_raw)
            temp = []
            db.connect()
            for i in a:
                get_tags = "SELECT tag FROM tags WHERE id = '" + str(i) + "'"
                res = db.execute_sql(get_tags)
                for j in res:
                    l = str(j).split("'")
                    temp.append(l[1])
            db.close()
            return temp
        else:
            return ['Nothing was read']
