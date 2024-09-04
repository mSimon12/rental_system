
from flask import Blueprint, current_app, request, render_template, Flask
from flaskr.db import get_db

from flaskr.store_forms import CommentForm

bp = Blueprint('store', __name__, url_prefix='/store')

comments = []

def get_store_items():
    db = get_db()

    items = db.execute(
        'SELECT * FROM generic_shelf'
    ).fetchall()

    return items


@bp.route('/')
def store():
    items = get_store_items()
    items = [(item['id'], item['item'],item['available']) for item in items]
    return render_template("store.html", template_items = items)


def get_product_info_by_id(id):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE id=?', (id,)
    ).fetchone()

    if item:
        return dict(item)
    return None


@bp.route('/<int:id>', methods=['GET', 'POST'])
def product_view(id):
    comment_form = CommentForm()

    if request.method == 'POST':
        comments.append(comment_form.new_comment.data)
        comment_form.new_comment.data = None

    item_info = get_product_info_by_id(id)
    if not item_info:
        return '', 404
    return render_template("product_view.html",
                           template_product_name = item_info['item'],
                           template_product_description = item_info['description'],
                           template_product_available = item_info['available'],
                           template_product_stock = item_info['stock_size'],
                           template_product_comments = comments,
                           template_add_comment = comment_form)


def check_item_existence_by_name(item_name):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE item = ?', (item_name,)
    ).fetchone()

    if item:
        return True
    return False


def check_item_availability(item_name):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE item = ?', (item_name,)
    ).fetchone()

    if item:
        if item['available'] <= 0:
            return False
        return True
    return False


def check_item_full_stock(item_name):
    db = get_db()

    item = db.execute(
        'SELECT * FROM generic_shelf WHERE item = ?', (item_name,)
    ).fetchone()

    if item and (item['available'] == item['stock_size']):
        return True
    return False


def pop_item_from_db(item_name):
    if not check_item_existence_by_name(item_name):
        return False, 'Required item not found'

    if not check_item_availability(item_name):
        return False, 'Required item not available'

    db = get_db()
    try:
        db.execute(
            "UPDATE generic_shelf SET available = available-1 WHERE item = ?",
            (item_name,),
        )
        db.commit()
    except db.Error:
        return False, 'Error updating item from database'
    else:
        return True, ''


def append_item_to_db(item_name):
    if not check_item_existence_by_name(item_name):
        return False, 'Required item not found'

    if check_item_full_stock(item_name):
        return False, 'The stock is full'

    db = get_db()
    try:
        db.execute(
            "UPDATE generic_shelf SET available = available+1 WHERE item = ?",
            (item_name,),
        )
        db.commit()
    except db.Error:
        return False, 'Error updating item from database'
    else:
        return True, ''


@bp.route('/rent_item', methods=['PUT'])
def rent_item_request():
    request_input = request.get_json()

    if 'item' not in request_input.keys():
        return 'Item name missing!', 400

    status, er_msg = pop_item_from_db(request_input['item'])

    if status:
        return '', 204
    else:
        return er_msg, 404


@bp.route('/return_item', methods=['PUT'])
def return_item_request():
    request_input = request.get_json()

    if 'item' not in request_input.keys():
        return 'Item name missing!', 400

    status, er_msg = append_item_to_db(request_input['item'])

    if status:
        return '', 204
    else:
        return er_msg, 404
