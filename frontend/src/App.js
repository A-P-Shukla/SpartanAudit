import React, { useState, useEffect } from 'react';
import styles from './App.module.css';
import GenerateAudit from './components/GenerateAudit';
import AuditHistory from './components/AuditHistory'; // We'll rename PastQuizzes later

const API_URL = 'http://127.0.0.1:8000'; // Development URL

function App() {
  const [activeTab, setActiveTab] = useState('audit');
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    document.title = activeTab === 'audit' 
      ? 'SpartanAudit - Code Quality Screener' 
      : 'SpartanAudit - Audit History';
  }, [activeTab]);

  return (
    <div className={styles.appWrapper}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logoIcon}>🛡️</div>
          <h1 className={styles.appName}>SpartanAudit</h1>
          <span className={styles.tagline}>// Code Quality & Relevancy Screener</span>
        </div>
      </header>
      
      <main className={styles.mainContent}>
        <nav className={styles.tabContainer}>
          <button 
            className={`${styles.tab} ${activeTab === 'audit' ? styles.active : ''}`} 
            onClick={() => setActiveTab('audit')}>
            Run Audit
          </button>
          <button 
            className={`${styles.tab} ${activeTab === 'history' ? styles.active : ''}`} 
            onClick={() => setActiveTab('history')}>
            History
          </button>
        </nav>

        <div className={styles.contentArea}>
          {activeTab === 'audit' ? (
            <GenerateAudit 
                apiUrl={API_URL} 
                onAuditComplete={() => setRefreshKey(k => k + 1)}
            />
          ) : (
             <AuditHistory key={refreshKey} apiUrl={API_URL} />
          )}
        </div>
      </main>

      <footer className={styles.footer}>
        <div className={styles.footerContent}>
            <span>&copy; {new Date().getFullYear()} TechKareer SpartanAudit</span>
            <span>Built for the Bold.</span>
        </div>
      </footer>
    </div>
  );
}

export default App;