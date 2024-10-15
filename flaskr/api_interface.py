import requests

def get_item_info(item_id):
    resp = requests.get(f"http://127.0.0.1:5000/api/items/{item_id}")
    if resp.status_code == 200:
        return dict(resp.json())
    else:
        return None


def get_items_id_map():
    resp = requests.get('http://127.0.0.1:5000/api/items')
    if resp.status_code == 200:
        return dict(resp.json())
    else:
        return None


def get_store_items():
    store_items = {}

    items_map = get_items_id_map()
    if items_map:
        for key in items_map.keys():
            item_info = get_item_info(key)
            if item_info:
                store_items[key] = item_info

    return store_items


def add_new_item_to_store(new_item) -> bool:
    resp = requests.post('http://127.0.0.1:5000/api/items', json= new_item)
    if resp.status_code == 201:
        return True

    return False


def rent_item(item_id) -> bool:
    resp = requests.put(f"http://127.0.0.1:5000/api/items/{item_id}/rent")
    if resp.status_code == 204:
        return True
    else:
        return False


def return_item(item_id) -> bool:
    resp = requests.put(f"http://127.0.0.1:5000/api/items/{item_id}/return")
    if resp.status_code == 204:
        return True
    else:
        return False