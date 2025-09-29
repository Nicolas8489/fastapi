from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime

class Product(BaseModel):
    id: int = Field(..., description="Unique identifier for the product")
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    in_stock: bool = Field(default=True, description="Availability status")
    category: Optional[str] = Field(None, description="Product category")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Creation timestamp")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip()

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return round(v, 2)  # Round to 2 decimal places for consistency

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop Pro",
                "description": "High-performance laptop",
                "price": 1299.99,
                "in_stock": True,
                "category": "Electronics",
                "created_at": "2025-09-29T00:06:00-05:00"
            }
        }

class ProductCreate(Product):
    id: Optional[int] = None  # ID is optional on creation, auto-generated if needed

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    in_stock: Optional[bool] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True