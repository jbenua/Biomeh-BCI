__author__ = 'user'
from emotiv import Emotiv

class User(object):
    def __init__(self):
        self.userid = -1
        self.username = ""
        self.current_session_raw = []
        self.prev_data = {}

    def print_all_info(self):
        print "id: ", self.userid
        print "name: " + self.username
        print "current raw: ", self.current_session_raw
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
        get_tags = "SELECT DISTINCT tag_id FROM sessions WHERE user_id = '" + str(self.userid) + "'"
        tags = db.execute_sql(get_tags)
        t = []
        for i in tags:
            t.append(i[0])
        for i in t:
            get_raw_t = "SELECT f3, fc6, p7, t8, f7, f8, t7, p8, af4, f4, af3, o2, o1, fc5, x, y, unknown from raw " +\
                "WHERE id in (SELECT raw_id FROM sessions WHERE user_id= '" + str(self.userid) + "' AND " +\
                "tag_id = '" + str(i) + "')"
            each_tag = db.execute_sql(get_raw_t)
            lst_raw = []
            for j in each_tag:
                lst_raw.append(j)
            self.prev_data[i] = lst_raw