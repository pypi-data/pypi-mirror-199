from abc import ABCMeta, abstractmethod
from functools import partial
from itertools import chain
from typing import Generic, Iterator, Sequence, Tuple, Type, TypeVar

from more_itertools import ichunked
from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument as LegacyDocument
from tdm.future.abstract.datamodel import TalismanDocument

from tp_interfaces.abstract.model import AbstractModel
from tp_interfaces.abstract.schema import ImmutableBaseModel
from tp_interfaces.logging.context import with_log_extras

_DocumentContent = TypeVar('_DocumentContent', bound=AbstractTreeDocumentContent)
_Config = TypeVar('_Config', bound=ImmutableBaseModel)

_Document = LegacyDocument[_DocumentContent] | TalismanDocument


class AbstractDocumentProcessor(AbstractModel, Generic[_Config, _DocumentContent], metaclass=ABCMeta):

    @abstractmethod
    def process_doc(self, document: _Document, config: _Config) -> _Document:
        pass

    def process_docs(self, documents: Sequence[_Document], config: _Config) \
            -> Tuple[_Document, ...]:
        log_extras = with_log_extras(doc_id=lambda kwargs: kwargs['document'].doc_id)
        return tuple(map(partial(log_extras(self.process_doc), config=config), documents))

    def process_stream(self, documents: Iterator[_Document], config: _Config, batch_size: int) \
            -> Iterator[LegacyDocument[_DocumentContent]]:
        return chain.from_iterable(map(partial(self.process_docs, config=config), map(tuple, ichunked(documents, batch_size))))

    @property
    @abstractmethod
    def config_type(self) -> Type[_Config]:
        pass
