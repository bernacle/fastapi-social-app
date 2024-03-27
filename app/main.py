from typing import Optional
from fastapi import Response, FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randint


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Post 1", "content": "This is the content of post 1", "published": True, "rating": 5, "id": 1},
            {"title": "Post 2", "content": "This is the content of post 2", "published": False, "rating": 4, "id": 2},
            {"title": "Post 3", "content": "This is the content of post 3", "published": True, "rating": 3, "id": 3},]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randint(0, 10000000)
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {"data": [post for post in my_posts if post["id"] == id]}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_dict = post.model_dump()

    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}