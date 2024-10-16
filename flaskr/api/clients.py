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


def check_client_by_name(first_name, last_name):
    db = get_db()

    client_info = db.execute(
        'SELECT * FROM clients WHERE first_name = ? AND last_name = ?',
        (first_name.lower(), last_name.lower())
    ).fetchone()

    if client_info:
        return True, dict(client_info)
    return False, client_info


def add_new_client(client_info):
    firstname = client_info['first_name'].lower()
    lastname = client_info['last_name'].lower()
    age = client_info['age'] if 'age' in client_info else None

    db = get_db()
    try:
        db.execute(
            "INSERT INTO clients (first_name, last_name, age) VALUES (?,?,?)",
            (firstname,lastname,age)
        )
        db.commit()
    except db.Error:
        return False

    return True


@bp.route('/add', methods = ['POST'])
def add_client():
    request_input = request.get_json()

    if 'first_name' not in request_input:
        return 'first_name missing!', 400
    elif 'last_name' not in request_input:
        return 'last_name missing!', 400

    already_client, info = check_client_by_name(request_input['first_name'], request_input['last_name'])

    if already_client:
        return f"Client {request_input['first_name']} {request_input['last_name']}  is already registered.", 400

    if add_new_client(request_input):
        return '', 201
    else:
        return '', 400


@bp.route('/')
def get_clients_request():
    db = get_db()

    clients = db.execute(
        'SELECT id,first_name,last_name FROM clients'
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
