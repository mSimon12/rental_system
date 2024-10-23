import requests


class ItemsInterface:

    @staticmethod
    def get_item_info(item_id):
        resp = requests.get(f"http://127.0.0.1:5000/api/items/{item_id}")
        if resp.status_code == 200:
            return dict(resp.json())
        else:
            return None

    @staticmethod
    def get_items_id_map():
        resp = requests.get('http://127.0.0.1:5000/api/items')
        if resp.status_code == 200:
            return dict(resp.json())
        else:
            return None

    @classmethod
    def get_store_items(cls):
        store_items = {}

        items_map = cls.get_items_id_map()
        if items_map:
            for key in items_map.keys():
                item_info = cls.get_item_info(key)
                if item_info:
                    store_items[key] = item_info

        return store_items

    @staticmethod
    def add_new_item_to_store(new_item) -> bool:
        resp = requests.post('http://127.0.0.1:5000/api/items', json= new_item)
        if resp.status_code == 201:
            return True

        return False

    @staticmethod
    def delete_item_from_store(item_id) -> bool:
        pass

    @staticmethod
    def rent_item(item_id) -> bool:
        resp = requests.put(f"http://127.0.0.1:5000/api/items/{item_id}/rent")
        if resp.status_code == 204:
            return True
        else:
            return False

    @staticmethod
    def return_item(item_id) -> bool:
        resp = requests.put(f"http://127.0.0.1:5000/api/items/{item_id}/return")
        if resp.status_code == 204:
            return True
        else:
            return False

class UserInterface:

    @staticmethod
    def add_user(new_user) -> bool:
        resp = requests.post('http://127.0.0.1:5000/api/clients/add', json=new_user)
        if resp.status_code == 201:
            return True

        return False

    @staticmethod
    def delete_user(user_info) -> bool:
        resp = requests.post('http://127.0.0.1:5000/api/clients', json=user_info)
        if resp.status_code == 204:
            return True

        return False

    @staticmethod
    def get_user_info(user_id):
        resp = requests.get(f"http://127.0.0.1:5000/api/clients/{user_id}")
        if resp.status_code == 200:
            return dict(resp.json())
        else:
            return None

    @staticmethod
    def get_users_list():
        resp = requests.get('http://127.0.0.1:5000/api/clients')
        if resp.status_code == 200:
            return dict(resp.json())
        else:
            return None

    @classmethod
    def get_user(cls, username='', email=''):
        users_list = cls.get_users_list()
        if users_list:
            for user_id in users_list.keys():
                list_user_username = users_list[user_id]['username']
                list_user_email = users_list[user_id]['email']

                if username == list_user_username or email == list_user_email:
                    user_info = cls.get_user_info(user_id)
                    if user_info:
                        from flaskr.user import User
                        user = User(user_info['id'],
                                    user_info['username'],
                                    user_info['email'],
                                    user_info['password'],
                                    )
                        return user
        return None