from typing import List
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path

class WatchedFolderConfig(BaseModel):
    path: Path
    name: str
    description: str | None = None

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "Monica File System API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # File System Settings
    BASE_PATH: Path = Path.home()  # Default to user's home directory
    ALLOWED_EXTENSIONS: List[str] = ["md", "txt", "json"]
    MAX_FILE_SIZE_MB: int = 10
    
    # Watched Folders Configuration
    WATCHED_FOLDERS: List[WatchedFolderConfig] = []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()