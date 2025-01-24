from typing import List
import yaml
import uuid
from pydantic import BaseModel, field_validator, Field
from pydantic_settings import BaseSettings
from pathlib import Path
import ast
import secrets


class WatchedFolderConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    path: Path
    name: str
    description: str | None = None


class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "TalkTo Personal API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = False
    API_TOKEN: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Secret API token for authentication",
    )

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # File System Settings
    ALLOWED_EXTENSIONS: List[str] = ["md", "txt", "json"]
    MAX_FILE_SIZE_MB: int = 10

    # Watched Folders Configuration
    WATCHED_FOLDERS: List[WatchedFolderConfig] = []
    WATCHED_FOLDERS_MAP: dict = {}

    @classmethod
    def _load_watched_folders(cls):
        """
        Load watched folders from YAML configuration file.
        Looks for watched_folders.yaml in project root or current directory.
        """
        yaml_paths = [
            Path.cwd() / "watched_folders.yaml",
            Path(__file__).parent.parent.parent / "watched_folders.yaml",
        ]

        for yaml_path in yaml_paths:
            if yaml_path.exists():
                try:
                    with open(yaml_path, "r") as f:
                        config = yaml.safe_load(f)
                        if config and "watched_folders" in config:
                            watched_folders = []
                            for folder in config["watched_folders"]:
                                # Generate UUID if not provided
                                folder_id = folder.get(
                                    "id",
                                    str(uuid.uuid5(uuid.NAMESPACE_URL, folder["path"])),
                                )
                                watched_folder = WatchedFolderConfig(
                                    id=folder_id,
                                    path=Path(folder["path"]),
                                    name=folder["name"],
                                    description=folder.get("description"),
                                )
                                watched_folders.append(watched_folder)
                            return watched_folders
                except Exception as e:
                    print(f"Error loading watched folders from {yaml_path}: {e}")

        return []

    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        if isinstance(v, str):
            try:
                return ast.literal_eval(v)
            except (SyntaxError, ValueError):
                return v.split(",")
        return v

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra environment variables

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load watched folders after initialization
        self.WATCHED_FOLDERS = self._load_watched_folders()
        # Create a map of folder IDs to paths for quick lookup
        self.WATCHED_FOLDERS_MAP = {
            folder.id: folder.path for folder in self.WATCHED_FOLDERS
        }


# Create global settings instance
settings = Settings()
