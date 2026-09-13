# SPDX-License-Identifier: Apache-2.0
"""Dependency-free behavioral checks against fractions and authored fixtures."""
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
import unittest
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code/part-ii"))
sys.path.insert(0, str(ROOT / "code/knowledge-assistant"))
from numerical import dot, matmul, cosine, softmax, target_loss, kl
from ngram import fit, probabilities, sequence_probability, generate
from text_processing import search_key, describe
from baselines import load_fixture, run_locale, rank, tokens


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class ArithmeticTests(unittest.TestCase):
    def test_matrix_cells_and_equal_shape_semantic_failure(self):
        fixture = read("data/part-ii/arithmetic.json")["shape"]
        self.assertEqual([matmul(sample, fixture["weight"]) for sample in fixture["input"]], fixture["expected_output"])
        self.assertEqual(dot([2, 1], [-1, 1]), -1)
        # Swapping candidate columns preserves shape and changes their meaning.
        swapped = [[row[2], row[1], row[0]] for row in fixture["weight"]]
        self.assertEqual(matmul([[2, 1]], swapped), [[-1, 1, 2]])
        for left, right in [([[1, 2]], [[1]]), ([[1], [2, 3]], [[1]])]:
            with self.assertRaises(ValueError):
                matmul(left, right)

    def test_cosine_scale_order_units_and_zero(self):
        self.assertAlmostEqual(cosine([2, 1], [1, -1]), 1 / math.sqrt(10), places=12)
        self.assertAlmostEqual(cosine([20, 10], [1, -1]), 1 / math.sqrt(10), places=12)
        self.assertEqual(cosine([1, 0], [-1, 0]), -1)
        self.assertIsNone(cosine([0, 0], [1, 2]))
        with self.assertRaises(ValueError):
            cosine([1], [1, 2])

    def test_softmax_loss_units_padding_and_stability(self):
        self.assertEqual(softmax([math.log(2), 0, 0]), [0.5, 0.25, 0.25])
        for shift in [0, 1000, -1000]:
            z = [shift, shift + math.log(3)]
            self.assertAlmostEqual(softmax(z)[1], 3/4, places=12)
            self.assertAlmostEqual(target_loss(z, 1), math.log(4/3), places=12)
        self.assertEqual(target_loss([0, -1000], 1), 1000)
        total = -math.log((1/2) * (1/2) * (1/4))
        self.assertAlmostEqual(math.exp(total / 3), 16 ** (1/3), places=12)
        self.assertAlmostEqual(math.exp(total / 4), 2, places=12)
        self.assertAlmostEqual(2 ** 1.5, math.exp(1.5 * math.log(2)), places=12)
        for invalid in [[], [math.inf], [math.nan]]:
            with self.assertRaises(ValueError):
                softmax(invalid)

    def test_kl_direction_support_and_entropy_decomposition(self):
        q, p = [3/4, 1/4], [1/2, 1/2]
        expected = 3/4 * math.log(3/2) + 1/4 * math.log(1/2)
        self.assertAlmostEqual(kl(q, p), expected, places=12)
        self.assertNotEqual(kl(q, p), kl(p, q))
        self.assertAlmostEqual(math.log(2) + sum(x * math.log(x) for x in q), expected, places=12)
        self.assertEqual(kl([1, 0], [1, 0]), 0)
        self.assertEqual(kl([1/2, 1/2], [1, 0]), math.inf)
        self.assertAlmostEqual(kl([1, 0], [1/2, 1/2]), math.log(2), places=12)
        with self.assertRaises(ValueError):
            kl([1, 1], [1/2, 1/2])


class NgramBridgeTests(unittest.TestCase):
    def setUp(self):
        self.fixture = read("data/part-i/ngram.json")
        self.expected = read("data/part-i/expected.json")

    def test_all_six_part_i_settings_and_exact_generation(self):
        f = self.fixture
        for case in self.expected["held_out"]:
            model = fit(f["train"], f["vocabulary"], case["n"], case["alpha"])
            for text in f["held_out"]:
                self.assertAlmostEqual(sequence_probability(model, text), case[text], places=12)
        model = fit(f["train"], f["vocabulary"])
        before = copy.deepcopy(model)
        result = generate(model, f["seed"], f["max_draws"])
        self.assertEqual(result["tokens"], self.expected["generation"]["tokens"])
        self.assertEqual(result["draws"], self.expected["generation"]["draws"])
        self.assertEqual(model, before)
        self.assertEqual(sum(sum(row.values()) for row in model["rows"].values()), 9)
        self.assertNotIn(("EOS",), model["rows"])

    def test_transfer_data_change_unseen_and_zero_are_distinct(self):
        vocabulary = self.fixture["vocabulary"]
        changed = fit(["ab", "ac"], vocabulary)
        self.assertEqual(probabilities(changed, ["a"]), [0, 1/2, 1/2, 0])
        self.assertAlmostEqual(sequence_probability(fit(["ab", "ab", "ac"], vocabulary, 2, 1), "ab"), 6/49, places=12)
        model = fit(self.fixture["train"], vocabulary, 3, 0)
        self.assertIsNone(probabilities(model, ["a", "a"]))
        self.assertEqual(sequence_probability(model, "aa"), 0)
        self.assertEqual(probabilities(fit([], vocabulary, 3, 1), ["a", "a"]), [1/4] * 4)
        with self.assertRaises(ValueError):
            fit(["ad"], vocabulary)


class TextTests(unittest.TestCase):
    def test_contract_outputs_idempotence_and_raw_retention(self):
        fixture = read("data/part-ii/text-contract.json")
        original = copy.deepcopy(fixture)
        for row in fixture["cases"]:
            self.assertEqual(search_key(row["raw"]), row["expected"], row["id"])
            self.assertEqual(search_key(search_key(row["raw"])), search_key(row["raw"]))
        self.assertEqual(fixture, original)
        for invalid in [None, b"abc", ["abc"], 750]:
            with self.assertRaisesRegex(TypeError, "raw must be a string"):
                search_key(invalid)

    def test_bytes_collisions_offsets_and_compatibility(self):
        fixture = read("data/part-ii/text-contract.json")
        for row in fixture["display_cases"]:
            actual = describe(row["raw"])
            for key in ["code_points", "utf8_hex", "code_point_count", "byte_count"]:
                self.assertEqual(actual[key], row[key])
        cases = {row["id"]: row for row in fixture["cases"]}
        self.assertNotEqual(cases["casefold-collision"]["raw"], cases["casefold-counterpart"]["raw"])
        self.assertEqual(search_key(cases["casefold-collision"]["raw"]), search_key(cases["casefold-counterpart"]["raw"]))
        self.assertNotEqual(search_key(cases["width"]["raw"]), search_key(cases["ascii-identifier"]["raw"]))
        loss = {row["kind"]: row for row in fixture["loss_counterexamples"]}
        self.assertEqual(unicodedata.normalize("NFKC", loss["compatibility"]["before"]), loss["compatibility"]["after"])
        raw = loss["offsets"]["before"]
        self.assertEqual((raw.index("750"), search_key(raw).index("750")), (6, 5))
        self.assertNotEqual(raw[5:8], "750")


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.fixture = load_fixture()
        self.expected = read("data/knowledge-assistant/ka0-expected.json")

    def test_full_same_set_bilingual_outputs_against_independent_evidence(self):
        results = [run_locale(self.fixture, locale) for locale in ["en", "zh-hans"]]
        for result in results:
            self.assertEqual(result["count_matrix"], self.expected["count_matrix"])
            self.assertEqual(result["document_frequency"], [3, 2, 1, 1, 1, 2, 1, 1])
            self.assertEqual(result["success_counts"], {"keyword": 5, "count": 6, "tfidf": 7})
            for method, rows in result["methods"].items():
                self.assertEqual([row["prediction"] for row in rows], self.expected[method + "_predictions"])
            for index, key in [(0, "tfidf_current_scores"), (1, "tfidf_geographic_scores")]:
                for actual, expected in zip(result["methods"]["tfidf"][index]["scores"], self.expected[key]):
                    self.assertAlmostEqual(actual, expected, places=12)
            for actual, expected in zip(result["methods"]["count"][1]["scores"], [1/math.sqrt(6), 1/math.sqrt(12), 3/math.sqrt(20), 1/2, 0]):
                self.assertAlmostEqual(actual, expected, places=12)
        self.assertEqual(results[0]["query_count_matrix"], results[1]["query_count_matrix"])
        self.assertEqual(results[0]["methods"], results[1]["methods"])

    def test_ties_abstention_oov_and_failure_labels_remain_visible(self):
        self.assertEqual(rank([1, 1], ["a", "b"])["prediction"], "a")
        self.assertIsNone(rank([0, 0], ["a", "b"])["prediction"])
        self.assertIsNone(rank([-0.2, -0.1], ["a", "b"])["prediction"])
        results = run_locale(self.fixture, "en")
        for method in results["methods"].values():
            self.assertIsNone(method[3]["prediction"])
            self.assertFalse(method[3]["success"])
            self.assertIsNone(method[8]["prediction"])
            self.assertTrue(method[8]["success"])
            self.assertEqual(method[7]["prediction"], "travel-v1")
            self.assertFalse(method[7]["success"])

    def test_corpus_change_updates_idf_without_changing_document_frequency(self):
        changed = copy.deepcopy(self.fixture)
        extra = copy.deepcopy(changed["documents"][0])
        extra["id"] = "extra"
        extra["index_text"] = {locale: "unrelated" for locale in ["en", "zh-hans"]}
        changed["documents"].append(extra)
        changed["candidate_order"].append("extra")
        result = run_locale(changed, "en")
        self.assertEqual(result["document_frequency"][0], 3)
        self.assertAlmostEqual(result["idf"][0], 1 + math.log(7/4), places=12)
        self.assertEqual(len(self.fixture["documents"]), 5)

    def test_word_order_collision_is_not_a_language_model(self):
        original = copy.deepcopy(self.fixture)
        reversed_cards = copy.deepcopy(self.fixture)
        for document in reversed_cards["documents"]:
            document["index_text"]["en"] = " ".join(reversed(document["index_text"]["en"].split()))
        self.assertEqual(run_locale(original, "en")["methods"], run_locale(reversed_cards, "en")["methods"])
        self.assertNotEqual(tokens(original["documents"][0]["index_text"]["en"], "en", original), tokens(reversed_cards["documents"][0]["index_text"]["en"], "en", reversed_cards))
        pairs = [list(zip(words, words[1:])) for words in run_locale(original, "en")["document_tokens"]]
        self.assertEqual({pair for row in pairs for pair in row}, {
            ("beijing", "lodging"), ("lodging", "600"), ("lodging", "lodging"), ("lodging", "750"),
            ("beijing", "beijing"), ("beijing", "train"), ("order", "processing"), ("order", "approval"),
        })
        self.assertEqual(pairs[2].count(("beijing", "beijing")), 2)


class EvidenceTests(unittest.TestCase):
    def test_measured_records_name_the_exact_sources_and_inputs(self):
        for record, source, dataset in [
            ("data/part-ii/classifier-run.json", "code/part-ii/classifier.py", "data/part-ii/classifier-data.json"),
            ("data/part-ii/nnlm-run.json", "code/part-ii/nnlm.py", "data/part-ii/nnlm-data.json"),
            ("data/knowledge-assistant/ka0-lexical-run.json", "code/knowledge-assistant/baselines.py", "data/knowledge-assistant/ka0-v1.json"),
        ]:
            result = read(record)
            for key, path in [("source_sha256", source), ("dataset_sha256", dataset)]:
                self.assertEqual(result[key], hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
