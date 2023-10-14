from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    answer = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, text: str, answer: str):
        self.text = text
        self.answer = answer
