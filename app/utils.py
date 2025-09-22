import os
import shutil
from flask import current_app
from werkzeug.utils import secure_filename


def clear_post_images(post_id: int):
    img_dir = os.path.join(current_app.static_folder, "uploads", "images", str(post_id))
    if os.path.exists(img_dir):
        for filename in os.listdir(img_dir):
            file_path = os.path.join(img_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(img_dir, exist_ok=True)


def replace_geojson_file(post_id: int, geojson_file):
    geo_dir = os.path.join(current_app.static_folder, "uploads", "geojson")
    os.makedirs(geo_dir, exist_ok=True)

    filename = f"post_{post_id}.geojson"
    file_path = os.path.join(geo_dir, filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    geojson_file.save(file_path)
    return f"uploads/geojson/{filename}"