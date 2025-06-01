"""Character Routes for the FastAPI application."""

from fastapi import UploadFile, File, Header, HTTPException, APIRouter
from uuid import UUID
from http import HTTPStatus
from app.services.constant import CHARACTER_DIR, IMAGE_CONTENT_TYPE_EXTENSION_MAP
from app.services.blob import AzureBlobService, character_white_background

router = APIRouter(tags=["character"])


@router.post("/api/submit/character", summary="Submit character data")
async def handle_character_request(image_file: UploadFile = File(...), x_cd_user_id: str = Header(...)) -> dict:
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")

    if image_file.content_type not in IMAGE_CONTENT_TYPE_EXTENSION_MAP:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Only PNG images are allowed")
    
    extension = IMAGE_CONTENT_TYPE_EXTENSION_MAP[image_file.content_type]
    image_bytes = await image_file.read()

    try:
        white_bg_image_bytes = character_white_background(image_bytes=image_bytes)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error processing image: {str(e)}")

    BlobService = AzureBlobService()
    try:
        BlobService.upload_binary_image(binary_data=white_bg_image_bytes, blob_name=f"{CHARACTER_DIR}/{user_uuid}.{extension}")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error uploading image to Blob: {str(e)}")

    return {
        "message": "Character Image Data received successfully and saved to Blob.",
        "user_id": str(user_uuid),
    }
