from functools import reduce
from typing import Dict, List, Sequence, Set

import numpy
from tdm.datamodel import TalismanDocument

from tie_datamodel.datamodel import TIEDocumentContent
from tie_datamodel.datamodel.markup import Mention
from .metrics import bcub_score, ceafe_score, conll2012_score, lea_score, muc_score


def evaluate_coref(
        gold: Sequence[TalismanDocument], predicted: Sequence[TalismanDocument]) -> Dict[str, float]:
    if len(predicted) != len(gold):
        raise ValueError("Predicted and gold sequences are not aligned")
    pred_clusters = [chains_to_entities(doc.content) for doc in predicted]
    gold_clusters = [chains_to_entities(doc.content) for doc in gold]
    mean_scores = [get_mean_scores(gold_clusters, pred_clusters, scorer, tag)
                   for scorer, tag in [(bcub_score, "bcub"),
                                       (muc_score, "muc"),
                                       (ceafe_score, "ceafe"),
                                       (lea_score, "lea")]]
    mean_scores.append({"conll2012_score": float(numpy.mean([conll2012_score(g, p) for g, p in zip(gold_clusters, pred_clusters)]))})
    return reduce(lambda a, b: {**a, **b}, mean_scores)


def get_mean_scores(gold: Sequence, pred: Sequence, scorer, tag):
    scores = [scorer(g, p) for g, p in zip(gold, pred)]
    means = numpy.mean(scores, axis=0)
    return {f"{tag}_precision": means[1],
            f"{tag}_recall": means[0],
            f"{tag}_f1": means[2]}


def mention_to_id(mention: Mention) -> str:
    return f"{mention.node_id}_{mention.start_idx}_{mention.end_idx}"


def chains_to_entities(content: TIEDocumentContent) -> List[Set[str]]:
    if content.has_chains:
        sorted_chains = sorted(content.chains, key=lambda chain: min(mention.start_idx for mention in list(chain)), reverse=True)
        return [{mention_to_id(ment) for ment in chain} for chain in sorted_chains]
    else:
        return []
