from fastapi_users.authentication import JWTAuthentication

# Auth JWT
SECRET = "~#$2uzHs)~6y94_b"
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=604800)
