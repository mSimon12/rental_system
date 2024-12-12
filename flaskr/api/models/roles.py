from flaskr.api.db import get_db


class Roles:

    @staticmethod
    def query_role_name(role_id):
        db = get_db()

        role_name = db.execute(
            'SELECT role FROM roles WHERE id = ?',
            (role_id, ),
        ).fetchone()

        if role_name:
            return dict(role_name)['role']

        return ''

    def query_role_id(role_name):
        db = get_db()

        role_id = db.execute(
            'SELECT id FROM roles WHERE role = ?',
            (role_name, ),
        ).fetchone()

        if role_name:
            return dict(role_id)['id']

        return ''
