"""Entry point for the FastAPI application."""

from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse
from app.api.v1.routers import background, character, model

app = FastAPI(title="MotionCanvas", version="1.0.0")

app.include_router(background.router)
app.include_router(character.router)
app.include_router(model.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_msg = exc.detail
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": error_msg},
    )
