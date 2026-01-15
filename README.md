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

```text
lyftr-ai-backend/
├── app/
│   ├── __init__.py
│   ├── main.py        # API routes
│   ├── config.py     # Environment configuration
│   ├── db.py         # Database logic
│   ├── models.py     # Request & response models
│   └── metrics.py    # Prometheus-style metrics
│
├── data/
│   └── app.db        # SQLite database (Docker volume)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


## ⚙️ Prerequisites
- Git
- Docker Desktop

---

▶️ Run the Project (Recommended)
git clone https://github.com/ayushsingh0104/lyftr-ai-backend.git
cd lyftr-ai-backend
docker compose up --build

On Success

Uvicorn running on http://0.0.0.0:8000


Open API Docs

Swagger UI: http://localhost:8000/docs


🔌 API Endpoints
Health Checks

| Method | Endpoint        | Description     |
| ------ | --------------- | --------------- |
| GET    | `/health/live`  | Liveness probe  |
| GET    | `/health/ready` | Readiness probe |


Webhook

| Method | Endpoint   |
| ------ | ---------- |
| POST   | `/webhook` |

1.Secured using HMAC-SHA256
2.Requires header: X-Signature
3.Idempotent message storage


Messages

| Method | Endpoint    |
| ------ | ----------- |
| GET    | `/messages` |

Query Parameters

1.limit
2.offset
3.from
since
5.q

Stats

| Method | Endpoint |
| ------ | -------- |
| GET    | `/stats` |

Aggregated message analytics


Metrics

| Method | Endpoint   |
| ------ | ---------- |
| GET    | `/metrics` |

Prometheus-style plaintext metrics


🔐 Environment Variables

Configured via Docker Compose
| Variable         | Description              |
| ---------------- | ------------------------ |
| `WEBHOOK_SECRET` | HMAC verification secret |
| `DATABASE_URL`   | SQLite database path     |


🛑 Stop the Services
 
docker compose down


📌 Notes for Reviewers

1.Dockerized multi-stage build

2.Non-root container execution

3.Clean separation of concerns

Idempotent webhook handling

5.Metrics aligned with Prometheus scraping


👤 Author

Ayush Kumar Singh
GitHub: https://github.com/ayushsingh0104