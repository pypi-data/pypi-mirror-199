import uuid
from typing import Dict, Iterable, Optional, Tuple

from tdm.abstract.datamodel.document import DocumentMetadata
from tdm.future.abstract.datamodel import AbstractDirective, AbstractFact, AbstractNode, AbstractNodeLink
from tdm.future.abstract.datamodel.document import AbstractDocumentFactory, TalismanDocument
from ._container import TypedIdsContainer
from ._impl import TalismanDocumentImpl
from ._structure import NodesStructure


class TalismanDocumentFactory(AbstractDocumentFactory):

    def create_document(self, *, id_: Optional[str] = None) -> TalismanDocument:
        return TalismanDocumentImpl(
            id2view={},
            dependencies={},
            structure=NodesStructure(),
            containers={
                AbstractNode: TypedIdsContainer(AbstractNode, ()),
                AbstractNodeLink: TypedIdsContainer(AbstractNodeLink, ()),
                AbstractFact: TypedIdsContainer(AbstractFact, ()),
                AbstractDirective: TypedIdsContainer(AbstractDirective, ())
            },
            metadata=None,
            id_=id_ or self.generate_id())

    def construct(
            self,
            content: Iterable[AbstractNode] = (),
            structure: Dict[str, Tuple[str, ...]] = None,
            root: Optional[str] = None,
            node_links: Iterable[AbstractNodeLink] = (),
            facts: Iterable[AbstractFact] = (),
            directives: Iterable[AbstractDirective] = (),
            metadata: Optional[DocumentMetadata] = None,
            *, id_: Optional[str] = None
    ) -> TalismanDocument:
        doc: TalismanDocumentImpl = self.create_document(id_=id_)
        doc = doc.with_elements((*content, *node_links, *facts, *directives)) \
            .with_links(structure) \
            .with_main_root(root) \
            .with_metadata(metadata)
        return doc

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())
