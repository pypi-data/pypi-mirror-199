import pickle
from abc import ABCMeta
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Type, TypeVar


_Picklable = TypeVar('_Picklable', bound='Picklable')


class Picklable:
    @classmethod
    def load(cls: Type[_Picklable], path: Path) -> _Picklable:
        if path.suffix == '.dvc':
            import dvc.api
            # problem with dvc.api.open: https://github.com/iterative/dvc/issues/4667
            model = pickle.loads(dvc.api.read(str(path.with_suffix('')), mode='rb'))
        else:
            with path.open('rb') as f:
                model = pickle.load(f)
        if not isinstance(model, cls):
            raise pickle.PickleError(f"Pickled object at {path} is not an instance of {cls.__name__} class.")
        return model

    def save(self, path: Path, *, rewrite: bool = False) -> None:
        if path.exists() and not rewrite:
            raise Exception(f"Saving path exists: {path}.")

        with path.open('wb') as f:
            pickle.dump(self, f, protocol=5)  # fixed protocol version to avoid issues with serialization on Python 3.10+ versions


_Model = TypeVar('_Model', bound='AbstractModel')


class AbstractModel(AbstractContextManager, Picklable, metaclass=ABCMeta):
    def __enter__(self: _Model) -> _Model:
        return self

    def __getstate__(self):
        return self.__dict__.copy()
