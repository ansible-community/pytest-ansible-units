"""Setup the collection for testing."""


import logging
import os
import sys

from pathlib import Path
from typing import Optional
from typing import Tuple

import pytest
import yaml


logger = logging.getLogger(__name__)


try:
    from ansible.utils.collection_loader._collection_finder import (
        _AnsibleCollectionFinder,
    )

    HAS_COLLECTION_FINDER = True
except ImportError:
    HAS_COLLECTION_FINDER = False


def pytest_configure(config: pytest.Config) -> None:
    """Configure the logger.

    :param config: The pytest configuration object
    """
    level = logging.DEBUG if config.option.verbose > 1 else logging.INFO
    logging.basicConfig(level=level)
    logger.debug("Logging initialized")


def get_collection_name(start_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """Get the collection namespace and name from the galaxy.yml file.

    :param start_path: The path to the root of the collection
    :returns: A tuple of the namespace and name
    """
    info_file = start_path / "galaxy.yml"
    logger.debug("Looking for collection info in %s", info_file)

    try:
        with info_file.open(encoding="utf-8") as fh:
            galaxy_info = yaml.safe_load(fh)
    except FileNotFoundError:
        logger.error("No galaxy.yml file found, plugin not activated")
        return None, None

    try:
        namespace = galaxy_info["namespace"]
        name = galaxy_info["name"]
    except KeyError:
        logger.error("galaxy.yml file does not contain namespace and name")
        return None, None

    logger.debug("galaxy.yml file found, plugin activated")
    logger.debug("Collection namespace: %s", namespace)
    logger.debug("Collection name: %s", name)
    return namespace, name


def pytest_collection(session: pytest.Session) -> None:
    """Prepare for a test session.

    In the case of ansible > 2.9, initialize the collection finder with the collection path
    otherwise, inject the collection path into sys.path.

    :param session: The pytest session object
    """
    start_path = session.startpath
    logger.debug("Start path: %s", start_path)
    namespace, name = get_collection_name(start_path)
    if namespace is None or name is None:
        # Tests may not being run from the root of the repo.
        return

    # Determine if the start_path is in a collections tree
    collection_tree = ("collections", "ansible_collections", namespace, name)
    if start_path.parts[-4:] == collection_tree:
        logger.debug("In collection tree")
        collections_dir = start_path.parents[2]

    else:
        logger.debug("Not in collection tree")
        collections_dir = start_path / "collections"
        name_dir = collections_dir / "ansible_collections" / namespace / name

        # If it's here, we will trust it was from this
        if not name_dir.is_dir():
            os.makedirs(name_dir, exist_ok=True)

            for entry in start_path.iterdir():
                if entry.name == "collections":
                    continue
                os.symlink(entry, name_dir / entry.name)

    logger.debug("Collections dir: %s", collections_dir)

    # TODO: Make this a configuration option, check COLLECTIONS_PATHS
    # Add the user location for any dependencies
    paths = [str(collections_dir), "~/.ansible/collections"]
    logger.debug("Paths: %s", paths)

    if HAS_COLLECTION_FINDER:
        # pylint: disable=protected-access
        _AnsibleCollectionFinder(paths=paths)._install()
    else:
        sys.path.insert(0, str(collections_dir))

    # TODO: Should we install any collection dependencies as well?
    # or let the developer do that?
    # e.g. ansible-galaxy collection install etc
