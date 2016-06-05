from .emotiv import Emotiv
from sklearn import svm
import scikit_test

from .db_model import raw, users, sessions, tags


class User:

    def __init__(self, db):
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
        self.classifier = None

    def print_all_info(self):
        print("id: ", self.userid)
        print("name: " + self.username)
        print("current raw: ", self.current_session_raw)
        print("current raw_id:", self.current_session_id)
        print("previous tags: ", self.prev_tags)
        print("previous sessions: ", self.prev_data)

    # def read_data(self):
        # try:
        #     a = Emotiv()
        #     self.current_session_raw = a.setupWin()
        # a.device.close()
        #     self.get_raw_id()
        #     return True
        # except Exception as err:
        #     print("Error reading raw data! ")
        #     for t in err.args:
        #         print(t)
        #     return False

    def get_raw_id(self, this_raw):
        try:
            res = raw.get(raw.f3 == this_raw[0],
                          raw.fc6 == this_raw[1],
                          raw.p7 == this_raw[2],
                          raw.t8 == this_raw[3],
                          raw.f7 == this_raw[4],
                          raw.f8 == this_raw[5],
                          raw.t7 == this_raw[6],
                          raw.p8 == this_raw[7],
                          raw.af4 == this_raw[8],
                          raw.f4 == this_raw[9],
                          raw.af3 == this_raw[10],
                          raw.o2 == this_raw[11],
                          raw.o1 == this_raw[12],
                          raw.fc5 == this_raw[13],
                          raw.x == this_raw[14],
                          raw.y == this_raw[15],
                          raw.unknown == this_raw[16])
        except raw.DoesNotExist:
            res = raw.create(f3=this_raw[0],
                             fc6=this_raw[1],
                             p7=this_raw[2],
                             t8=this_raw[3],
                             f7=this_raw[4],
                             f8=this_raw[5],
                             t7=this_raw[6],
                             p8=this_raw[7],
                             af4=this_raw[8],
                             f4=this_raw[9],
                             af3=this_raw[10],
                             o2=this_raw[11],
                             o1=this_raw[12],
                             fc5=this_raw[13],
                             x=this_raw[14],
                             y=this_raw[15],
                             unknown=this_raw[16])
            print("it's a new raw")
        finally:
            self.current_session_id = res.id

    def fill_info(self, name, pswd):
        self.db.connect()
        self.username = name
        this_user = users.get(
            users.username == self.username, users.passwd == pswd)
        self.userid = this_user.id
        try:
            entries = sessions.select(
                sessions.tag_id, sessions.raw_id).where(
                    sessions.user_id == self.userid)
            print(entries)
            for entry in entries:
                get_raw = raw.select().where(
                    raw.id == entry.raw_id)
                for item in get_raw:
                    print(item)
                    self.prev_data.append([
                        item.f3, item.fc6, item.p7, item.t8,
                        item.f7, item.f8, item.t7, item.p8,
                        item.af4, item.f4, item.af3, item.o2,
                        item.o1, item.fc5, item.x, item.y,
                        item.unknown])
                self.prev_tags.append(entry.tag_id)
        except sessions.DoesNotExist:
            print("no previous data found")
        finally:
            self.db.close()
        self.classifier = svm.SVC()

    def detect(self):
        self.classifier.fit(self.prev_data, self.prev_tags)
        # test
        # self.current_session_raw = [
        #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # self.get_raw_id()
        #
        if self.current_session_raw and len(set(self.prev_tags)) > 1:
            # maybe change the method
            a = self.classifier.predict(self.current_session_raw)
            temp = []
            self.db.connect()
            for i in a:
                try:
                    get_tags = tags.get(tags.id == i).tag
                    temp.append(get_tags)
                except tags.DoesNotExist:
                    print('nothing was found')
            #
            #
            # tests
            # mach = scikit_test.Learn().test(
            #     self.prev_data, self.prev_tags, self.current_session_raw)
            # mach_out = []
            # for i in mach:
            #     try:
            #         get_tags = tags.get(tags.id == i).tag
            #         mach_out.append(get_tags)
            #     except tags.DoesNotExist:
            #         print('nothing was found')
            # print("svm, nn, tree: ", mach_out)
            # #
            #
            self.db.close()
            return temp
        else:
            return ['Lack of data']
