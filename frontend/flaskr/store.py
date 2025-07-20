import json

from flask import Blueprint, request, render_template, redirect, url_for
from flaskr.api_interface import ItemsInterface
from flaskr.forms import CommentForm, RentItemForm, ReturnItemForm
import base64

bp = Blueprint('store', __name__, url_prefix='/store')
comments = []

items_interface = ItemsInterface()

@bp.route('/')
def store():
    items = items_interface.get_store_items()
    items = [(items[item]['id'], items[item]['item'], items[item]['available']) for item in items]
    return render_template("store.html", template_items=items)


@bp.route('/<int:id>', methods=['GET', 'POST'])
def product_view(id):
    comment_form = CommentForm()
    rent_form = RentItemForm()
    return_form = ReturnItemForm()

    token = request.cookies.get("access_token_cookie")
    items_interface.set_token(token)

    if token is not None:
        payload = token.split(sep='.')[1]

        client_id = int(json.loads(base64.b64decode(payload))['sub'])
    else:
        return redirect(url_for('user.login_view'))

    if request.method == 'POST':
        if comment_form.validate_on_submit():
            comments.append(comment_form.new_comment.data)
            comment_form.new_comment.data = None
        elif rent_form.validate_on_submit() and rent_form.rent_item.data:
            call_status, resp_status = items_interface.rent_item(id, client_id)
            if not call_status:
                return redirect(url_for('user.login_view'))
        elif return_form.validate_on_submit() and return_form.return_item.data:
            call_status, resp = items_interface.return_item(id, client_id)
            if not call_status:
                return redirect(url_for('user.login_view'))

        return redirect(url_for('store.product_view', id=id))

    item_info = items_interface.get_item_info(id)
    if not item_info:
        return '', 404
    return render_template("product_view.html",
                           template_product_name=item_info['item'],
                           template_product_description=item_info['description'],
                           template_product_available=item_info['available'],
                           template_product_stock=item_info['stock_size'],
                           template_rent_button=rent_form,
                           template_return_button=return_form,
                           template_product_comments=comments,
                           template_add_comment=comment_form)
