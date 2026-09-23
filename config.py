from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ngrok_url: str
    app_name: str = "Pug Information Line"
    app_host: str = "0.0.0.0"
    app_port: int = 3000

    class Config:
        env_file = ".env"


settings = Settings()
