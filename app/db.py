import os
import sqlite3
from app.config import settings


def get_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection from DATABASE_URL.

    Supports:
    - sqlite:////data/app.db   (Docker)
    - sqlite:///./data/app.db  (local)
    """
    db_url = settings.DATABASE_URL

    if not db_url.startswith("sqlite:///"):
        raise ValueError("Only sqlite DATABASE_URL is supported")

    # Remove sqlite:/// prefix
    db_path = db_url.replace("sqlite:///", "", 1)

    # Ensure directory exists (important for local dev)
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initialize database schema.
    This function is safe to call multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            from_msisdn TEXT NOT NULL,
            to_msisdn TEXT NOT NULL,
            ts TEXT NOT NULL,
            text TEXT,
            created_at TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()


def fetch_messages(
    limit: int,
    offset: int,
    from_filter: str | None = None,
    since_filter: str | None = None,
    search_q: str | None = None,
):
    conn = get_connection()
    cursor = conn.cursor()

    base_query = "FROM messages WHERE 1=1"
    params: list = []

    # Optional filters
    if from_filter:
        base_query += " AND from_msisdn = ?"
        params.append(from_filter)

    if since_filter:
        base_query += " AND ts >= ?"
        params.append(since_filter)

    if search_q:
        base_query += " AND LOWER(text) LIKE LOWER(?)"
        params.append(f"%{search_q}%")

    # Total count (before pagination)
    cursor.execute(f"SELECT COUNT(*) {base_query}", params)
    total = cursor.fetchone()[0]

    # Fetch paginated rows
    cursor.execute(
        f"""
        SELECT message_id, from_msisdn, to_msisdn, ts, text
        {base_query}
        ORDER BY ts ASC, message_id ASC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    rows = cursor.fetchall()
    conn.close()

    data = [
        {
            "message_id": row["message_id"],
            "from": row["from_msisdn"],
            "to": row["to_msisdn"],
            "ts": row["ts"],
            "text": row["text"],
        }
        for row in rows
    ]

    return data, total

def fetch_stats():
    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    # Total number of messages
    cursor.execute("SELECT COUNT(*) FROM messages")
    stats["total_messages"] = cursor.fetchone()[0]

    # Number of unique senders
    cursor.execute("SELECT COUNT(DISTINCT from_msisdn) FROM messages")
    stats["senders_count"] = cursor.fetchone()[0]

    # Top 10 senders by message count
    cursor.execute(
        """
        SELECT from_msisdn AS sender, COUNT(*) AS count
        FROM messages
        GROUP BY from_msisdn
        ORDER BY count DESC
        LIMIT 10
        """
    )

    stats["messages_per_sender"] = [
        {
            "from": row["sender"],
            "count": row["count"],
        }
        for row in cursor.fetchall()
    ]

    # First and last message timestamps
    cursor.execute("SELECT MIN(ts), MAX(ts) FROM messages")
    row = cursor.fetchone()
    stats["first_message_ts"] = row[0]
    stats["last_message_ts"] = row[1]

    conn.close()
    return stats
