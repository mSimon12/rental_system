from flask import Blueprint, request, jsonify
from flaskr.api.db import get_db

bp = Blueprint('api-clients', __name__, url_prefix='/api/clients')

def check_client_by_id(client_id):
    db = get_db()

    client_info = db.execute(
        'SELECT * FROM clients WHERE id = ?',
        (client_id,)
    ).fetchone()

    if client_info:
        return True, dict(client_info)
    return False, client_info


def check_client_by_username(username):
    db = get_db()

    client_info = db.execute(
        'SELECT * FROM clients WHERE username = ?',
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
            "INSERT INTO clients (username, email, password) VALUES (?,?,?)",
            (username, email, password)
        )
        db.commit()
    except db.Error:
        return False

    return True


@bp.route('/add', methods = ['POST'])
def add_client():
    request_input = request.get_json()

    if 'username' not in request_input:
        return 'username missing!', 400
    elif 'password' not in request_input:
        return 'password missing!', 400
    elif 'email' not in request_input:
        return 'email missing!', 400

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

    clients = db.execute(
        'SELECT id,username,email FROM clients'
    ).fetchall()

    print(clients)

    if clients:
        clients_dict = {}
        for client in clients:
            clients_dict[client["id"]] = client["first_name"] + " " + client["last_name"]
        return jsonify(clients_dict)
    else:
        return 'Required item not found', 404


@bp.route('/<int:client_id>')
def get_client_info(client_id):
    status, client_info = check_client_by_id(client_id)
    if status:
        return jsonify(client_info), 200
    return '', 404
