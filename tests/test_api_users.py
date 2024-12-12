import pytest
import json


class TestApiUsers:

    header = {'Authorization': ""}

    @pytest.fixture
    def client_request_data(self):
        return {'username': 'new_user',
                'email': 'email@email.com',
                'password': 'lsdjfjnasdldfdas12312knbwiuu3231uh13'}

    @pytest.fixture
    def login_admin_user(self, api_client):
        with open("tests/test_vars.json", "r") as test_file:
            test_vars = json.load(test_file)

        admin_user = test_vars['users']['admin_user']
        login_request = {"username": admin_user['username'],
                         "password": admin_user['password']
                         }

        response = api_client.post('/api/users/login', json=login_request)

        if response.status_code == 200:
            try:
                token = response.json['access_token']
                self.header['Authorization'] = f"Bearer {token}"
            except IndexError:
                pass

    @pytest.fixture
    def login_normal_user(self, api_client):
        with open("tests/test_vars.json", "r") as test_file:
            test_vars = json.load(test_file)

        admin_user = test_vars['users']['normal_user']
        login_request = {"username": admin_user['username'],
                         "password": admin_user['password']
                         }

        response = api_client.post('/api/users/login', json=login_request)

        if response.status_code == 200:
            try:
                token = response.json['access_token']
                self.header['Authorization'] = f"Bearer {token}"
            except IndexError:
                pass

    # TEST GETTING USERS LIST
    def test_get_clients_request(self, api_client, login_admin_user):
        response = api_client.get('/api/users/', headers=self.header)
        assert response.status_code == 200
        assert len(response.json) == 3  # There is one extra user automatically added (Admin)
        for client_id in response.json.keys():
            assert list(response.json[client_id].keys()) == ['email', 'username']

    # TEST GETTING SPECIFIC USER INFO
    def test_get_client_info(self, api_client, login_admin_user):
        response = api_client.get('/api/users/', headers=self.header)

        for client_id in response.json.keys():
            response = api_client.get(f'/api/users/{client_id}', headers=self.header)
            assert response.status_code == 200

    # TESTS FOR CREATING NEW USER
    def test_add_client_right_data(self, api_client, client_request_data, login_admin_user):
        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 201

        response = api_client.get('/api/users/', headers=self.header)
        assert client_request_data['username'] in list(response.json.values())[-1]['username']

    def test_add_client_avoid_duplicated(self, api_client, client_request_data, login_admin_user):
        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 201
        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 400

    def test_add_client_missing_info(self, api_client, client_request_data, login_admin_user):
        # missing username
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'username'}
        response = api_client.post('/api/users/', json=missing_req_data, headers=self.header)
        assert response.status_code == 400

        # missing email
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'email'}
        response = api_client.post('/api/users/', json=missing_req_data, headers=self.header)
        assert response.status_code == 400

        # missing password
        missing_req_data = {key: value for key, value in client_request_data.items() if key != 'password'}
        response = api_client.post('/api/users/', json=missing_req_data, headers=self.header)
        assert response.status_code == 400

    def test_add_client_invalid_username(self, api_client, client_request_data, login_admin_user):
        # invalid username
        client_request_data['username'] = None
        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 400

        client_request_data['username'] = 100
        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 400

    def test_add_client_invalid_email(self, api_client, client_request_data, login_admin_user):
        # invalid email
        client_request_data['email'] = 200
        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 400

    def test_add_client_invalid_password(self, api_client, client_request_data, login_admin_user):
        # invalid password
        client_request_data['password'] = 300
        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 400

    # TESTS FOR DELETING A USER
    def test_delete_client_admin_request(self, api_client, client_request_data, login_admin_user):
        response = api_client.get('/api/users/', headers=self.header)
        assert response.status_code == 200
        initial_clients = response.json

        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 201

        response2 = api_client.delete('/api/users/4', json=client_request_data, headers=self.header)
        assert response2.status_code == 204

        response = api_client.get('/api/users/', headers=self.header)

        assert response.status_code == 200
        assert initial_clients == response.json

    def test_delete_client_owner_request(self, api_client, client_request_data, login_admin_user):
        response = api_client.get('/api/users/', headers=self.header)
        assert response.status_code == 200
        initial_clients = response.json

        response = api_client.post('/api/users/', json=client_request_data, headers=self.header)
        assert response.status_code == 201

        response1 = api_client.post('/api/users/login', json=client_request_data)
        assert response1.status_code == 200

        new_user_id = response1.json['user_id']
        user_header = {'Authorization': f"Bearer {response1.json['access_token']}"}

        response2 = api_client.delete(f"/api/users/{new_user_id}", json=client_request_data, headers=user_header)
        assert response2.status_code == 204

        response3 = api_client.get('/api/users/', headers=self.header)

        assert response3.status_code == 200
        assert initial_clients == response3.json

    def test_delete_client_invalid_user(self, api_client, client_request_data, login_normal_user):
        response = api_client.delete('/api/users/1', json=client_request_data, headers=self.header)
        assert response.status_code == 403
