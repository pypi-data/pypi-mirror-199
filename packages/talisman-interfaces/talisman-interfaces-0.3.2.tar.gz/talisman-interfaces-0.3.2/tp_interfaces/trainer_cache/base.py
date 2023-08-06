import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple

from jsonpath_ng import JSONPath, parse

from tp_interfaces.abstract.model.model import Picklable


def get_git_revision_hash() -> str:
    # stolen from https://stackoverflow.com/a/21901260
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()


def make_hashable(x):
    if isinstance(x, dict):
        return frozenset((k, make_hashable(v)) for k, v in x.items())
    if isinstance(x, set):
        return frozenset(x)
    if isinstance(x, Iterable) and not isinstance(x, str):
        return tuple(map(make_hashable, x))
    return x


@dataclass(frozen=True)
class Cache(Picklable):
    trainer_config: dict
    git_revision: str = field(default=None, init=False)
    match_fields: Tuple[Tuple[str, Any], ...] = field(default=(('$', None),), init=False)  # pairs of (jsonpath pattern, default value)
    match_env: Tuple[Tuple[str, str], ...] = field(default=tuple(os.environ.items()), init=False)  # pairs of (var name, default var value)
    path: Optional[Path] = field(init=False)
    precomputed_hash: Optional[int] = field(init=False)

    def __post_init__(self):
        current_envs = []
        for env_name, default_env_value in self.match_env:
            current_envs.append((env_name, os.environ.get(env_name, default_env_value)))

            # fill in current git revision
            object.__setattr__(self, 'git_revision', get_git_revision_hash())
            object.__setattr__(self, 'precomputed_hash', self.get_hash(self.trainer_config))

    @staticmethod
    def _find_matches(expression: JSONPath, json_dict: dict, *, default: Any = None) -> set:
        value_matches = {make_hashable(match.value) for match in expression.find(json_dict)}
        if not len(value_matches):
            value_matches = {make_hashable(default)}
        return value_matches

    @classmethod
    def get_hash(cls, trainer_config: dict) -> int:
        all_matches = set()
        for pattern, default in cls.match_fields:
            jsonpath_expression = parse(pattern)

            self_matches = cls._find_matches(jsonpath_expression, trainer_config, default=default)
            all_matches.add((pattern, frozenset(self_matches)))

        return hash(frozenset(all_matches))

    @classmethod
    def configs_match(cls, trainer_config: dict, other_trainer_config: dict) -> bool:
        for pattern, default in cls.match_fields:
            jsonpath_expression = parse(pattern)

            matches = cls._find_matches(jsonpath_expression, trainer_config, default=default)
            other_matches = cls._find_matches(jsonpath_expression, other_trainer_config, default=default)
            if matches != other_matches:
                return False
        return True

    def matches(self, trainer_config: dict, *, compare_revisions: bool = True) -> bool:
        """Checks if the cache is suitable for a given trainer config.
        By default, this method checks for the full match of training configurations and environment variables. Override `match_fields`
        and `match_env` to specify what fields and variables should be considered.
        """
        # compare git revisions
        if compare_revisions and not self.git_revision == get_git_revision_hash():
            return False

        # compare configurations
        if not self.configs_match(self.trainer_config, trainer_config):
            return False

        # compare environments
        for name, value in self.match_env:
            actual_value = os.environ.get(name)
            if value != actual_value:
                return False

        return True

    def save(self, path: Path, *, rewrite: bool = False) -> None:
        object.__setattr__(self, 'path', path)
        super(Cache, self).save(path, rewrite=rewrite)
        object.__setattr__(self, 'path', None)
