from dataclasses import dataclass, field
from typing import Generic, Set, TypeVar

from frozendict import frozendict

from tdm.future.helper import generics_mapping
from .base import Identifiable


@dataclass(frozen=True)
class BaseNodeMetadata:
    hidden: bool = False


_NodeMetadata = TypeVar("_NodeMetadata", bound=BaseNodeMetadata)


@dataclass(frozen=True)
class AbstractNode(Identifiable, Generic[_NodeMetadata]):
    metadata: _NodeMetadata = None

    def __post_init__(self):
        super().__post_init__()
        if self.metadata is None:
            # hack for runtime metadata generation (if no value passed)
            object.__setattr__(self, 'metadata', self._generate_metadata())

    def _generate_metadata(self) -> _NodeMetadata:
        type_vars = generics_mapping(type(self))
        return type_vars[self.__dataclass_fields__['metadata'].type]()

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return set()


_Content = TypeVar('_Content')


@dataclass(frozen=True)
class _AbstractContentNode(Generic[_Content]):
    content: _Content
    markup: dict = field(default_factory=frozendict, hash=False)

    def __post_init__(self):
        object.__setattr__(self, 'markup', frozendict(self.markup))


@dataclass(frozen=True)
class AbstractContentNode(AbstractNode[_NodeMetadata], _AbstractContentNode[_Content], Generic[_NodeMetadata, _Content]):

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'content'}
