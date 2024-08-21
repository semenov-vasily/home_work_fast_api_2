import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "app_fast_api_2")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5439")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app_fast_api_2")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

TOKEN_TTL = int(os.getenv("TOKEN_TTL", 60 * 60 * 24))
DEFAULT_ROLE = os.getenv("DEFAULT_ROLE", "user")

