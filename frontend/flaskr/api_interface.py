import requests

API_URL = "http://localhost:5001"

class APIInterface:

    def __init__(self):
        self.header = None

    def set_token(self, token):
        if token:
            self.header = {'Authorization': f"Bearer {token}"}

    def clear_token(self, token):
        self.header = None


class ItemsInterface(APIInterface):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_item_info(item_id):
        resp = requests.get(f"{API_URL}/api/items/{item_id}")
        if resp.status_code == 200:
            return dict(resp.json())
        else:
            return None

    @staticmethod
    def get_items_id_map():
        resp = requests.get(f"{API_URL}/api/items")
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

    def add_new_item_to_store(self, new_item) -> tuple:
        resp = requests.post(f"{API_URL}/api/items", json=new_item, headers=self.header)
        if resp.status_code == 201:
            return True, resp.status_code

        return False, resp.status_code

    def delete_item_from_store(self, item_id) -> bool:
        pass

    def rent_item(self, item_id, client_id) -> tuple:
        req_msg = {"user_id": client_id}
        resp = requests.put(f"{API_URL}/api/items/{item_id}/rent", json=req_msg, headers=self.header)
        if resp.status_code == 204:
            return True, resp.status_code
        else:
            return False, resp.status_code

    def return_item(self, item_id, client_id) -> tuple:
        req_msg = {"user_id": client_id}
        resp = requests.put(f"{API_URL}/api/items/{item_id}/return", json=req_msg, headers=self.header)
        if resp.status_code == 204:
            return True, resp.status_code
        else:
            return False, resp.status_code


class UserInterface(APIInterface):

    def __init__(self):
        super().__init__()

    def get_users_list(self):
        resp = requests.get(f"{API_URL}/api/users", headers=self.header)
        if resp.status_code == 200:
            return dict(resp.json())
        else:
            return None

    def get_user_by_id(self, user_id):
        resp = requests.get(f"{API_URL}/api/users/{user_id}", headers=self.header)
        if resp.status_code == 200:
            user_info = dict(resp.json())
            return user_info
        else:
            return None

    @classmethod
    def add_user(self, username, email, password) -> bool:
        new_user = {
            "username": username,
            "email": email,
            "password": password
        }
        resp = requests.post(f"{API_URL}/api/users", json=new_user)
        if resp.status_code == 201:
            return True

        return False

    def delete_user(self, user_info) -> bool:
        resp = requests.post(f"{API_URL}/api/users", json=user_info, headers=self.header)
        if resp.status_code == 204:
            return True

        return False

    @staticmethod
    def login_user(username, password) -> (bool, dict):
        user_info = {
            "username": username,
            "password": password
        }
        resp = requests.post(f"{API_URL}/api/users/login", json=user_info)
        if resp.status_code == 200:
            return True, resp.json()["access_token"]

        return False, None

    def logout_user(self, user_id) -> bool:
        resp = requests.post(f"{API_URL}/api/users/{user_id}/logout", headers=self.header)
        if resp.status_code == 204:
            return True

        return False