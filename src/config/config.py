import os

if os.environ.get("FLASK_ENV") != "production" and os.environ.get("FLASK_ENV") != None:
    from dotenv import load_dotenv
    load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://dev_user:dev_pass@localhost:5432/flask_db"


class ProdConfig(Config):
    DEBUG = False
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = "postgresql://dev_user:dev_pass@localhost:5432/flask_db"
    
    if not os.environ.get("SECRET_KEY"):
        raise ValueError("SECRET_KEY environment variable must be set in production")


def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    if env == "development":
        return DevConfig()
    else:
        return ProdConfig()