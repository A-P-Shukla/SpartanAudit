import React from 'react';
import styles from './AuditReport.module.css';

const AuditReport = ({ data, onBack }) => {
    const getVerdictColor = (verdict) => {
        if (verdict.includes('HIRE')) return styles.verdictGreen;
        if (verdict.includes('WRONG FIT')) return styles.verdictYellow;
        return styles.verdictRed;
    };

    return (
        <div className={styles.container}>
            <button onClick={onBack} className={styles.backButton}>&larr; Back to Dashboard</button>

            <div className={styles.header}>
                <h2 className={styles.repoTitle}>
                    <a href={data.repo_url} target="_blank" rel="noopener noreferrer">{data.repo_url}</a>
                </h2>
                <span className={styles.date}>{new Date(data.created_at).toLocaleDateString()}</span>
            </div>

            <div className={`${styles.verdictBanner} ${getVerdictColor(data.verdict)}`}>
                <h1 className={styles.verdictText}>{data.verdict}</h1>
            </div>

            <div className={styles.statsGrid}>
                <div className={styles.statCard}>
                    <span className={styles.statLabel}>Engineering Score</span>
                    <span className={styles.statValue}>{data.engineering_score}/10</span>
                </div>
                {data.match_score !== null && (
                    <div className={styles.statCard}>
                        <span className={styles.statLabel}>Relevancy Match</span>
                        <span className={styles.statValue}>{data.match_score}%</span>
                    </div>
                )}
            </div>

            <div className={styles.section}>
                <h3>The Critique</h3>
                <p className={styles.critiqueText}>{data.critique}</p>
            </div>

            <div className={styles.section}>
                <h3>Reconnaissance Data</h3>
                <div className={styles.reconGrid}>
                    <div className={styles.reconItem}>
                        <strong>Tech Stack:</strong>
                        <div className={styles.tags}>
                            {data.tech_stack.map(tech => <span key={tech} className={styles.tag}>{tech}</span>)}
                        </div>
                    </div>
                    <div className={styles.reconItem}>
                        <strong>Proof of Engineering:</strong>
                        <div className={styles.tags}>
                            {data.found_files.map(file => <span key={file} className={styles.fileTag}>{file}</span>)}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AuditReport;
