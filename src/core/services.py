from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class IFileSystemService(ABC):
    @abstractmethod
    async def list_directory(self, path: str) -> List[dict]:
        pass

class FileSystemService(IFileSystemService):
    async def list_directory(self, path: str) -> List[dict]:
        directory = Path(path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory {path} does not exist")
        
        return [
            {
                "name": item.name,
                "is_file": item.is_file(),
                "is_dir": item.is_dir()
            }
            for item in directory.iterdir()
        ]