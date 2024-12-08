from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class ProduceReport(Base):
    __tablename__ = "produce_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    produce_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    remarks = Column(Text)

    user = relationship("User")
