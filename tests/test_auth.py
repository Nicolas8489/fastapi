from app import auth

def test_password_hashing():
    password = "mi_password_123"
    hashed = auth.hash_password(password)
    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("password_incorrecto", hashed)

def test_jwt_tokens():
    username = "juan123"
    token = auth.create_access_token({"sub": username})
    assert auth.verify_token(token) == username