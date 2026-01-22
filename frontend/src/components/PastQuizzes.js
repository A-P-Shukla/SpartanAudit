import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './PastQuizzes.module.css';
import QuizDisplay from './QuizDisplay';

const PastQuizzes = ({ apiUrl }) => {
    // --- Initial state is a SAFE empty array, not null ---
    const [quizzes, setQuizzes] = useState([]);
    const [selectedQuiz, setSelectedQuiz] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        setIsLoading(true);
        setError('');
        axios.get(`${apiUrl}/quizzes/`)
            .then(res => {
                // The backend already sends the most recent first, but we can re-sort just in case
                setQuizzes(res.data.sort((a, b) => b.id - a.id));
            })
            .catch(err => {
                setError('Failed to load quiz history. Please try again later.');
                console.error("Error fetching quizzes:", err);
            })
            .finally(() => {
                setIsLoading(false);
            });
    }, [apiUrl]); // This useEffect runs when the component is mounted

    // --- Render the loading state FIRST ---
    if (isLoading) {
        return (
            <div className={styles.centered}>
                <div className="spinner"></div>
                <p>Loading Quiz History...</p>
            </div>
        );
    }
    
    if (error) {
        return <div className={styles.centered}><p className={styles.error}>{error}</p></div>;
    }

    if (quizzes.length === 0) {
        return (
            <div className={styles.centered}>
                <p className={styles.noQuizzes}>
                    No quizzes generated yet.
                </p>
                <p>Go to the "Create New Quiz" tab to get started!</p>
            </div>
        );
    }

    return (
        <div className={styles.container}>
             <h2 className={styles.title}>Quiz History</h2>
            <table className={styles.quizTable}>
                <thead>
                    <tr>
                        <th>Article Title</th>
                        <th>URL</th>
                        <th style={{ textAlign: 'center' }}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {quizzes.map(quiz => (
                        <tr key={quiz.id}>
                            <td>{quiz.title}</td>
                            <td><a href={quiz.url} target="_blank" rel="noopener noreferrer">{quiz.url}</a></td>
                            <td style={{ textAlign: 'center' }}>
                                <button className={styles.detailsButton} onClick={() => setSelectedQuiz(quiz)}>
                                    View Details
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {selectedQuiz && (
                <div className={styles.modalBackdrop} onClick={() => setSelectedQuiz(null)}>
                    <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
                        <button className={styles.closeButton} onClick={() => setSelectedQuiz(null)}>&times;</button>
                        <QuizDisplay quizData={selectedQuiz} />
                    </div>
                </div>
            )}
        </div>
    );
};

export default PastQuizzes;