"""Setup the collection for testing."""


import os
import sys

from pathlib import Path
from typing import Optional
from typing import Tuple

import pytest
import yaml


try:
    from ansible.utils.collection_loader._collection_finder import (
        _AnsibleCollectionFinder,
    )

    HAS_COLLECTION_FINDER = True
except ImportError:
    HAS_COLLECTION_FINDER = False


def get_collection_name(start_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """Get the collection namespace and name from the galaxy.yml file.

    :param startpath: The path to the root of the collection.
    """
    info_file = start_path / "galaxy.yml"

    try:
        with info_file.open(encoding="utf-8") as fh:
            galaxy_info = yaml.safe_load(fh)
    except FileNotFoundError:
        return None, None

    return galaxy_info["namespace"], galaxy_info["name"]


def pytest_collection(session: pytest.Session) -> None:
    """Prepare for a test session.

    In the case of ansible > 2.9, initialize the collection finder with the collection path
    otherwise, inject the collection path into sys.path.

    """
    start_path = session.startpath
    namespace, name = get_collection_name(start_path)
    if namespace is None or name is None:
        # Tests may not being run from the root of the repo.
        return

    collections_dir = start_path / "collections"
    name_dir = collections_dir / "ansible_collections" / namespace / name

    # If it's here, we will trust it was from this
    if not name_dir.is_dir():
        os.makedirs(name_dir, exist_ok=True)

        for entry in start_path.iterdir():
            if entry.name == "collections":
                continue
            os.symlink(entry, name_dir / entry.name)

    # TODO: Make this a configuration option, check COLLECTIONS_PATHS
    # Add the user location for any dependencies
    paths = [str(collections_dir), "~/.ansible/collections"]

    if HAS_COLLECTION_FINDER:
        # pylint: disable=protected-access
        _AnsibleCollectionFinder(paths=paths)._install()
    else:
        sys.path.insert(0, str(collections_dir))
