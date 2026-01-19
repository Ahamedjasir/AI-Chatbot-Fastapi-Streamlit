from sqlalchemy import Column,String,Integer,Text
from sqlalchemy.orm import declarative_base
base=declarative_base()


class ChatHistory(base):
    __tablename__="chat_history"
    id =Column(Integer,autoincrement=True,primary_key=True,)
    role=Column(String(20))
    content=Column(Text)