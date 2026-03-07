import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load nội dung file .env vào biến môi trường
load_dotenv()

# Lấy giá trị từ .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Nếu quên cấu hình trong .env thì báo lỗi ngay để biết
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("Chưa cấu hình DATABASE_URL trong file .env")

# Tạo engine kết nối
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Tạo SessionLocal để thao tác với DB trong từng request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class cho các Model sau này kế thừa
Base = declarative_base()


# Dependency để lấy DB session (Dùng trong API Controller)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
