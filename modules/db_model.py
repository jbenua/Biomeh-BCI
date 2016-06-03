from peewee import *

db = MySQLDatabase('headset', host='localhost', user='jbenua', passwd='jbenua')


class users(Model):
    id = IntegerField()
    username = CharField()
    passwd = CharField()

    class Meta:
        database = db

    def __repr__(self):
        return "<User(id={}, username={})>".format(self.id, self.username)


class tags(Model):
    id = IntegerField()
    tag = TextField()

    class Meta:
        database = db

    def __repr__(self):
        return "<Tag(id={}, text={})>".format(self.id, self.tag)


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

    def __repr__(self):
        fields = [
            '{}={}'.format(sensor, getattr(self, sensor)) for sensor in [
                'id', 'f3', 'fc6', 'p7', 't8', 'f7', 'f8', 't7', 'p8',
                'af4', 'f4', 'af3', 'o2', 'o1', 'fc5', 'x', 'y', 'unknown']]
        return "<Raw({})>".format(
            ', '.join(fields))


class sessions(Model):
    id = IntegerField()
    raw_id = IntegerField()
    tag_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        database = db

    def __repr__(self):
        return "<Session(raw_id={raw}, tag_id={tag},  user_id={user}".format(
            raw=self.raw_id, tag=self.tag_id, user=self.user_id)


db.create_tables([users, raw, tags, sessions], safe=True)
