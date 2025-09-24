from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("DB_USER", "root")
PASS = os.getenv("DB_PASS", "")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "food_wastage")

DB_URI = f"mysql+mysqlconnector://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}?charset=utf8mb4"

def get_engine():
    """Create and return a SQLAlchemy engine connected to our DB."""
    return create_engine(DB_URI, future=True)

def run_sql(sql, params=None):
    """Execute a query and return results as list of dicts."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        cols = result.keys()
        rows = [dict(zip(cols, r)) for r in result.fetchall()]
    return rows
