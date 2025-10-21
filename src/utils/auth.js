/**
 * Auth utility functions for Azure Static Web Apps
 */

/**
 * Fetch current user information from Azure SWA auth endpoint
 * @returns {Promise<Object|null>} User object or null if not authenticated
 */
export const getCurrentUser = async () => {
  try {
    // Check for test user in localStorage first (for development)
    const testUser = localStorage.getItem('swa-test-user');
    if (testUser) {
      console.log('Using test user from localStorage:', JSON.parse(testUser));
      return JSON.parse(testUser);
    }

    const response = await fetch('/.auth/me');
    
    if (!response.ok) {
      return null;
    }
    
    const userData = await response.json();
    console.log('Raw user data from API:', userData);
    
    // Handle different response formats
    if (userData.clientPrincipal && userData.clientPrincipal !== null) {
      // SWA emulator format: { clientPrincipal: { ... } }
      return userData.clientPrincipal;
    } else if (Array.isArray(userData) && userData.length > 0) {
      // Production format: [ { ... } ]
      return userData[0];
    } else if (userData && typeof userData === 'object' && userData.userId) {
      // Direct user object
      return userData;
    }
    
    return null;
  } catch (error) {
    console.error('Error fetching user:', error);
    return null;
  }
};

/**
 * Get the login URL for GitHub authentication
 * @returns {string} GitHub login URL
 */
export const getGitHubLoginUrl = () => {
  return '/.auth/login/github';
};

/**
 * Get the logout URL
 * @returns {string} Logout URL
 */
export const getLogoutUrl = () => {
  return '/.auth/logout';
};
