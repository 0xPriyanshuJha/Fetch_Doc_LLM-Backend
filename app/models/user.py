from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    _tablename_ = 'users'

    user_id = Column(String(255), primary_key=True, index=True)
    api_calls = Column(Integer, default=1)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, api_calls={self.api_calls})>"