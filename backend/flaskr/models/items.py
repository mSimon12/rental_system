from flaskr.db import get_db


class Items:

    @staticmethod
    def query_items_list():
        db = get_db()

        items = db.execute(
            'SELECT id,name FROM items'
        ).fetchall()

        return items

    @staticmethod
    def query_item_by_id(item_id):
        db = get_db()

        item = db.execute(
            'SELECT * FROM items WHERE id = ?', (item_id,)
        ).fetchone()

        return item

    @staticmethod
    def query_user_by_name(name):
        db = get_db()

        item = db.execute(
            'SELECT * FROM items WHERE name = ?', (name,)
        ).fetchone()

        return item

    @staticmethod
    def get_item_info_from_db(item_id):
        db = get_db()

        item = db.execute(
            'SELECT * FROM items WHERE id = ?', (item_id,)
        ).fetchone()

        if item:
            item = dict(item)

        return item

    @staticmethod
    def add_item(item_info):
        db = get_db()

        try:
            db.execute(
                "INSERT INTO items (name, description, stock_size, available) VALUES (?, ?, ?, ?)",
                (item_info['name'], item_info['description'], item_info['stock'], item_info['stock']),
            )
            db.commit()
        except db.Error:
            return False

        return True

    @staticmethod
    def delete_item(item_name):
        db = get_db()

        try:
            db.execute(
                "DELETE FROM items WHERE name = ?",
                (item_name,),
            )
            db.commit()
        except db.Error:
            return False

        return True

    @staticmethod
    def pop_item_stock(item_id):
        db = get_db()
        try:
            db.execute(
                "UPDATE items SET available = available-1 WHERE id = ?",
                (item_id,),
            )
            db.commit()

        except db.Error:
            return False

        return True

    @staticmethod
    def append_item_stock(item_id):
        db = get_db()
        try:
            db.execute(
                "UPDATE items SET available = available+1 WHERE id = ?",
                (item_id,),
            )
            db.commit()

        except db.Error:
            return False

        return True
