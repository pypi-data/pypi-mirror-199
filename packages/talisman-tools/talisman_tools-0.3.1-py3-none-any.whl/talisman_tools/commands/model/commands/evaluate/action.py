import json
import time
from functools import partial
from itertools import chain
from pathlib import Path
from typing import Dict, Optional, Set

from tdm.abstract.datamodel import AbstractFact
from tdm.abstract.datamodel.fact import AbstractLinkValue
from tdm.datamodel import ConceptFact, TalismanDocument, ValueFact

from talisman_tools.commands.model.commands.evaluate.coreference import evaluate_coref
from talisman_tools.commands.model.commands.evaluate.disambiguation_quality import evaluate_dmb
from talisman_tools.commands.model.commands.evaluate.evaluation import evaluate_nerc, evaluate_relext, evaluate_relext_upper_bound
from talisman_tools.plugin import KBPlugins
from tp_interfaces.abstract import AbstractDocumentProcessor
from tp_interfaces.helpers.io import read_json
from tp_interfaces.knowledge_base.kb_schema import AnySchemaType, BaseValueType, KBSchema, RelExtModel, SchemaConceptType, \
    SchemaRelationType, \
    SchemaValueType
from tp_interfaces.knowledge_base.manager import KBManager
from tp_interfaces.readers.abstract import AbstractReader


def print_scores(scores: Dict[str, dict]):
    def round_floats(val, precision=4):
        if isinstance(val, int):
            return val
        if isinstance(val, float):
            return round(val, precision)
        if isinstance(val, dict):
            return {k: round_floats(v) for k, v in val.items()}
        raise ValueError

    def stringify_keys(d: dict):
        ret = {}
        for key, val in d.items():
            if isinstance(key, (tuple, frozenset)):
                key = str(key)
            if isinstance(val, dict):
                val = stringify_keys(val)

            ret[key] = val

        return ret

    json_repr = json.dumps(stringify_keys(round_floats(scores)), sort_keys=True, indent=2)
    print(json_repr)


def keep_nerc(doc: TalismanDocument) -> TalismanDocument:
    facts = chain(
        map(lambda f: f.with_changes(value=tuple()), doc.filter_facts(ConceptFact)),  # TODO: replace value with None instead of empty tuple
        doc.filter_facts(ValueFact)
    )
    return doc.without_facts().with_facts(facts)


def clear_values(doc: TalismanDocument) -> TalismanDocument:
    return doc.with_facts(
        map(lambda f: f.with_changes(value=tuple()), doc.filter_facts(ConceptFact)),  # TODO: replace value with None instead of empty tuple
    )


def clear_chains(doc: TalismanDocument) -> TalismanDocument:
    return doc.with_content(doc.content.without_chains())


def get_fake_schema(fact: AbstractFact) -> AnySchemaType:
    common_attributes = dict(id=fact.type_id, name=fact.type_id, fact_type=fact.fact_type)

    if isinstance(fact, ConceptFact):
        return SchemaConceptType(**common_attributes, pretrained_nercmodels=(fact.type_id,))

    if isinstance(fact, ValueFact):
        # there is no way to set correct value type
        return SchemaValueType(**common_attributes, pretrained_nercmodels=(fact.type_id,), value_type=BaseValueType.STRING)

    # fact is property fact or relation fact
    fact: AbstractFact[AbstractLinkValue]
    from_type_id = fact.value.from_fact.type_id
    to_type_id = fact.value.to_fact.type_id
    return SchemaRelationType(
        **common_attributes,
        pretrained_relext_models=(RelExtModel(relation_type=fact.type_id),),
        from_id=from_type_id,
        to_id=to_type_id
    )


mode = {
    "all": lambda doc: doc.without_facts(),  # start from clear document (no facts provided)
    "nerc": lambda doc: doc.without_facts(),  # start from clear document (no facts provided)
    "relext": keep_nerc,  # start from document with concept and value facts (no link facts, no fact values)
    "dmb": clear_values,  # start from document with facts without values
    "coref": clear_chains
}

evaluators = {
    'all': {
        'nerc': evaluate_nerc,
        'relext': evaluate_relext,
        'relext-upper-bound': evaluate_relext_upper_bound,
        'dmb': partial(evaluate_dmb, at_ks=[1, 2, 3])  # TODO: make configurable from cli
    },
    'relext': {
        'relext': evaluate_relext
    },
    'nerc': {
        'nerc': evaluate_nerc
    },
    'dmb': {
        'dmb': partial(evaluate_dmb, at_ks=[1, 2, 3])  # TODO: make configurable from cli
    },
    'coref': {
        'coref': evaluate_coref
    }
}


def evaluate(
        processor: AbstractDocumentProcessor,
        eval_mode: str,
        reader: AbstractReader,
        config_path: Path,
        input_reader: Optional[AbstractReader] = None
):
    gold_docs = tuple(reader.read())
    actual_docs = tuple(map(mode[eval_mode], gold_docs)) if input_reader is None else tuple(input_reader.read())

    # collect fake type mappings from dataset
    types: Set[AnySchemaType] = set()
    for fact in chain.from_iterable(doc.facts for doc in gold_docs):
        types.add(get_fake_schema(fact))
    gold_type_ids = {t.id for t in types}

    # set stub kb as knowledge base to infer type mappings from it
    KBManager().knowledge_base = KBPlugins.plugins[None]()(KBSchema(types))  # DMBCommonnessStub

    evaluation_start = time.time()

    with processor:
        processor_config_type = processor.config_type
        config = processor_config_type.parse_obj(read_json(config_path)) if config_path else processor_config_type()
        actual_docs = processor.process_docs(actual_docs, config)

    evaluation_end = time.time()

    # drop unannotated fact types
    def correct_type_id(f: AbstractFact) -> bool:
        return f.type_id in gold_type_ids
    filtered_docs = [doc.without_facts().with_facts(doc.filter_facts(AbstractFact, correct_type_id)) for doc in actual_docs]

    scores = {name: evaluator(filtered_docs, gold_docs) for name, evaluator in evaluators[eval_mode].items()}

    print_scores(scores)
    print(f'Total evaluation time: {evaluation_end - evaluation_start:.04f} seconds')
