from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users", response_model=List[User], summary="Get all users", response_description="List of all users")
def get_users():
    """
    Retrieve the list of all users.

    - **Returns**: List of users
    """
    return users


@app.post("/user/{username}/{age}", response_model=User, summary="Create a new user",
          response_description="The created user")
def create_user(
        username: str = Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
        age: int = Path(ge=18, le=120, description='Enter age', example=24)
) -> User:
    """
    Create a new user.

    - **username**: The username of the user (5-20 characters).
    - **age**: The age of the user (18-120).

    - **Returns**: The created user.
    """
    new_id = 1 if not users else users[-1].id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}", response_model=User, summary="Update an existing user",
         response_description="The updated user")
def update_user(
        user_id: int,
        username: str = Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
        age: int = Path(ge=18, le=120, description='Enter age', example=24)
):
    """
    Update an existing user.

    - **user_id**: The ID of the user to update.
    - **username**: The new username of the user (5-20 characters).
    - **age**: The new age of the user (18-120).

    - **Returns**: The updated user.
    """
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User, summary="Delete a user", response_description="The deleted user")
def delete_user(user_id: int):
    """
    Delete a user by ID.

    - **user_id**: The ID of the user to delete.

    - **Returns**: The deleted user.
    """
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")

