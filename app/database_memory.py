import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/memory.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id)
                    REFERENCES sessions(session_id)
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def create_session(session_id):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT OR IGNORE INTO sessions (
                session_id
            )
            VALUES (?)
            """,
            (session_id,),
        )

        connection.commit()

    finally:
        connection.close()


def save_message(
    session_id,
    role,
    content,
):
    create_session(session_id)

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO messages (
                session_id,
                role,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                session_id,
                role,
                content,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_messages(
    session_id,
    limit=10,
):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT role, content
            FROM messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                session_id,
                limit,
            ),
        ).fetchall()

    finally:
        connection.close()

    rows = list(reversed(rows))

    return [
        {
            "role": row["role"],
            "content": row["content"],
        }
        for row in rows
    ]


def get_sessions(limit=20):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                s.session_id,
                s.created_at,
                (
                    SELECT m.content
                    FROM messages m
                    WHERE m.session_id = s.session_id
                    ORDER BY m.id ASC
                    LIMIT 1
                ) AS first_message,
                (
                    SELECT m.created_at
                    FROM messages m
                    WHERE m.session_id = s.session_id
                    ORDER BY m.id DESC
                    LIMIT 1
                ) AS last_message_at
            FROM sessions s
            WHERE EXISTS (
                SELECT 1
                FROM messages m
                WHERE m.session_id = s.session_id
            )
            ORDER BY last_message_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    finally:
        connection.close()

    return [
        {
            "session_id": row["session_id"],
            "created_at": row["created_at"],
            "first_message": row["first_message"],
            "last_message_at": row["last_message_at"],
        }
        for row in rows
    ]


def delete_session(session_id):
    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM messages
            WHERE session_id = ?
            """,
            (session_id,),
        )

        connection.execute(
            """
            DELETE FROM sessions
            WHERE session_id = ?
            """,
            (session_id,),
        )

        connection.commit()

    finally:
        connection.close()
