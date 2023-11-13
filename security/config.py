from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "bsale airline"
    admin_email: str = "gomez00federico@gmail.com"
    is_test_db: bool
    # jwt_secretkey: str
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    # password_for_testing: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()