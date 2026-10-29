import os
from urllib.parse import quote_plus


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    user = os.getenv("PGUSER", "postgres")
    socket_dir = os.getenv("PGHOST", "/tmp")
    port = os.getenv("PGPORT", "5432")
    db = os.getenv("PGDATABASE", "mansur_db")

    return (
        f"postgresql+psycopg2://{user}@/{db}"
        f"?host={quote_plus(socket_dir)}&port={port}"
    )


DATABASE_URL = get_database_url()
