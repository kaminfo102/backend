from pydantic import BaseModel
from typing import Optional, List

# Base Schemas
class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    slug: str

# Create Schemas
class CategoryCreate(CategoryBase):
    pass

# Response Schemas
class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    items: List[Category]
    total: int
    has_more: bool


class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    exam_url: Optional[str] = None
    category_id:int
    
class ExamInCategory(ExamBase):
    id:int
    class Config:
        from_attributes = True
