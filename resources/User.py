import sqlite3
from flask_restful import Resource,reqparse     #reqparse for request parsing
from models.User import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field can not be blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field can not be blank!"
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        # Prevent duplicate user signing

        if UserModel.find_by_username(data['username']):
            return {"message" : "A user with name {} already exists".format(data['username'])},400

        # inser new user
#        user - UserModel(data['username'],data['password'])   # Simplfy this line as below
        user - UserModel(**data)                # like, user - UserModel(data['username'],data['password'])
        user.save_to_db()

        return ('"message" : "User created successfully."'), 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'},404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'},404
        user.delete_from_db()
        return {'message':'User deleted'},200
