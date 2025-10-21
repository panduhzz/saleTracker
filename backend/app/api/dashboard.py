"""
Dashboard API endpoints for statistics and analytics.
"""
from fastapi import APIRouter, HTTPException, Depends
from app.models.sales import DashboardStats, RecentSale
from app.services.cosmos_service import cosmos_service
from app.auth.swa_auth import get_user_id

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(user_id: str = Depends(get_user_id)):
    """
    Get dashboard statistics for the authenticated user.
    
    Returns:
        Dashboard statistics including total sales, items, monthly data, and average price
    """
    try:
        stats = await cosmos_service.get_dashboard_stats(user_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard stats: {str(e)}")


@router.get("/recent", response_model=list[RecentSale])
async def get_recent_sales(
    limit: int = 5,
    user_id: str = Depends(get_user_id)
):
    """
    Get recent sales for the authenticated user.
    
    Args:
        limit: Maximum number of recent sales to return (default: 5, max: 20)
        user_id: Authenticated user ID
        
    Returns:
        List of recent sales
    """
    # Limit the maximum number of recent sales
    limit = min(limit, 20)
    
    try:
        recent_sales = await cosmos_service.get_recent_sales(user_id, limit)
        return recent_sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve recent sales: {str(e)}")


@router.get("/", response_model=dict)
async def get_dashboard_data(user_id: str = Depends(get_user_id)):
    """
    Get complete dashboard data including stats and recent sales.
    
    Returns:
        Combined dashboard data with statistics and recent sales
    """
    try:
        # Get both stats and recent sales in parallel
        stats = await cosmos_service.get_dashboard_stats(user_id)
        recent_sales = await cosmos_service.get_recent_sales(user_id, 5)
        
        return {
            "stats": stats,
            "recentSales": recent_sales
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard data: {str(e)}")
