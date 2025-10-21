import React from 'react';
import { getGitHubLoginUrl, getLogoutUrl } from '../utils/auth';
import styles from './Login.module.css';

const Login = ({ user, onLogout }) => {
  const handleRefresh = () => {
    window.location.reload();
  };

  const handleTestLogin = () => {
    // For testing: simulate a logged-in user
    const testUser = {
      userId: 'test-user-123',
      userDetails: 'Test User',
      provider: 'github',
      claims: [
        { typ: 'name', val: 'Test User' },
        { typ: 'email', val: 'test@example.com' }
      ]
    };
    
    // Store in localStorage to simulate authentication
    localStorage.setItem('swa-test-user', JSON.stringify(testUser));
    window.location.reload();
  };

  if (user) {
    return (
      <div className={styles.userInfo}>
        <h2 className={styles.welcome}>Welcome, {user.userDetails || user.claims?.find(c => c.typ === 'name')?.val || 'User'}!</h2>
        <div className={styles.userDetails}>
          <p><strong>Provider:</strong> {user.provider}</p>
          <p><strong>User ID:</strong> {user.userId}</p>
        </div>
        <a 
          href={getLogoutUrl()} 
          className={styles.logoutButton}
        >
          Logout
        </a>
      </div>
    );
  }

  return (
    <div className={styles.loginContainer}>
      <h1 className={styles.title}>Sale Tracker</h1>
      <p className={styles.subtitle}>Please sign in to continue</p>
      <a 
        href={getGitHubLoginUrl()} 
        className={styles.loginButton}
      >
        Sign in with GitHub
      </a>
      <button 
        onClick={handleRefresh}
        className={styles.refreshButton}
      >
        Refresh Page
      </button>
      <button 
        onClick={handleTestLogin}
        className={styles.testButton}
      >
        Test Login (Simulate)
      </button>
    </div>
  );
};

export default Login;
