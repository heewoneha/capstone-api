"""Service to run the model and generate animations from images."""

import os
from moviepy import VideoFileClip
from app.services.examples.image_to_annotations import image_to_annotations
from app.services.examples.annotations_to_animation import annotations_to_animation
from app.services.constant import LOCAL_PATH, BACKGROUND_DIR, CHARACTER_DIR, SOURCE_DIR, MODEL_RESULT_DIR, DanceName


def delete_tmp_files(user_uuid: str) -> None:
    """Delete temporary files for the given user UUID.

    Args:
        user_uuid (str): The user UUID for which to delete temporary files.
    """
    background_img_path = os.path.join(SOURCE_DIR, BACKGROUND_DIR, f"{user_uuid}.png")
    character_img_path = os.path.join(SOURCE_DIR, CHARACTER_DIR, f"{user_uuid}.png")
    char_anno_dir = os.path.join(MODEL_RESULT_DIR, user_uuid)
    model_result_gif_path = os.path.join(MODEL_RESULT_DIR, f"{user_uuid}.gif")
    model_result_mp4_path = os.path.join(MODEL_RESULT_DIR, f"{user_uuid}.mp4")
    
    if os.path.exists(background_img_path):
        os.remove(background_img_path)
    if os.path.exists(character_img_path):
        os.remove(character_img_path)
    if os.path.exists(char_anno_dir):
        os.rmdir(char_anno_dir)
    if os.path.exists(model_result_gif_path):
        os.remove(model_result_gif_path)
    if os.path.exists(model_result_mp4_path):
        os.remove(model_result_mp4_path)


def image_to_animation(user_uuid: str, dance_name: DanceName) -> tuple[str, str]:
    # TODO: apply the background_img_path to the model
    background_img_path = os.path.join(SOURCE_DIR, BACKGROUND_DIR, f"{user_uuid}.png")
    character_img_path = os.path.join(SOURCE_DIR, CHARACTER_DIR, f"{user_uuid}.png")

    if not os.path.exists(background_img_path) or not os.path.exists(character_img_path):
        error_message = f"One or more source images not found for user_uuid={user_uuid}"
        raise FileNotFoundError(error_message)

    char_anno_dir = os.path.join(MODEL_RESULT_DIR, user_uuid)
    motion_cfg_fn = os.path.join(LOCAL_PATH, "examples", "config", "motion", f"{dance_name.value}.yaml")
    retarget_cfg_fn = os.path.join(LOCAL_PATH, "examples", "config", "retarget", f"{dance_name.value}.yaml")

    try:
        image_to_annotations(img_fn=character_img_path, out_dir=char_anno_dir)
    except Exception as e:
        error_message = f"Error occurred while creating annotations - Exception={e}"
        raise Exception(error_message)
    
    try:
        annotations_to_animation(char_anno_dir=char_anno_dir, motion_cfg_fn=motion_cfg_fn, retarget_cfg_fn=retarget_cfg_fn)
    except Exception as e:
        error_message = f"Error occurred while creating animations - Exception={e}"
        raise Exception(error_message)

    result_gif_path = os.path.join(MODEL_RESULT_DIR, user_uuid, "video.gif")
    result_mp4_path = os.path.join(MODEL_RESULT_DIR, user_uuid, "video.mp4")
    
    try:
        clip = VideoFileClip(result_gif_path)
        clip.write_videofile(result_mp4_path, codec="libx264", fps=30)
    except Exception as e:
        error_message = f"Error occurred while converting GIF to MP4 - Exception={e}"
        raise Exception(error_message)

    if os.path.exists(result_gif_path) and os.path.exists(result_mp4_path):
        return result_gif_path, result_mp4_path
    else:
        error_message = f"Error occurred - GIF or MP4 file not found for user_uuid={user_uuid}"
        raise Exception(error_message)

