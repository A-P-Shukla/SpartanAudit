# SpartanAudit Frontend

SpartanAudit Frontend is a high-contrast, professional-grade interface designed to present AI-powered engineering audits. It provides a streamlined workflow for triggering new repository assessments and reviewing historical analysis with a focus on technical transparency and aesthetic excellence.

## Technical Architecture

The application is built as a Single Page Application (SPA) using React 19, following a modular component-based architecture.

### Primary Technologies
- **React**: Core UI library for component management and state orchestration.
- **CSS Modules**: Provides scoped styling to ensure design consistency and prevent global namespace collisions.
- **Axios**: Manages asynchronous communication with the backend REST API.
- **Nginx**: Serves the production build within a containerized environment.

## Design System

The platform utilizes a "Spartan" aesthetic—a dark, high-contrast theme focused on readability and professional intensity.

### Visual Foundations
- **Color Palette**: Deep blacks (#0d0d0d), slate grays (#1a1a1a), and high-intensity signal reds (#c0392b, #ff4d4d) for critical highlights.
- **Typography**: Uses the 'Inter' sans-serif family for a modern, engineering-focused feel.
- **Interactive Elements**: Includes CSS-based micro-animations, gradient-animated progress indicators, and transition-based hover effects.

## Component Breakdown

### 1. GenerateAudit
The primary entry point for user interaction.
- **Functionality**: Captures GitHub URLs and optional job descriptions.
- **Transparency**: Includes the "Audit Protocol Disclosure," clearly stating that the audit is metadata-based rather than a line-by-line source code scan.
- **State Management**: Handles caching bypass via the "Force Re-audit" flag.

### 2. AuditReport
The detailed dashboard for individual repository assessments.
- **Visuals**: Displays the "Verdict Banner" (Hire/Wrong Fit/Tutorial Hell) with color-coded status indicators.
- **Data Layers**: Shows an engineering score (0-10), relevancy match percentage, a brutal technical critique, and the raw "Reconnaissance Data" (Tech Stack and Proof of Engineering artifacts).

### 3. AuditHistory
A management interface for past audits.
- **Features**: Allows users to revisit historical reports stored in the backend database.

## Environment Configuration

The frontend requires connection to a SpartanAudit backend instance. Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Audit Protocol Transparency

A core feature of the UI is the explicit disclosure of the auditing methodology. This ensures users understand that decisions are based on:
- Infrastructure detection (Docker, CI/CD).
- Modular architecture (Source code file structure).
- ML Engineering artifacts (Models, Notebooks, Datasets).
- Dependency management.

## Setup and Installation

### Docker (Recommended)
This is the preferred method for production-equivalent environments. Run from the project root:
```bash
docker-compose up --build
```
The frontend will be accessible at `http://localhost:3000`.

### Manual Local Development
1. Navigate to the directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`
4. Access the application: `http://localhost:3000`

## Production Build
To generate a production-ready bundle manually:
```bash
npm run build
```
The artifacts will be generated in the `build/` directory.
