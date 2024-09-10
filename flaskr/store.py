
from flask import Blueprint, current_app, request, render_template, Flask
from flaskr.db import get_db

from flaskr.forms import CommentForm

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

