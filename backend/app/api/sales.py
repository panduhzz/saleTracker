"""
Sales API endpoints for CRUD operations.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.sales import SaleItem, SaleCreate, SaleUpdate
from app.services.cosmos_service import cosmos_service
from app.auth.swa_auth import get_user_id

router = APIRouter(prefix="/api/sales", tags=["sales"])


@router.get("/", response_model=List[SaleItem])
async def get_sales(user_id: str = Depends(get_user_id)):
    """
    Get all sales for the authenticated user.
    
    Returns:
        List of sale items
    """
    try:
        sales = await cosmos_service.get_sales_by_user(user_id)
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve sales: {str(e)}")


@router.post("/", response_model=SaleItem, status_code=201)
async def create_sale(
    sale_data: SaleCreate,
    user_id: str = Depends(get_user_id)
):
    """
    Create a new sale.
    
    Args:
        sale_data: Sale creation data
        user_id: Authenticated user ID
        
    Returns:
        Created sale item
    """
    try:
        sale = await cosmos_service.create_sale(user_id, sale_data)
        return sale
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create sale: {str(e)}")


@router.get("/{sale_id}", response_model=SaleItem)
async def get_sale(
    sale_id: str,
    user_id: str = Depends(get_user_id)
):
    """
    Get a specific sale by ID.
    
    Args:
        sale_id: Sale ID
        user_id: Authenticated user ID
        
    Returns:
        Sale item
    """
    sale = await cosmos_service.get_sale(user_id, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.put("/{sale_id}", response_model=SaleItem)
async def update_sale(
    sale_id: str,
    update_data: SaleUpdate,
    user_id: str = Depends(get_user_id)
):
    """
    Update a specific sale.
    
    Args:
        sale_id: Sale ID
        update_data: Update data
        user_id: Authenticated user ID
        
    Returns:
        Updated sale item
    """
    sale = await cosmos_service.update_sale(user_id, sale_id, update_data)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.delete("/{sale_id}", status_code=204)
async def delete_sale(
    sale_id: str,
    user_id: str = Depends(get_user_id)
):
    """
    Delete a specific sale.
    
    Args:
        sale_id: Sale ID
        user_id: Authenticated user ID
    """
    success = await cosmos_service.delete_sale(user_id, sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
