# Web App Setup Guide

## Project Structure

```
mock_interview_platform/
├── src/                    # Python backend code
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py         # FastAPI application
│   ├── agents/
│   ├── core/
│   └── utils/
├── frontend/              # React frontend
│   ├── public/
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── pages/         # React pages
│   │   ├── styles/        # CSS files
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── requirements.txt       # Python dependencies
└── docker-compose.yml     # Docker Compose config
```

## Backend Setup

### Prerequisites
- Python 3.10+
- pip/conda

### Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_api_key_here
```

3. **Run the FastAPI server:**
```bash
python -m uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, access the interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

- `POST /api/interview/initialize` - Start a new interview
- `GET /api/interview/{session_id}/question` - Get current question
- `POST /api/interview/{session_id}/submit-answer` - Submit answer for evaluation
- `GET /api/interview/{session_id}/conclude` - Get final report
- `DELETE /api/interview/{session_id}` - Delete a session
- `GET /api/health` - Health check

## Frontend Setup

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure API endpoint:**
Create a `.env` file in the `frontend` directory:
```
REACT_APP_API_URL=http://localhost:8000
```

4. **Start the React development server:**
```bash
npm start
```

The app will open at `http://localhost:3000`

## Running Both Together

### Option 1: Separate Terminals

Terminal 1 (Backend):
```bash
python -m uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm start
```

### Option 2: Using Docker Compose

1. **Build and run containers:**
```bash
docker-compose up --build
```

2. **Access the app:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## Production Deployment

### Build React for production:
```bash
cd frontend
npm run build
```

### Serve with a production server:
```bash
# Use Gunicorn for Python
pip install gunicorn
gunicorn src.api.app:app --workers 4 --bind 0.0.0.0:8000
```

## Troubleshooting

### CORS Issues
If you see CORS errors, make sure:
1. Backend is running on `http://localhost:8000`
2. `REACT_APP_API_URL` in frontend `.env` matches the backend URL
3. Backend has CORS middleware configured (already done in `app.py`)

### Port Already in Use
- Backend: Change port with `--port 9000` (also update `REACT_APP_API_URL`)
- Frontend: Use `PORT=3001 npm start`

### Dependencies Issues
```bash
# Clear cache and reinstall
rm -rf node_modules
npm cache clean --force
npm install
```

## Features

✅ **Interview Setup**
- Paste resume and job description
- Enter candidate name and job title
- AI analyzes documents and identifies skill gaps

✅ **Interactive Interview**
- Real-time question display
- Dynamic difficulty adjustment
- Timer for each question
- Immediate answer evaluation

✅ **Answer Evaluation**
- Multi-dimensional scoring (Accuracy, Completeness, Clarity, Relevance)
- Detailed feedback for each answer
- Difficulty adjustment based on performance

✅ **Final Report**
- Overall score and readiness level
- Hiring readiness indicator
- Role fit percentage
- Comprehensive feedback

## Notes

- All interview sessions are stored in-memory. For production, integrate a database.
- The backend uses Google's Generative AI API for question generation and answer evaluation.
- The frontend is fully responsive and works on mobile devices.
