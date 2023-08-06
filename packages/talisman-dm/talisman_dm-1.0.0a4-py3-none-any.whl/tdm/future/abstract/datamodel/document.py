from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterable, Optional, Set, Tuple, Type, TypeVar, Union

from .directive import AbstractDirective
from .fact import AbstractFact
from .link import AbstractNodeLink
from .node import AbstractNode

_TD = TypeVar('_TD', bound='TalismanDocument')

NodeOrId = Union[str, AbstractNode]


class TalismanDocument(metaclass=ABCMeta):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def nodes(self) -> Dict[str, AbstractNode]:
        pass

    @abstractmethod
    def with_nodes(self: _TD, nodes: Iterable[AbstractNode]) -> _TD:
        pass

    @abstractmethod
    def without_nodes(self: _TD, nodes: Iterable[NodeOrId], *, cascade: bool = True) -> _TD:
        pass

    @property
    @abstractmethod
    def roots(self) -> Set[AbstractNode]:
        pass

    @property
    @abstractmethod
    def main_root(self) -> Optional[AbstractNode]:
        pass

    @abstractmethod
    def with_main_root(self: _TD, node: Optional[NodeOrId], *, update: bool = False) -> _TD:
        pass

    @abstractmethod
    def parent(self, node: NodeOrId) -> Optional[AbstractNode]:
        pass

    @abstractmethod
    def child_nodes(self, node: Union[str, AbstractNode]) -> Tuple[AbstractNode, ...]:
        pass

    @abstractmethod
    def with_links(self: _TD, links: Dict[NodeOrId, Iterable[NodeOrId]], *, force: bool = False, update: bool = False) -> _TD:
        pass

    @abstractmethod
    def with_link(self: _TD, parent: NodeOrId, child: NodeOrId, *, force: bool = False, update: bool = False) -> _TD:
        pass

    @abstractmethod
    def without_parent_links(self: _TD, nodes: Iterable[NodeOrId]) -> _TD:
        pass

    @abstractmethod
    def without_links(self: _TD, links: Dict[NodeOrId, Iterable[NodeOrId]]) -> _TD:
        pass

    @property
    @abstractmethod
    def node_links(self) -> Dict[Type[AbstractNodeLink], Iterable[AbstractNodeLink]]:
        pass

    @abstractmethod
    def with_node_links(self: _TD, links: Iterable[AbstractNodeLink], *, update: bool = False) -> _TD:
        pass

    @abstractmethod
    def without_node_links(self: _TD, links: Iterable[Union[str, AbstractNodeLink]], *, cascade: bool = False) -> _TD:
        pass

    @property
    @abstractmethod
    def facts(self) -> Dict[Type[AbstractFact], Iterable[AbstractFact]]:
        pass

    @abstractmethod
    def with_facts(self: _TD, facts: Iterable[AbstractFact], *, update: bool = False) -> _TD:
        pass

    @abstractmethod
    def without_facts(self: _TD, facts: Iterable[Union[str, AbstractFact]], *, cascade: bool = False) -> _TD:
        pass

    @property
    @abstractmethod
    def directives(self) -> Dict[Type[AbstractDirective], AbstractDirective]:
        pass

    @abstractmethod
    def with_directives(self: _TD, directives: Iterable[AbstractDirective], *, update: bool = False) -> _TD:
        pass

    @abstractmethod
    def without_directives(self: _TD, directives: Iterable[Union[str, AbstractDirective]], *, cascade: bool = False) -> _TD:
        pass

    @property
    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def with_metadata(self: _TD, metadata: Dict[str, Any]) -> _TD:
        pass


class AbstractDocumentFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_document(self, *, id_: Optional[str] = None) -> TalismanDocument:
        pass
