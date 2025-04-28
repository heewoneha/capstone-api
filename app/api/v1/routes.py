"""Routes for the FastAPI application."""

from fastapi import UploadFile, File, FastAPI, Header, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from http import HTTPStatus
from app.api.v1.constant import (
    BackgroundType,
    BACKGROUND_DIR,
    CHARACTER_DIR,
    CHARACTER_CONTENT_TYPE_EXTENSION_MAP,
    DanceName,
    RESULT_DIR,
)

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
async def handle_background_request(payload: DataRequest, x_cd_user_id: str = Header(...)) -> dict:
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")

    if not payload.text and not payload.image_base64:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="At least one of text or image is required")

    BlobService = AzureBlobService()

    if payload.text and payload.image_base64:
        background_type = BackgroundType.TEXT_IMAGE
    elif payload.text:
        background_type = BackgroundType.TEXT
    elif payload.image_base64:
        background_type = BackgroundType.IMAGE
    else:
        background_type = BackgroundType.NONE

    # TODO: Open AI process
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
        "message": "Background Image Data received successfully and saved to Blob.",
        "user_id": str(user_uuid),
        "text_length": len(payload.text) if payload.text else 0,
        "has_image": bool(payload.image_base64)
    }


@app.post("/api/submit/character", summary="Submit character data")
async def handle_character_request(image_file: UploadFile = File(...), x_cd_user_id: str = Header(...)) -> dict:
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")

    if image_file.content_type not in CHARACTER_CONTENT_TYPE_EXTENSION_MAP:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Only PNG images are allowed")
    
    extension = CHARACTER_CONTENT_TYPE_EXTENSION_MAP[image_file.content_type]
    image_bytes = await image_file.read()

    BlobService = AzureBlobService()
    try:
        BlobService.upload_binary_image(binary_data=image_bytes, blob_name=f"{CHARACTER_DIR}/{user_uuid}.{extension}")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error uploading image to Blob: {str(e)}")

    return {
        "message": "Character Image Data received successfully and saved to Blob.",
        "user_id": str(user_uuid),
    }


@app.post("/api/model", summary="Run the model using the saved background and character images")
async def handle_model_request(x_cd_user_id: str = Header(...)):
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")
    
    # TODO: Save the background and character images in the local directory

    # TODO: Run AnimatedDrawings model

    # TODO: Save all model results to blob storage

    return {
        "message": "Model has been executed successfully.",
        "user_id": str(user_uuid),
    }


@app.get("/api/result/{dance_name}", summary="Return result data")
async def handle_result_request(dance_name: DanceName, x_cd_user_id: str = Header(...)):
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")
    
    try:
        BlobService = AzureBlobService()
        result_image_bytes = BlobService.get_result_image(blob_name=f"{RESULT_DIR}/{dance_name}/{user_uuid}.gif")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error retrieving image from Blob: {str(e)}")

    return {
        "message": "Dance result image retrieved successfully.",
        "result_image_bytes": result_image_bytes,
        "user_id": str(user_uuid)
    }
