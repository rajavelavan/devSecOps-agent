import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import health, webhooks, ingestion
from app.core.sqs_worker import sqs_polling_worker

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the background SQS polling worker
    worker_task = asyncio.create_task(sqs_polling_worker())
    yield
    # Shutdown: Cancel the worker task
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

def create_app() -> FastAPI:
    app = FastAPI(title="Autonomous Cloud Security Agent", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:3000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(health.router, tags=["Health"])
    app.include_router(webhooks.router, prefix="/webhook", tags=["Webhooks"])
    app.include_router(ingestion.router, prefix="/api/ingestion", tags=["Ingestion"])

    return app

app = create_app()
