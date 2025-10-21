import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import { getCurrentUser } from './utils/auth';
import styles from './App.module.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUser = async () => {
    try {
      console.log('Fetching user...');
      const userData = await getCurrentUser();
      console.log('User data:', userData);
      setUser(userData);
    } catch (error) {
      console.error('Error fetching user:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
    
    // Listen for storage changes (when user logs in/out)
    const handleStorageChange = () => {
      console.log('Storage changed, refetching user...');
      fetchUser();
    };

    // Listen for focus events (when user returns to tab after login)
    const handleFocus = () => {
      console.log('Window focused, refetching user...');
      fetchUser();
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('focus', handleFocus);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('focus', handleFocus);
    };
  }, []);

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading...</div>
      </div>
    );
  }

  console.log('Rendering app, user:', user);

  return (
    <div className={styles.container}>
      {user ? <Dashboard user={user} /> : <Login user={user} />}
    </div>
  );
}

export default App;
