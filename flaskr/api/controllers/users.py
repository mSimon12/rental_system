from flask import Blueprint, request, jsonify
from flaskr.api.services.users import UsersService
from flask_login import login_required, current_user

bp = Blueprint('api-users', __name__, url_prefix='/api/users')

####################################################################################
# API calls
@bp.route('/')
def get_users():
    service = UsersService()
    users_dict = service.get_users_list()

    if users_dict:
        return jsonify(users_dict), 200
    else:
        return 'No users registered', 200


@bp.route('/', methods=['POST'])
def add_user():
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

    service = UsersService()
    user_exists = service.verify_user_match(username=request_input['username'])

    if user_exists:
        return f"Username {request_input['username']} is already registered.", 400

    new_user_added = service.add_user(request_input['username'],
                                      request_input['email'],
                                      request_input['password'])

    if new_user_added:
        return '', 201
    else:
        return '', 400


@bp.route('/', methods=['DELETE'])
# TODO: require login here
def delete_user():
    request_input = request.get_json()

    if 'username' not in request_input:
        return 'username missing!', 400
    elif 'password' not in request_input:
        return 'password missing!', 400

    service = UsersService()
    delete_user_status = service.delete_user(request_input['username'],
                                     request_input['password'])

    if delete_user_status:
        return '', 204
    else:
        return 'Required user not found', 404


@bp.route('/<int:user_id>')
def get_user_info(user_id):
    service = UsersService()
    user_exists = service.verify_user_match(user_id=user_id)

    if user_exists:
        user_info = service.get_user_info(user_id)
        if user_info:
            return jsonify(user_info), 200

    return 'Required user not found', 404


# TODO: implement login endpoint
@bp.route('/login', methods=['POST'])
def login_user():
    if current_user.is_authenticated:
        return 'Some user already logged', 401

    request_input = request.get_json()

    if 'username' not in request_input:
        return 'username missing!', 400
    elif 'password' not in request_input:
        return 'password missing!', 400

    service = UsersService()
    user_exists = service.verify_user_match(username=request_input['username'])

    if not user_exists:
        return 'Required user not found', 400

    login_approved = service.login(request_input['username'], request_input['password'])
    if login_approved:
        return '', 200

    return '', 400


@bp.route('<int:user_id>/logout', methods=['POST'])
def logout_user(user_id):
    if current_user.is_authenticated:
        if user_id == current_user.id:
            service = UsersService()
            if service.logout():
                return '', 200
            else:
                return 'Failed to logout', 400
        else:
            return 'Required user is not logged in', 400

    return 'No user authenticated', 400
