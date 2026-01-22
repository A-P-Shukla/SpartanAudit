import React, { useState, useRef } from 'react';
import axios from 'axios';
import styles from './GenerateQuiz.module.css';
import QuizDisplay from './QuizDisplay';

const GenerateQuiz = ({ apiUrl, onQuizGenerated }) => {
    const [url, setUrl] = useState('');
    
    // --- KEY CHANGE 1: A more descriptive loading state ---
    // It can be 'idle', 'warming', or 'generating'.
    const [loadingState, setLoadingState] = useState('idle');
    
    const [error, setError] = useState('');
    const [titlePreview, setTitlePreview] = useState('');
    const [generatedQuiz, setGeneratedQuiz] = useState(null);
    
    // This ref will track if a request has been made in this session.
    const hasMadeRequest = useRef(false);

    const handleUrlChange = (e) => {
        const newUrl = e.target.value;
        setUrl(newUrl);
        setError('');
        setGeneratedQuiz(null);
        
        if (newUrl && newUrl.includes('wikipedia.org/wiki/')) {
            axios.get(`${apiUrl}/validate-url/?url=${encodeURIComponent(newUrl)}`)
                .then(res => setTitlePreview(res.data.title))
                .catch(() => setTitlePreview(''));
        } else {
            setError('Please enter a valid Wikipedia URL to begin.');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!url) {
            setError('Please enter a valid Wikipedia URL to begin.');
            return;
        }

        // --- KEY CHANGE 2: Differentiate loading type ---
        if (!hasMadeRequest.current) {
            setLoadingState('warming');
        } else {
            setLoadingState('generating');
        }
        
        setError('');
        setGeneratedQuiz(null);

        try {
            const response = await axios.post(`${apiUrl}/generate-quiz/`, { url });
            setGeneratedQuiz(response.data);
            onQuizGenerated();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate quiz. Please check the URL and try again.');
        } finally {
            setLoadingState('idle'); // Set loading to false regardless of outcome
            hasMadeRequest.current = true; // Mark that we've made our first request
        }
    };

    const isCurrentlyLoading = loadingState === 'warming' || loadingState === 'generating';

    return (
        // The container is now relative for positioning the overlay
        <div className={styles.container}>

            {/* --- KEY CHANGE 3: The Loading Overlay --- */}
            {isCurrentlyLoading && (
                <div className={styles.loadingOverlay}>
                    <div className="spinner"></div>
                    {loadingState === 'warming' ? (
                        <>
                            <h2>Waking Up The Server...</h2>
                            <p>This is a free service, so the server spins down when inactive.</p>
                            <p>The first request can take up to 50 seconds. Please wait!</p>
                        </>
                    ) : (
                        <h2>Generating Your Quiz...</h2>
                    )}
                </div>
            )}
            
            <div className={styles.hero}>
                <h1>Create a Quiz Instantly</h1>
                <p>Turn any Wikipedia article into a multiple-choice quiz. Just paste the URL below to get started.</p>
            </div>
            
            <form onSubmit={handleSubmit} className={styles.form}>
                <div className={styles.inputGroup}>
                    <input
                        type="url"
                        value={url}
                        onChange={handleUrlChange}
                        className={styles.urlInput}
                        placeholder="Paste a Wikipedia article link here..."
                        disabled={isCurrentlyLoading}
                    />
                     {titlePreview && !isCurrentlyLoading && <span className={styles.preview}>✓ {titlePreview}</span>}
                </div>
                <button type="submit" className={styles.submitButton} disabled={isCurrentlyLoading}>
                    {isCurrentlyLoading ? 'Please Wait...' : 'Create Quiz'}
                </button>
            </form>
            
            {error && <p className={styles.error}>{error}</p>}

            {generatedQuiz && (
                <div className={styles.results}>
                    <h2 className={styles.resultsTitle}>Quiz Ready!</h2>
                    <QuizDisplay quizData={generatedQuiz} startInQuizMode={true} />
                </div>
            )}
        </div>
    );
};

export default GenerateQuiz;