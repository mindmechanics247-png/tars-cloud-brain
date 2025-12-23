1) Activate venv (Windows cmd)
   venv\Scripts\activate

2) Install dependencies
   pip install -r requirements.txt

3) Create .env from .env.example and fill keys.

4) Start server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5) Swagger UI
   http://127.0.0.1:8000/docs
