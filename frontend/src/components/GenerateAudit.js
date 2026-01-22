import React, { useState } from 'react';
import axios from 'axios';
import styles from './GenerateAudit.module.css';
import AuditReport from './AuditReport';

const GenerateAudit = ({ apiUrl, onAuditComplete }) => {
    const [repoUrl, setRepoUrl] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [auditResult, setAuditResult] = useState(null);

    const handleAudit = async () => {
        if (!repoUrl) {
            setError("Repo URL is mandatory. Spartans don't audit thin air.");
            return;
        }

        setLoading(true);
        setError(null);
        setAuditResult(null);

        try {
            const response = await axios.post(`${apiUrl}/audit/`, {
                repo_url: repoUrl,
                job_description: jobDescription || null
            });

            setAuditResult(response.data);
            if (onAuditComplete) onAuditComplete();

        } catch (err) {
            console.error("Audit failed:", err);
            setError(err.response?.data?.detail || "The Spartan Engine failed. Check your connection.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            {/* Input Section */}
            {!auditResult && (
                <div className={styles.inputCard}>
                    <h2 className={styles.title}>Initiate Reconnaissance</h2>

                    <div className={styles.formGroup}>
                        <label className={styles.label}>GITHUB REPOSITORY URL *</label>
                        <input
                            type="url"
                            className={styles.input}
                            placeholder="https://github.com/username/project"
                            value={repoUrl}
                            onChange={(e) => setRepoUrl(e.target.value)}
                            disabled={loading}
                        />
                    </div>

                    <div className={styles.formGroup}>
                        <label className={styles.label}>JOB DESCRIPTION (OPTIONAL)</label>
                        <textarea
                            className={styles.textarea}
                            placeholder="Paste the JD here to run the Relevancy Check..."
                            value={jobDescription}
                            onChange={(e) => setJobDescription(e.target.value)}
                            disabled={loading}
                        />
                    </div>

                    {error && <div className={styles.error}>⚠️ {error}</div>}

                    <button
                        className={styles.auditButton}
                        onClick={handleAudit}
                        disabled={loading}
                    >
                        {loading ? "INITIALIZING SCANNERS..." : "RUN SPARTAN AUDIT"}
                    </button>

                    {loading && (
                        <div className={styles.loadingContainer}>
                            <p>Fetching Repository...</p>
                            <p>Checking Docker Configs...</p>
                            <p>Consulting Cynical Staff Engineer...</p>
                        </div>
                    )}
                </div>
            )}

            {/* Results Section */}
            {auditResult && (
                <AuditReport
                    data={auditResult}
                    onReset={() => setAuditResult(null)}
                />
            )}
        </div>
    );
};

export default GenerateAudit;
