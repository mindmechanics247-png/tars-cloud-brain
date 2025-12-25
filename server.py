import asyncio
from fastapi import FastAPI
from app.router_ai import router as ai_router

app = FastAPI(title="TARS Cloud Brain")

app.include_router(ai_router)

@app.get("/")
def health():
    return {"status": "TARS Cloud Brain Online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000)
