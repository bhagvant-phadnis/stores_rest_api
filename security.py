from werkzeug.security import safe_str_cmp    # for safe string compare in all python versions
from models.User import UserModel

"""
users=[
    {
        'id':1,
        'username':'bob',
        'password':'asdf'
    }
]
"""
"""
users=[
        User(1,'bob','asdf')
]
"""
"""
username_mapping = { 'bob': {
        'id':1,
        'username':'bob',
        'password':'asdf'
    }
}
"""


"""
userid_mapping = { 1: {
        'id':1,
        'username':'bob',
        'password':'asdf'
    }
}

"""

#username_mapping = {u.username: u for u in users}
#userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    #user = username_maping.get(username, None)
    #if user and user.password == password):
    user = UserModel.find_by_username(username)               #Withput string compare function
    if user and safe_str_cmp(user.password, password):      # With string compare function
        return user

def identity(payload):
    user_id = payload['identity']
    #return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
