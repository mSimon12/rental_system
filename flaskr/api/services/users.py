from flask import jsonify
from flask_login import UserMixin
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from functools import wraps
from flaskr.api.models.users import Users
from flaskr.api.models.roles import Roles

class UsersService:

    def __init__(self):
        pass

    @staticmethod
    def get_users_list():
        queried_users = Users.query_users_list()

        if queried_users:
            users_dict = {}
            for user in queried_users:
                users_dict[user["id"]] = {"username": user["username"], "email": user["email"]}
            return users_dict
        else:
            return None

    @staticmethod
    def verify_user_match(user_id=None, username=None):
        if user_id:
            user_info = Users.query_user_by_id(user_id)
        elif username:
            user_info = Users.query_user_by_username(username)
        else:
            return False

        if user_info:
            return True
        return False

    @staticmethod
    def add_user(username, email, password):
        user_info = {'username': username,
                     'email': email,
                     'password': generate_password_hash(password),
                     'role_id': 2
        }

        return Users.add_user(user_info)


    @staticmethod
    def delete_user(username, password):
        user_info = Users.query_user_by_username(username)
        if user_info:
            user_info = dict(user_info)
            return Users.delete_user(user_info['id'])

        return False


    @staticmethod
    def get_user_info(user_id):
        user_info = Users.query_user_by_id(user_id)

        if user_info:
            user_info = dict(user_info)

            user_info['role'] = Users.get_role_name(user_info['role_id'])
            user_info.pop('role_id')
            user_info.pop('password')

            return user_info

        return None

    @staticmethod
    def __check_credentials(username, password):
        user_info = Users.query_user_by_username(username)

        if user_info:
            user_info = dict(user_info)

            if check_password_hash(user_info['password'], password):
                return user_info

        return None

    def login(self, username, password):
        user_info = self.__check_credentials(username, password)
        token_response = None
        if user_info is not None:
            user = self.get_user(user_info['id'])

            # Generate access and refresh tokens
            access_token = create_access_token(identity=str(user.id),
                                               expires_delta=timedelta(minutes=10))
            token_response = jsonify({
                    "access_token": access_token
            })

            # set_access_cookies()

            return True, token_response
        return False, token_response

    @staticmethod
    def block_user(user_id):
        # TODO: implement user blacklist with cache
        return True

    @staticmethod
    def login_required():
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if verify_jwt_in_request():
                    return f(*args, **kwargs)

            return decorated_function

        return decorator

    @classmethod
    def role_required(cls, role):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                jwt_header = verify_jwt_in_request()
                if jwt_header:
                    user_id = get_jwt_identity()
                    user = cls.get_user(user_id)
                    if user.role == role:
                        return f(*args, **kwargs)
                    else:
                        return "error': Access denied", 403

            return decorated_function

        return decorator

    @staticmethod
    def get_user(user_id):
        user_info = Users.query_user_by_id(user_id)

        if user_info:
            user_info = dict(user_info)
            user = User(user_info['id'],
                        user_info['username'],
                        user_info['email'],
                        user_info['password'],
                        user_info['role_id'],
                        )
            return user

        return None


class User(UserMixin):

    def __init__(self, id, username, email, password, role_id):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = Roles.query_role_name(role_id)
