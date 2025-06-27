from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    calendar_id: str = "ankitkumaraurangabad3@gmail.com"  # e.g. primary
    credentials_file: str = "credentials.json"       # service account file

settings = Settings()
#jhhdhjndhfvn
