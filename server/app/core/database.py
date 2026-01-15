from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL kết nối: postgresql://user:password@host:port/dbname
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5433/chat_db"

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
