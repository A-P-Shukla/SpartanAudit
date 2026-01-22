import React, { useState, useEffect } from 'react';
import styles from './App.module.css';
import GenerateAudit from './components/GenerateAudit';
import AuditHistory from './components/AuditHistory';
import AuditReport from './components/AuditReport';

const API_URL = 'http://localhost:8000'; // Hardcoded for local dev

function App() {
  const [activeTab, setActiveTab] = useState('new');
  const [historyKey, setHistoryKey] = useState(1);
  const [currentAudit, setCurrentAudit] = useState(null);

  // --- TITLE BLOCK ---
  useEffect(() => {
    document.title = activeTab === 'new' ? 'SpartanAudit - New Audit' : 'SpartanAudit - History';
  }, [activeTab]);

  const handleAuditComplete = (auditData) => {
    setCurrentAudit(auditData);
    setHistoryKey(prev => prev + 1); // Refresh history
  };

  const handleStartNew = () => {
    setCurrentAudit(null);
    setActiveTab('new');
  };

  return (
    <div className={styles.appWrapper}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logoGroup} onClick={handleStartNew}>
            <span className={styles.logoIcon}>⚔️</span>
            <h1 className={styles.appName}>SpartanAudit</h1>
          </div>
          <nav className={styles.nav}>
            <button
              className={`${styles.navButton} ${activeTab === 'new' ? styles.active : ''}`}
              onClick={handleStartNew}
            >
              New Audit
            </button>
            <button
              className={`${styles.navButton} ${activeTab === 'history' ? styles.active : ''}`}
              onClick={() => { setActiveTab('history'); setCurrentAudit(null); }}
            >
              History
            </button>
          </nav>
        </div>
      </header>

      <main className={styles.mainContent}>
        {activeTab === 'new' && !currentAudit && (
          <GenerateAudit apiUrl={API_URL} onAuditComplete={handleAuditComplete} />
        )}

        {currentAudit && (
          <AuditReport data={currentAudit} onBack={handleStartNew} />
        )}

        {activeTab === 'history' && !currentAudit && (
          <AuditHistory key={historyKey} apiUrl={API_URL} onViewAudit={setCurrentAudit} />
        )}
      </main>

      <footer className={styles.footer}>
        <p>&copy; {new Date().getFullYear()} SpartanAudit. Built for the bold.</p>
      </footer>
    </div>
  );
}

export default App;