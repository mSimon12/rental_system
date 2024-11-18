from flaskr.api.db import get_db


class Rentals:

    @staticmethod
    def query_match_item_user(item_id, user_id):
        db = get_db()

        rent_id = db.execute(
            'SELECT id FROM items_rent_control WHERE item_id = ? AND user_id = ? AND return_date IS NULL',
            (item_id, user_id),
        ).fetchone()

        if rent_id:
            return rent_id['id']
        return None

    @staticmethod
    def add_item_user_link(rent_info):
        db = get_db()

        try:
            # Save matched info item x user
            db.execute(
                "INSERT INTO items_rent_control (item_id, user_id, rent_date) VALUES (?, ?, ?)",
                (rent_info['item_id'], rent_info['user_id'], rent_info['date']),
            )
            db.commit()
        except db.Error:
            return False

        return True

    @staticmethod
    def update_item_user_link(rent_id, date):
        db = get_db()

        try:
            # Update matched info item x user
            db.execute(
                "UPDATE items_rent_control SET return_date = ? WHERE id = ?",
                (date, rent_id),
            )
            db.commit()
        except db.Error:
            return False

        return True
