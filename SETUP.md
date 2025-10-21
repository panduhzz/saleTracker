# Sale Tracker - Setup Guide

## Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- Azure Cosmos DB account
- GitHub account (for authentication)

### Local Development Setup

#### Option 1: Automated Setup (Recommended)
```bash
# Windows PowerShell
.\setup-dev.ps1

# Linux/Mac
./setup-dev.sh
```

#### Option 2: Manual Setup

1. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install uv
   uv sync
   cd ..
   ```

3. **Configure Environment Variables**
   ```bash
   # Copy environment files
   cp env.development .env.development
   cp backend/env.local backend/.env
   
   # Edit backend/.env with your Cosmos DB connection string
   ```

4. **Start the Application**
   ```bash
   # Terminal 1: Start Backend
   cd backend
   uvicorn app.main:app --reload
   
   # Terminal 2: Start Frontend
   npm start
   ```

### Production Deployment

#### Azure Static Web Apps Deployment

1. **Build the Application**
   ```bash
   npm run build
   ```

2. **Deploy to Azure**
   ```bash
   # Using PowerShell
   .\deploy.ps1
   
   # Or manually with SWA CLI
   swa deploy --app-location "src" --output-location "build"
   ```

3. **Configure Azure Environment Variables**
   - `GITHUB_CLIENT_ID`: Your GitHub OAuth app client ID
   - `GITHUB_CLIENT_SECRET`: Your GitHub OAuth app client secret
   - `COSMOSDB_CONNECTION_STRING`: Your Cosmos DB connection string

## Configuration

### Frontend Environment Variables
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000 for dev, /api for production)
- `REACT_APP_ENVIRONMENT`: Environment (development/production)
- `REACT_APP_DEBUG`: Enable debug logging (true/false)

### Backend Environment Variables
- `COSMOSDB_CONNECTION_STRING`: Azure Cosmos DB connection string
- `COSMOSDB_ENDPOINT`: Cosmos DB endpoint (for managed identity)
- `AZURE_CLIENT_ID`: Managed identity client ID (for production)
- `ENVIRONMENT`: Environment (development/production)
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

## Troubleshooting

### Common Issues

1. **Frontend won't start**
   - Check Node.js version: `node --version`
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

2. **Backend won't start**
   - Check Python version: `python --version`
   - Install dependencies: `cd backend && uv sync`
   - Check environment variables in `.env` file

3. **Database connection fails**
   - Verify Cosmos DB connection string
   - Check if Cosmos DB account is accessible
   - Ensure database and container exist

4. **Authentication issues**
   - Check GitHub OAuth configuration
   - Verify environment variables in Azure
   - Check staticwebapp.config.json routing

### Development Tips

1. **Test Authentication Locally**
   - Use the "Test Login" button in the login component
   - This simulates authentication for local development

2. **Database Testing**
   - The app gracefully handles database connection failures
   - Mock data is returned when Cosmos DB is not available

3. **API Testing**
   - Backend API docs available at http://localhost:8000/docs
   - Test endpoints using the interactive Swagger UI

## File Structure

```
saleTracker/
├── src/                    # Frontend React application
├── backend/               # Backend FastAPI application
├── build/                 # Built frontend (generated)
├── public/               # Static assets
├── env.development       # Frontend development environment
├── env.production        # Frontend production environment
├── setup-dev.ps1         # Development setup script
├── deploy.ps1            # Production deployment script
└── staticwebapp.config.json  # Azure Static Web Apps config
```

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the production-readiness-analysis.md file
3. Check Azure Static Web Apps documentation
4. Check FastAPI and React documentation
