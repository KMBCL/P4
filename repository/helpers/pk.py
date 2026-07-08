from pathlib import Path
from repository.repository import Repository


def make_pk(repository: Repository, path: Path) -> str:
    models = repository.get_raw_models(path)
    return str(len(models) + 1)
