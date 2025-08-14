# app/models/prompt.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    prompt_text = Column(Text, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)
    share_token = Column(String, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)


    user = relationship("User", back_populates="prompts")
    images = relationship("PromptImage", back_populates="prompt", cascade="all, delete")


class PromptImage(Base):
    __tablename__ = "prompt_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    prompt_id = Column(Integer, ForeignKey("prompts.id", ondelete="CASCADE"))

    prompt = relationship("Prompt", back_populates="images")


