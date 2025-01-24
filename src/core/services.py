import os
import asyncio
import secrets
from pathlib import Path
from typing import List, Dict, Union
from ..core.config import settings
from ..utils.helpers import validate_path, normalize_path


class AuthService:
    async def validate_token(self, token: str) -> bool:
        """
        Validate the provided API token using constant-time comparison.

        Args:
            token (str): The token to validate

        Returns:
            bool: True if token is valid, False otherwise
        """
        return secrets.compare_digest(token, settings.API_TOKEN)


class FileSystemService:
    async def list_directory(self, path: str) -> List[Dict[str, Union[str, int]]]:
        """
        List contents of a directory with additional metadata.

        Args:
            path (str): Path to the directory to list

        Returns:
            List of dictionaries containing file/directory information
        """
        full_path = Path(path)

        if not validate_path(str(full_path)):
            raise ValueError("Invalid path or path outside of allowed directory")

        if not full_path.exists() or not full_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {path}")

        contents = []
        # Fix: Properly await the to_thread calls
        it = await asyncio.to_thread(os.scandir, full_path)
        entries = await asyncio.to_thread(list, it)

        for entry in entries:
            try:
                stat = entry.stat()
                contents.append(
                    {
                        "name": entry.name,
                        "type": "directory" if entry.is_dir() else "file",
                        "size": stat.st_size if entry.is_file() else 0,
                        "modified": stat.st_mtime,
                    }
                )
            except (PermissionError, FileNotFoundError):
                continue

        return contents

    async def get_directory_structure(
        self, base_path: Path
    ) -> Dict[str, Union[str, List]]:
        """
        Recursively get directory structure.

        Args:
            base_path (Path): Root path to start scanning

        Returns:
            Nested dictionary representing directory structure
        """

        def _get_structure(path: Path) -> Dict[str, Union[str, List]]:
            structure = {"name": path.name, "type": "directory", "children": []}

            for item in path.iterdir():
                if item.is_dir():
                    structure["children"].append(_get_structure(item))
                else:
                    structure["children"].append(
                        {"name": item.name, "type": "file", "size": item.stat().st_size}
                    )

            return structure

        return _get_structure(base_path)

    async def get_file_content(self, file_path: Path) -> str:
        """
        Read file content.

        Args:
            file_path (Path): Path to the file

        Returns:
            File content as string
        """
        if not validate_path(str(file_path)):
            raise ValueError("Invalid file path")

        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check file extension
        if file_path.suffix.lstrip(".") not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )

        chunk_size = 8192  # 8KB chunks
        content = []

        async with asyncio.to_thread(open, file_path, "r") as file:
            while chunk := await asyncio.to_thread(file.read, chunk_size):
                content.append(chunk)

        return "".join(content)

    async def create_file(self, file_path: Path, content: str) -> bool:
        """
        Create a new file with given content.

        Args:
            file_path (Path): Path to create the file
            content (str): Content to write to the file

        Returns:
            Boolean indicating success
        """
        # Normalize the path to prevent traversal
        normalized_path = normalize_path(str(file_path))

        if not validate_path(str(normalized_path)):
            raise ValueError("Invalid file path")

        # Ensure parent directory exists
        normalized_path.parent.mkdir(parents=True, exist_ok=True)

        # Check file extension
        if normalized_path.suffix.lstrip(".") not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )

        async with asyncio.to_thread(open, normalized_path, "w") as file:
            await asyncio.to_thread(file.write, content)

        return True

    async def batch_create_files(
        self, files: List[Dict[str, Union[Path, str]]]
    ) -> List[bool]:
        results = []
        for file_info in files:
            try:
                result = await self.create_file(file_info["path"], file_info["content"])
                results.append(result)
            except Exception:
                results.append(False)
        return results

    async def update_file(self, file_path: Path, content: str) -> bool:
        """
        Update an existing file with new content.

        Args:
            file_path (Path): Path to the file
            content (str): New content to write

        Returns:
            Boolean indicating success
        """
        # Normalize the path to prevent traversal
        normalized_path = normalize_path(str(file_path))

        if not validate_path(str(normalized_path)):
            raise ValueError("Invalid file path")

        if not normalized_path.is_file():
            raise FileNotFoundError(f"File not found: {normalized_path}")

        # Check file extension
        if normalized_path.suffix.lstrip(".") not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )

        async with asyncio.to_thread(open, normalized_path, "w") as file:
            await asyncio.to_thread(file.write, content)

        return True

    async def delete_file(self, file_path: Path) -> bool:
        """
        Delete a file.

        Args:
            file_path (Path): Path to the file to delete

        Returns:
            Boolean indicating success
        """
        # Normalize the path to prevent traversal
        normalized_path = normalize_path(str(file_path))

        if not validate_path(str(normalized_path)):
            raise ValueError("Invalid file path")

        if not normalized_path.is_file():
            raise FileNotFoundError(f"File not found: {normalized_path}")

        # Check file extension
        if normalized_path.suffix.lstrip(".") not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
            )

        await asyncio.to_thread(os.remove, normalized_path)
        return True
