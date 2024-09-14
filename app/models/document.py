from sqlalchemy import Column, Integer, String, Float
from app.db import Base

# Base class for the User model
class Document(Base):
    __tablename__ = "documents"

# Columns for the User model
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    similarity = Column(Float, default=0.0)