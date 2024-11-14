from flaskr.api.db import get_db


class Users:

    @staticmethod
    def query_users_list():
        db = get_db()

        users = db.execute(
            'SELECT id,username,email FROM users'
        ).fetchall()

        return users

    @staticmethod
    def query_user_by_id(user_id):
        db = get_db()

        user_info = db.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()

        return user_info

    @staticmethod
    def query_user_by_username(username):
        db = get_db()

        user_info = db.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        return user_info

    @staticmethod
    def add_user(user_info):
        print(user_info)
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, email, password, role_id) VALUES (?,?,?,?)",
                (user_info['username'],
                 user_info['email'],
                 user_info['password'],
                 user_info['role_id'])
            )
            db.commit()
        except db.Error:
            return False

        return True

    @staticmethod
    def delete_user(user_id):
        db = get_db()

        try:
            db.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )
            db.commit()
        except db.Error:
            return False
        else:
            return True


    @staticmethod
    def get_role_name(role_id):
        db = get_db()
        user_role = db.execute(
            'SELECT role FROM roles WHERE id = ?',
            (role_id,)
        ).fetchone()

        return dict(user_role)['role']