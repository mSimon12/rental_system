from flask import Blueprint, request, jsonify
from flaskr.api.db import get_db

bp = Blueprint('api-clients', __name__, url_prefix='/api/clients')


def check_client_by_id(client_id):
    db = get_db()

    client_info = db.execute(
        'SELECT * FROM users WHERE id = ?',
        (client_id,)
    ).fetchone()

    if client_info:
        client_info = dict(client_info)
        client_role = db.execute(
            'SELECT role FROM roles WHERE id = ?',
            (client_info['role_id'],)
        ).fetchone()
        client_info['role'] = dict(client_role)['role']
        client_info.pop('role_id')

        return True, client_info
    return False, client_info


def check_client_by_username(username):
    db = get_db()

    client_info = db.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()

    if client_info:
        return True, dict(client_info)
    return False, client_info


def add_new_client(client_info):
    username = client_info['username']
    email = client_info['email']
    password = client_info['password']

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, email, password, role_id) VALUES (?,?,?,?)",
            (username, email, password, 2)
        )
        db.commit()
    except db.Error:
        return False

    return True


def delete_client_from_db(client_info):
    username = client_info['username']
    password = client_info['password']

    db = get_db()

    client = db.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()

    if client:
        try:
            db.execute(
                "DELETE FROM users WHERE id = ?",
                (client['id'],)
            )
            db.commit()
        except db.Error:
            return False
        else:
            return True

    return False

####################################################################################
# API calls


@bp.route('/add', methods=['POST'])
def add_client():
    request_input = request.get_json()

    if 'username' not in request_input:
        return 'Username missing!', 400
    elif 'password' not in request_input:
        return 'Password missing!', 400
    elif 'email' not in request_input:
        return 'Email missing!', 400
    elif (not isinstance(request_input['username'], str) or
          not isinstance(request_input['email'], str) or
          not isinstance(request_input['password'], str)):
        return 'Invalid data type!', 400

    already_client, info = check_client_by_username(request_input['username'])

    if already_client:
        return f"Username {request_input['username']} is already registered.", 400

    if add_new_client(request_input):
        return '', 201
    else:
        return '', 400


@bp.route('/')
def get_clients_request():
    db = get_db()

    users = db.execute(
        'SELECT id,username,email FROM users'
    ).fetchall()

    if users:
        users_dict = {}
        for user in users:
            users_dict[user["id"]] = {"username": user["username"], "email": user["email"]}
        return jsonify(users_dict), 200
    else:
        return 'No users registered', 200


@bp.route('/<int:client_id>')
def get_client_info(client_id):
    status, client_info = check_client_by_id(client_id)
    if status:
        return jsonify(client_info), 200
    return '', 404


@bp.route('/', methods=['DELETE'])
def delete_client_request():
    request_input = request.get_json()

    if 'username' not in request_input:
        return 'username missing!', 400
    elif 'password' not in request_input:
        return 'password missing!', 400

    if delete_client_from_db(request_input):
        return '', 204
    else:
        return 'Required client not found', 404
