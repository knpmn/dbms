"""
db.py - cx_Oracle connection pool helper.
All routes import get_connection() to get a pooled Oracle connection.
"""
import oracledb
import config

_pool = None


def init_pool():
    """Initialize the Oracle connection pool. Called once at app startup."""
    global _pool
    # Thin mode is default in oracledb, makedsn and pool creation look like this:
    dsn = f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_SERVICE}"
    _pool = oracledb.create_pool(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        dsn=dsn,
        min=2,
        max=10,
        increment=1
    )


def get_connection():
    """Acquire a connection from the pool."""
    if _pool is None:
        init_pool()
    return _pool.acquire()


def release_connection(conn):
    """Release a connection back to the pool."""
    if _pool and conn:
        _pool.release(conn)


def execute_query(sql, params=None, fetch=True):
    """
    Utility: run a SELECT and return rows as list-of-dicts.
    For DML (INSERT/UPDATE/DELETE) set fetch=False; it returns None and auto-commits.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or {})
        if fetch:
            cols = [desc[0].lower() for desc in cursor.description]
            rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
            return rows
        else:
            conn.commit()
            return None
    finally:
        cursor.close()
        release_connection(conn)


def execute_one(sql, params=None):
    """Run a SELECT and return only the first row as a dict (or None)."""
    rows = execute_query(sql, params, fetch=True)
    return rows[0] if rows else None
