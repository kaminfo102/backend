from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_tests = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    pass_rate = Column(Float, default=0.0)
    total_time = Column(Integer, default=0)  # in minutes

    user = relationship("User", back_populates="stats")
