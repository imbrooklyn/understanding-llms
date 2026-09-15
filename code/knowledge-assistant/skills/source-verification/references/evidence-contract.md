# Evidence contract 1.0.0

License: Apache-2.0. Original implementation guidance.

The request is a JSON object with `locale` (`en` or `zh-hans`), ISO `on_date`, `topic` (`travel` or `approval`), `context`, and `answer`. Read the pinned corpus at data/knowledge-assistant/ka4-documents-v1.json. The host may pass a modified corpus for an explicit negative test, never as a new trust root.

A date interval includes valid_from and excludes valid_until; null has no recorded upper bound. Only fictional-policy-office is allowlisted. Evidence must equal its cited source/version and complete support span. The answer must equal the exact source quotation plus citation under KA-4, with a matching amount. An authentic source may still be wrong; this test does not establish real-world truth. Historical v1 is valid for a 2025 question and invalid for a 2026 question.

A report records `supported`, `authority_ok`, `context_matches`, the inherited support details and a reason. Loading this document grants no capability. The host verifies the package against its separately reviewed source inventory before executing the helper.
