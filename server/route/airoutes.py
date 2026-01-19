from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from models.schema import ChatRequest, ImageRequest
from services.aiservices import chat_with_ai, generate_image
from models.aimodels import ChatHistory
from database.db import get_db

router = APIRouter()

# ---------------- CHAT ----------------
@router.post("/chat")
def ai_chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        chat_history = [
            {"role": "user", "content": req.message}
        ]

        reply = chat_with_ai(chat_history)

        # ✅ SAVE TO DB
        db.add(ChatHistory(role="user", content=req.message))
        db.add(ChatHistory(role="assistant", content=reply))
        db.commit()

        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- IMAGE ----------------
@router.post("/image")
def ai_image(req: ImageRequest):
    try:
        img_bytes = generate_image(req.prompt)

        return Response(content=img_bytes, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- GET SAVED CHATS ----------------
@router.get("/history")
def get_chat_history(db: Session = Depends(get_db)):
    chats = db.query(ChatHistory).order_by(ChatHistory.id.asc()).all()

    history = []
    for c in chats:
        history.append({
            "id": c.id,
            "role": c.role,        
            "content": c.content  
        })

    return history
