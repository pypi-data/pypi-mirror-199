from enum import Enum, EnumMeta


class BaseMetadataEnum(EnumMeta):
    def __contains__(self, other):
        try:
            self(other)
        except ValueError:
            return False
        else:
            return True


class BaseEnum(str, Enum, metaclass=BaseMetadataEnum):
    """Base enum class."""


class PackageManager(BaseEnum):
    PIP = "pip"
    POETRY = "poetry"

    def __str__(self) -> str:
        return self.value


class PythonVersion(BaseEnum):
    THREE_DOT_SEV = "3.7"
    THREE_DOT_EIG = "3.8"
    THREE_DOT_NIN = "3.9"
    THREE_DOT_TEN = "3.10"
    THREE_DOT_ELE = "3.11"

    def __str__(self) -> str:
        return self.value


class License(BaseEnum):
    MIT = "MIT"
    BSD = "BSD"
    GNU = "GNU"
    APACHE = "Apache"

    def __str__(self) -> str:
        return self.value


class Database(BaseEnum):
    POSTGRES = "Postgres"
    MYSQL = "MySQL"
    SQLITE = "SQLite"

    def __str__(self) -> str:
        return self.value


class DatabaseORM(BaseEnum):
    TORTOISE = "TortoiseORM"
    SQLALCHEMY = "SQLAlchemy"
    
    
    def __str__(self) -> str:
        return self.value
