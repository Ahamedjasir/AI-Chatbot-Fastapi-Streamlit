from fastapi import FastAPI
from route.airoutes import router 
from models.aimodels import base
from database.db import engine

app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0"
)

base.metadata.create_all(bind=engine)
app.include_router(router)
@app.get("/")
def home():
    return {"message": "AI Chatbot backend is running"}
