from flaskr.api.db import get_db
from datetime import datetime

def item_rented_by_client(item_id, client):
    db = get_db()
    rent_date = datetime.now().date()
    try:
        # Save matched info item x client
        db.execute(
            "INSERT INTO items_rent_control (item_id, client_id, rent_date) VALUES (?, ?, ?)",
            (item_id, client, rent_date),
        )
        db.commit()
    except db.Error:
        return False
    else:
        return True

def item_returned_by_client(item_id, client):
    db = get_db()
    return_date = datetime.now().date()
    try:
        # Update matched info item x client
        db.execute(
            "UPDATE items_rent_control SET return_date = ? WHERE item_id = ? AND client_id = ?",
            (return_date, item_id, client),
        )
        db.commit()
    except db.Error:
        return False
    else:
        return True