# Simple Long-Term Memory Module
- This project builds a simple long-term memory component for use with Large Language Models (LLMs).
- Memories and embeddings are stored within a PostgreSQL database, with semantic search capability via pg_vector.

# Setup
1. Setup a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Create a .env file and add the following variables:
```.env
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
POSTGRES_HOST=... # localhost for local setup
POSTGRES_PORT=... # typically 5432
```
3. Open Docker desktop
4. Run the Makefile command:
```bash
make start
```
5. See play.ipynb for examples of usage