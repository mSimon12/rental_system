import pytest


class TestApiItems:

    @pytest.fixture
    def item_request_data(self):
        return {"item": "Lord of the Rings 1",
                "description": "The Ring Society",
                "stock": 8}

    @pytest.fixture
    def client_request_data(self):
        return {'user_id': 1}

    # TEST GETTING ITEMS LIST
    def test_get_items_request(self, api_client):
        response = api_client.get('/api/items/')
        assert response.status_code == 200
        assert len(response.json) == 1
        print(response.json)
        for item_id in response.json.keys():
            assert response.json[item_id] == 'test item'

    # TEST GETTING SPECIFIC ITEM INFO
    def test_get_item_info(self, api_client):
        response = api_client.get('/api/items/')

        for item_id in response.json.keys():
            response = api_client.get(f'/api/items/{item_id}')
            assert response.status_code == 200

    # TESTS FOR ADDING NEW ITEM
    def test_add_item_right_data(self, api_client, item_request_data):
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 201

        response = api_client.get('/api/items/')
        assert item_request_data['item'] in list(response.json.values())[-1]

    def test_add_item_avoid_duplicated(self, api_client, item_request_data):
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 201
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 400

    def test_add_item_missing_info(self, api_client, item_request_data):
        # missing item name
        missing_req_data = {key: value for key, value in item_request_data.items() if key != 'item'}
        response = api_client.post('/api/items/', json=missing_req_data)
        assert response.status_code == 400

        # missing description
        missing_req_data = {key: value for key, value in item_request_data.items() if key != 'description'}
        response = api_client.post('/api/items/', json=missing_req_data)
        assert response.status_code == 400

        # missing stock
        missing_req_data = {key: value for key, value in item_request_data.items() if key != 'stock'}
        response = api_client.post('/api/items/', json=missing_req_data)
        assert response.status_code == 400

    def test_add_item_invalid_item_name(self, api_client, item_request_data):
        # invalid item
        item_request_data['item'] = None
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 400

        item_request_data['item'] = 1.1
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 400

    def test_add_item_invalid_description(self, api_client, item_request_data):
        # invalid description
        item_request_data['description'] = None
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 400

        item_request_data['description'] = 10
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 400

    def test_add_item_invalid_stock(self, api_client, item_request_data):
        # invalid stock
        item_request_data['stock'] = None
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 400

        item_request_data['stock'] = 'Hello'
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 400

    # TESTS FOR DELETING AN ITEM
    def test_delete_item_request(self, api_client, item_request_data):
        response = api_client.get('/api/items/')
        assert response.status_code == 200
        initial_items = response.json

        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 201

        response2 = api_client.delete('/api/items/', json=item_request_data)
        assert response2.status_code == 204

        response = api_client.get('/api/items/')
        assert response.status_code == 200
        assert initial_items == response.json

    def test_delete_item_missing_info(self, api_client, item_request_data):
        response = api_client.post('/api/items/', json=item_request_data)
        assert response.status_code == 201

        # missing item name
        missing_req_data = {key: value for key, value in item_request_data.items() if key != 'item'}
        response = api_client.delete('/api/items/', json=missing_req_data)
        assert response.status_code == 400

    def test_delete_item_invalid_item(self, api_client, item_request_data):
        response = api_client.delete('/api/items/', json=item_request_data)
        assert response.status_code == 404

    # TESTS FOR RENTING AN ITEM
    def test_rent_item_valid_data(self, api_client, client_request_data):
        response = api_client.get('/api/items/1')
        available_in_stock = response.json['available']

        response = api_client.put('/api/items/1/rent', json=client_request_data)
        assert response.status_code == 204

        response = api_client.get('/api/items/1')
        new_availability = response.json['available']

        assert new_availability == available_in_stock - 1

    def test_rent_item_missing_client_info(self, api_client):
        response = api_client.put('/api/items/1/rent', json={})
        assert response.status_code == 400

    # TESTS FOR RETURNING AN ITEM
    def test_return_item_valid_data(self, api_client, client_request_data):
        response = api_client.get('/api/items/1')
        available_in_stock = response.json['available']

        response = api_client.put('/api/items/1/rent', json=client_request_data)
        assert response.status_code == 204

        response = api_client.put('/api/items/1/return', json=client_request_data)
        assert response.status_code == 204

        response = api_client.get('/api/items/1')
        new_availability = response.json['available']

        assert new_availability == available_in_stock

    def test_return_item_without_renting(self, api_client, client_request_data):
        response = api_client.put('/api/items/1/return', json=client_request_data)
        assert response.status_code == 400

    def test_return_item_missing_client_info(self, api_client):
        response = api_client.put('/api/items/1/return', json={})
        assert response.status_code == 400
