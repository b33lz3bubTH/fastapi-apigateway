from pydantic import BaseSettings


class APPSettings(BaseSettings):
    app_name: str = "FASTGateway"
    admin_email: str = ""
    SECRET_KEY: str = "2e6a61152363616bfc288285124a78e5fba4979636138fa0bbf7ba221ed0f6b8"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    media_path: str = "uploads/"
    thumbnail_path: str = "uploads/thumb/"
    mongo_database_url: str = ""
    mysql_database_url: str = ""
    PORT: int = 8080
    HOST: str = '0.0.0.0'
    thumnail_size = (300,300)

config = APPSettings()
