from .emotiv import Emotiv
from sklearn import svm
from peewee import *
import scikit_test

db = MySQLDatabase('headset', host='localhost', user='jbenua', passwd='jbenua')


class users(Model):
    id = IntegerField()
    username = CharField()
    passwd = CharField()

    class Meta:
        database = db


class tags(Model):
    id = IntegerField()
    tag = TextField()

    class Meta:
        database = db


class raw(Model):
    id = IntegerField()
    f3 = IntegerField()
    fc6 = IntegerField()
    p7 = IntegerField()
    t8 = IntegerField()
    f7 = IntegerField()
    f8 = IntegerField()
    t7 = IntegerField()
    p8 = IntegerField()
    af4 = IntegerField()
    f4 = IntegerField()
    af3 = IntegerField()
    o2 = IntegerField()
    o1 = IntegerField()
    fc5 = IntegerField()
    x = IntegerField()
    y = IntegerField()
    unknown = IntegerField()

    class Meta:
        database = db


class sessions(Model):
    id = IntegerField()
    raw_id = IntegerField()
    tag_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        database = db

db.create_tables([users, raw, tags, sessions], safe=True)


class User(object):
    def __init__(self):
        self.vk = False
        self.vk_token = False
        self.fb = False
        self.userid = -1
        self.username = ""
        self.current_session_raw = []
        self.current_session_id = -1
        self.prev_tags = []
        self.prev_data = []
        self.db = db

    def print_all_info(self):
        print("id: ", self.userid)
        print("name: " + self.username)
        print("current raw: ", self.current_session_raw)
        print("current raw_id:", self.current_session_id)
        print("previous tags: ", self.prev_tags)
        print("previous sessions: ", self.prev_data)

    def read_data(self):
        try:
            a = Emotiv()
            self.current_session_raw = a.setupWin()
            # a.device.close()
            self.get_raw_id()
            return True
        except Exception as err:
            print("Error reading raw data! ")
            for t in err.args:
                print(t)
            return False

    def get_raw_id(self):
        try:
            res = raw.get(raw.f3 == self.current_session_raw[0],
                          raw.fc6 == self.current_session_raw[1],
                          raw.p7 == self.current_session_raw[2],
                          raw.t8 == self.current_session_raw[3],
                          raw.f7 == self.current_session_raw[4],
                          raw.f8 == self.current_session_raw[5],
                          raw.t7 == self.current_session_raw[6],
                          raw.p8 == self.current_session_raw[7],
                          raw.af4 == self.current_session_raw[8],
                          raw.f4 == self.current_session_raw[9],
                          raw.af3 == self.current_session_raw[10],
                          raw.o2 == self.current_session_raw[11],
                          raw.o1 == self.current_session_raw[12],
                          raw.fc5 == self.current_session_raw[13],
                          raw.x == self.current_session_raw[14],
                          raw.y == self.current_session_raw[15],
                          raw.unknown == self.current_session_raw[16])
        except raw.DoesNotExist:
            res = raw.create(f3=self.current_session_raw[0],
                             fc6=self.current_session_raw[1],
                             p7=self.current_session_raw[2],
                             t8=self.current_session_raw[3],
                             f7=self.current_session_raw[4],
                             f8=self.current_session_raw[5],
                             t7=self.current_session_raw[6],
                             p8=self.current_session_raw[7],
                             af4=self.current_session_raw[8],
                             f4=self.current_session_raw[9],
                             af3=self.current_session_raw[10],
                             o2=self.current_session_raw[11],
                             o1=self.current_session_raw[12],
                             fc5=self.current_session_raw[13],
                             x=self.current_session_raw[14],
                             y=self.current_session_raw[15],
                             unknown=self.current_session_raw[16])
            print("it's a new raw")
        finally:
            self.current_session_id = res.id

    def fill_info(self, name, pswd):
        db.connect()
        self.username = name
        get_id = users.get(
          users.username == self.username, users.passwd == pswd)
        self.userid = get_id.id
        try:
            get_tags_and_raw = sessions.select(
              sessions.tag_id, sessions.raw_id).where(
              sessions.user_id == self.userid)
            for i in get_tags_and_raw:
                get_raw = raw.select(raw.f3, raw.fc6, raw.p7, raw.t8, raw.f7,
                                     raw.f8, raw.t7, raw.p8, raw.af4, raw.f4,
                                     raw.af3, raw.o2, raw.o1, raw.fc5, raw.x,
                                     raw.y, raw.unknown).where(
                                     raw.id == i.raw_id)
                for j in get_raw:
                    self.prev_data.append([
                      j.f3, j.fc6, j.p7, j.t8, j.f7, j.f8, j.t7, j.p8, j.af4,
                      j.f4, j.af3, j.o2, j.o1, j.fc5, j.x, j.y, j.unknown])
                self.prev_tags.append(i.tag_id)
        except sessions.DoesNotExist:
            print("no previous data found")
        finally:
            db.close()

    def detect(self):
        # test
        # self.current_session_raw = [
        #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # self.get_raw_id()
        #
        if self.current_session_raw and (n_of_classes(self.prev_tags) > 1):
            # maybe change the method
            clf = svm.SVC()
            clf.fit(self.prev_data, self.prev_tags)
            a = clf.predict(self.current_session_raw)
            temp = []
            db.connect()
            for i in a:
                try:
                    get_tags = tags.get(tags.id == i).tag
                    temp.append(get_tags)
                except tags.DoesNotExist:
                    print('nothing was found')
            #
            #
            # tests
            mach = scikit_test.Learn().test(
              self.prev_data, self.prev_tags, self.current_session_raw)
            mach_out = []
            for i in mach:
                try:
                    get_tags = tags.get(tags.id == i).tag
                    mach_out.append(get_tags)
                except tags.DoesNotExist:
                    print('nothing was found')
            print("svm, nn, tree: ", mach_out)
            #
            #
            db.close()
            return temp
        else:
            return ['Lack of data']


def n_of_classes(lst):
    seen = set()
    for x in lst:
        if x in seen:
            continue
        seen.add(x)
    return len(seen)
