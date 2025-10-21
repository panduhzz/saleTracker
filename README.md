# Sale Tracker

A modern sales tracking web application built with React and deployed on Azure Static Web Apps, featuring GitHub authentication and a comprehensive dashboard for managing sales data.

## 🚀 Features

- **GitHub Authentication**: Secure login using Azure Static Web Apps built-in authentication
- **Modern Dashboard**: Beautiful, responsive dashboard with sales statistics and recent transactions
- **Real-time Data**: Track sales across multiple platforms (StockX, GOAT, eBay, manual entries)
- **Responsive Design**: Mobile-first design with glassmorphism UI elements
- **Azure Integration**: Fully deployed on Azure Static Web Apps with automatic CI/CD

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 with functional components and hooks
- **Styling**: CSS Modules for scoped styling
- **Authentication**: Azure Static Web Apps built-in GitHub OAuth
- **Deployment**: Azure Static Web Apps (Preview environment)

### Backend
- **Framework**: FastAPI with async/await support
- **Database**: Azure Cosmos DB with SQL API
- **Authentication**: Azure Static Web Apps built-in authentication
- **Containerization**: Docker with multi-stage builds
- **Package Management**: uv for fast Python package management

### Project Structure
```
saleTracker/
├── src/                     # React frontend
│   ├── components/
│   │   ├── Login.js              # Authentication component
│   │   ├── Login.module.css      # Login styling
│   │   ├── Dashboard.js          # Main dashboard component
│   │   └── Dashboard.module.css  # Dashboard styling
│   ├── utils/
│   │   └── auth.js              # Authentication utilities
│   ├── App.js                   # Main application component
│   ├── App.module.css          # App-level styling
│   ├── index.js                # React entry point
│   └── index.html              # HTML template
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/             # API endpoints
│   │   │   ├── sales.py     # Sales CRUD endpoints
│   │   │   └── dashboard.py # Dashboard analytics endpoints
│   │   ├── models/          # Pydantic models
│   │   │   └── sales.py     # Data validation models
│   │   ├── services/        # Business logic
│   │   │   └── cosmos_service.py # Cosmos DB operations
│   │   ├── auth/            # Authentication
│   │   │   └── swa_auth.py  # SWA authentication utilities
│   │   └── main.py          # FastAPI application
│   ├── tests/               # Unit and integration tests
│   ├── Dockerfile           # Multi-stage Docker build
│   ├── pyproject.toml       # Python project configuration
│   ├── test_cosmos.py       # Cosmos DB connection test
│   └── .env                 # Environment variables
├── public/                  # Static assets
├── build/                   # React build output
└── Configuration files
```

## 🛠️ Technologies Used

### Frontend
- **React 18** - Modern React with hooks
- **CSS Modules** - Scoped CSS styling
- **Azure Static Web Apps** - Hosting and authentication
- **GitHub OAuth** - Authentication provider
- **SWA CLI** - Local development and deployment

### Backend
- **FastAPI** - Modern Python web framework
- **Azure Cosmos DB** - NoSQL database for data storage
- **Pydantic** - Data validation and settings management
- **uv** - Fast Python package manager
- **Docker** - Containerization for deployment
- **Azure Identity** - Managed identity for secure authentication

## 📊 Dashboard Features

### Statistics Cards
- **Total Sales**: Track overall revenue
- **Items Sold**: Count of total transactions
- **Monthly Performance**: Current month sales
- **Average Price**: Mean transaction value

### Recent Sales Table
- **Product Details**: Item names and descriptions
- **Transaction Amounts**: Sale prices and values
- **Platform Tracking**: StockX, GOAT, eBay, manual entries
- **Date Tracking**: Transaction timestamps

### User Interface
- **Glassmorphism Design**: Modern UI with backdrop blur effects
- **Responsive Layout**: Mobile-first responsive design
- **Interactive Elements**: Hover effects and smooth transitions
- **Professional Styling**: Clean, modern aesthetic

## 🔐 Authentication

### Azure Static Web Apps Integration
- **Built-in Authentication**: No custom OAuth implementation needed
- **GitHub Provider**: Secure login with GitHub accounts
- **Automatic Session Management**: Handled by Azure SWA
- **Protected Routes**: Dashboard only accessible to authenticated users

### Authentication Flow
1. User clicks "Sign in with GitHub"
2. Redirected to GitHub OAuth (in production) or SWA emulator (in development)
3. User authenticates with GitHub credentials
4. Redirected back to application with authentication token
5. Dashboard displays with user-specific data

## 🚀 Deployment

### Azure Static Web Apps
- **Preview Environment**: Successfully deployed using `swa deploy`
- **Automatic CI/CD**: GitHub integration for continuous deployment
- **Global CDN**: Fast content delivery worldwide
- **SSL/TLS**: Automatic HTTPS encryption

### Local Development
- **SWA CLI**: Local development with authentication emulation
- **Hot Reload**: Real-time development updates
- **Authentication Testing**: Local emulator for testing auth flows

## 🛠️ Development Setup

### Prerequisites
- Node.js 16+ and npm
- Python 3.11+
- Azure CLI
- Azure Static Web Apps CLI (`npm install -g @azure/static-web-apps-cli`)
- Azure Cosmos DB account

### Frontend Development
```bash
# Install dependencies
npm install

# Start local development server
swa start

# Access application
# Frontend: http://localhost:4280
# API: http://localhost:7071
```

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Install uv package manager
pip install uv

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your Cosmos DB connection string

# Test Cosmos DB connection
python test_cosmos.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000

# Access API documentation
# http://localhost:8000/docs
```

### Full Stack Development
```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
swa start
```

### Deployment Commands
```bash
# Deploy frontend to Azure
swa deploy

# Deploy with specific configuration
swa deploy --env production
```

## 🔧 Backend API

### API Endpoints

#### Sales Management
- `GET /api/sales` - List all sales for authenticated user
- `POST /api/sales` - Create new sale
- `GET /api/sales/{id}` - Get specific sale
- `PUT /api/sales/{id}` - Update sale
- `DELETE /api/sales/{id}` - Delete sale

#### Dashboard Analytics
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent` - Get recent sales
- `GET /api/dashboard` - Get complete dashboard data

#### System
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/user` - Current user info

### Database Schema

#### Sales Collection
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

#### Partition Key
- **Partition Key**: `userId` for data isolation
- **Indexing**: Automatic indexing enabled
- **Query Performance**: Optimized for user-scoped queries

### Testing Backend

#### Test Cosmos DB Connection
```bash
cd backend
python test_cosmos.py
```

#### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# API documentation
# Visit: http://localhost:8000/docs
```

#### Environment Variables
```env
# Local development
COSMOSDB_CONNECTION_STRING=AccountEndpoint=https://your-cosmosdb-account.documents.azure.com:443/;AccountKey=your-primary-key;
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 📁 Configuration Files

### Frontend Configuration

#### `staticwebapp.config.json`
- **Routes**: SPA routing configuration
- **Authentication**: GitHub OAuth provider setup
- **Navigation**: Fallback routing for React Router

#### `swa-cli.config.json`
- **Build Configuration**: React build settings
- **Development Server**: Local development setup
- **Deployment Settings**: Azure deployment configuration

#### `package.json`
- **Dependencies**: React, ReactDOM, react-scripts
- **Scripts**: Build, start, test, and deployment commands
- **Browserslist**: Browser compatibility configuration

### Backend Configuration

#### `pyproject.toml`
- **Dependencies**: FastAPI, Azure Cosmos DB, Pydantic
- **Build System**: Hatchling for package building
- **Development Tools**: pytest, black, isort, flake8

#### `Dockerfile`
- **Multi-stage Build**: Optimized for production
- **Security**: Non-root user execution
- **Health Checks**: Built-in health monitoring

## 🎨 UI/UX Features

### Design System
- **Color Palette**: Professional blue-purple gradient theme
- **Typography**: System font stack for optimal performance
- **Spacing**: Consistent padding and margins
- **Shadows**: Subtle depth with box-shadow effects

### Responsive Design
- **Mobile First**: Optimized for mobile devices
- **Breakpoints**: Tablet and desktop responsive layouts
- **Grid System**: CSS Grid for flexible layouts
- **Touch Friendly**: Appropriate button sizes for touch interfaces

### Interactive Elements
- **Hover Effects**: Smooth transitions on interactive elements
- **Loading States**: User feedback during authentication
- **Error Handling**: Graceful error states and fallbacks

## 🔧 Development Features

### Authentication Testing
- **SWA Emulator**: Local authentication simulation
- **Test Login**: Development testing button
- **Console Logging**: Detailed authentication debugging
- **Storage Management**: LocalStorage for test user data

### Code Organization
- **Component Structure**: Modular React components
- **CSS Modules**: Scoped styling to prevent conflicts
- **Utility Functions**: Reusable authentication helpers
- **Error Boundaries**: Graceful error handling

## 📈 Future Enhancements

### Planned Features
- **Frontend-Backend Integration**: Connect React frontend to FastAPI backend
- **Real-time Data**: Replace dummy data with live API calls
- **Advanced Analytics**: Charts and graphs for sales insights
- **Export Functionality**: CSV/PDF export of sales data
- **Multi-user Support**: Team collaboration features
- **Mobile App**: React Native mobile application

### Technical Improvements
- **State Management**: Redux or Zustand for complex state
- **Testing**: Jest and React Testing Library for frontend, pytest for backend
- **Performance**: Code splitting and lazy loading
- **Accessibility**: WCAG compliance improvements
- **Monitoring**: Application insights and logging
- **CI/CD**: Automated testing and deployment pipelines

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Connecting Frontend and Backend

### Local Development Setup

1. **Start the Backend API**:
   ```bash
   cd backend
   # Copy environment template
   cp env.template .env
   # Edit .env with your Cosmos DB connection string
   # Install dependencies and run
   uv sync
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start the Frontend**:
   ```bash
   # Install dependencies
   npm install
   # Create environment file
   echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
   # Start development server
   npm start
   ```

3. **Test the Connection**:
   - Frontend will be available at `http://localhost:3000`
   - Backend API will be available at `http://localhost:8000`
   - The frontend will automatically proxy API calls to the backend

### Environment Variables

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

#### Backend (.env)
```env
COSMOSDB_CONNECTION_STRING=your-cosmosdb-connection-string
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

### Production Deployment

1. **Deploy Backend to Azure Container Apps**:
   - Build and push Docker image to Azure Container Registry
   - Deploy container app with managed identity
   - Configure Cosmos DB connection

2. **Deploy Frontend to Azure Static Web Apps**:
   - Update `staticwebapp.config.json` with backend URL
   - Set environment variables in SWA settings
   - Deploy using GitHub Actions or Azure CLI

3. **Update Configuration**:
   - Update `REACT_APP_API_URL` in production environment
   - Update `staticwebapp.config.json` with actual backend URL
   - Configure authentication providers

### Troubleshooting

#### Common Issues:

1. **CORS Errors**: Ensure backend CORS is configured for your frontend domain
2. **Authentication Issues**: Check that SWA authentication headers are properly forwarded
3. **API Connection**: Verify environment variables are set correctly
4. **Database Connection**: Ensure Cosmos DB connection string is valid

#### Debug Steps:

1. Check browser network tab for API call failures
2. Verify backend logs for authentication issues
3. Test API endpoints directly using tools like Postman
4. Check Azure Static Web Apps logs for deployment issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the Azure Static Web Apps documentation
- Review the React documentation for component development

---

**Built with ❤️ using React, FastAPI, Azure Static Web Apps, Azure Cosmos DB, and modern web technologies.**