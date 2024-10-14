from flask import Blueprint, current_app, request, jsonify, flash, url_for

from flaskr.db import get_db
bp = Blueprint('api-items', __name__, url_prefix='/api/items')


item_pattern = {
    'item': str,
    'description': str,
    'stock': int
}


def validate_input(req_input, pattern):
    for req_key in req_input:
        try:
            assert req_key in pattern.keys()
            assert isinstance(req_input[req_key], pattern[req_key])
        except AssertionError:
            return False

    return True


def get_item_info_from_db(item_id):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE id = ?', (item_id,)
    ).fetchone()

    if item:
        item = dict(item)

    return item


def add_item_to_db(item_info):
    db = get_db()

    try:
        db.execute(
            "INSERT INTO generic_shelf (item, description, stock_size, available) VALUES (?, ?, ?, ?)",
            (item_info['item'], item_info['description'], item_info['stock'], item_info['stock']),
        )
        db.commit()
    except db.IntegrityError:
        return f"Item {item_info['item']} is already registered."
    else:
        return ''


def delete_item_from_db(item_name):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE item = ?', (item_name,)
    ).fetchone()

    if item:
        try:
            db.execute(
                "DELETE FROM generic_shelf WHERE item = ?",
                (item_name,),
            )
            db.commit()
        except db.Error:
            return False
        else:
            return True

    return False


def check_item_existence(item_id):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE id = ?', (item_id,)
    ).fetchone()

    if item:
        return True
    return False


def check_item_availability(item_id):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE id = ?', (item_id,)
    ).fetchone()

    if item:
        if item['available'] <= 0:
            return False
        return True
    return False


def check_item_full_stock(item_id):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE id = ?', (item_id,)
    ).fetchone()

    if item and (item['available'] == item['stock_size']):
        return True
    return False


def pop_item_from_db(item_id):
    if not check_item_existence(item_id):
        return False, 'Required item not found'

    if not check_item_availability(item_id):
        return False, 'Required item not available'

    db = get_db()
    try:
        db.execute(
            "UPDATE generic_shelf SET available = available-1 WHERE id = ?",
            (item_id,),
        )
        db.commit()
    except db.Error:
        return False, 'Error updating item from database'
    else:
        return True, ''


def append_item_to_db(item_id):
    if not check_item_existence(item_id):
        return False, 'Required item not found'

    if check_item_full_stock(item_id):
        return False, 'The stock is full'

    db = get_db()
    try:
        db.execute(
            "UPDATE generic_shelf SET available = available+1 WHERE id = ?",
            (item_id,),
        )
        db.commit()
    except db.Error:
        return False, 'Error updating item from database'
    else:
        return True, ''

####################################################################################
# API calls

@bp.route('/')
def get_items_request():
    db = get_db()

    items = db.execute(
        'SELECT id,item FROM generic_shelf'
    ).fetchall()

    if items:
        items = dict(items)
        return jsonify(items)
    else:
        return 'Required item not found', 404


@bp.route('/', methods=['POST'])
def add_item_request():

    request_input = request.get_json()
    valid = validate_input(request_input, item_pattern)

    # Check it is logged
    if valid:
        error = add_item_to_db(request_input)

        if not error:
            return '', 201
        else:
            return error, 400
    else:
        return '', 400


@bp.route('/', methods=['DELETE'])
def delete_item_request():
    request_input = request.get_json()

    if 'item' not in request_input.keys():
        return 'Item name missing!', 400

    if delete_item_from_db(request_input['item']):
        return '', 204
    else:
        return 'Required item not found', 404


@bp.route('/<int:item_id>')
def get_item_info(item_id):
    info = get_item_info_from_db(item_id)

    if info:
        return jsonify(info)
    else:
        return 'Required item not found', 404


@bp.route('/<int:item_id>/rent', methods=['PUT'])
def rent_item_request(item_id):
    status, er_msg = pop_item_from_db(item_id)

    if status:
        return '', 204
    else:
        return er_msg, 404


@bp.route('/<int:item_id>/return', methods=['PUT'])
def return_item_request(item_id):
    status, er_msg = append_item_to_db(item_id)

    if status:
        return '', 204
    else:
        return er_msg, 404