# Sale Tracker API Backend

FastAPI backend for the Sale Tracker application with Azure Cosmos DB integration.

## 🏗️ Architecture

- **Framework**: FastAPI with async/await support
- **Database**: Azure Cosmos DB with SQL API
- **Authentication**: Azure Static Web Apps built-in authentication
- **Containerization**: Docker with multi-stage builds
- **Package Management**: uv for fast Python package management

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── sales.py         # Sales CRUD endpoints
│   │   └── dashboard.py     # Dashboard analytics endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── sales.py         # Pydantic models for data validation
│   ├── services/
│   │   ├── __init__.py
│   │   └── cosmos_service.py # Cosmos DB operations
│   └── auth/
│       ├── __init__.py
│       └── swa_auth.py      # Azure SWA authentication
├── tests/                   # Unit and integration tests
├── Dockerfile              # Multi-stage Docker build
├── pyproject.toml          # Python project configuration
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Azure Cosmos DB account
- Docker (for containerization)

### Local Development

1. **Install dependencies**:
   ```bash
   # Install uv package manager
   pip install uv
   
   # Install project dependencies
   uv sync
   ```

2. **Set up environment variables**:
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your Cosmos DB connection details
   ```

3. **Run the application**:
   ```bash
   # Activate virtual environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Run with uvicorn
   uvicorn app.main:app --reload --port 8000
   ```

4. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Docker Development

1. **Build the image**:
   ```bash
   docker build -t sale-tracker-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 --env-file .env sale-tracker-api
   ```

## 🔐 Authentication

The API uses Azure Static Web Apps built-in authentication:

- **Headers**: Extracts user info from `x-ms-client-principal` header
- **User ID**: Used as partition key for Cosmos DB
- **Protected Routes**: All `/api/*` endpoints require authentication

## 📊 API Endpoints

### Sales Management
- `GET /api/sales` - List all sales for user
- `POST /api/sales` - Create new sale
- `GET /api/sales/{id}` - Get specific sale
- `PUT /api/sales/{id}` - Update sale
- `DELETE /api/sales/{id}` - Delete sale

### Dashboard Analytics
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent` - Get recent sales
- `GET /api/dashboard` - Get complete dashboard data

### System
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/user` - Current user info

## 🗄️ Database Schema

### Sales Collection
```json
{
  "id": "uuid",
  "userId": "user123",
  "productName": "Nike Air Jordan 1",
  "amount": 180.00,
  "saleDate": "2024-01-15T10:30:00Z",
  "customerName": "John Doe",
  "platform": "stockx",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

### Partition Key
- **Partition Key**: `userId` for data isolation
- **Indexing**: Automatic indexing enabled
- **Query Performance**: Optimized for user-scoped queries

## 🐳 Deployment

### Azure Container Apps

1. **Build and push to ACR**:
   ```bash
   # Build image
   docker build -t yourregistry.azurecr.io/sale-tracker-api:latest .
   
   # Push to registry
   docker push yourregistry.azurecr.io/sale-tracker-api:latest
   ```

2. **Deploy to Container Apps**:
   ```bash
   az containerapp create \
     --name sale-tracker-api \
     --resource-group sale-tracker-rg \
     --image yourregistry.azurecr.io/sale-tracker-api:latest \
     --target-port 8000 \
     --ingress external \
     --environment-variables COSMOSDB_ENDPOINT=$COSMOSDB_ENDPOINT \
     --secrets cosmosdb-key=$COSMOSDB_KEY
   ```

### Environment Variables

#### Production
- `COSMOSDB_ENDPOINT` - Cosmos DB endpoint
- `AZURE_CLIENT_ID` - Managed identity client ID
- `GITHUB_CLIENT_ID` - GitHub OAuth client ID
- `GITHUB_CLIENT_SECRET` - GitHub OAuth client secret

#### Development
- `COSMOSDB_CONNECTION_STRING` - Full connection string
- `ENVIRONMENT=development`
- `LOG_LEVEL=DEBUG`

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_sales.py
```

## 🔧 Development Tools

### Code Formatting
```bash
# Format code with black
black app/

# Sort imports with isort
isort app/
```

### Linting
```bash
# Run flake8 linter
flake8 app/
```

## 📝 API Documentation

- **Swagger UI**: `/docs` - Interactive API documentation
- **ReDoc**: `/redoc` - Alternative documentation format
- **OpenAPI Schema**: `/openapi.json` - Machine-readable API specification

## 🚨 Error Handling

- **HTTP Exceptions**: Proper status codes and error messages
- **Validation Errors**: Pydantic model validation
- **Database Errors**: Cosmos DB exception handling
- **Authentication Errors**: SWA authentication failures

## 🔒 Security

- **Non-root User**: Docker container runs as non-root user
- **Managed Identity**: Production uses Azure managed identity
- **CORS Configuration**: Configurable allowed origins
- **Input Validation**: Pydantic model validation for all inputs

## 📈 Performance

- **Async Operations**: All database operations are async
- **Connection Pooling**: Cosmos DB client connection pooling
- **Query Optimization**: Efficient Cosmos DB queries
- **Caching**: Consider adding Redis for frequently accessed data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the FastAPI documentation
- Review Azure Cosmos DB documentation
