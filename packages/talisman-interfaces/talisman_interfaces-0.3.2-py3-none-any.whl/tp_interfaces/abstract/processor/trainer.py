from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generic, Optional, TypeVar

from .processor import AbstractDocumentProcessor
from ..model.model import Picklable

DEFAULT_CACHE_DIR = Path('trainer_cache')


class Cache(Picklable):
    pass


@dataclass
class TrainingResults:
    model: AbstractDocumentProcessor
    metrics: Optional[Dict[str, float]]


_Processor = TypeVar('_Processor', bound=AbstractDocumentProcessor)
_TrainingResults = TypeVar('_TrainingResults', bound=TrainingResults)


class AbstractTrainer(Generic[_Processor, _TrainingResults], metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict):
        pass

    @abstractmethod
    def train(self, cache_dir: Optional[Path] = DEFAULT_CACHE_DIR, pretrained_model: Optional[_Processor] = None) -> _TrainingResults:
        pass
