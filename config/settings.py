class Settings:
    environment: str = "dev"

    mongo_url: str = "mongodb://localhost:27017/coordinator"


settings = Settings()
