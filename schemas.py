"""
Database Schemas for University Website

Each Pydantic model below maps to a MongoDB collection (lowercased class name).
Use these models for validation when creating documents via the API.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Faculty(BaseModel):
    name: str = Field(..., description="Faculty name, e.g., 'Faculty of Engineering'")
    description: Optional[str] = Field(None, description="Short description of the faculty")
    dean: Optional[str] = Field(None, description="Name of the dean")
    website: Optional[str] = Field(None, description="Public URL for the faculty")
    featured_image: Optional[str] = Field(None, description="Hero/cover image URL")

class Program(BaseModel):
    title: str = Field(..., description="Program title, e.g., 'Computer Science (BSc)'")
    level: str = Field(..., description="Program level, e.g., 'Undergraduate', 'Postgraduate'")
    faculty_id: Optional[str] = Field(None, description="Related faculty id as string")
    duration_years: Optional[int] = Field(None, ge=1, le=8, description="Typical duration in years")
    overview: Optional[str] = Field(None, description="Short overview of the program")

class News(BaseModel):
    title: str = Field(..., description="News title")
    content: str = Field(..., description="News content or summary")
    author: Optional[str] = Field(None, description="Author name")
    published_at: Optional[datetime] = Field(None, description="Publish datetime")
    cover_image: Optional[str] = Field(None, description="Cover image URL")

class Inquiry(BaseModel):
    full_name: str = Field(..., description="Prospective student full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    interest_program: Optional[str] = Field(None, description="Program of interest")
    message: Optional[str] = Field(None, description="Additional message")

# Existing example schemas can remain for reference
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
