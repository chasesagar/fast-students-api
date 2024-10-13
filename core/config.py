from pydantic.v1 import BaseSettings


class __Settings(BaseSettings):
    """
    Settings class to store environment variables

    """
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    google_api_key: str
    here_maps_api_key: str

    class Config:
        env_file = ".env"

    _instance = None

    @classmethod
    def get_instance(cls) -> "__Settings":
        """
        Singleton pattern to avoid multiple instances of the class

        Returns:
            __Settings: instance of the class
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

settings = __Settings.get_instance()
