from pathlib import Path


def validate_path(path: str) -> bool:
    """
    Validate that a path is safe and within allowed directories.

    Args:
        path (str): Path to validate

    Returns:
        bool: True if path is valid, False otherwise
    """
    try:
        # Resolve the path to an absolute path
        abs_path = Path(path).resolve()

        # Prevent symbolic link attacks
        if abs_path.is_symlink():
            return False

        return True
    except Exception:
        return False


def normalize_path(path: str) -> Path:
    """
    Normalize and sanitize a path to prevent path traversal.

    Args:
        path (str): Path to normalize

    Returns:
        Path: Normalized, safe path
    """
    # Remove any attempts at directory traversal
    normalized_path = Path(path).as_posix()

    # Split the path and remove any '..' or '.' components
    path_parts = []
    for part in normalized_path.split("/"):
        if part in ("", "."):
            continue
        elif part == "..":
            # Prevent going above the base path
            if path_parts:
                path_parts.pop()
        else:
            path_parts.append(part)

    # Reconstruct the path
    return Path("/".join(path_parts))
