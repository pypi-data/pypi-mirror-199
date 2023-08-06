from core.conf.base_settings import BaseConfig


class Seetings(BaseConfig):
    DEBUG = True
    
    API_V1_STR:str = "/api/v1"
    
    # Choose a Password Hasher Default is bcrypt
    # "sha256_crypt", "md5_crypt", "bcrypt", "pbkdf2_sha256","pbkdf2_sha512"
    PASSWORD_HASHER = "bcrypt"

    # Change the Database URL to your used DB
    DATABASE_URL = "sqlite:///db.sqlite"
    {% if cookiecutter.database_orm == "TortoiseORM" %}
    APP_MODELS = []
    {% endif %}


settings = Seetings()
