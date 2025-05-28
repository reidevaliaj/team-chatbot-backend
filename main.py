from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, get_db
from models import Message
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://team-chatbot-frontend.vercel.app"],  # allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/messages")
async def create_message(message: dict, db: AsyncSession = Depends(get_db)):
    new_msg = Message(
        sender_name=message["sender_name"],
        content=message["content"]
    )
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)
    return new_msg

@app.get("/messages")
async def get_messages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message))
    return result.scalars().all()
