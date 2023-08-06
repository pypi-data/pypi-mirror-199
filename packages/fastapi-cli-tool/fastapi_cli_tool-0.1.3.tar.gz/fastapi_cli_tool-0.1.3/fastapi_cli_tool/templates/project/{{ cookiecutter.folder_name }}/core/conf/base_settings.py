from datetime import timedelta
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, DirectoryPath, EmailStr


class BaseConfig(BaseSettings):
    DEBUG = False
    # Local time zone for this installation. All choices can be found here:
    # https://en.wikipedia.org/wiki/List_of_tz_zones_by_name (although not all
    # systems may support all possibilities). When USE_TZ is True, this is
    # interpreted as the default user time zone.
    TIME_ZONE = "Europe/Berlin"

    # If you set this to True, FAST API will use timezone-aware datetimes.
    USE_TZ: bool = False

    USE_DEPRECATED_PYTZ: bool = False

    # Hosts/domain names that are valid for this site.
    # "*" matches anything, ".example.com" matches example.com and all subdomains
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: EmailStr = "fastAPI@mail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = "FastAPI App"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_FOLDER: Optional[DirectoryPath] = None

    PROJECT_NAME = "{{ cookiecutter.name}}"
    PROJECT_VERSION = "0.0.1"

    # Choose a Password Hasher Default is bcrypt
    # "sha256_crypt", "md5_crypt", "bcrypt", "pbkdf2_sha256","pbkdf2_sha512"
    PASSWORD_HASHER = "bcrypt"

    JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
        "ALGORITHM": "HS256",
        "JWT_SECRET_KEY": "SUPER_SECRET_KEY",
        "JWT_REFRESH_SECRET_KEY": "SUPER_SECRET_KEY",
    }
