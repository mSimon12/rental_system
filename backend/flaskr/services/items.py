from flaskr.models.items import Items


class ItemsService:
    item_pattern = {
        'item': str,
        'description': str,
        'stock': int
    }

    def validate_input(self, req_input):
        for key in self.item_pattern:
            try:
                assert key in req_input.keys()
                assert isinstance(req_input[key], self.item_pattern[key])
            except AssertionError:
                return False

        return True

    @staticmethod
    def verify_item_match(item_id=None, name=None):
        if item_id:
            item_info = Items.query_item_by_id(item_id)
        elif name:
            item_info = Items.query_user_by_name(name)
        else:
            return False

        if item_info:
            return True
        return False

    @staticmethod
    def get_items_list():
        queried_items = Items.query_items_list()

        if queried_items:
            return dict(queried_items)
        else:
            return None

    @staticmethod
    def add_item(item_info):
        return Items.add_item(item_info)

    @staticmethod
    def delete_item(item_name):
        return Items.delete_item(item_name)

    @staticmethod
    def get_item_info(item_id):
        item_info = Items.query_item_by_id(item_id)

        if item_info:
            item_info = dict(item_info)
            return item_info

        return None

    @staticmethod
    def available_stock(item_id):
        item_info = Items.query_item_by_id(item_id)

        if item_info:
            item_info = dict(item_info)
            if item_info['available'] <= 0:
                return False
            return True
        return False

    @staticmethod
    def check_item_full_stock(item_id):
        item_info = Items.query_item_by_id(item_id)

        if item_info:
            item_info = dict(item_info)
            if item_info['available'] == item_info['stock_size']:
                return True
        return False

    @staticmethod
    def rent_item(item_id):
        return Items.pop_item_stock(item_id)

    @staticmethod
    def return_item(item_id):
        return Items.append_item_stock(item_id)

