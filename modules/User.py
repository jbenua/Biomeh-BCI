from sklearn import svm
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

    def add_tag(self, tag_name, raw_ids):
        tag_id = tags.create(tag=tag_name)
        for id_ in raw_ids:
            sessions.create(
                tag_id=tag_id,
                raw_id=id_,
                user_id=self.userid)

    def put_raws(self, raws):
        ids = []
        for index in range(len(raws['f3'])):
            id_ = raw.create(f3=raws['f3'][index],
                             fc6=raws['fc6'][index],
                             p7=raws['p7'][index],
                             t8=raws['t8'][index],
                             f7=raws['f7'][index],
                             f8=raws['t8'][index],
                             t7=raws['t7'][index],
                             p8=raws['p8'][index],
                             af4=raws['af4'][index],
                             f4=raws['f4'][index],
                             af3=raws['af3'][index],
                             o2=raws['o2'][index],
                             o1=raws['o1'][index],
                             fc5=raws['fc5'][index],
                             x=raws['x'][index],
                             y=raws['y'][index],
                             unknown=raws['unknown'][index])
            ids.append(id_)
        return ids

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

    def update_prev_data(self):
        self.prev_tags = []
        self.prev_data = []

        self.db.connect()
        try:
            entries = sessions.select(
                sessions.tag_id, sessions.raw_id).where(
                sessions.user_id == self.userid)
            for entry in entries:
                get_raw = raw.select().where(
                    raw.id == entry.raw_id)
                for item in get_raw:
                    self.prev_data.append([
                        item.f3, item.fc6, item.p7, item.t8,
                        item.f7, item.f8, item.t7, item.p8,
                        item.af4, item.f4, item.af3, item.o2,
                        item.o1, item.fc5, item.x, item.y,
                        item.unknown])
                self.prev_tags.append(tags.get(id=entry.tag_id).tag)
        except sessions.DoesNotExist:
            print("no previous data found")
        finally:
            self.db.close()

        self.classifier = svm.SVC()  # maybe change method ?
        self.classifier.fit(self.prev_data, self.prev_tags)

    def fill_info(self, name, pswd):
        self.db.connect()
        self.username = name
        this_user = users.get(
            users.username == self.username, users.passwd == pswd)
        self.userid = this_user.id
        self.db.close()
        self.update_prev_data()

    def detect(self, this_raw):
        if len(set(self.prev_tags)) <= 1:
            return ['Lack of data']
        return self.classifier.predict([this_raw])
