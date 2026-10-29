import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import init_db
from app.routers import conversations, messages, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Mansur API",
    description="REST API backed by PostgreSQL and SQLAlchemy",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(messages.router)


@app.get("/HelloWorld")
def helloworld():
    return {"message": "Hello World"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
