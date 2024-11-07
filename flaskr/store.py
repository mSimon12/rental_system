
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from flaskr.api_interface import ItemsInterface
from flaskr.forms import CommentForm, RentItemForm, ReturnItemForm

bp = Blueprint('store', __name__, url_prefix='/store')

comments = []

@bp.route('/')
def store():
    items = ItemsInterface.get_store_items()
    items = [(items[item]['id'], items[item]['item'], items[item]['available']) for item in items]
    return render_template("store.html", template_items=items)


@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def product_view(id):
    comment_form = CommentForm()
    rent_form = RentItemForm()
    return_form = ReturnItemForm()

    if request.method == 'POST':
        if comment_form.validate_on_submit():
            comments.append(comment_form.new_comment.data)
            comment_form.new_comment.data = None
        elif rent_form.validate_on_submit() and rent_form.rent_item.data:
            ItemsInterface.rent_item(id, current_user.id)
        elif return_form.validate_on_submit() and return_form.return_item.data:
            ItemsInterface.return_item(id, current_user.id)

        return redirect(url_for('store.product_view', id=id))

    item_info = ItemsInterface.get_item_info(id)
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
