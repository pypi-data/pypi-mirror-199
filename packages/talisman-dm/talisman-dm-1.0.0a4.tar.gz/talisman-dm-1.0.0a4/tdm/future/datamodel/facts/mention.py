from dataclasses import dataclass
from typing import Set

from tdm.future.abstract.datamodel import AbstractFact, AbstractNodeMention, Identifiable
from tdm.future.abstract.json_schema import generate_model
from .value import AtomValueFact


@dataclass(frozen=True)
class _MentionFact(AbstractFact):
    mention: AbstractNodeMention
    value: AtomValueFact

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return {'mention', 'value'}


@generate_model(label='mention')
@dataclass(frozen=True)
class MentionFact(Identifiable, _MentionFact):
    pass
