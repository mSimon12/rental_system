import logging

from flask import Blueprint, request, render_template, url_for, redirect
from logging import Logger
from flaskr.forms import AddItemForm
from flaskr.api_interface import ItemsInterface


logger = Logger('manager', level='DEBUG')
file_handler = logging.FileHandler("debug.log")
logger.addHandler(file_handler)

bp = Blueprint('manager', __name__, url_prefix='/manager')


@bp.route("/", methods=['GET', 'POST'])
def manager():
    add_item_form = AddItemForm(request.form)

    if add_item_form.validate_on_submit():
        api_request = {
            "item": add_item_form.name.data,
            "description": add_item_form.description.data,
            "stock": add_item_form.stock.data
        }

        call_status = ItemsInterface.add_new_item_to_store(api_request)
        if not call_status:
            print("Not able to add new item!")
        else:
            return redirect(url_for('manager.manager'))

    items = ItemsInterface.get_store_items()

    return render_template("manager.html",
                           template_items=items,
                           template_add_item=add_item_form)
