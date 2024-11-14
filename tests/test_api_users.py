import pytest


class TestApiClients:

    @pytest.fixture
    def client_request_data(self):
        return {'username': 'new_client',
                'email': 'email@email.com',
                'password': 'lsdjfjnasdldfdas12312knbwiuu3231uh13'}

    # TEST GETTING CLIENTS LIST
    def test_get_clients_request(self, api_client):
        response = api_client.get('/api/users/')
        assert response.status_code == 200
        assert len(response.json) == 3  # There is one extra user automatically added (Admin)
        for client_id in response.json.keys():
            assert list(response.json[client_id].keys()) == ['email', 'username']

    # TEST GETTING SPECIFIC CLIENT INFO
    def test_get_client_info(self, api_client):
        response = api_client.get('/api/users/')

        for client_id in response.json.keys():
            response = api_client.get(f'/api/users/{client_id}')
            assert response.status_code == 200

    # TESTS FOR CREATING NEW CLIENT
    def test_add_client_right_data(self, api_client, client_request_data):
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 201

        response = api_client.get('/api/users/')
        assert client_request_data['username'] in list(response.json.values())[-1]['username']

    def test_add_client_avoid_duplicated(self, api_client, client_request_data):
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 201
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 400

    def test_add_client_missing_info(self, api_client, client_request_data):
        # missing username
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'username'}
        response = api_client.post('/api/users/', json=missing_req_data)
        assert response.status_code == 400

        # missing email
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'email'}
        response = api_client.post('/api/users/', json=missing_req_data)
        assert response.status_code == 400

        # missing password
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'password'}
        response = api_client.post('/api/users/', json=missing_req_data)
        assert response.status_code == 400

    def test_add_client_invalid_username(self, api_client, client_request_data):
        # invalid username
        client_request_data['username'] = None
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 400

        client_request_data['username'] = 100
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 400

    def test_add_client_invalid_email(self, api_client, client_request_data):
        # invalid email
        client_request_data['email'] = 200
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 400

    def test_add_client_invalid_password(self, api_client, client_request_data):
        # invalid password
        client_request_data['password'] = 300
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 400

    # TESTS FOR DELETING A CLIENT
    def test_delete_client_request(self, api_client, client_request_data):
        response = api_client.get('/api/users/')
        assert response.status_code == 200
        initial_clients = response.json

        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 201

        response2 = api_client.delete('/api/users/', json=client_request_data)
        assert response2.status_code == 204

        response = api_client.get('/api/users/')
        assert response.status_code == 200
        assert initial_clients == response.json

    def test_delete_client_missing_info(self, api_client, client_request_data):
        response = api_client.post('/api/users/', json=client_request_data)
        assert response.status_code == 201

        # missing username
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'username'}
        response = api_client.delete('/api/users/', json=missing_req_data)
        assert response.status_code == 400

        # missing password
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'password'}
        response = api_client.delete('/api/users/', json=missing_req_data)
        assert response.status_code == 400

    def test_delete_client_invalid_user(self, api_client, client_request_data):
        response = api_client.delete('/api/users/', json=client_request_data)
        assert response.status_code == 404
