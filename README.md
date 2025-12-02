Installation:

1. clone this repo

```
https://github.com/brilbrilbril/simple-RAG.git

cd simple-RAG
```

2. create virtual environment and activate it

```
python -m venv venv

venv/Scripts/activate
```

3. install dependencies

```
pip install -r requirements.txt
```

Optional, install the development kit

```
pip install -r requirements-dev.txt
```

4. create .env file:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

EMBEDDING_MODEL=models/gemini-embedding-001

QDRANT_COLLECTION_NAME=demo_collection

CHAT_MODEL=gemini-2.0-flash

API_URL=http://localhost:8000
```

4. run the backend service

```
uvicorn rag.routes:app --reload
```

5. run the streamlit interface

```
python -m streamlit run rag/app.py
```