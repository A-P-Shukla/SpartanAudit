# Frontend Documentation: IntelliQuiz Application

---

## Overview

The **IntelliQuiz Frontend** is a modern, responsive web client built using React and TypeScript. It enables users to generate custom quizzes from Wikipedia articles, visualize summary and entities, and interact with AI-generated content. This documentation explains the full architecture, component structure, styling conventions, environment setup, and integration process.

---

## Directory Structure
```
frontend/
│
├── public/ # Static assets
├── src/
│ ├── components/ # Reusable UI components
│ │ ├── QuizGenerator.tsx
│ │ ├── QuizQuestion.tsx
│ │ ├── QuizRecap.tsx
│ │ └── ...other components
│ ├── pages/ # Page routes (Home, Quiz, Results)
│ │ ├── Home.tsx
│ │ ├── Quiz.tsx
│ │ └── Results.tsx
│ ├── styles/ # Custom CSS/SCSS modules
│ ├── utils/ # Helper functions (API, formatting, etc.)
│ ├── hooks/ # Custom React hooks
│ ├── App.tsx # Main app entry point
│ ├── index.tsx # ReactDOM root
│ └── ... # Additional logic and tests
├── .env # Environment variables
├── package.json # Dependencies and scripts
├── README.md
└── ...other configs
```

---

## Technologies Used

- **React 18+** (TypeScript)
- **Vite or Create React App**
- **Tailwind CSS / CSS Modules / SCSS** for styling
- **Axios** for API calls
- **React Router** for navigation
- **State Management:** React Context or Redux (if needed)
- **Jest / React Testing Library** for unit testing

---

## Setup Instructions

1. **Clone the repository:**

    ```
    git clone https://github.com/A-P-Shukla/quiz-generator-project.git
    cd quiz-generator-project/frontend
    ```

2. **Install dependencies:**

    ```
    npm install
    # OR
    yarn install
    ```

3. **Configure the .env file:**

    ```
    VITE_BACKEND_URL=http://localhost:8000   # Point to FastAPI backend
    ```

4. **Run the development server:**

    ```
    npm run dev
    # OR
    yarn dev
    ```

5. **Build for production:**

    ```
    npm run build
    # OR
    yarn build
    ```

---

## Core Components

### QuizGenerator

- Accepts Wikipedia URL from user
- Validates input (optional: live feedback using `/validate-url`)
- Submits request to backend `/generate-quiz/` endpoint
- Loads and displays the generated quiz

### QuizQuestion

- Renders each quiz question, its options, and handles answer selection
- Provides instant feedback and stores answers in local state

### QuizRecap

- Shows user's overall performance, correct answers, explanations, and summary

### Entity & Summary Displays

- Renders key entities (people, organizations, locations)
- Displays AI-generated summary and related topics

### Navigation

- **React Router** allows users to switch between: Home → Quiz → Results
- Routing configuration in `App.tsx` and `pages/`

---

## API Integration

- All requests to the backend use the URL specified in `.env`
- APIs used:
    - `POST /generate-quiz/` - Generates a new quiz for a Wikipedia article
    - `GET /quizzes/` - Loads all previously generated quizzes
    - `GET /validate-url/` - Checks Wikipedia URL for validity

- **Axios** is used for all HTTP requests, with error handling and user notifications.

---

## Styling and UI/UX

- **Mobile-first and responsive:** All components adapt for desktop and mobile
- **Tailwind CSS** or **CSS Modules** for UI consistency
- Components are modular, testable, and reusable
- Accessibility (ARIA) and form validation best practices

---

## State Management

- **Local state:** For quiz progress and answers
- **Global state (Context/Redux):** For persistent user data (if needed)
- **API responses:** Are cached in session/local storage for performance

---

## Testing

- **Jest** and **React Testing Library** used for unit/component tests
- `__tests__/` directory for component-level tests

---

## Development Workflow

1. Fork and clone repo
2. Create feature branches per component/feature
3. Lint and format code using ESLint/Prettier
4. Add/expand unit tests as needed
5. Submit pull requests with descriptive commit messages

---

## Authors & Maintainers

**Akhand Pratap Shukla**

- [GitHub: A-P-Shukla](https://github.com/A-P-Shukla/)
- [LinkedIn: Akhand Pratap Shukla](https://www.linkedin.com/in/akhand-pratap-shukla/)
- Contact: akhandshukla36@gmail.com

---

## License

This project is open-source and available under the MIT License.

---
