# server/app/main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.api import auth, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# tao bang (chi chay lan dau neu chua co bang)
Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép React truy cập
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép mọi method (GET, POST...)
    allow_headers=["*"],
)

# Dang ky cac router
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Chat App Backend is running!"}
