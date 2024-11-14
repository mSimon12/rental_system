from flask import Blueprint, request, jsonify
from flaskr.api.services.users import UsersService

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
    user_exists = service.verify_user_match(request_input['username'])

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

    return '', 404


# TODO: implement login endpoint
@bp.route('/login', methods=['POST'])
def login_user():
    pass

# TODO: implement logout endpoint
@bp.route('/logout', methods=['POST'])
def logout_user():
    pass

# TODO: create decorator for required auth here