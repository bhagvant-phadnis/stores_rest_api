#Adding authentication
#psycopg2 sdded in requiremtns.txt used to interact with postgres, SQLAlchemy uses psycopg2
import os                       #after postgres installation
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
#from flask.helpers import _endpoint_from_view_func

from security import authenticate,identity
from resources.User import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')     # TO know sqlalchemy, where to find db,    currenlty it is root directory, get() function uses dburl or sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
app.secret_key='Mahesh'
api = Api(app)

jwt = JWT(app, authenticate, identity)   #/auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
