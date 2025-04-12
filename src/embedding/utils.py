from sentence_transformers.util import cos_sim

from src.embedding.model import embedding_model


def get_text_embedding(text: list[str]) -> list[list[float]]:
    """
    Get the embedding of a text using the embedding model.

    Args:
        text (list[str]): The text to get the embedding for.

    Returns:
        list[list[float]]: The embedding of the text.
    """
    return embedding_model.encode(text).tolist()


def get_query_embedding(query: str) -> list[float]:
    """
    Get the embedding of a query using the embedding model.

    Args:
        query (str): The query to get the embedding for.

    Returns:
        list[float]: The embedding of the query.
    """
    return embedding_model.encode(query, prompt_name="query").tolist()


async def aget_text_embedding(text: list[str]) -> list[list[float]]:
    """
    Get the embedding of a text using the embedding model asynchronously.

    Args:
        text (list[str]): The text to get the embedding for.

    Returns:
        list[list[float]]: The embedding of the text.
    """
    return await embedding_model.encode(text).tolist()


async def aget_query_embedding(query: str) -> list[float]:
    """
    Get the embedding of a query using the embedding model asynchronously.

    Args:
        query (str): The query to get the embedding for.

    Returns:
        list[float]: The embedding of the query.
    """
    return await embedding_model.encode(query, prompt_name="query").tolist()


def get_similarity_scores(
    query_embedding: list[float], doc_embeddings: list[list[float]]
) -> list[float]:
    """
    Get the similarity scores between a query embedding and document embeddings.

    Args:
        query_embedding (list[float]): The embedding of the query.
        doc_embeddings (list[float]): The embeddings of the documents.

    Returns:
        list[float]: The similarity scores between the query embedding and document embeddings.
    """
    similarities = cos_sim(query_embedding, doc_embeddings)
    return similarities.tolist()
