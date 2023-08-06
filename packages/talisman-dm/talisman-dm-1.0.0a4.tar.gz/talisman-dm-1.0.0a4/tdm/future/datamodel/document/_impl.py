from copy import deepcopy
from functools import wraps
from typing import Any, Dict, Iterable, Iterator, Optional, Set, Tuple, Type, TypeVar, Union

from tdm.abstract.datamodel.document import DocumentMetadata
from tdm.future.abstract.datamodel import AbstractDirective, AbstractFact, AbstractNode, AbstractNodeLink, EnsureIdentifiable, \
    TalismanDocument
from ._base import BaseImpl
from ._container import TypedIdsContainer
from ._structure import NodesStructure
from ._view import AbstractView, restore_object

_TD = TypeVar('_TD', bound='TalismanDocumentImpl')
_D = TypeVar('_D', bound=EnsureIdentifiable)


def _filter_elements(base_type: Type[_D]):
    def decorator(f):
        @wraps(f)
        def wrapper(self: _TD, els: Iterable[Union[str, _D]], *args, **kwargs):
            return f(self, _filter(self._containers[base_type], self._id2view, els, base_type), *args, **kwargs)

        return wrapper

    return decorator


class TalismanDocumentImpl(TalismanDocument, BaseImpl):
    __slots__ = (
        '_id', '_structure', '_metadata'
    )

    def __init__(
            self,
            id2view: Dict[str, Union[EnsureIdentifiable, AbstractView]],
            dependencies: Dict[str, Set[Tuple[str, Type[EnsureIdentifiable]]]],
            containers: Dict[Type[EnsureIdentifiable], TypedIdsContainer],
            structure: NodesStructure,
            metadata: Optional[DocumentMetadata],  # should be removed in future
            *, id_: str):
        super().__init__(id2view, dependencies, containers)
        self._id = id_
        self._structure = structure

        self._metadata = deepcopy(metadata)  # should be removed in future

    def _replace(self: _TD, **kwargs) -> _TD:
        return super()._replace(
            **{
                'structure': self._structure,
                'metadata': self._metadata,
                'id_': self._id,
                **kwargs
            }
        )

    def _update_structure(self: _TD, other: _TD) -> _TD:
        if other._containers[AbstractNode] is not self._containers[AbstractNode]:  # something has changed
            other._structure = self._structure.update_nodes(other._containers[AbstractNode].ids)
        return other

    def with_elements(self: _TD, elements: Iterable[EnsureIdentifiable], *, update: bool = False) -> _TD:
        return self._update_structure(super().with_elements(elements, update=update))

    def without_elements(self: _TD, ids: Iterable[str], *, cascade: bool = False) -> _TD:
        return self._update_structure(super().without_elements(ids, cascade=cascade))

    @property
    def id(self) -> str:
        return self._id

    @property
    def nodes(self) -> Dict[str, AbstractNode]:
        return {id_: restore_object(self._id2view[id_], self._id2view) for id_ in self._containers[AbstractNode].ids}

    @_filter_elements(AbstractNode)
    def with_nodes(self: _TD, nodes: Iterable[AbstractNode]) -> _TD:
        return self.with_elements(nodes, update=True)

    @_filter_elements(AbstractNode)
    def without_nodes(self: _TD, nodes: Iterable[Union[str, AbstractNode]], *, cascade: bool = False) -> _TD:
        return self.without_elements(map(_to_id, nodes), cascade=cascade)

    @property
    def roots(self) -> Set[AbstractNode]:
        return {restore_object(self._id2view[id_], self._id2view) for id_ in self._structure.roots}

    @property
    def main_root(self) -> Optional[AbstractNode]:
        main_root = self._structure.main_root
        return restore_object(self._id2view[main_root], self._id2view) if main_root is not None else None

    def with_main_root(self: _TD, node: Optional[Union[str, AbstractNode]], *, update: bool = False) -> _TD:
        if node is None:
            return self._replace(structure=self._structure.with_main_root(None))
        if update:
            if not isinstance(node, AbstractNode):
                raise ValueError(f"could not update node {node} with id only")
            result = self.with_nodes((node,))
            result._structure = result._structure.with_main_root(node.id)
            return result
        return self._replace(structure=self._structure.with_main_root(_to_id(node)))

    def parent(self, node: Union[str, AbstractNode]) -> Optional[AbstractNode]:
        node_id = _to_id(node)
        parent_id = self._structure.parent.get(node_id)
        if parent_id is not None:
            return restore_object(self._id2view[parent_id], self._id2view)
        return None

    def child_nodes(self, node: Union[str, AbstractNode]) -> Tuple[AbstractNode, ...]:
        return tuple(restore_object(self._id2view[id_], self._id2view) for id_ in self._structure.children.get(_to_id(node), ()))

    def with_links(
            self: _TD,
            links: Dict[Union[str, AbstractNode], Iterable[Union[str, AbstractNode]]],
            *, force: bool = False, update: bool = False
    ) -> _TD:
        structure = {}
        nodes = set()

        for parent, children in links.items():
            children = list(children)
            if update:
                if isinstance(parent, AbstractNode):
                    nodes.add(parent)
                nodes.update(node for node in children if isinstance(node, AbstractNode))
            structure[_to_id(parent)] = [_to_id(node) for node in children]

        result = self
        if update:
            result = self.with_nodes(nodes)

        return result._replace(structure=result._structure.with_children(structure, force=force))

    def with_link(
            self: _TD,
            parent: Union[str, AbstractNode], child: Union[str, AbstractNode],
            *, force: bool = False, update: bool = False
    ) -> _TD:
        result = self

        if update:
            nodes = {node for node in (child, parent) if isinstance(node, AbstractNode)}
            result = result.with_nodes(nodes)

        return result._replace(structure=result._structure.with_parent(_to_id(parent), _to_id(child), force=force))

    def without_parent_links(self: _TD, nodes: Iterable[Union[str, AbstractNode]]) -> _TD:
        return self._replace(structure=self._structure.as_roots(map(_to_id, nodes)))

    def without_links(self: _TD, links: Dict[Union[str, AbstractNode], Iterable[Union[str, AbstractNode]]]) -> _TD:
        links = {_to_id(parent): set(map(_to_id, children)) for parent, children in links.items()}
        return self._replace(structure=self._structure.without_children(links))

    @property
    def node_links(self) -> Dict[Type[AbstractNodeLink], Set[AbstractNodeLink]]:
        return {
            t: {restore_object(self._id2view[i], self._id2view) for i in ids}
            for t, ids in self._containers[AbstractNodeLink].type2ids.items()
        }

    @_filter_elements(AbstractNodeLink)
    def with_node_links(self: _TD, links: Iterable[AbstractNodeLink], *, update: bool = False) -> _TD:
        return self.with_elements(links, update=update)

    @_filter_elements(AbstractNodeLink)
    def without_node_links(self: _TD, links: Iterable[Union[str, AbstractNodeLink]], *, cascade: bool = False) -> _TD:

        return self.without_elements(map(_to_id, links), cascade=cascade)

    @property
    def facts(self) -> Dict[Type[AbstractFact], Iterable[AbstractFact]]:
        return {
            t: tuple(restore_object(self._id2view[i], self._id2view) for i in ids)
            for t, ids in self._containers[AbstractFact].type2ids.items()
        }

    @_filter_elements(AbstractFact)
    def with_facts(self: _TD, facts: Iterable[AbstractFact], *, update: bool = False) -> _TD:
        return self.with_elements(facts, update=update)

    @_filter_elements(AbstractFact)
    def without_facts(self: _TD, facts: Iterable[Union[str, AbstractFact]], *, cascade: bool = False) -> _TD:
        return self.without_elements(map(_to_id, facts), cascade=cascade)

    @property
    def directives(self) -> Dict[Type[AbstractDirective], Iterable[AbstractDirective]]:
        return {
            t: tuple(restore_object(self._id2view[i], self._id2view) for i in ids)
            for t, ids in self._containers[AbstractDirective].type2ids
        }

    @_filter_elements(AbstractDirective)
    def with_directives(self: _TD, directives: Iterable[AbstractDirective], *, update: bool = False) -> _TD:
        return self.with_elements(directives, update=update)

    @_filter_elements(AbstractDirective)
    def without_directives(self: _TD, directives: Iterable[Union[str, AbstractDirective]], *, cascade: bool = False) -> _TD:
        return self.without_elements(map(_to_id, directives), cascade=cascade)

    @property
    def metadata(self) -> Dict[str, Any]:
        return deepcopy(self._metadata)

    def with_metadata(self: _TD, metadata: Dict[str, Any]) -> _TD:
        return self._replace(metadata=deepcopy(metadata))

    def __hash__(self):
        return hash((self._id, self._containers[AbstractNode], self._containers[AbstractFact]))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TalismanDocumentImpl):
            return NotImplemented
        return self._id == o._id and self._id2view == o._id2view and self._containers == o._containers and \
            self._structure == o._structure and self._metadata == o._metadata


def _to_id(obj: Union[str, EnsureIdentifiable]) -> str:
    return obj if isinstance(obj, str) else obj.id


def _filter(
        container: TypedIdsContainer[_D], known_ids: Dict[str, Any], elements: Iterable[Union[str, _D]], base_type: Type[_D]
) -> Iterator[Union[str, _D]]:
    for element in elements:
        if isinstance(element, str):
            if element in known_ids and element not in container:
                raise ValueError(f'Unexpected type for element {element}. Expected: {base_type}')
        else:
            if not isinstance(element, base_type):
                raise ValueError(f'Unexpected type for element {element}. Expected: {base_type}')
            if element.id in known_ids and element.id not in container:
                raise ValueError(f'Identifier collision for {element}')
        yield element
