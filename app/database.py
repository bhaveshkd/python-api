from sqlalchemy import create_engine, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# SQL_ALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>/<hostname>/<db-name>'
SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connectrion was successful")
#         break
#     except Exception as error:
#         print("Database connectrion was not successful")
#         print("Error: ", error)
#         time.sleep(2)