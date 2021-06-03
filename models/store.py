from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
        # To fetch the details
        return cls.query.filter_by(name=name).first()           # SELECT * from items where name=name  LIMIT 1
#        return cls.query.filter_by(name=name, id=1)             # SELECT * from items where name=name and id=1
    def save_to_db(self):
        # To insert the details using SQLAlchemy
        db.session.add(self)                                       # add() this method perform insert as well as update operation.
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
