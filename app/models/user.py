from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    # user_id is the primary key
    user_id = Column(String(255), primary_key=True, index=True)
    api_calls = Column(Integer, default=1)
    # __repr__ method to represent the object
    def __repr__(self):
        return f"<User(user_id={self.user_id}, api_calls={self.api_calls})>"