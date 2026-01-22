import React, { useState } from 'react';
import styles from './QuizDisplay.module.css';

// SVG Icons for visual feedback
const CheckIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
    </svg>
);

const CrossIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" />
    </svg>
);

const QuizDisplay = ({ quizData, startInQuizMode = false }) => {
    const [takeQuizMode, setTakeQuizMode] = useState(startInQuizMode);
    const [userAnswers, setUserAnswers] = useState({});
    const [submitted, setSubmitted] = useState(false);

    const handleAnswerChange = (questionIndex, answer) => {
        setUserAnswers({
            ...userAnswers,
            [questionIndex]: answer,
        });
    };

    const handleSubmit = () => {
        if (Object.keys(userAnswers).length < quizData.quiz_data.length) {
            alert('Please answer all questions before submitting.');
            return;
        }
        setSubmitted(true);
    };
    
    const calculateScore = () => {
        if (!quizData || !quizData.quiz_data) return 0;
        return quizData.quiz_data.reduce((score, question, index) => {
            return userAnswers[index] === question.answer ? score + 1 : score;
        }, 0);
    };

    const getDifficultyClass = (difficulty) => {
        if (!difficulty) return styles.easy;
        switch (difficulty.toLowerCase()) {
            case 'easy': return styles.easy;
            case 'medium': return styles.medium;
            case 'hard': return styles.hard;
            default: return styles.easy;
        }
    };
    
    if (!quizData || !quizData.quiz_data) {
        return <p>Quiz data is not available.</p>;
    }

    const resetQuiz = () => {
        setUserAnswers({});
        setSubmitted(false);
        setTakeQuizMode(true);
    };
    
    // View Answers / Explanations Mode
    if (!takeQuizMode) {
        return (
            <div className={styles.container}>
                <div className={styles.header}>
                    <h2>{quizData.title}</h2>
                    <button className={styles.modeButton} onClick={resetQuiz}>
                        Take Quiz Again
                    </button>
                </div>
                <p className={styles.summary}>{quizData.summary}</p>
                
                {quizData.quiz_data.map((q, index) => (
                    <div key={index} className={styles.questionCard}>
                        <div className={styles.questionHeader}>
                            <p className={styles.questionText}><strong>{index + 1}.</strong> {q.question}</p>
                            <span className={`${styles.difficulty} ${getDifficultyClass(q.difficulty)}`}>{q.difficulty || 'Easy'}</span>
                        </div>
                        <ul className={styles.optionsList}>
                            {q.options.map((option, i) => (
                                <li key={i} className={option === q.answer ? styles.correctOptionStatic : ''}>
                                    {option === q.answer && <CheckIcon />}
                                    {option}
                                </li>
                            ))}
                        </ul>
                        <p className={styles.explanation}><strong>Explanation:</strong> {q.explanation}</p>
                    </div>
                ))}
                
                <div className={styles.footer}>
                    <strong>Related Topics:</strong>
                    <div className={styles.topics}>
                        {quizData.related_topics && quizData.related_topics.map(topic => <span key={topic} className={styles.topicTag}>{topic}</span>)}
                    </div>
                </div>
            </div>
        );
    }
    
    // Take Quiz Mode
    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h2>{quizData.title}</h2>
                <span className={styles.quizModePill}>Quiz Mode</span>
            </div>
            {submitted && (
                <div className={styles.scoreCard}>
                    <h3>Quiz Complete!</h3>
                    <p>You scored</p>
                    <div className={styles.scoreValue}>
                      {calculateScore()} / {quizData.quiz_data.length}
                    </div>
                </div>
            )}
            
            {quizData.quiz_data.map((q, index) => (
                <div key={index} className={styles.questionCard}>
                    <p className={styles.questionText}><strong>{index + 1}.</strong> {q.question}</p>
                    <div className={styles.quizOptions}>
                        {q.options.map((option, i) => {
                            const isSelected = userAnswers[index] === option;
                            const isCorrect = option === q.answer;
                            
                            let optionClass = styles.quizOption;
                            if (isSelected) {
                                optionClass += ` ${styles.selectedOption}`;
                            }
                            if (submitted) {
                                if (isCorrect) optionClass += ` ${styles.correctOption}`;
                                else if (isSelected && !isCorrect) optionClass += ` ${styles.incorrectOption}`;
                            }

                            return (
                                <label key={i} className={optionClass}>
                                    <input
                                        type="radio"
                                        name={`question-${index}`}
                                        value={option}
                                        checked={isSelected}
                                        onChange={() => handleAnswerChange(index, option)}
                                        disabled={submitted}
                                    />
                                    <span>{option}</span>
                                    {submitted && isCorrect && <span className={styles.icon}><CheckIcon /></span>}
                                    {submitted && isSelected && !isCorrect && <span className={styles.icon}><CrossIcon /></span>}
                                </label>
                            );
                        })}
                    </div>
                </div>
            ))}

            <div className={styles.quizActions}>
                {!submitted ? (
                    <button className={styles.submitQuizButton} onClick={handleSubmit}>
                        Submit Answers
                    </button>
                ) : (
                    <div className={styles.postSubmitActions}>
                        <button className={styles.modeButton} onClick={resetQuiz}>Try Again</button>
                        <button className={styles.primaryButton} onClick={() => setTakeQuizMode(false)}>
                            View Explanations
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default QuizDisplay;