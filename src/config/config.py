import os
from dotenv import load_dotenv

if os.environ.get("FLASK_ENV") != "production":
    load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://dev_user:dev_pass@localhost:5432/dev_db"
    )

class ProdConfig(Config):
    DEBUG = False
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
    
    # Ensure SECRET_KEY is set in production
    if not os.environ.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY environment variable must be set in production")

def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    if env == "development":
        return DevConfig()
    else:
        return ProdConfig()