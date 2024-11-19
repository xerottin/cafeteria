from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from settings import DATABASE_URL, REDIS_CLIENT

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_timeout=60,
    pool_recycle=1800,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_pg_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

redis = REDIS_CLIENT

async def check_redis_connection():
    try:
        await redis.ping()
        print("Connected to Redis")
    except redis.ConnectionError:
        print("Failed to connect to Redis")