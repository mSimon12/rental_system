from flaskr.api.models.users import Users


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
                     'password': password,
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
