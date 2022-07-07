from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException

from models import Gender, Role, User, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("bebc1161-f647-4103-8822-2812f5c34f3d"),
        first_name="Gala",
        last_name="Grudinina",
        gender=Gender.female,
        roles=[Role.admin]
    ),
    User(
        id=UUID("b5595179-a265-4345-95d6-56d99e1ee3cf"),
        first_name="Martin",
        last_name="Wang",
        gender=Gender.male,
        roles=[Role.user, Role.admin]
    )
]


@app.get("/")
async def root():
    return {"Hello": "World"}

url = "/api/v1/users"


@app.get(url)
async def fetch_users():
    return db


@app.post(url)
async def register(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist")


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )
