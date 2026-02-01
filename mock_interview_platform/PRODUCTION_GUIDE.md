# 🚀 InterviewIQ - Production Deployment Guide

## Application Overview

**InterviewIQ** is an AI-powered mock interview platform with a React frontend and FastAPI backend. It analyzes resumes and job descriptions to conduct adaptive interviews with real-time feedback.

**Stack:**
- **Frontend:** React 18 + Axios
- **Backend:** FastAPI + Python 3.10
- **Database:** In-memory (ready for PostgreSQL/MongoDB)
- **Deployment:** Docker & Docker Compose

---

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.10+
- Node.js 16+
- Docker (optional)

### Local Development

**Terminal 1 - Backend:**
```bash
pip install -r requirements.txt
python -m uvicorn src.api.app:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:3000`

### Docker Deployment
```bash
docker-compose up --build
```

---

## Environment Configuration

### Backend (.env)
```env
# AI Model Configuration
GOOGLE_API_KEY=your_key_here

# Optional: For other AI models
# FOUNDRY_API_KEY=...
# GITHUB_TOKEN=...
```

### Frontend (frontend/.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=InterviewIQ
```

---

## API Documentation

### Base URL
- Local: `http://localhost:8000`
- Production: `https://api.interviewiq.com`

### Interactive Documentation
Swagger UI: `http://localhost:8000/docs`

### Core Endpoints

#### 1. Initialize Interview
```
POST /api/interview/initialize
```
**Request:**
```json
{
  "candidate_name": "John Doe",
  "job_title": "Senior Developer",
  "resume_text": "...",
  "jd_text": "..."
}
```

**Response:**
```json
{
  "session_id": "session_1234567890",
  "status": "success",
  "skill_gaps": ["Docker", "Kubernetes"],
  "total_questions": 5,
  "initial_question": { ... }
}
```

#### 2. Get Current Question
```
GET /api/interview/{session_id}/question
```

**Response:**
```json
{
  "session_id": "session_1234567890",
  "question_number": 1,
  "total_questions": 5,
  "difficulty": "medium",
  "time_limit": 120,
  "question_type": "technical",
  "question_text": "Explain REST APIs..."
}
```

#### 3. Submit Answer
```
POST /api/interview/{session_id}/submit-answer
```

**Request:**
```json
{
  "session_id": "session_1234567890",
  "answer_text": "REST stands for...",
  "time_taken": 85
}
```

**Response:**
```json
{
  "session_id": "session_1234567890",
  "score": 4.2,
  "accuracy": 4.5,
  "completeness": 4.0,
  "clarity": 4.0,
  "relevance": 4.2,
  "feedback": "Good explanation...",
  "interview_continues": true,
  "difficulty_adjusted": false,
  "next_question": { ... }
}
```

#### 4. Conclude Interview
```
GET /api/interview/{session_id}/conclude
```

**Response:**
```json
{
  "session_id": "session_1234567890",
  "status": "completed",
  "candidate_name": "John Doe",
  "job_title": "Senior Developer",
  "final_score": 78.5,
  "readiness": "Ready",
  "hiring_ready": true,
  "role_fit": 0.82,
  "report": "Comprehensive feedback...",
  "duration_minutes": 15.5
}
```

---

## File Structure

```
interview-iq/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py              # FastAPI application
│   ├── agents/
│   │   └── ai_interviewer.py   # Interview orchestration
│   ├── core/
│   │   ├── resume_analyzer.py
│   │   ├── job_description_analyzer.py
│   │   ├── question_generator.py
│   │   ├── answer_evaluator.py
│   │   └── interview_scorer.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── models.py
│   │   └── gemini_provider.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── InterviewSetup.js
│   │   │   ├── InterviewSession.js
│   │   │   └── InterviewReport.js
│   │   ├── styles/
│   │   │   ├── InterviewSetup.css
│   │   │   ├── InterviewSession.css
│   │   │   └── InterviewReport.css
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   └── package.json
│
├── docker-compose.yml
├── Dockerfile.backend
├── requirements.txt
├── .env.example
├── README.md
├── WEB_APP_SETUP.md
└── PRODUCTION_GUIDE.md
```

---

## Scaling for Production

### Database Migration
Replace in-memory storage in `src/api/app.py`:

```python
# Before: In-memory dictionary
interview_sessions: Dict[str, InterviewOrchestrator] = {}

# After: Use PostgreSQL/MongoDB
from sqlalchemy import create_engine
Session = sessionmaker(bind=engine)
db_session = Session()
```

### Load Balancing
With Docker Compose:
```yaml
services:
  backend-1:
    ...
  backend-2:
    ...
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    # Configure reverse proxy
```

### Caching
Add Redis for session caching:
```python
import redis
cache = redis.Redis(host='localhost', port=6379)
```

---

## Monitoring & Logging

### Backend Logs
```bash
# Real-time logs
docker-compose logs -f backend

# All logs
docker-compose logs backend
```

### Frontend Logs
Browser DevTools Console (`F12`)

### Health Checks
```bash
curl http://localhost:8000/api/health
```

---

## Security Checklist

- [ ] Enable HTTPS/SSL certificates
- [ ] Update CORS origins for production domain
- [ ] Implement rate limiting
- [ ] Add authentication (JWT/OAuth)
- [ ] Validate all user inputs
- [ ] Sanitize AI responses
- [ ] Use environment variables for secrets
- [ ] Enable request logging
- [ ] Set up monitoring/alerts
- [ ] Regular security audits

### CORS Configuration (Production)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://interviewiq.com"],  # Specify domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Troubleshooting

### Backend Issues

**Port Already in Use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Dependencies Error**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**API Key Error**
```bash
# Verify .env is in project root
cat .env

# Check API key is valid
echo $GOOGLE_API_KEY
```

### Frontend Issues

**Node Modules Error**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 in Use**
```bash
PORT=3001 npm start
```

**API Connection Error**
- Check backend is running on port 8000
- Verify `REACT_APP_API_URL` in frontend/.env
- Check browser console for CORS errors

### Docker Issues

**Container Won't Start**
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Rebuild Containers**
```bash
docker-compose down
docker-compose up --build
```

---

## Performance Tips

1. **Lazy Load React Components**
   ```javascript
   const InterviewSession = React.lazy(() => import('./pages/InterviewSession'));
   ```

2. **Optimize API Calls**
   - Implement request caching
   - Batch requests where possible
   - Use pagination for large datasets

3. **Database Indexing**
   - Index session_id for fast lookups
   - Index created_at for time-based queries

4. **Frontend Optimization**
   - Minify CSS/JS in production build
   - Use CDN for static assets
   - Implement service workers for offline support

5. **Backend Optimization**
   - Use async/await for I/O operations
   - Implement connection pooling
   - Cache AI model responses

---

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL
pg_dump interview_iq > backup.sql

# Restore
psql interview_iq < backup.sql
```

### Environment Backup
```bash
# Backup credentials
cp .env .env.backup

# Keep in secure location (not version control)
```

---

## Version Updates

### Update Dependencies
```bash
# Backend
pip list --outdated
pip install -U package_name

# Frontend
npm outdated
npm update
```

### Code Deployment
```bash
# Pull latest code
git pull

# Rebuild containers
docker-compose down
docker-compose up --build

# Run migrations if needed
python manage.py migrate
```

---

## Support & Resources

- **Documentation:** See README.md, WEB_APP_SETUP.md
- **API Docs:** http://localhost:8000/docs
- **Issues:** Check SETUP.md troubleshooting section
- **Code:** All source code in `src/` with docstrings

---

**Last Updated:** February 1, 2026  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
