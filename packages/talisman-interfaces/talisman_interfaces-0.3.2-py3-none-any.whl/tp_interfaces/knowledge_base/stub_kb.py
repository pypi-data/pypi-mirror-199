from collections import Counter, defaultdict
from typing import Counter as TypingCounter, DefaultDict, Dict, Iterable, Tuple, Type

from tdm.abstract.datamodel import AbstractTalismanDocument
from tdm.datamodel import CreateConceptDirective
from tdm.datamodel.fact import ConceptFact

from tp_interfaces.abstract import ImmutableBaseModel
from tp_interfaces.knowledge_base.interfaces import DBConcept, KB, MentionCandidates, MentionConceptFeatures
from tp_interfaces.knowledge_base.kb_schema import KBSchema

EMPTY_SCHEMA = KBSchema(tuple())


class DMBCommonnessStub(KB[ImmutableBaseModel]):
    def __init__(self, kb_schema: KBSchema = EMPTY_SCHEMA):
        self._id2concept: Dict[str, DBConcept] = {}
        self._mention2ids_counter: DefaultDict[str, TypingCounter[DBConcept]] = defaultdict(Counter)
        self._kb_schema = kb_schema

    def __exit__(self, *exc):
        pass

    def refresh_schema(self):
        pass

    def bind_facts_and_load_docs(self, docs: Iterable[AbstractTalismanDocument]):
        for doc in docs:
            for directive in doc.filter_directives(CreateConceptDirective):
                self._load_directive(directive)

        for doc in docs:
            for fact in doc.filter_facts(ConceptFact, lambda f: isinstance(f.value, str) and f.mention is not None):
                concept = fact.value
                if concept not in self._id2concept:
                    raise ValueError(f"Provided document {doc.doc_id} contains concept not in KB: concept id = {concept}")

                self._mention2ids_counter[' '.join(doc.fact_text_mention(fact))][concept] += 1

    def _load_directive(self, directive: CreateConceptDirective):
        self._id2concept[directive.id] = DBConcept(directive.id, directive.name, directive.concept_type)
        self._mention2ids_counter[directive.name][directive.id] += 1

    def _compute_mention_candidates(self, mention: str) -> MentionCandidates:
        candidates_counter = self._mention2ids_counter[mention]  # Counter[candidate_id, candidate_occ_num]
        mention_occs = sum(candidates_counter.values())
        candidate2feats = dict()
        for candidate_id, candidate_occs in candidates_counter.items():
            candidate = self._id2concept[candidate_id]
            candidate2feats[candidate] = MentionConceptFeatures(candidate_occs / mention_occs)

        return MentionCandidates(candidate2feats)

    def get_candidates(self, doc: AbstractTalismanDocument, config: ImmutableBaseModel
                       ) -> Tuple[Tuple[ConceptFact, ...], Tuple[CreateConceptDirective, ...]]:
        facts = []

        # facts without values only
        for fact in doc.filter_facts(ConceptFact, lambda f: not f.value and doc.fact_text_mention(f) is not None):
            mention_str = ' '.join(doc.fact_text_mention(fact))
            if mention_str not in self._mention2ids_counter:
                continue
            facts.append(self._compute_mention_candidates(mention_str).fact_with_candidates(fact, lambda f: f.commonness))

        return tuple(facts), tuple()

    @property
    def config_type(self) -> Type[ImmutableBaseModel]:
        return ImmutableBaseModel

    @property
    def schema(self) -> KBSchema:
        return self._kb_schema

    @classmethod
    def from_config(cls, config: dict) -> 'DMBCommonnessStub':
        """Config example:
        {
            "schema": {
                ...`KBSchema` config...
            }
        }
        """
        return cls(kb_schema=KBSchema.from_config(config['schema']))
