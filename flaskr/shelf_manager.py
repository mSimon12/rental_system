import logging

from flask import Blueprint, current_app, request, jsonify, flash, render_template, url_for, redirect
from logging import Logger
from flaskr.forms import AddItemForm
import requests as req
import json

from flaskr.db import get_db

logger = Logger('manager', level='DEBUG')
file_handler = logging.FileHandler("debug.log")
logger.addHandler(file_handler)

bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route("/", methods=['GET', 'POST'])
def manager():
    add_item_form = AddItemForm()

    if request.method == 'POST':
        api_request = {
            "item": add_item_form.name.data,
            "description": add_item_form.description.data,
            "stock": add_item_form.stock.data
        }

        resp = req.post('http://127.0.0.1:5000/api/items', json= api_request)

    resp = req.get('http://127.0.0.1:5000/api/items')
    if resp.status_code == 200:
        items = resp.json()
    else:
        return resp


    return render_template("manager.html",
                           template_items = items,
                           template_add_item = add_item_form)

