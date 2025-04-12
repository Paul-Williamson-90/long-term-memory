import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.pg_user: str = os.getenv("POSTGRES_USER", "")
        self.pg_password: str = os.getenv("POSTGRES_PASSWORD", "")
        self.pg_db: str = os.getenv("POSTGRES_DB", "")
        self.pg_url: str = "postgresql://{}:{}@db:5432/{}".format(
            self.pg_user,
            self.pg_password,
            self.pg_db,
        )
        self.async_pg_url: str = "postgresql+asyncpg://{}:{}@db:5432/{}".format(
            self.pg_user,
            self.pg_password,
            self.pg_db,
        )
        self.embedding_model_name: str = "mixedbread-ai/mxbai-embed-large-v1"
        self.embedding_model_dir: Path = Path("./model_cache/")
        self.embedding_model_dims: int = 512

    def get_embedding_model_dir(self) -> str:
        if not self.embedding_model_dir.exists():
            return self.embedding_model_name
        else:
            return str(self.embedding_model_dir)


settings = Settings()
