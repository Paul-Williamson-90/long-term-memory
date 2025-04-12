import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from src.db import Base, engine

logger = logging.getLogger(__name__)

# Create a session to execute raw SQL commands
Session = sessionmaker(bind=engine)
session = Session()

try:
    result = session.execute(
        text("SELECT * FROM pg_extension WHERE extname = 'vector';")
    ).fetchone()
    if result:
        logger.info("pgvector extension is already installed.")
    else:
        logger.info("pgvector extension is NOT installed, attempting to install it.")
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        session.commit()  # Commit to apply the change
        logger.info("pgvector extension installed successfully.")
except Exception as e:
    logger.error(f"Error checking/creating pgvector extension: {e}")
    session.rollback()  # Rollback if there's an error
    raise e
finally:
    session.close()

# Now create the tables
Base.metadata.create_all(bind=engine)
logger.info("Tables created successfully.")

# Close the session
session.close()
