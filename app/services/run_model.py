"""Service to run the model and generate animations from images."""

import os
import imageio
import shutil
from PIL import Image
from moviepy import VideoFileClip
from app.services.examples.image_to_annotations import image_to_annotations
from app.services.examples.annotations_to_animation import annotations_to_animation
from app.services.constant import VIDEO_CODEC, VIDEO_FPS, LOCAL_PATH, BACKGROUND_DIR, CHARACTER_DIR, MODEL_SOURCE_DIR, MODEL_RESULT_DIR, DanceName


def delete_tmp_source_files(user_uuid: str) -> None:
    """Delete temporary source files for the given user UUID.

    Args:
        user_uuid (str): The user UUID for which to delete temporary source files.
    """
    background_img_path = os.path.join(MODEL_SOURCE_DIR, BACKGROUND_DIR, f"{user_uuid}.png")
    character_img_path = os.path.join(MODEL_SOURCE_DIR, CHARACTER_DIR, f"{user_uuid}.png")

    if os.path.exists(background_img_path):
        os.remove(background_img_path)
    if os.path.exists(character_img_path):
        os.remove(character_img_path)

def delete_tmp_result_files(user_uuid: str) -> None:
    """Delete temporary result files for the given user UUID.

    Args:
        user_uuid (str): The user UUID for which to delete temporary result files.
    """
    char_anno_dir = os.path.join(MODEL_RESULT_DIR, user_uuid)
    
    if os.path.exists(char_anno_dir):
        shutil.rmtree(char_anno_dir)

def apply_background_image(background_img_path: str, result_character_gif_path: str) -> None:
    """Apply a background image to the character GIF.

    Args:
        background_img_path (str): Path to the background image.
        result_character_gif_path (str): Path to the character GIF.
    """
    background = Image.open(background_img_path).convert("RGBA")
    bg_width, bg_height = background.size

    reader = imageio.get_reader(result_character_gif_path)
    fps = reader.get_meta_data()['duration']

    frames = []

    for id, frame in enumerate(reader):
        if id == 0:
            continue
        frame_image = Image.fromarray(frame).convert("RGBA")
        fg_width, fg_height = frame_image.size

        composed = background.copy()
        paste_x = (bg_width - fg_width) // 2
        paste_y = (bg_height - fg_height) // 2
        composed.paste(frame_image, (paste_x, paste_y), frame_image)
        frames.append(composed)

    frames[0].save(
        result_character_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=fps,
        loop=0
    )

def image_to_animation(user_uuid: str, dance_name: DanceName) -> tuple[str, str]:
    """Convert images to animation.

    Args:
        user_uuid (str): The user UUID.
        dance_name (DanceName): The name of the dance.
    Returns:
        tuple[str, str]: Paths to the generated GIF and MP4 files.
    """
    background_img_path = os.path.join(MODEL_SOURCE_DIR, BACKGROUND_DIR, f"{user_uuid}.png")
    character_img_path = os.path.join(MODEL_SOURCE_DIR, CHARACTER_DIR, f"{user_uuid}.png")

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

    try:
        result_gif_path = os.path.join(MODEL_RESULT_DIR, user_uuid, "video.gif")
        apply_background_image(background_img_path=background_img_path, result_character_gif_path=result_gif_path)
    except Exception as e:
        error_message = f"Error occurred while applying background image - Exception={e}"
        raise Exception(error_message)

    try:
        result_mp4_path = os.path.join(MODEL_RESULT_DIR, user_uuid, "video.mp4")
        clip = VideoFileClip(result_gif_path)
        clip.write_videofile(result_mp4_path, codec=VIDEO_CODEC, fps=VIDEO_FPS)
    except Exception as e:
        error_message = f"Error occurred while converting GIF to MP4 - Exception={e}"
        raise Exception(error_message)

    if os.path.exists(result_gif_path) and os.path.exists(result_mp4_path):
        return result_gif_path, result_mp4_path
    else:
        error_message = f"Error occurred - GIF or MP4 file not found for user_uuid={user_uuid}"
        raise Exception(error_message)
