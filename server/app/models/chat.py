from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    type = Column(String, default="DIRECT")  # direct = 1-1 or group
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Denormalization: Lưu tin nhắn cuối cùng để load sidebar cho nhanh
    last_message_content = Column(String, nullable=True)
    last_message_at = Column(DateTime(timezone=True), nullable=True)

    # Quan hệ
    participants = relationship("Participant", back_populates="conversation")
    messages = relationship("Message", back_populates="conversation")


class Participant(Base):
    __tablename__ = "participants"
    conversation_id = Column(Integer, ForeignKey('conversations.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)