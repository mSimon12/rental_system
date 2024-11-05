import pytest

class TestApiClients:

    @pytest.fixture
    def add_client_request(self):
        return {'username': 'new_client',
                'email': 'email@email.com',
                'password': 'lsdjfjnasdldfdas12312knbwiuu3231uh13'}

    def test_get_clients_request(self, api_client):
        response = api_client.get('/api/clients/')
        assert response.status_code == 200
        assert len(response.json) == 2
        for item in response.json.keys():
            assert list(response.json[item].keys()) == ['email', 'username']

    def test_get_client_info(self, api_client):
        response = api_client.get('/api/clients/')

        for client_id in response.json.keys():
            response = api_client.get(f'/api/clients/{client_id}')
            assert response.status_code == 200


    def test_add_client_right_data(self, api_client, add_client_request):
        response = api_client.post('/api/clients/add', json=add_client_request)
        assert response.status_code == 201

        response = api_client.get('/api/clients/')
        assert add_client_request['username'] in list(response.json.values())[-1]['username']

    def test_add_client_avoid_duplicated(self, api_client, add_client_request):
        response = api_client.post('/api/clients/add', json=add_client_request)
        assert response.status_code == 201
        response = api_client.post('/api/clients/add', json=add_client_request)
        assert response.status_code == 400

    def test_add_client_missing_info(self, api_client, add_client_request):
        # missing username
        missing_req_data = {key:value for key, value in add_client_request.items() if key != 'username'}
        response = api_client.post('/api/clients/add', json=missing_req_data)
        assert response.status_code == 400

        # missing email
        missing_req_data = {key: value for key, value in add_client_request.items() if key != 'email'}
        response = api_client.post('/api/clients/add', json=missing_req_data)
        assert response.status_code == 400

        # missing password
        missing_req_data = {key: value for key, value in add_client_request.items() if key != 'password'}
        response = api_client.post('/api/clients/add', json=missing_req_data)
        assert response.status_code == 400

    def test_add_client_invalid_username(self, api_client, add_client_request):
        # invalid username
        add_client_request['username'] = None
        response = api_client.post('/api/clients/add', json=add_client_request)
        assert response.status_code == 400

        add_client_request['username'] = 100
        response = api_client.post('/api/clients/add', json=add_client_request)
        assert response.status_code == 400

    def test_add_client_invalid_email(self, api_client, add_client_request):
        # invalid username
        add_client_request['email'] = 200
        response = api_client.post('/api/clients/add', json=add_client_request)
        assert response.status_code == 400

    def test_add_client_invalid_password(self, api_client, add_client_request):
        # invalid username
        add_client_request['password'] = 300
        response = api_client.post('/api/clients/add', json=add_client_request)
        assert response.status_code == 400

    # def test_delete_client_request(self, api_client, add_client_request):
    #     response = api_client.post('/api/clients/add', json=add_client_request)
    #     assert response.status_code == 201
    #
    #     response2 = api_client.delete('/api/clients', json=add_client_request)
    #     assert response2.status_code == 204

