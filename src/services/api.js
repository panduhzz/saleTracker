/**
 * API service for communicating with the FastAPI backend
 */

// To this:
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api'  // Use SWA API routes in production
  : (process.env.REACT_APP_API_URL || '/api');  // Use environment variable in development
  
class ApiService {
  /**
   * Make a request to the API with proper error handling
   * @param {string} endpoint - API endpoint path
   * @param {Object} options - Fetch options
   * @returns {Promise<Object>} Parsed JSON response
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Get authentication headers for local development
    const authHeaders = this.getAuthHeaders();
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API request failed: ${response.status} ${response.statusText} - ${errorText}`);
      }
      
      // Handle empty responses (like DELETE)
      if (response.status === 204) {
        return null;
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  /**
   * Get authentication headers for API requests
   * @returns {Object} Headers object with authentication
   */
  getAuthHeaders() {
    // Check for test user in localStorage (local development)
    const testUser = localStorage.getItem('swa-test-user');
    if (testUser) {
      try {
        const user = JSON.parse(testUser);
        // Create a mock client principal header for local development
        const clientPrincipal = {
          userId: user.userId,
          userDetails: user.userDetails,
          identityProvider: user.provider,
          claims: user.claims || []
        };
        
        // Base64 encode the client principal (like SWA does)
        const encodedPrincipal = btoa(JSON.stringify(clientPrincipal));
        return {
          'x-ms-client-principal': encodedPrincipal
        };
      } catch (error) {
        console.error('Error parsing test user:', error);
        return {};
      }
    }
    
    // In production, SWA will provide these headers automatically
    return {};
  }

  // Dashboard endpoints
  /**
   * Get dashboard statistics
   * @returns {Promise<Object>} Dashboard stats
   */
  async getDashboardStats() {
    return this.request('/dashboard/stats');
  }

  /**
   * Get recent sales
   * @param {number} limit - Maximum number of recent sales to return
   * @returns {Promise<Array>} Recent sales array
   */
  async getRecentSales(limit = 5) {
    return this.request(`/dashboard/recent?limit=${limit}`);
  }

  /**
   * Get complete dashboard data (stats + recent sales)
   * @returns {Promise<Object>} Combined dashboard data
   */
  async getDashboardData() {
    return this.request('/dashboard');
  }

  // Sales CRUD endpoints
  /**
   * Get all sales for the authenticated user
   * @returns {Promise<Array>} Sales array
   */
  async getSales() {
    return this.request('/sales');
  }

  /**
   * Create a new sale
   * @param {Object} saleData - Sale data to create
   * @returns {Promise<Object>} Created sale
   */
  async createSale(saleData) {
    return this.request('/sales', {
      method: 'POST',
      body: JSON.stringify(saleData),
    });
  }

  /**
   * Get a specific sale by ID
   * @param {string} saleId - Sale ID
   * @returns {Promise<Object>} Sale data
   */
  async getSale(saleId) {
    return this.request(`/sales/${saleId}`);
  }

  /**
   * Update an existing sale
   * @param {string} saleId - Sale ID
   * @param {Object} updateData - Update data
   * @returns {Promise<Object>} Updated sale
   */
  async updateSale(saleId, updateData) {
    return this.request(`/sales/${saleId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  /**
   * Delete a sale
   * @param {string} saleId - Sale ID
   * @returns {Promise<null>} No return value
   */
  async deleteSale(saleId) {
    return this.request(`/sales/${saleId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Get current user information
   * @returns {Promise<Object>} User data
   */
  async getCurrentUser() {
    return this.request('/user');
  }
}

export default new ApiService();
