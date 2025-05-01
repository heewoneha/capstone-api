"""Routes for the FastAPI application."""

from fastapi import Header, HTTPException, APIRouter
from uuid import UUID
from http import HTTPStatus
from app.services.constant import DanceName, RESULT_DIR
from app.services.blob import AzureBlobService

router = APIRouter(tags=["model"])

@router.post("/api/model", summary="Run the model using the saved background and character images")
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


@router.get("/api/result/{dance_name}", summary="Return result data")
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
