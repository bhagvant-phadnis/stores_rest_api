from werkzeug.security import safe_str_cmp    # for safe string compare in all python versions
from flask_restful import Resource,reqparse     #reqparse for request parsing
from flask_jwt_extended import create_access_token, create_refresh_token
from models.User import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
        type=str,
        required=True,
        help="This field can not be blank!"
    )
_user_parser.add_argument('password',
            type=str,
        required=True,
        help="This field can not be blank!"
    )

class UserRegister(Resource):


    def post(self):

        data = _user_parser.parse_args()

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

class UserLogin(Resource):

    @classmethod
    def post(cls):
        #get data from parser
        data = _user_parser.parse_args()

        #find user in DATABASE
        user = UserModel.find_by_username(data['username'])
        #check password
        if user and safe_str_cmp(user.password, data['password']):
            #create access tokan
            access_token = create_access_token(identity=user.id, fresh=True)
            #create refresh token
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            }, 200
        #return them
        return {'message':'Invalid credentials'}, 401
