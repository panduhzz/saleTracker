"""
Pydantic models for sales data validation and serialization.
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    """Supported sales platforms."""
    EBAY = "ebay"
    GOAT = "goat"
    STOCKX = "stockx"
    MANUAL = "manual"


class SaleItem(BaseModel):
    """Complete sale item model with all fields."""
    id: str = Field(..., description="Unique identifier for the sale")
    userId: str = Field(..., description="User ID (partition key)")
    productName: str = Field(..., min_length=1, max_length=200, description="Name of the product sold")
    amount: float = Field(..., gt=0, description="Sale amount in USD")
    saleDate: str = Field(..., description="Date of sale in ISO format")
    customerName: Optional[str] = Field(None, max_length=100, description="Customer name (optional)")
    platform: Platform = Field(..., description="Platform where the sale occurred")
    createdAt: str = Field(..., description="Creation timestamp in ISO format")
    updatedAt: str = Field(..., description="Last update timestamp in ISO format")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "userId": "user123",
                "productName": "Nike Air Jordan 1",
                "amount": 180.00,
                "saleDate": "2024-01-15T10:30:00Z",
                "customerName": "John Doe",
                "platform": "stockx",
                "createdAt": "2024-01-15T10:30:00Z",
                "updatedAt": "2024-01-15T10:30:00Z"
            }
        }


class SaleCreate(BaseModel):
    """Model for creating a new sale (without system fields)."""
    productName: str = Field(..., min_length=1, max_length=200, description="Name of the product sold")
    amount: float = Field(..., gt=0, description="Sale amount in USD")
    saleDate: str = Field(..., description="Date of sale in ISO format")
    customerName: Optional[str] = Field(None, max_length=100, description="Customer name (optional)")
    platform: Platform = Field(..., description="Platform where the sale occurred")

    class Config:
        json_schema_extra = {
            "example": {
                "productName": "Nike Air Jordan 1",
                "amount": 180.00,
                "saleDate": "2024-01-15T10:30:00Z",
                "customerName": "John Doe",
                "platform": "stockx"
            }
        }


class SaleUpdate(BaseModel):
    """Model for updating an existing sale."""
    productName: Optional[str] = Field(None, min_length=1, max_length=200, description="Name of the product sold")
    amount: Optional[float] = Field(None, gt=0, description="Sale amount in USD")
    saleDate: Optional[str] = Field(None, description="Date of sale in ISO format")
    customerName: Optional[str] = Field(None, max_length=100, description="Customer name (optional)")
    platform: Optional[Platform] = Field(None, description="Platform where the sale occurred")

    class Config:
        json_schema_extra = {
            "example": {
                "productName": "Nike Air Jordan 1 Retro",
                "amount": 185.00,
                "customerName": "Jane Doe"
            }
        }


class DashboardStats(BaseModel):
    """Dashboard statistics model."""
    totalSales: float = Field(..., description="Total sales amount")
    totalItems: int = Field(..., description="Total number of items sold")
    thisMonth: float = Field(..., description="Sales for current month")
    avgPrice: float = Field(..., description="Average price per item")

    class Config:
        json_schema_extra = {
            "example": {
                "totalSales": 12450.00,
                "totalItems": 23,
                "thisMonth": 3250.00,
                "avgPrice": 541.30
            }
        }


class RecentSale(BaseModel):
    """Model for recent sales display."""
    id: str
    productName: str
    amount: float
    saleDate: str
    platform: Platform
    customerName: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "productName": "Nike Air Jordan 1",
                "amount": 180.00,
                "saleDate": "2024-01-15T10:30:00Z",
                "platform": "stockx",
                "customerName": "John Doe"
            }
        }
