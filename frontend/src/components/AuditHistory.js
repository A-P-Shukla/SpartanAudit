import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './AuditHistory.module.css';

const AuditHistory = ({ apiUrl, onViewAudit }) => {
    const [audits, setAudits] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await axios.get(`${apiUrl}/history/`);
                setAudits(res.data);
            } catch (err) {
                console.error("Failed to fetch history", err);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, [apiUrl]);

    if (loading) return <div className={styles.loading}>Loading archives...</div>;

    return (
        <div className={styles.container}>
            <h2 className={styles.title}>Audit Archives</h2>
            {audits.length === 0 ? (
                <p className={styles.empty}>No audits recorded yet. Be the first to judge.</p>
            ) : (
                <div className={styles.grid}>
                    {audits.map(audit => (
                        <div key={audit.id} className={styles.card} onClick={() => onViewAudit(audit)}>
                            <div className={styles.cardHeader}>
                                <span className={styles.repoUrl}>{audit.repo_url.replace('https://github.com/', '')}</span>
                                <span className={`${styles.badge} ${audit.verdict.includes('HIRE') ? styles.green : styles.red}`}>
                                    {audit.engineering_score}/10
                                </span>
                            </div>
                            <p className={styles.verdictPreview}>{audit.verdict}</p>
                            <span className={styles.date}>{new Date(audit.created_at).toLocaleDateString()}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default AuditHistory;
