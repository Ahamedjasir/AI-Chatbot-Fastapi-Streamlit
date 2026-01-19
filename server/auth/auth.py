from jose import jwt
from datetime import timedelta,datetime
SECRET_KEY="fastAPI"
EXPIRE_TIME=30
ALGORITHM="HS256"
def auth(data:dict):
    encode_text=data.copy()
    expire=datetime.now()+timedelta(minutes=EXPIRE_TIME)
    encode_text.update({"exp":expire})
    token=jwt.encode(encode_text,SECRET_KEY,algorithm=ALGORITHM)
    return token







