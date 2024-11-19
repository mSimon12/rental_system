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
        resp = requests.post('http://127.0.0.1:5000/api/items', json=new_item)
        if resp.status_code == 201:
            return True

        return False

    @staticmethod
    def delete_item_from_store(item_id) -> bool:
        pass

    @staticmethod
    def rent_item(item_id, client_id) -> bool:
        req_msg = {"client_id": client_id}
        resp = requests.put(f"http://127.0.0.1:5000/api/items/{item_id}/rent", json=req_msg)
        if resp.status_code == 204:
            return True
        else:
            return False

    @staticmethod
    def return_item(item_id, client_id) -> bool:
        req_msg = {"client_id": client_id}
        resp = requests.put(f"http://127.0.0.1:5000/api/items/{item_id}/return", json=req_msg)
        if resp.status_code == 204:
            return True
        else:
            return False


class UserInterface:

    @staticmethod
    def get_users_list():
        resp = requests.get('http://127.0.0.1:5000//api/users')
        if resp.status_code == 200:
            return dict(resp.json())
        else:
            return None

    @staticmethod
    def get_user_by_id(user_id):
        resp = requests.get(f"http://127.0.0.1:5000//api/users/{user_id}")
        if resp.status_code == 200:
            user_info = dict(resp.json())
            return user_info
        else:
            return None

    @staticmethod
    def add_user(username, email, password) -> bool:
        new_user = {
            "username": username,
            "email": email,
            "password": password
        }
        resp = requests.post('http://127.0.0.1:5000//api/users', json=new_user)
        if resp.status_code == 201:
            return True

        return False

    @staticmethod
    def delete_user(user_info) -> bool:
        resp = requests.post('http://127.0.0.1:5000//api/users', json=user_info)
        if resp.status_code == 204:
            return True

        return False

    @staticmethod
    def login_user(username, password) -> bool:
        user_info = {
            "username": username,
            "password": password
        }
        resp = requests.post('http://127.0.0.1:5000//api/users/login', json=user_info)
        if resp.status_code == 200:
            return True

        return False

    @staticmethod
    def logout_user(user_id) -> bool:
        resp = requests.post(f"http://127.0.0.1:5000//api/users/{user_id}/logout")
        if resp.status_code == 204:
            return True

        return False