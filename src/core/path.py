from pathlib import Path


def get_root_directory() -> Path:
    # Locate base directory
    root = Path(__file__).resolve().parent.parent.parent

    return root


def get_data_path() -> Path:
    # Locate base directory
    root = get_root_directory()
    # Define the path of data directory
    dir = root / "data"
    dir.mkdir(parents=True, exist_ok=True)

    return dir
