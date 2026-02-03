"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class EmployeeBase(BaseModel):
    """Base employee model with common attributes"""
    employee_id: str = Field(..., min_length=1, max_length=50, description="Unique employee ID")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    position: Optional[str] = Field(None, max_length=100, description="Position/Job title")
    salary: Optional[Decimal] = Field(None, ge=0, description="Salary")
    hire_date: Optional[date] = Field(None, description="Date of joining")
    is_active: bool = Field(True, description="Active status")


class EmployeeCreate(EmployeeBase):
    """Model for creating a new employee"""
    pass


class EmployeeUpdate(BaseModel):
    """Model for updating an employee (all fields optional)"""
    employee_id: Optional[str] = Field(None, min_length=1, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    salary: Optional[Decimal] = Field(None, ge=0)
    hire_date: Optional[date] = None
    is_active: Optional[bool] = None


class EmployeeResponse(EmployeeBase):
    """Model for employee response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }


class EmployeeListResponse(BaseModel):
    """Model for list of employees response"""
    total: int
    employees: list[EmployeeResponse]


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    success: bool = False