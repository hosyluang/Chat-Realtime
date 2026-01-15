# server/app/main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user  # Import để Base nhận biết được model User

# Lệnh này sẽ tạo tất cả các bảng trong DB (nếu chưa có)
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Chat App Backend is running!"}
