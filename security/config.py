from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app_name: str = "Bsale Airline"
    # admin_email: str = "example@email.com"
    is_test_db: bool
    # jwt_secretkey: str
    mysql_user: str
    mysql_password: str
    mysql_host: str
    # password_for_testing: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()