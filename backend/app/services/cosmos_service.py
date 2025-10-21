"""
Azure Cosmos DB service for sales data operations.
"""
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from app.models.sales import SaleItem, SaleCreate, SaleUpdate, DashboardStats, RecentSale

# Load environment variables
load_dotenv()


class CosmosService:
    """Service class for Cosmos DB operations."""
    
    def __init__(self):
        """Initialize Cosmos DB client."""
        self.database_name = "sales-database"
        self.container_name = "sales"
        self.client = None
        self.database = None
        self.container = None
        
        # Use managed identity in production, connection string locally
        if os.getenv("AZURE_CLIENT_ID"):
            # Production with managed identity
            credential = DefaultAzureCredential()
            cosmos_endpoint = os.environ.get('COSMOSDB_ENDPOINT')
            if not cosmos_endpoint:
                raise ValueError("COSMOSDB_ENDPOINT environment variable is required for production")
            self.client = CosmosClient(url=cosmos_endpoint, credential=credential)
        else:
            # Local development with connection string
            connection_string = os.environ.get('COSMOSDB_CONNECTION_STRING')
            if not connection_string:
                raise ValueError("COSMOSDB_CONNECTION_STRING environment variable is required for local development")
            
            # Check if connection string is a placeholder
            if "your-cosmosdb-account" in connection_string or "your-primary-key" in connection_string:
                print("WARNING: Using placeholder Cosmos DB connection string. Please update .env file with real values.")
                # Don't initialize the client yet - will fail gracefully
                return
            
            try:
                self.client = CosmosClient.from_connection_string(connection_string)
            except Exception as e:
                print(f"WARNING: Failed to connect to Cosmos DB: {e}")
                print("Please check your COSMOSDB_CONNECTION_STRING in .env file")
                # Don't raise the error - allow the app to start
                return
        
        # Get database and container references
        if self.client:
            self.database = self.client.get_database_client(self.database_name)
            self.container = self.database.get_container_client(self.container_name)
    
    async def create_sale(self, user_id: str, sale_data: SaleCreate) -> SaleItem:
        """
        Create a new sale item.
        
        Args:
            user_id: User ID (partition key)
            sale_data: Sale creation data
            
        Returns:
            Created sale item
        """
        if not self.client:
            # For local development, return a mock sale item
            print("WARNING: Cosmos DB not available, returning mock sale for development")
            now = datetime.now(timezone.utc).isoformat()
            sale_id = str(uuid.uuid4())
            
            return SaleItem(
                id=sale_id,
                userId=user_id,
                productName=sale_data.productName,
                amount=sale_data.amount,
                saleDate=sale_data.saleDate,
                customerName=sale_data.customerName,
                platform=sale_data.platform,
                createdAt=now,
                updatedAt=now
            )
        
        now = datetime.now(timezone.utc).isoformat()
        sale_id = str(uuid.uuid4())
        
        sale_item = SaleItem(
            id=sale_id,
            userId=user_id,
            productName=sale_data.productName,
            amount=sale_data.amount,
            saleDate=sale_data.saleDate,
            customerName=sale_data.customerName,
            platform=sale_data.platform,
            createdAt=now,
            updatedAt=now
        )
        
        try:
            # Convert to dict for Cosmos DB
            sale_dict = sale_item.model_dump()
            created_item = self.container.create_item(sale_dict)
            return SaleItem(**created_item)
        except exceptions.CosmosResourceExistsError:
            raise ValueError("Sale with this ID already exists")
        except Exception as e:
            raise RuntimeError(f"Failed to create sale: {str(e)}")
    
    async def get_sale(self, user_id: str, sale_id: str) -> Optional[SaleItem]:
        """
        Get a specific sale by ID.
        
        Args:
            user_id: User ID (partition key)
            sale_id: Sale ID
            
        Returns:
            Sale item or None if not found
        """
        if not self.client:
            raise RuntimeError("Cosmos DB client not initialized. Please check your connection string.")
        
        try:
            item = self.container.read_item(
                item=sale_id,
                partition_key=user_id
            )
            return SaleItem(**item)
        except exceptions.CosmosResourceNotFoundError:
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to get sale: {str(e)}")
    
    async def get_sales_by_user(self, user_id: str, limit: int = 100) -> List[SaleItem]:
        """
        Get all sales for a user.
        
        Args:
            user_id: User ID (partition key)
            limit: Maximum number of items to return
            
        Returns:
            List of sale items
        """
        if not self.client:
            # Return empty list for local development when Cosmos DB is not available
            print("WARNING: Cosmos DB not available, returning empty sales list for development")
            return []
        
        try:
            query = "SELECT * FROM c WHERE c.userId = @userId ORDER BY c.saleDate DESC"
            parameters = [{"name": "@userId", "value": user_id}]
            
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=False,
                max_item_count=limit
            ))
            
            return [SaleItem(**item) for item in items]
        except Exception as e:
            raise RuntimeError(f"Failed to get sales: {str(e)}")
    
    async def update_sale(self, user_id: str, sale_id: str, update_data: SaleUpdate) -> Optional[SaleItem]:
        """
        Update an existing sale.
        
        Args:
            user_id: User ID (partition key)
            sale_id: Sale ID
            update_data: Update data
            
        Returns:
            Updated sale item or None if not found
        """
        if not self.client:
            raise RuntimeError("Cosmos DB client not initialized. Please check your connection string.")
        
        try:
            # Get existing item
            existing_item = await self.get_sale(user_id, sale_id)
            if not existing_item:
                return None
            
            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict['updatedAt'] = datetime.now(timezone.utc).isoformat()
            
            # Merge with existing data
            updated_data = existing_item.model_dump()
            updated_data.update(update_dict)
            
            # Update in Cosmos DB
            updated_item = self.container.replace_item(
                item=sale_id,
                body=updated_data
            )
            
            return SaleItem(**updated_item)
        except exceptions.CosmosResourceNotFoundError:
            return None
        except Exception as e:
            raise RuntimeError(f"Failed to update sale: {str(e)}")
    
    async def delete_sale(self, user_id: str, sale_id: str) -> bool:
        """
        Delete a sale.
        
        Args:
            user_id: User ID (partition key)
            sale_id: Sale ID
            
        Returns:
            True if deleted, False if not found
        """
        if not self.client:
            raise RuntimeError("Cosmos DB client not initialized. Please check your connection string.")
        
        try:
            self.container.delete_item(
                item=sale_id,
                partition_key=user_id
            )
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
        except Exception as e:
            raise RuntimeError(f"Failed to delete sale: {str(e)}")
    
    async def get_dashboard_stats(self, user_id: str) -> DashboardStats:
        """
        Get dashboard statistics for a user.
        
        Args:
            user_id: User ID (partition key)
            
        Returns:
            Dashboard statistics
        """
        if not self.client:
            # Return mock data for local development when Cosmos DB is not available
            print("WARNING: Cosmos DB not available, returning mock data for development")
            return DashboardStats(
                totalSales=0.0,
                totalItems=0,
                thisMonth=0.0,
                avgPrice=0.0
            )
        
        try:
            # Get current month for filtering
            now = datetime.now(timezone.utc)
            current_month = now.strftime("%Y-%m")
            
            # Use separate queries for each aggregate to avoid composition issues
            # Get total sales
            total_sales_query = """
                SELECT VALUE SUM(c.amount)
                FROM c 
                WHERE c.userId = @userId
            """
            
            # Get total items
            total_items_query = """
                SELECT VALUE COUNT(1)
                FROM c 
                WHERE c.userId = @userId
            """
            
            # Get average price
            avg_price_query = """
                SELECT VALUE AVG(c.amount)
                FROM c 
                WHERE c.userId = @userId
            """
            
            # Get this month's sales
            this_month_query = """
                SELECT VALUE SUM(c.amount)
                FROM c 
                WHERE c.userId = @userId AND STARTSWITH(c.saleDate, @currentMonth)
            """
            
            parameters = [{"name": "@userId", "value": user_id}]
            this_month_parameters = [
                {"name": "@userId", "value": user_id},
                {"name": "@currentMonth", "value": current_month}
            ]
            
            # Execute all queries
            total_sales_result = list(self.container.query_items(
                query=total_sales_query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            total_items_result = list(self.container.query_items(
                query=total_items_query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            avg_price_result = list(self.container.query_items(
                query=avg_price_query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            this_month_result = list(self.container.query_items(
                query=this_month_query,
                parameters=this_month_parameters,
                enable_cross_partition_query=True
            ))
            
            # Extract values from results with proper null handling
            total_sales = total_sales_result[0] if total_sales_result and len(total_sales_result) > 0 and total_sales_result[0] is not None else 0
            total_items = total_items_result[0] if total_items_result and len(total_items_result) > 0 and total_items_result[0] is not None else 0
            avg_price = avg_price_result[0] if avg_price_result and len(avg_price_result) > 0 and avg_price_result[0] is not None else 0
            this_month_sales = this_month_result[0] if this_month_result and len(this_month_result) > 0 and this_month_result[0] is not None else 0
            
            return DashboardStats(
                totalSales=float(total_sales),
                totalItems=int(total_items),
                thisMonth=float(this_month_sales),
                avgPrice=float(avg_price)
            )
        except Exception as e:
            raise RuntimeError(f"Failed to get dashboard stats: {str(e)}")
    
    async def get_recent_sales(self, user_id: str, limit: int = 5) -> List[RecentSale]:
        """
        Get recent sales for a user.
        
        Args:
            user_id: User ID (partition key)
            limit: Maximum number of recent sales
            
        Returns:
            List of recent sales
        """
        if not self.client:
            # Return empty list for local development when Cosmos DB is not available
            print("WARNING: Cosmos DB not available, returning empty recent sales for development")
            return []
        
        try:
            query = """
                SELECT c.id, c.productName, c.amount, c.saleDate, c.platform, c.customerName
                FROM c 
                WHERE c.userId = @userId
                ORDER BY c.saleDate DESC
            """
            
            parameters = [{"name": "@userId", "value": user_id}]
            
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=False,
                max_item_count=limit
            ))
            
            return [RecentSale(**item) for item in items]
        except Exception as e:
            raise RuntimeError(f"Failed to get recent sales: {str(e)}")


# Global service instance
cosmos_service = CosmosService()
