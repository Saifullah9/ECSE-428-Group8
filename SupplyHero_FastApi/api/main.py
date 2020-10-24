from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.user import User

from api import supply_list
from api.auth import fastapi_users
from api.config import jwt_authentication

# Backend FastAPI Server Declaration
app = FastAPI()


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router to /login endpoint More info:
# https://frankie567.github.io/fastapi-users/configuration/routers/auth/
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), tags=["auth"]
)

# Router to /register endpoint More info:
# https://frankie567.github.io/fastapi-users/configuration/routers/register/
app.include_router(
    fastapi_users.get_register_router(), tags=["auth"]
)

# Routers for Logic related to School Supply Lists
app.include_router(supply_list.router)


@app.get("/")
async def main(user: User = Depends(fastapi_users.get_current_active_user)):
    return {'username': user.email,
            'pass': user.hashed_password}
