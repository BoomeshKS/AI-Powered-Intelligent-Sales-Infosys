
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models

from .routers import (
    leads,
    analysis,
    outreach,
    scoring
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SalesGenie AI",
    description="AI Sales Assistant and Lead Intelligence Platform",
    version="2.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# MILESTONE 1
app.include_router(leads.router)
app.include_router(analysis.router)

# MILESTONE 2
app.include_router(outreach.router)
app.include_router(scoring.router)


@app.get("/")
def home():
    return {
        "message": "SalesGenie AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
