# 🎯 InterviewIQ - Quick Reference Card

## 📱 What is InterviewIQ?

AI-powered mock interview platform that simulates real interviews with intelligent question generation, real-time evaluation, and personalized feedback.

---

## ⚡ Quick Start (Pick One)

### Option 1: Local Development (Easiest)
```bash
# Terminal 1: Backend
pip install -r requirements.txt
python -m uvicorn src.api.app:app --reload

# Terminal 2: Frontend
cd frontend && npm install && npm start

# Open: http://localhost:3000
```

### Option 2: Docker (Fastest)
```bash
docker-compose up --build
# Open: http://localhost:3000
```

### Option 3: Production
See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)

---

## 📚 Documentation

| Need | File |
|------|------|
| **I want to start using it** | [WEB_APP_SETUP.md](WEB_APP_SETUP.md) |
| **I want to deploy it** | [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) |
| **Pre-launch checklist** | [LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md) |
| **Project status** | [STATUS.md](STATUS.md) |
| **API reference** | [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md#api-documentation) |
| **Troubleshooting** | [WEB_APP_SETUP.md](WEB_APP_SETUP.md#troubleshooting) |

---

## 🔑 Key Files

```
Backend:     src/api/app.py
Frontend:    frontend/src/App.js  
Database:    In-memory (ready for PostgreSQL)
Config:      .env (backend) + frontend/.env
Docker:      docker-compose.yml
```

---

## 🌐 Endpoints

```
Backend API:        http://localhost:8000
Frontend:           http://localhost:3000
API Docs:           http://localhost:8000/docs
Health Check:       http://localhost:8000/api/health
```

---

## ✅ Feature Checklist

- ✅ Resume upload & analysis
- ✅ Job description matching
- ✅ AI-generated questions (adaptive difficulty)
- ✅ Real-time answer evaluation
- ✅ Multi-dimensional scoring
- ✅ Comprehensive report
- ✅ Responsive design
- ✅ Docker deployment

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip` errors | `pip install -r requirements.txt` |
| `npm` errors | `cd frontend && npm install` |
| Port in use | Change port in command or kill process |
| API not connecting | Check backend running on :8000 |
| CORS error | Check `.env` files |

---

## 📊 Technology Stack

**Frontend:** React 18 + Axios  
**Backend:** FastAPI + Python 3.10  
**Database:** In-memory (ready for PostgreSQL)  
**DevOps:** Docker & Docker Compose  

---

## 🎯 Interview Flow

1. **Setup** → Enter candidate info + resume + JD
2. **Initialize** → Backend analyzes documents
3. **Questions** → AI generates adaptive questions
4. **Evaluate** → Real-time scoring per answer
5. **Report** → Final score + recommendations

---

## 🔒 Security

✅ CORS enabled  
✅ Input validation  
✅ Environment variables for secrets  
✅ Error handling  

For production: Add HTTPS, rate limiting, auth

---

## 📊 Project Status

**Version:** 1.0.0  
**Status:** ✅ PRODUCTION READY  
**Last Updated:** February 1, 2026

---

## 🚀 Let's Go!

```bash
# Copy this command to get started:
docker-compose up --build

# Then open: http://localhost:3000
```

---

*Questions? Check [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) or [WEB_APP_SETUP.md](WEB_APP_SETUP.md)*
