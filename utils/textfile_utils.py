import ast

from utils.logger import Logger
from utils.path_utils import get_project_root

DATA_DIR = get_project_root() / "test_data"
DATA_DIR.mkdir(exist_ok=True)


def read_dict_from_text_file(file_name: str) -> dict:
    file_path = DATA_DIR / file_name

    Logger.checkpoint(f"Read dictionary from text file {file_path}")

    if not file_path.exists():
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        return ast.literal_eval(f.read())


def save_dict_to_text_file(file_name: str, dict_data: dict) -> None:
    file_path = DATA_DIR / file_name

    Logger.checkpoint(f"Save dictionary {dict_data} to text file {file_path}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(dict_data))
