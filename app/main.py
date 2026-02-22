
from email.policy import default
from multiprocessing import synchronize
from xmlrpc.client import boolean

from fastapi import  Depends, FastAPI, HTTPException, Response,status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


#sqlalchemy
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

# // sqlalchemy

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:boolean=True


while(True):
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi_practice',user='postgres',password='postgres123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection is successful")
        break
    except Exception as error:
        print("Failed to connect to database")
        print("error: ", error)
        time.sleep(2)
    



my_posts=[{"title":"Post1","content":"THis is post1","id":1},{"title":"Post2","content":"This is post2","id":2}]


def find_post(id):
    for p in my_posts:
        if(p["id"]==int(id)):
            return p

@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/posts")
async def testing(db: Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data":posts}

@app.post("/createpost",status_code=status.HTTP_201_CREATED)
async def createpost(post: Post, db : Session=Depends(get_db)):

    ##SQL only->
    #cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING * """,(post.title,post.content))
    #new_post=cursor.fetchone()
    #conn.commit()

    ## SQLAlchemy->
    #new_post=models.Post(title=post.title,content=post.content)  # if we have 50+ fields like title, content etc etc it will become messy so we use **post.dict()
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}


@app.get("/posts/{id}")
async def getpost(id:int, db:Session=Depends(get_db)):
    #sql only
    #cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),)) #the comma after str(id) needs to be studied here and str should be added because of type checking 
    #post=cursor.fetchone()

    #sqlalchemy
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found") #better way
    return {"post_detail":post} 


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def deletepost(id:int,db:Session=Depends(get_db)):

#       sql only
#     cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id),))
#     deleted_post=cursor.fetchone()
#     conn.commit()

#       sql alchemy
    deleted_post=db.query(models.Post).filter(models.Post.id==id)

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def updatepost(id:int,post:Post,db:Session=Depends(get_db)):


#     cursor.execute("""UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING * """,(post.title,post.content,str(id)))
#     updated_post=cursor.fetchone()
#     conn.commit()
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    db.refresh(updated_post)
    return {"data":updated_post}


#this is without sqlalchemy
  
# @app.get("/posts")
# async def posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts=cursor.fetchall()
#     return {"data":posts}

# @app.post("/createpost",status_code=status.HTTP_201_CREATED)
# async def createpost(post: Post):
#     cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING * """,(post.title,post.content))
#     new_post=cursor.fetchone()
#     conn.commit()
#     return {"data":new_post} 

# # @app.get("/posts/{id}")
# # async def getpost(id:int):
# #     post=find_post((id))
# #     return {"post":post}   order matters because if in the next route of latest "latest" can be interpreted as {id} in fastapi 

# @app.get("/posts/latest")
# async def getlatestpost():
#     post=my_posts[len(my_posts)-1]
#     return {"post":post}

# @app.get("/posts/{id}")
# async def getpost(id:int, response: Response):
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),)) #the comma after str(id) needs to be studied here and str should be added because of type checking 
#     post=cursor.fetchone()
#     if not post:
#         # response.status_code=status.HTTP_404_NOT_FOUND           (can be done like this but there's a better way)
#         # return {"message":f"post with id {id} not found"}
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found") #better way
#     return {"post_detail":post}  #this is where "/posts/{id}" should be after "/posts/latest"


# def find_index_post(id):
#     print(my_posts)
#     for i,p in enumerate(my_posts):
#         if(p["id"]==id):
#             return i

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# async def deletepost(id:int):
#     cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id),))
#     deleted_post=cursor.fetchone()
#     conn.commit()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# async def updatepost(id:int,post:Post):
#     cursor.execute("""UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING * """,(post.title,post.content,str(id)))
#     updated_post=cursor.fetchone()
#     conn.commit()
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
#     return {"data":updated_post}

