from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env"
    )

    app_name: str = "bsale airline"
    admin_email: str = "gomez00federico@gmail.com"
    is_test_db: bool
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    # password_for_testing: str


settings = Settings()
