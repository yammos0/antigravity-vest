import duckdb
from app.core.config import settings

class Database:
    def __init__(self):
        self._conn = None

    def get_connection(self):
        if self._conn is None:
            # Create data directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(settings.DUCKDB_PATH), exist_ok=True)
            
            self._conn = duckdb.connect(settings.DUCKDB_PATH)
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

db = Database()

def get_db():
    conn = db.get_connection()
    try:
        yield conn
    finally:
        # We generally keep the connection open for DuckDB in file mode,
        # but for clean dependency injection, we yield it.
        pass
