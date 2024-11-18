from flask import Blueprint, request, jsonify
from flaskr.api.services.items import ItemsService
from flaskr.api.services.users import UsersService
from flaskr.api.services.rentals import RentalsService
from flask_login import login_required

bp = Blueprint('api-items', __name__, url_prefix='/api/items')


@bp.route('/')
def get_items():
    service = ItemsService()
    items_dict = service.get_items_list()

    if items_dict:
        return jsonify(items_dict), 200
    else:
        return 'No items registered', 200

@bp.route('/', methods=['POST'])
# TODO: require login here and role
@login_required
@UsersService.role_required('Admin')
def add_item():
    request_input = request.get_json()

    service = ItemsService()
    valid = service.validate_input(request_input)

    if valid:
        item_exists = service.verify_item_match(name=request_input['item'])

        if item_exists:
            return f"Item {request_input['item']} is already registered.", 400

        new_item_added = service.add_item(request_input)

        if new_item_added:
            return '', 201

    return '', 400

@bp.route('/', methods=['DELETE'])
# TODO: require login here and role
@login_required
@UsersService.role_required('Admin')
def delete_item():
    request_input = request.get_json()

    if 'item' not in request_input.keys():
        return 'Item name missing!', 400

    service = ItemsService()
    item_exists = service.verify_item_match(name=request_input['item'])

    if item_exists:
        if service.delete_item(request_input['item']):
            return '', 204

    return 'Required item not found', 404


@bp.route('/<int:item_id>')
def get_item_info(item_id):
    service = ItemsService()
    item_exists = service.verify_item_match(item_id=item_id)

    if item_exists:
        item_info = service.get_item_info(item_id)
        if item_info:
            return jsonify(item_info), 200

    return 'Required item not found', 404

# TODO: require login here
@bp.route('/<int:item_id>/rent', methods=['PUT'])
@login_required
def rent_item(item_id):
    request_input = request.get_json()

    item_service = ItemsService()
    if not item_service.verify_item_match(item_id=item_id):
        return 'Required item not found', 400

    if 'user_id' not in request_input.keys():
        return 'Bad data', 400
    user_id = request_input['user_id']

    user_service = UsersService()
    if not user_service.verify_user_match(user_id=user_id):
        return 'Required user not found', 400

    if not item_service.available_stock(item_id):
        return 'Required item not available', 404

    if item_service.rent_item(item_id):
        if not RentalsService.associate_user_to_rent(item_id, user_id):
            item_service.return_item(item_id)
            return 'Error updating the rentals database', 409

        return '', 204

    return '', 404

# TODO: require login here
@bp.route('/<int:item_id>/return', methods=['PUT'])
@login_required
def return_item(item_id):
    request_input = request.get_json()

    item_service = ItemsService()
    if not item_service.verify_item_match(item_id=item_id):
        return 'Required item not found', 400

    if 'user_id' not in request_input.keys():
        return 'Bad data', 400
    user_id = request_input['user_id']

    user_service = UsersService()
    if not user_service.verify_user_match(user_id=user_id):
        return 'Required user not found', 400

    rent_id = RentalsService.get_rent_match(item_id, user_id)
    if rent_id is None:
        return 'No open rent for required return!', 400

    if item_service.check_item_full_stock(item_id):
        return 'The stock is full', 404

    if item_service.return_item(item_id):
        if not RentalsService.disassociate_user_from_rent(rent_id):
            item_service.rent_item(item_id)
            return 'Error updating the rentals database', 409

        return '', 204

    return '', 404
