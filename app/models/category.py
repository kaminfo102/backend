
from sqlalchemy import Column, Integer, String, Text
from ..database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    image_url = Column(String)
    slug = Column(String, unique=True, index=True)
