# SPDX-License-Identifier: Apache-2.0
"""KA-0 lexical baselines share tokenization, documents, queries and relevance."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code/part-ii"))
from text_processing import search_key
from numerical import cosine


def load_fixture():
    return json.loads((ROOT / "data/knowledge-assistant/ka0-v1.json").read_text(encoding="utf-8"))


def tokens(text, locale, fixture):
    text = search_key(text)
    entries = fixture["vocabulary"] + fixture["extra_lexemes"]
    mapping = {search_key(row["surface"][locale]): row["term"] for row in entries}
    if locale == "en":
        pieces = re.findall(r"[a-z]+|[0-9]+", text)
    elif locale == "zh-hans":
        pieces, position = [], 0
        surfaces = sorted(mapping, key=lambda word: (-len(word), word))
        while position < len(text):
            remainder = text[position:]
            ascii_run = re.match(r"[a-z]+|[0-9]+", remainder)
            if ascii_run:
                piece = ascii_run.group()
            else:
                piece = next((word for word in surfaces if remainder.startswith(word)), text[position])
            if not piece.isspace() and not all(unicodedata.category(c).startswith("P") for c in piece):
                pieces.append(piece)
            position += len(piece)
    else:
        raise ValueError("unsupported locale")
    return [mapping.get(piece, piece) for piece in pieces]


def count_vector(pieces, vocabulary):
    counts = Counter(pieces)
    return [counts[term] for term in vocabulary]


def rank(scores, candidate_order):
    order = sorted(range(len(scores)), key=lambda i: (-round(scores[i], 12), i))
    prediction = candidate_order[order[0]] if scores[order[0]] > 0 else None
    return {"scores": scores, "ranking": [candidate_order[i] for i in order], "prediction": prediction}


def success(prediction, relevant):
    return prediction in relevant if relevant else prediction is None


def evaluate_vectors(document_vectors, query_vectors, fixture):
    results = []
    for query, vector in zip(fixture["queries"], query_vectors):
        scores = [cosine(vector, row) or 0.0 for row in document_vectors]
        result = rank(scores, fixture["candidate_order"])
        result.update({"query_id": query["id"], "success": success(result["prediction"], query["relevant"])})
        results.append(result)
    return results


def run_locale(fixture, locale):
    vocabulary = [row["term"] for row in fixture["vocabulary"]]
    document_tokens = [tokens(row["index_text"][locale], locale, fixture) for row in fixture["documents"]]
    query_tokens = [tokens(row["text"][locale], locale, fixture) for row in fixture["queries"]]
    matrix = [count_vector(row, vocabulary) for row in document_tokens]
    queries = [count_vector(row, vocabulary) for row in query_tokens]
    df = [sum(row[column] > 0 for row in matrix) for column in range(len(vocabulary))]
    idf = [math.log((1 + len(matrix)) / (1 + frequency)) + 1 for frequency in df]
    weighted = [[count * weight for count, weight in zip(row, idf)] for row in matrix]
    query_weighted = [[count * weight for count, weight in zip(row, idf)] for row in queries]
    keyword = []
    for query, vector in zip(fixture["queries"], queries):
        result = rank([sum(q > 0 and d > 0 for q, d in zip(vector, row)) for row in matrix], fixture["candidate_order"])
        result.update({"query_id": query["id"], "success": success(result["prediction"], query["relevant"])})
        keyword.append(result)
    methods = {"keyword": keyword, "count": evaluate_vectors(matrix, queries, fixture),
               "tfidf": evaluate_vectors(weighted, query_weighted, fixture)}
    return {"vocabulary": vocabulary, "document_tokens": document_tokens, "query_tokens": query_tokens,
            "count_matrix": matrix, "query_count_matrix": queries, "document_frequency": df, "idf": idf,
            "tfidf_matrix": weighted, "query_tfidf_matrix": query_weighted, "methods": methods,
            "success_counts": {method: sum(row["success"] for row in rows) for method, rows in methods.items()}, "query_count": len(queries)}


def run(write=False):
    fixture = load_fixture()
    output = {"version": "ka0-lexical-run-v1", "status": "measured deterministic CPU run", "as_of": "2026-09-12",
              "dataset_sha256": hashlib.sha256((ROOT / "data/knowledge-assistant/ka0-v1.json").read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "normalizer_sha256": hashlib.sha256((ROOT / "code/part-ii/text_processing.py").read_bytes()).hexdigest(),
              "python": sys.version.split()[0], "unicode_database": unicodedata.unidata_version,
              "locales": {locale: run_locale(fixture, locale) for locale in ["en", "zh-hans"]}}
    if write:
        (ROOT / "data/knowledge-assistant/ka0-lexical-run.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({locale: {"success_counts": result["success_counts"], "query_count": result["query_count"],
          "predictions": {method: [row["prediction"] for row in rows] for method, rows in result["methods"].items()}}
          for locale, result in output["locales"].items()}, indent=2))
    return output


if __name__ == "__main__":
    run(write=True)
