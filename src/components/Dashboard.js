import React, { useState, useEffect } from 'react';
import styles from './Dashboard.module.css';
import apiService from '../services/api';

const Dashboard = ({ user }) => {
  const [stats, setStats] = useState(null);
  const [recentSales, setRecentSales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getDashboardData();
      setStats(data.stats);
      setRecentSales(data.recentSales);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.dashboard}>
        <div className={styles.loading}>Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.dashboard}>
        <div className={styles.error}>
          <h3>Error loading dashboard</h3>
          <p>{error}</p>
          <button onClick={fetchDashboardData} className={styles.retryButton}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.dashboard}>
      <header className={styles.header}>
        <h1 className={styles.title}>Sales Dashboard</h1>
        <div className={styles.userInfo}>
          <span className={styles.welcome}>Welcome back, {user.userDetails}!</span>
        </div>
      </header>

      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <h3 className={styles.statTitle}>Total Sales</h3>
          <p className={styles.statValue}>${stats?.totalSales?.toLocaleString() || '0'}</p>
        </div>
        <div className={styles.statCard}>
          <h3 className={styles.statTitle}>Items Sold</h3>
          <p className={styles.statValue}>{stats?.totalItems || '0'}</p>
        </div>
        <div className={styles.statCard}>
          <h3 className={styles.statTitle}>This Month</h3>
          <p className={styles.statValue}>${stats?.thisMonth?.toLocaleString() || '0'}</p>
        </div>
        <div className={styles.statCard}>
          <h3 className={styles.statTitle}>Avg Price</h3>
          <p className={styles.statValue}>${stats?.avgPrice?.toFixed(2) || '0.00'}</p>
        </div>
      </div>

      <div className={styles.recentSales}>
        <h2 className={styles.sectionTitle}>Recent Sales</h2>
        {recentSales.length === 0 ? (
          <div className={styles.emptyState}>
            <p>No sales found. Start by adding your first sale!</p>
          </div>
        ) : (
          <div className={styles.salesTable}>
            <div className={styles.tableHeader}>
              <div className={styles.headerCell}>Product</div>
              <div className={styles.headerCell}>Amount</div>
              <div className={styles.headerCell}>Platform</div>
              <div className={styles.headerCell}>Date</div>
            </div>
            {recentSales.map(sale => (
              <div key={sale.id} className={styles.tableRow}>
                <div className={styles.cell}>{sale.productName}</div>
                <div className={styles.cell}>${sale.amount.toFixed(2)}</div>
                <div className={styles.cell}>
                  <span className={styles.platform}>{sale.platform}</span>
                </div>
                <div className={styles.cell}>{new Date(sale.saleDate).toLocaleDateString()}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className={styles.actions}>
        <button className={styles.primaryButton}>Add New Sale</button>
        <button className={styles.secondaryButton}>View All Sales</button>
        <a href="/.auth/logout" className={styles.logoutButton}>Logout</a>
      </div>
    </div>
  );
};

export default Dashboard;
