from turtle import title
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True,
    rating:Optional[int]=None


my_posts=[{"title":"Post1","content":"THis is post1","id":1},{"title":"Post2","content":"This is post2","id":2}]

def find_post(id):
    for p in my_posts:
        if(p["id"]==int(id)):
            return p


@app.get("/")
async def root():
    return {"message": "Welcome"}
  
@app.get("/posts")
async def posts():
    return {"message":"This is posts"}

@app.post("/createpost")
async def createpost(new_post: Post):
    print(new_post)
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
async def getpost(id:int):
    post=find_post((id))
    return {"post":post}  #this is where "/posts/{id}" should be after "/posts/latest"