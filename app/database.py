#sqlalchemy setup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='postgresql://postgres:postgres123@localhost/fastapi_practice'  
# format of postgres url is 'postgres://<username>:<password>@<ip-address/hostname>/<database_name>'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

  #dependency
def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:db.close()