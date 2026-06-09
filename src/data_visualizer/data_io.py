from pathlib import Path

import pandas as pd

from .config import DATA_DIR, MAX_UPLOAD_SIZE_MB


def get_default_files(data_dir: Path = DATA_DIR) -> list[str]:
    if not data_dir.exists():
        return []
    return sorted(path.name for path in data_dir.glob("*.csv"))


def load_default_csv(file_name: str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return pd.read_csv(data_dir / file_name)


def validate_uploaded_size(size_bytes: int, max_mb: int = MAX_UPLOAD_SIZE_MB) -> None:
    size_mb = size_bytes / (1024 * 1024)
    if size_mb > max_mb:
        raise ValueError(f"Uploaded file is {size_mb:.1f} MB. Limit is {max_mb} MB.")


def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    validate_uploaded_size(uploaded_file.size)
    return pd.read_csv(uploaded_file)
