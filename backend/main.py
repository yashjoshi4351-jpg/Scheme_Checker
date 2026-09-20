from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import init_db

from app.api.routes import (
    health,
    schemes,
    eligibility,
    profile,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.
    """

    # Create database tables if they do not exist.
    init_db()

    yield


app = FastAPI(
    title="Government Scheme Eligibility Checker",
    description=(
        "API for checking citizen eligibility for "
        "government welfare schemes."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

app.include_router(
    health.router,
    prefix="/api",
    tags=["Health"],
)

app.include_router(
    schemes.router,
    prefix="/api",
    tags=["Schemes"],
)

app.include_router(
    eligibility.router,
    prefix="/api",
    tags=["Eligibility"],
)

app.include_router(
    profile.router,
    prefix="/api",
    tags=["Profile"],
)


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Government Scheme Eligibility Checker API",
        "status": "running",
        "version": "1.0.0",
    }