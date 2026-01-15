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

## 🚀 Running the Service

### 1. Clone the repository
```bash
git clone https://github.com/ayushsingh0104/lyftr-ai-backend.git
cd lyftr-ai-backend


2. Start the service using Docker (recommended)
docker compose up --build

On success, the API will be available at:
http://localhost:8000


3. Verify the service
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready

Expected response:
{ "status": "ok" }

4. View API documentation
http://localhost:8000/docs

5. Stop the service
docker compose down
