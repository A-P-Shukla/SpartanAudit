import React, { useState, useEffect } from 'react';
import './App.css';
import styles from './App.module.css';
import GenerateQuiz from './components/GenerateQuiz';
import PastQuizzes from './components/PastQuizzes';

const API_URL = 'https://intelliquiz-api.onrender.com';

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [historyKey, setHistoryKey] = useState(1);

  // --- TITLE BLOCK ---
  useEffect(() => {
    if (activeTab === 'generate') {
      document.title = 'IntelliQuiz - Create New Quiz';
    } else {
      document.title = 'IntelliQuiz - Quiz History';
    }
  }, [activeTab]); // The effect re-runs whenever 'activeTab' changes
  // --- END OF BLOCK ---


  return (
    <div className={styles.appWrapper}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <img 
              src="/logo.png" 
              alt="IntelliQuiz Logo" 
              className={styles.logo} 
            />
            <h1 className={styles.appName}>IntelliQuiz</h1>
        </div>
      </header>
      
      <main className={styles.mainContent}>
        <div className={styles.tabContainer}>
          <button 
            className={`${styles.tab} ${activeTab === 'generate' ? styles.active : ''}`} 
            onClick={() => setActiveTab('generate')}>
            Create New Quiz
          </button>
          <button 
            className={`${styles.tab} ${activeTab === 'history' ? styles.active : ''}`} 
            onClick={() => setActiveTab('history')}>
            Quiz History
          </button>
        </div>

        <div className={styles.contentArea}>
          {activeTab === 'generate' ? (
            <GenerateQuiz 
                apiUrl={API_URL} 
                onQuizGenerated={() => setHistoryKey(prevKey => prevKey + 1)} 
            />
          ) : (
            <PastQuizzes key={historyKey} apiUrl={API_URL} />
          )}
        </div>
      </main>

      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <div className={styles.footerText}>
            <span>&copy; {new Date().getFullYear()} IntelliQuiz</span>
            <span>|</span>
            <span>Created by Akhand Pratap Shukla</span>
          </div>

          <div className={styles.socialLinks}>
            {/* PERSONAL WEBSITE LINK */}
            <a href="https://akhandshukla.vercel.app/" target="_blank" rel="noopener noreferrer" title="Personal Website">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="2" y1="12" x2="22" y2="12"></line>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
              </svg>
            </a>
            
            {/* LINKEDIN LINK */}
            <a href="https://www.linkedin.com/in/akhand-pratap-shukla" target="_blank" rel="noopener noreferrer" title="LinkedIn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                <rect x="2" y="9" width="4" height="12"></rect>
                <circle cx="4" cy="4" r="2"></circle>
              </svg>
            </a>
            
            {/* GITHUB LINK */}
            <a href="https://github.com/A-P-Shukla" target="_blank" rel="noopener noreferrer" title="GitHub">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
              </svg>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;