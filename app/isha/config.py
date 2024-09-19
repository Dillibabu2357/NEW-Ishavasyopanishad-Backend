from pydantic_settings import BaseSettings, SettingsConfigDict


# Define the Settings class to manage application configuration
# This class inherits from BaseSettings, which provides support for loading settings from environment variables and a .env file
# Refer to https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support for more details
class Settings(BaseSettings):
    db_url: str

    # Test Database Config
    test_db_url: str

    # JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    # Configuration for Pydantic Settings
    # The env_file parameter specifies the .env file to load the environment variables from
    model_config = SettingsConfigDict(env_file="isha.env")


# Instantiate the Settings class
# This will load the configuration from the environment variables and the specified .env file
settings = Settings()
