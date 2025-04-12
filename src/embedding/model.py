from sentence_transformers import SentenceTransformer

from src.settings import settings

embedding_model = SentenceTransformer(
    settings.embedding_model_name,
    truncate_dim=settings.embedding_model_dims,
    cache_folder=settings.embedding_model_dir,
)
