# SPDX-License-Identifier: Apache-2.0
"""Versioned search keys, not a universal text-cleaning policy."""
import unicodedata

VERSION = "search-key-v1"


def search_key(raw):
    if not isinstance(raw, str):
        raise TypeError("raw must be a string")
    composed = unicodedata.normalize("NFC", raw)
    folded = unicodedata.normalize("NFC", composed.casefold())
    return " ".join(folded.split())


def describe(raw):
    if not isinstance(raw, str):
        raise TypeError("raw must be a string")
    return {"code_points": [f"U+{ord(c):04X}" for c in raw], "utf8_hex": raw.encode("utf-8").hex(" "),
            "code_point_count": len(raw), "byte_count": len(raw.encode("utf-8")), "key": search_key(raw)}
