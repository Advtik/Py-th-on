import enum
from tkinter import NO
from turtle import title
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Response,status
from pydantic import BaseModel

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    id:int


my_posts=[{"title":"Post1","content":"THis is post1","id":1},{"title":"Post2","content":"This is post2","id":2}]

print(my_posts)

def find_post(id):
    for p in my_posts:
        if(p["id"]==int(id)):
            return p


@app.get("/")
async def root():
    return {"message": "Welcome"}
  
@app.get("/posts")
async def posts():
    return {"data":my_posts}

@app.post("/createpost",status_code=status.HTTP_201_CREATED)
async def createpost(new_post: Post):
    print(new_post)
    my_posts.append(new_post.dict())
    print(my_posts)
    return new_post

# @app.get("/posts/{id}")
# async def getpost(id:int):
#     post=find_post((id))
#     return {"post":post}   order matters because if in the next route of latest "latest" can be interpreted as {id} in fastapi 

@app.get("/posts/latest")
async def getlatestpost():
    post=my_posts[len(my_posts)-1]
    return {"post":post}

@app.get("/posts/{id}")
async def getpost(id:int, response: Response):
    post=find_post((id))
    print(post)
    if not post:
        # response.status_code=status.HTTP_404_NOT_FOUND           (can be done like this but there's a better way)
        # return {"message":f"post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found") #better way
    return {"post":post}  #this is where "/posts/{id}" should be after "/posts/latest"


def find_index_post(id):
    print(my_posts)
    for i,p in enumerate(my_posts):
        if(p["id"]==id):
            return i

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def deletepost(id:int):
    index=find_index_post(id) 
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def updatepost(id:int,post:Post):
    index=find_index_post(id) 
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    post_dict=post.model_dump()
    my_posts[index]=post_dict
    return {"data":post}

