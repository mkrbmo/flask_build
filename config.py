import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, 'images')
    GEOJSON_FOLDER = os.path.join(UPLOAD_FOLDER, 'geojson')
    SECRET_KEY = "dev"  # replace with environment variable in production
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "blog.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")  # replace with env var in production