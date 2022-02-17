import uvicorn
from fastapi import FastAPI, Body, Depends
from smores.model import PostSchema, UserSchema, UserLoginSchema
from smores.auth.jwt_handler import signJWT
from smores.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "Penguins",
        "text": "Penguins are flightless birds"
    },
    {
        "id": 2,
        "title": "tigers",
        "text": "tigers are big ol cats"
    },
    {
        "id": 3,
        "title": "koalas",
        "text": "koalas are cute"
    }
]
users = []

app = FastAPI()


# Get - for testing
@app.get('/', tags=['test'])
def greet():
    return {"Hello": "World!"}


# Get Posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}


# Get single post by id
@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return {
            "error": "Post with this Id does not exist!"
        }
    for post in posts:
        if post['id'] == id:
            return {
                "data": post
            }


# Post a single blog post
@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post Added!"
    }


# 5 User Signup
@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }
