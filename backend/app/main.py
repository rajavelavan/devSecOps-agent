from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import health, webhooks

def create_app() -> FastAPI:
    app = FastAPI(title="Autonomous Cloud Security Agent")

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

    return app

app = create_app()
