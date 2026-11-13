import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://appuser:apppass@localhost:5432/library")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
