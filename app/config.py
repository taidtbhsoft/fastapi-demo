from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_name: str
    database_username: str
    database_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int = 60
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: str
    mail_server: str
    mail_from_name: str

    class Config:
        env_file = ".env"


settings = Settings()