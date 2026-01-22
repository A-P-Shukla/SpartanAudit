import React from 'react';
import styles from './AuditReport.module.css';

const AuditReport = ({ data, onReset }) => {
    // Determine verdict color class
    const getVerdictClass = () => {
        const v = data.verdict?.toLowerCase() || '';
        if (v.includes('hire')) return styles.green;
        if (v.includes('good dev')) return styles.yellow;
        return styles.red;
    };

    return (
        <div className={styles.reportContainer}>
            {/* Verdict Banner */}
            <div className={`${styles.verdictBanner} ${getVerdictClass()}`}>
                {data.verdict}
            </div>

            {/* Score Grid */}
            <div className={styles.scoreGrid}>
                {/* Engineering Score */}
                <div className={styles.scoreCard}>
                    <span className={styles.scoreLabel}>Engineering Quality</span>
                    <span className={styles.scoreValue}>{data.engineering_score}/10</span>
                </div>

                {/* Match Score (Optional) */}
                {data.match_score !== null && (
                    <div className={styles.scoreCard}>
                        <span className={styles.scoreLabel}>Relevancy Match</span>
                        <span className={styles.scoreValue}>{data.match_score}%</span>
                    </div>
                )}
            </div>

            {/* Critique Section */}
            <div className={styles.critiqueCard}>
                <div className={styles.critiqueHeader}>
                    <span>Cynical Staff Engineer Says:</span>
                    <span>🛡️ AUDIT REPORT #{data.id}</span>
                </div>
                <p className={styles.critiqueText}>
                    "{data.critique}"
                </p>

                <div className={styles.techStack}>
                    {data.tech_stack && data.tech_stack.map((tech, i) => (
                        <span key={i} className={styles.techBadge}>{tech}</span>
                    ))}
                </div>
            </div>

            <button className={styles.resetButton} onClick={onReset}>
                Run Another Audit
            </button>
        </div>
    );
};

export default AuditReport;
