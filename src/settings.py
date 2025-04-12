import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.pg_user: str = os.getenv("POSTGRES_USER", "")
        self.pg_password: str = os.getenv("POSTGRES_PASSWORD", "")
        self.pg_db: str = os.getenv("POSTGRES_DB", "")
        self.pg_host: str = os.getenv("POSTGRES_HOST", "pgvector-db")
        self.pg_port: str = os.getenv("POSTGRES_PORT", "5432")

        self.pg_url: str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            self.pg_user,
            self.pg_password,
            self.pg_host,
            self.pg_port,
            self.pg_db,
        )
        self.async_pg_url: str = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.pg_user,
            self.pg_password,
            self.pg_host,
            self.pg_port,
            self.pg_db,
        )
        self.embedding_model_name: str = "mixedbread-ai/mxbai-embed-large-v1"
        self.embedding_model_dir: Path = Path("./model_cache/")
        self.embedding_model_dims: int = 512

    def embedding_model_exists(self) -> bool:
        """
        Check if the embedding model exists in the cache directory.
        """
        return (
            self.embedding_model_dir
            / f"model_cache/models--{self.embedding_model_name}/snapshots"
        ).exists()

    def get_embedding_model_dir(self) -> str:
        if not self.embedding_model_dir.exists():
            return (
                self.embedding_model_dir
                / f"model_cache/models--{self.embedding_model_name}/snapshots"
            )
        else:
            return str(self.embedding_model_dir)


settings = Settings()
