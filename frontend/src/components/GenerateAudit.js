import React, { useState } from 'react';
import axios from 'axios';
import styles from './GenerateAudit.module.css';

const GenerateAudit = ({ apiUrl, onAuditComplete }) => {
    const [repoUrl, setRepoUrl] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [forceReaudit, setForceReaudit] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await axios.post(`${apiUrl}/audit/`, {
                repo_url: repoUrl,
                job_description: jobDescription || null,
                force_reaudit: forceReaudit
            });
            onAuditComplete(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate audit. Ensure the repo is public.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.hero}>
                <h2 className={styles.title}>Relevancy & Quality Screener</h2>
                <p className={styles.subtitle}>Enter a GitHub URL. Get a brutal, AI-powered engineering audit in seconds.</p>
            </div>

            <form onSubmit={handleSubmit} className={styles.form}>
                <div className={styles.inputGroup}>
                    <label>Repository URL <span className={styles.required}>*</span></label>
                    <input
                        type="url"
                        placeholder="https://github.com/username/project"
                        value={repoUrl}
                        onChange={(e) => setRepoUrl(e.target.value)}
                        required
                        className={styles.input}
                    />
                </div>

                <div className={styles.inputGroup}>
                    <label>Job Description (Optional)</label>
                    <textarea
                        placeholder="Paste the JD here to check for relevancy match..."
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        className={styles.textarea}
                        rows={4}
                    />
                </div>

                <div className={styles.checkboxGroup}>
                    <label>
                        <input
                            type="checkbox"
                            checked={forceReaudit}
                            onChange={(e) => setForceReaudit(e.target.checked)}
                        />
                        Force Re-audit (bypass cache)
                    </label>
                </div>

                {error && <div className={styles.error}>{error}</div>}

                <button type="submit" className={styles.submitButton} disabled={loading}>
                    {loading ? 'RUNNING AUDIT...' : 'AUDIT THIS REPO'}
                </button>
            </form>
        </div>
    );
};

export default GenerateAudit;
