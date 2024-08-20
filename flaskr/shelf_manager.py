import logging

from flask import Blueprint, current_app, request, jsonify, flash
from logging import Logger

from flaskr.db import get_db

logger = Logger('manager', level='DEBUG')
file_handler = logging.FileHandler("debug.log")
logger.addHandler(file_handler)

bp = Blueprint('manager', __name__, url_prefix='/manager')


def validate_input(req_input, pattern):
    for req_key in req_input:
        try:
            assert req_key in pattern.keys()
            assert isinstance(req_input[req_key], pattern[req_key])
        except AssertionError:
            return False

    return True


item_pattern = {
    'item': str,
    'description': str,
    'stock': int
}


def get_item_info_from_db(item_name):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE item = ?', (item_name,)
    ).fetchone()

    if item:
        item = dict(item)
        item.pop('id')

    return item


@bp.route('/item')
def get_item_request():
    request_input = request.get_json()

    if 'item' not in request_input.keys():
        return 'Item name missing!', 400

    info = get_item_info_from_db(request_input['item'])

    if info:
        return jsonify(info)
    else:
        return 'Required item not found', 404


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


@bp.route('/item', methods=['POST'])
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


@bp.route('/item', methods=['DELETE'])
def delete_item_request():
    request_input = request.get_json()

    if 'item' not in request_input.keys():
        return 'Item name missing!', 400

    if delete_item_from_db(request_input['item']):
        return '', 204
    else:
        return 'Required item not found', 404
