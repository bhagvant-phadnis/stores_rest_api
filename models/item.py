from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'id': self.id,
        'name': self.name,
        'price': self.price,
        'store_id': self.store_id
        }

    @classmethod
    def find_by_name(cls, name):
        # To fetch the details
        return cls.query.filter_by(name=name).first()           # SELECT * from items where name=name  LIMIT 1
#        return cls.query.filter_by(name=name, id=1)             # SELECT * from items where name=name and id=1
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        # To insert the details using SQLAlchemy
        db.session.add(self)                                       # add() this method perform insert as well as update operation.
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
