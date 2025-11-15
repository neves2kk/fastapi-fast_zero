from http import HTTPStatus
from fast_zero.schemas import UserResponseSchema

""" 
def test_create_user_return_created_and_user_with_id():
    client = TestClient(app)

    response = client.post("/users/", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })

    assert response.status_code == HTTPStatus.CREATED
    assert  response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com"
    } """

def test_read_users_with_users(client, user,create_test_token):
    user_schema = UserResponseSchema.model_validate(user).model_dump()
    response = client.get('/users/', headers={'Authorization': f'Bearer {create_test_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [user_schema]

def test_update_user(client, user, create_test_token): 
    response = client.put(
        '/user/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {create_test_token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }

""" def test_update_integrity_error(client, user):
    r = client.post(
        "/users",
        json={"username": "fausto", "email": "fausto@example.com", "password": "secret"},
    )
    assert r.status_code == 201

    r_update = client.put(
        f"/users/{user.id}",
        json={"username": "fausto", "email": "bob@example.com", "password": "mynewpassword"},
    )
    assert r_update.status_code == HTTPStatus.CONFLICT
    assert r_update.json()["detail"].lower().startswith("username or email")
 """

def test_delete_user(client,user):
    response = client.delete('user/1')
    assert response.status_code == HTTPStatus.NO_CONTENT

""" def test_create_token(client, user):
    response = client.post(
        '/login',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )



    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'Bearer' """