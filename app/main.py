"""Entry point for the FastAPI application."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.api.v1.routers import background, character, model
from app.constant import FRONT_END_IP, FRONT_END_PORT

app = FastAPI(title="MotionCanvas", version="1.0.0")

app.include_router(background.router)
app.include_router(character.router)
app.include_router(model.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{FRONT_END_PORT}", f"http://{FRONT_END_IP}:{FRONT_END_PORT}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_msg = exc.detail
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": error_msg},
    )
