from fast_zero.security import create_token, SECRET_KEY, ALGORITHM
from jwt import decode

def test_token():
    data ={ 'test': 'test'}
    token = create_token(data)
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded
    