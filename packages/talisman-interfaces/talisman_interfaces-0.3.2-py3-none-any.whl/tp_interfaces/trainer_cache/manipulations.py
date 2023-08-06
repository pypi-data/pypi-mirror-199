import logging
import os
from datetime import datetime
from pathlib import Path
from pickle import PickleError
from typing import Iterable, Optional, Type, TypeVar

from tp_interfaces.abstract.processor.trainer import DEFAULT_CACHE_DIR
from tp_interfaces.trainer_cache.base import Cache

logger = logging.getLogger(__name__)
HASH_DIR_LENGTH = 5

_Cache = TypeVar('_Cache', bound=Cache)


def hash_to_dir(cache_hash: str, cache_dir: Path = DEFAULT_CACHE_DIR) -> Path:
    cache_dir = cache_dir.joinpath(cache_hash[-HASH_DIR_LENGTH:])
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def load_cache(cache_class: Type[_Cache], cache_dir: Path = DEFAULT_CACHE_DIR) -> Iterable[_Cache]:
    """Loads all caches of class `cache_class` from given directory."""
    for path in cache_dir.rglob('*.pkl'):
        try:
            yield cache_class.load(path)
        except (PickleError, OSError, EOFError):
            continue


def find_cache(cache_class: Type[_Cache], config: dict, cache_dir: Path = DEFAULT_CACHE_DIR) -> Optional[_Cache]:
    """Looks for suitable hash in `cache_dir`/<hash>/ directory"""
    cache_dir = hash_to_dir(str(cache_class.get_hash(config)), cache_dir)
    for cache in load_cache(cache_class, cache_dir):
        if cache.matches(config):
            logger.info(f'Loaded cache from {cache.path}')
            return cache


def save_cache(cache: Cache, cache_dir: Path = DEFAULT_CACHE_DIR):
    """Saves cache at `cache_dir`/<hash>/ directory. Rewrites any old caches."""
    cache_dir = hash_to_dir(str(cache.precomputed_hash), cache_dir)

    # look for the same caches
    for old_cache in load_cache(cache.__class__, cache_dir):
        if cache.matches(old_cache.trainer_config, compare_revisions=False) and old_cache.path is not None:
            try:
                os.remove(old_cache.path)
                logger.info(f'Removed old cache at {old_cache.path}')
            except OSError as e:
                logger.error(f'Failed to remove old cache at {old_cache.path}!', exc_info=e)

    cache_filename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    cache_file = cache_dir.joinpath(cache_filename + '.pkl')

    file_version = 1
    while cache_file.exists():
        cache_file = cache_dir.joinpath(cache_filename + f'_{file_version}.pkl')
        file_version += 1

    try:
        cache.save(cache_file)
        logger.info(f'Saved cache to {cache_file}')
    except (PickleError, OSError, EOFError) as e:
        logger.error(f'Failed to save cache to {cache_file}!', exc_info=e)
