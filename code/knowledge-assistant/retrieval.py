# SPDX-License-Identifier: Apache-2.0
"""KA-4 ranking over the immutable KA-0 cards; full precision, stable ties."""
from collections import Counter
import math
from contracts import load
from baselines import load_fixture, tokens, run_locale


def ordered(scores, order):
    return sorted(order, key=lambda key: (-round(scores[key], 12), order.index(key)))


def bm25(query, documents, k1=1.2, b=0.75):
    if not documents:
        return []
    size = len(documents)
    average = sum(map(len, documents)) / size
    if average == 0:
        return [0.0] * size
    counts = [Counter(doc) for doc in documents]
    terms = set(query)
    df = {term: sum(term in row for row in counts) for term in terms}
    scores = []
    for doc, row in zip(documents, counts):
        length = 1 - b + b * len(doc) / average
        scores.append(sum(math.log(1 + (size - df[t] + 0.5) / (df[t] + 0.5)) * row[t] * (k1 + 1) / (row[t] + k1 * length) for t in terms))
    return scores


def mean_vector(pieces, mapping):
    dimension = len(next(iter(mapping.values())))
    return [sum(mapping.get(t, [0.0] * dimension)[i] for t in pieces) / max(1, len(pieces)) for i in range(dimension)]


def cosine(left, right):
    denominator = math.sqrt(sum(x*x for x in left) * sum(x*x for x in right))
    return sum(x*y for x, y in zip(left, right)) / denominator if denominator else 0.0


def rrf(lists, order, offset=60):
    return {key: sum(1 / (offset + ranking.index(key) + 1) for ranking in lists if key in ranking) for key in order}


def infer_scope(query, locale, fixture):
    terms = tokens(query, locale, fixture)
    rules = load('ka4-retrieval-rules-v1.json')['scope_words'][locale]
    current = any(word in query.lower() for word in rules['current'])
    topic = 'order' if 'processing' in terms else 'approval' if 'approval' in terms else 'travel' if any(t in terms for t in ['lodging', 'hotel', 'allowance', '600', '750']) else None
    on_date = '2026-09-14' if current or '750' in terms else '2025-09-14' if '600' in terms else None
    return topic, on_date


def rerank(candidates, query, locale, fixture):
    topic, on_date = infer_scope(query, locale, fixture)
    metadata = {d['source_id']: d for d in load('ka4-documents-v1.json')['documents']}
    def fit(key):
        doc = metadata[key]
        return (topic is None or doc['topic'] == topic) and (on_date is None or doc['valid_from'] <= on_date and (doc['valid_until'] is None or on_date < doc['valid_until']))
    return sorted(candidates, key=lambda key: (not fit(key), candidates.index(key)))


def metrics(ranking, relevant, k=2, grades=None):
    if len(set(ranking)) != len(ranking):
        raise ValueError('duplicate_candidate')
    if not relevant:
        return dict(recall=None, rr=None, ndcg=None, correct_abstention=not ranking)
    grades = grades or {key: 1 for key in relevant}
    gains = lambda row: sum((2**grades.get(key, 0)-1) / math.log2(i+2) for i, key in enumerate(row[:k]))
    ideal = sorted(grades, key=lambda key: -grades[key])
    first = next((i+1 for i, key in enumerate(ranking) if key in relevant), None)
    return dict(recall=len(set(ranking[:k]) & set(relevant))/len(relevant),
                rr=1/first if first else 0.0, ndcg=gains(ranking)/gains(ideal), correct_abstention=None)


def run():
    fixture = load_fixture()
    order = fixture['candidate_order']
    learned = load('../part-ii/nnlm-run.json')['learned_vectors']
    static = load('ka-static-v1.json')
    mapping = static.get('vectors', static.get('mapping'))
    output = {}
    for locale in ['en', 'zh-hans']:
        docs = [tokens(doc['index_text'][locale], locale, fixture) for doc in fixture['documents']]
        old = run_locale(fixture, locale)
        rows = []
        for query in fixture['queries']:
            text = query['text'][locale]
            pieces = tokens(text, locale, fixture)
            score_sets = {'bm25': dict(zip(order, bm25(pieces, docs)))}
            for name, values in [('dense_authored', mapping), ('dense_nnlm', learned)]:
                qvec = mean_vector(pieces, values)
                score_sets[name] = dict(zip(order, [cosine(qvec, mean_vector(doc, values)) for doc in docs]))
            positive = {name: [key for key in ordered(scores, order) if scores[key] > 0] for name, scores in score_sets.items()}
            score_sets['hybrid'] = rrf([positive['bm25'], positive['dense_authored']], order)
            positive['hybrid'] = [key for key in ordered(score_sets['hybrid'], order) if score_sets['hybrid'][key] > 0]
            positive['reranked'] = rerank(positive['hybrid'][:3], text, locale, fixture)
            rows.append(dict(query_id=query['id'], query=text, relevant=query['relevant'], scores=score_sets,
                             full_order={name: ordered(scores, order) for name, scores in score_sets.items()},
                             returned=positive, metrics={name: metrics(rank, query['relevant']) for name, rank in positive.items()},
                             success={name: (rank[0] in query['relevant'] if rank else not query['relevant']) for name, rank in positive.items()}))
        names = list(rows[0]['success'])
        output[locale] = dict(inherited=old, rows=rows, success_counts={name: sum(r['success'][name] for r in rows) for name in names},
                             macro={name: {metric: sum(r['metrics'][name][metric] for r in rows if r['relevant']) / sum(bool(r['relevant']) for r in rows) for metric in ['recall', 'rr', 'ndcg']} for name in names})
    return dict(version='ka4-ranking-run-v1',producer='CPU Python; no new embedding training; authored map and retained learned NNLM vectors',k=2,locales=output)


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2))
