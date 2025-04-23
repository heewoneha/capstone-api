from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from http import HTTPStatus

app = FastAPI()

class DataRequest(BaseModel):
    text: Optional[str] = None
    image_base64: Optional[str] = None

    @field_validator("text")
    def check_text_length(cls, value):
        if value and len(value) > 120:
            error_message = "Text length exceeds 120 characters."
            raise ValueError(error_message)
        return value

@app.post("/api/submit/background", summary="Submit background data")
async def handle_request(payload: DataRequest, x_cd_user_id: str = Header(...)):
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")

    if not payload.text and not payload.image_base64:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="At least one of text or image is required")

    # Blob process

    return {
        "message": "Data received successfully and saved to Blob.",
        "user_id": str(user_uuid),
        "text_length": len(payload.text) if payload.text else 0,
        "has_image": bool(payload.image_base64)
    }
