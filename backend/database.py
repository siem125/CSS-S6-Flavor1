from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import time


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://scanner:scanner@postgres:5432/scannerdb"
)

for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("Database connected")
        break

    except Exception as e:
        print("Database not ready, retrying...")
        time.sleep(2)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()