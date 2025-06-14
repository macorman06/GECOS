import os

class Config:
    SQLALCHEMY_DATABASE_URI    = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY                 = os.environ.get("SECRET_KEY", "supersecret")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            # nota: el espacio tras -c es importante
            "options": "-c search_path=public"
        }
    }