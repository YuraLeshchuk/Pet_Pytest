from pathlib import Path


def get_project_root() -> Path:
    """
    Returns absolute path to project root directory
    """
    return Path(__file__).resolve().parents[1]
