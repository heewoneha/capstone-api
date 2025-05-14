"""Routes for the FastAPI application."""

from fastapi import Header, HTTPException, APIRouter
from uuid import UUID
from http import HTTPStatus
from app.services.constant import DanceName, BACKGROUND_DIR, CHARACTER_DIR, RESULT_DIR, MODEL_SOURCE_DIR, MODEL_RESULT_DIR
from app.services.blob import AzureBlobService
from app.services.run_model import delete_tmp_result_files, delete_tmp_source_files, image_to_animation

router = APIRouter(tags=["model"])


@router.post("/api/model", summary="Run the model using the saved background and character images")
async def handle_model_request(x_cd_user_id: str = Header(...)):
    try:
        user_uuid = UUID(x_cd_user_id)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid UUID format for the user ID")
    
    BlobService = AzureBlobService()

    try:
        BlobService.get_result_image(save_path=f"{MODEL_SOURCE_DIR}/{BACKGROUND_DIR}/{user_uuid}.png", blob_name=f"{BACKGROUND_DIR}/{user_uuid}.png")
        BlobService.get_result_image(save_path=f"{MODEL_SOURCE_DIR}/{CHARACTER_DIR}/{user_uuid}.png", blob_name=f"{CHARACTER_DIR}/{user_uuid}.png")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error downloading images from Blob: {str(e)}")

    try:
        for dance_name in DanceName:
            image_to_animation(
                user_uuid=user_uuid,
                dance_name=dance_name,
            )
            BlobService.upload_file(file_path=f"{MODEL_RESULT_DIR}/{user_uuid}/video.gif", blob_name=f"{RESULT_DIR}/{dance_name.value}/{user_uuid}.gif")
            BlobService.upload_file(file_path=f"{MODEL_RESULT_DIR}/{user_uuid}/video.mp4", blob_name=f"{RESULT_DIR}/{dance_name.value}/{user_uuid}.mp4")
            delete_tmp_result_files(user_uuid=user_uuid)
        delete_tmp_source_files(user_uuid=user_uuid)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Error processing model - dance_name={dance_name}: {str(e)}")

    return {
        "message": "Model has been executed successfully.",
        "user_id": str(user_uuid),
    }
