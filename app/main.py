import hmac
import hashlib

from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse

from app.config import settings
from app.db import init_db, get_connection
from app.models import WebhookPayload
from app.db import fetch_messages
from app.db import fetch_stats
from fastapi.responses import PlainTextResponse
from app.metrics import metrics


app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)
    metrics.inc_http(request.url.path, response.status_code)
    return response


@app.on_event("startup")
def on_startup():
    """
    This runs once when the application starts.
    We use it to initialize the database schema.
    """
    init_db()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/webhook")
async def webhook(
    request: Request,
    x_signature: str | None = Header(default=None, alias="X-Signature"),
):
    # 1. Signature must be present
    if not x_signature:
        metrics.inc_webhook("invalid_signature")
        return JSONResponse(
            status_code=401,
            content={"detail": "invalid signature"},
        )

    # 2. Read RAW request body (bytes)
    body_bytes = await request.body()

    # 3. Compute expected HMAC-SHA256 signature
    expected_signature = hmac.new(
        key=settings.WEBHOOK_SECRET.encode(),
        msg=body_bytes,
        digestmod=hashlib.sha256,
    ).hexdigest()

    # 4. Constant-time comparison
    if not hmac.compare_digest(x_signature, expected_signature):
        metrics.inc_webhook("invalid_signature")
        return JSONResponse(
            status_code=401,
            content={"detail": "invalid signature"},
        )

    # 5. Parse & validate JSON payload (Pydantic)
    try:
        payload_dict = await request.json()
        payload = WebhookPayload(**payload_dict)
    except Exception as exc:
        return JSONResponse(
            status_code=422,
            content={"detail": str(exc)},
        )

    # 6. Insert into DB (idempotent)
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO messages (
                message_id, from_msisdn, to_msisdn, ts, text, created_at
            )
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            (
                payload.message_id,
                payload.from_msisdn,
                payload.to_msisdn,
                payload.ts,
                payload.text,
            ),
        )
        conn.commit()

        metrics.inc_webhook("created")

    except Exception:
        # Duplicate message_id → idempotent success
        metrics.inc_webhook("duplicate")
        pass
    finally:
        conn.close()

    return {"status": "ok"}
    
@app.get("/messages")
def list_messages(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    since: str | None = None,
    q: str | None = None,
):
    # "from" is a reserved keyword in Python, so we read it manually
    from_param = request.query_params.get("from")

    data, total = fetch_messages(
        limit=limit,
        offset=offset,
        from_filter=from_param,
        since_filter=since,
        search_q=q,
    )

    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
    
@app.get("/stats")
def get_stats():
    return fetch_stats()
    
@app.get("/health/live")
def health_live():
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready():
    try:
        # DB must be reachable
        fetch_stats()

        # Secret must exist
        if not settings.WEBHOOK_SECRET:
            raise Exception("Secret missing")

        return {"status": "ok"}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "unhealthy"})
    
@app.get("/metrics")
def get_metrics():
    return PlainTextResponse(metrics.render())
