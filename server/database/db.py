from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()
db=os.getenv("DB_URL")

engine=create_engine(db,connect_args={"check_same_thread":False})
Sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()
