"""Generates the primary key of a record about to be stored."""

from pathlib import Path
from repository.repository import Repository


def make_pk(repository: Repository, path: Path) -> str:
    """Builds the primary key following the ones already stored.

    The key is derived from the number of stored records.

    Args:
        repository (Repository): The repository to count the records of.
        path (Path): The JSON file holding the records.

    Returns:
        str: The primary key of the next record.
    """
    models = repository.get_raw_models(path)
    return str(len(models) + 1)
