from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Path
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

users: List[User] = []

@app.on_event("startup")
async def startup_event():
    users.append(User(id=1, username='UrbanUser', age=24))
    users.append(User(id=2, username='UrbanTest', age=22))
    users.append(User(id=3, username='Capybara', age=60))

@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users_list": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int = Path(...)):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse("users.html", {"request": request, "user": user})
