from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    vonage_api_secret: str
    vonage_api_key: str
    vonage_application_id: str
    vonage_private_key_path: str
    vonage_virtual_number: str
    ngrok_url: str
    your_phone_number: str
    your_name: str
    app_name: str = "Customer Service Call Flow API"
    app_host: str = "0.0.0.0"
    app_port: int = 3000
    database_path: str = "./customer_calls.db"

    class Config:
        env_file = ".env"


settings = Settings()
