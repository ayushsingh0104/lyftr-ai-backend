# Lyftr AI — Backend Engineer Assignment

This repository contains the implementation of the **Lyftr AI Backend Engineer assignment** using **FastAPI**.  
The service ingests webhook messages securely, stores them idempotently, exposes analytics, and is fully **Dockerized**.

---

## 🚀 Tech Stack
- Python 3.11
- FastAPI
- Pydantic
- SQLite
- Docker & Docker Compose

---

## 📁 Project Structure
.
├── app/
│ ├── main.py # API routes
│ ├── config.py # Environment config
│ ├── db.py # Database logic
│ ├── models.py # Request validation
│ └── metrics.py # Prometheus-style metrics
├── data/ # SQLite DB (volume)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

## ⚙️ Prerequisites
- Git
- Docker Desktop

---

## ▶️ Run the Project (Recommended)

```bash
git clone <repository-url>
cd <repository-folder>
docker compose up --build



On success:

Uvicorn running on http://0.0.0.0:8000


Open:

http://localhost:8000/docs


Stop the service:

CTRL + C
docker compose down


🔗 API Endpoints
Health

GET /health/live

GET /health/ready

Webhook

POST /webhook

Secured via HMAC-SHA256

Header: X-Signature

Messages

GET /messages

Supports limit, offset, from, since, q

Stats

GET /stats

Aggregated message analytics

Metrics

GET /metrics

Prometheus-style plain text metrics



🔐 Environment Variables

Configured via Docker Compose:

Variable	Description
WEBHOOK_SECRET	HMAC verification secret
DATABASE_URL	SQLite database path


💾 Data Persistence

SQLite DB stored in data/

Persists across container restarts

👤 Author

Ayush Kumar Singh
Backend Engineer Candidate
