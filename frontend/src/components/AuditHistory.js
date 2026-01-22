import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './AuditHistory.module.css';

const AuditHistory = ({ apiUrl }) => {
    const [audits, setAudits] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await axios.get(`${apiUrl}/history/`);
                setAudits(response.data);
            } catch (error) {
                console.error("Failed to fetch history:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchHistory();
    }, [apiUrl]);

    const getVerdictClass = (verdict) => {
        const v = verdict?.toLowerCase() || '';
        if (v.includes('hire')) return styles.green;
        if (v.includes('good dev')) return styles.yellow;
        return styles.red;
    };

    if (loading) return <div className={styles.loading}>LOADING ARCHIVES...</div>;

    return (
        <div className={styles.historyContainer}>
            <h2 className={styles.historyHeader}>PREVIOUS OPERATIONS ({audits.length})</h2>

            {audits.map((audit) => (
                <div key={audit.id} className={styles.auditRow}>
                    <div className={styles.auditInfo}>
                        <a href={audit.repo_url} target="_blank" rel="noopener noreferrer" className={styles.repoUrl}>
                            {audit.repo_url.replace('https://github.com/', '')}
                        </a>
                        <span className={styles.date}>{new Date(audit.created_at).toLocaleDateString()}</span>
                    </div>

                    <div className={`${styles.verdictBadge} ${getVerdictClass(audit.verdict)}`}>
                        {audit.verdict}
                    </div>
                </div>
            ))}

            {audits.length === 0 && (
                <div className={styles.loading}>No audits found. GET TO WORK.</div>
            )}
        </div>
    );
};

export default AuditHistory;
