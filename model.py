from exts import db

class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        return fields

class Poem(db.Model, EntityBase):
    #数据表明、字段
    __tablename__ = 'poem'
    photo_path = db.Column(db.String(255), primary_key=True)
    poem = db.Column(db.String(255))
    score = db.Column(db.Float())
    time = db.Column(db.DateTime(255))
    shoucang = db.Column(db.INT)

class User(db.Model, EntityBase):
    #数据表明、字段
    __tablename__ = 'user'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

if __name__=="__main__":
    Poem.query.filter_by(time='2021-05-24 18:18:23')