from pathlib import Path
from typing import List

def validate_path(path: str) -> bool:
    """Validate if a path is safe to access."""
    try:
        Path(path).resolve()
        return True
    except (RuntimeError, ValueError):
        return False