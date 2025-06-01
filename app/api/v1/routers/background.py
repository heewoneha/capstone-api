"""Background Routes for the FastAPI application."""

from fastapi import Header, HTTPException, APIRouter
from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from http import HTTPStatus
from app.services.constant import BackgroundType, BACKGROUND_DIR
from app.services.blob import AzureBlobService
from app.services.open_ai import generate_background_image

router = APIRouter(tags=["background"])


class DataRequest(BaseModel):
    text: Optional[str] = None
    image_base64: Optional[str] = None

    @field_validator("text")
    def check_text_length(cls, value):
        if value and len(value) > 120:
            error_message = "Text length exceeds 120 characters."
            raise ValueError(error_message)
        return value


@router.post("/api/submit/background", summary="Submit background data")
async def handle_background_request(payload: DataRequest, x_cd_user_id: str = Header(...)) -> dict:
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")

    BlobService = AzureBlobService()

    if payload.text and payload.image_base64:
        background_type = BackgroundType.TEXT_IMAGE
    elif payload.text:
        background_type = BackgroundType.TEXT
    elif payload.image_base64:
        background_type = BackgroundType.IMAGE
    else:
        background_type = BackgroundType.NONE

    try:
        result_image = generate_background_image(background_type=background_type, text=payload.text, image_base64=payload.image_base64, x_cd_user_id=x_cd_user_id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error generating background image: {str(e)}")

    # Blob process
    try:
        BlobService.upload_base64_image(base64_str=result_image, blob_name=f"{BACKGROUND_DIR}/{user_uuid}.png")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error uploading image to Blob: {str(e)}")

    return {
        "message": "Background Image Data received successfully and saved to Blob.",
        "user_id": str(user_uuid),
        "text_length": len(payload.text) if payload.text else 0,
        "has_image": bool(payload.image_base64)
    }
