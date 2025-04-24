"""Routes for the FastAPI application."""

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from http import HTTPStatus
from app.api.v1.constant import BackgroundType, BACKGROUND_DIR
from app.services.blob import AzureBlobService
from app.services.open_ai import generate_background_image

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
async def handle_request(payload: DataRequest, x_cd_user_id: str = Header(...)) -> dict:
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")

    if not payload.text and not payload.image_base64:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="At least one of text or image is required")

    BlobService = AzureBlobService()
    BlobService.upload_base64_image()

    if payload.text and payload.image_base64:
        background_type = BackgroundType.TEXT_IMAGE
    elif payload.text:
        background_type = BackgroundType.TEXT
    elif payload.image_base64:
        background_type = BackgroundType.IMAGE
    else:
        background_type = BackgroundType.NONE

    # Open AI process
    try:
        result_image = generate_background_image(background_type=background_type, text=payload.text, image_base64=payload.image_base64)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error generating background image: {str(e)}")

    # Blob process
    try:
        BlobService.upload_base64_image(base64_str=result_image, blob_name=f"{BACKGROUND_DIR}/{user_uuid}.png")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error uploading image to Blob: {str(e)}")

    return {
        "message": "Data received successfully and saved to Blob.",
        "user_id": str(user_uuid),
        "text_length": len(payload.text) if payload.text else 0,
        "has_image": bool(payload.image_base64)
    }
