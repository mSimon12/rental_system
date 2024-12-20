import logging

from flask import Blueprint, request, render_template, url_for, redirect, flash
from logging import Logger
from flaskr.frontend.forms import AddItemForm
from flaskr.frontend.api_interface import ItemsInterface
from flaskr.api.services.users import UsersService

logger = Logger('manager', level='DEBUG')
file_handler = logging.FileHandler("debug.log")
logger.addHandler(file_handler)

bp = Blueprint('manager', __name__, url_prefix='/manager')


items_interface = ItemsInterface()

@bp.route("/", methods=['GET', 'POST'])
def manager():
    add_item_form = AddItemForm(request.form)

    token = request.cookies.get("access_token_cookie")
    items_interface.set_token(token)

    if add_item_form.validate_on_submit():
        api_request = {
            "item": add_item_form.name.data,
            "description": add_item_form.description.data,
            "stock": add_item_form.stock.data
        }

        call_status, resp_status = items_interface.add_new_item_to_store(api_request)
        if not call_status:
            if resp_status == 403:
                flash('Not enough authorization rights!')

            return redirect(url_for('user.login_view'))

        else:
            return redirect(url_for('manager.manager'))

    items = items_interface.get_store_items()

    return render_template("manager.html",
                           template_items=items,
                           template_add_item=add_item_form)
