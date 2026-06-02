import json
import os
import re
from functools import lru_cache

import fitz


CATEGORY_KEYWORDS = {
    "engineering": ["wind", "staad", "rcdc", "load", "seismic", "design", "calculation", "analysis"],
    "layout": ["layout", "clearance", "access", "spacing", "road", "plot", "arrangement"],
    "foundation": ["foundation", "pile", "soil", "sbc", "footing", "pedestal", "anchor"],
    "electrical": ["earthing", "cable", "transformer", "breaker", "voltage", "switchyard", "relay"],
    "structural": ["beam", "column", "steel", "structure", "bracing", "member", "welding"],
    "safety": ["fire", "emergency", "safety", "ppe", "hazard", "protection", "evacuation"],
}

STOP_WORDS = {
    "shall", "should", "with", "from", "this", "that", "have", "been", "will", "ntpc",
    "contractor", "vendor", "drawing", "document", "requirement", "submitted", "details",
    "where", "there", "their", "which", "during", "based", "under", "section",
}


def extract_text(pdf_path):
    """Extract lowercase text from a vendor drawing PDF."""
    text_parts = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts).lower()


@lru_cache(maxsize=1)
def load_rules():
    """Load the most review-friendly rule list available in the project."""
    for filename in ["clean_rules.json", "ntpc_rules.json"]:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf8") as file:
                rules = json.load(file)
            return [str(rule) for rule in rules if str(rule).strip()]
    return []


def tokenize(text):
    return re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", text.lower())


def rule_keywords(rule, limit=12):
    keywords = []
    for word in tokenize(rule):
        if word not in STOP_WORDS and word not in keywords:
            keywords.append(word)
        if len(keywords) >= limit:
            break
    return keywords


def classify_rule(rule):
    text = rule.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "engineering"


def score_rule_against_text(rule, vendor_text):
    keywords = rule_keywords(rule)
    if not keywords:
        return 0.0
    matched = sum(1 for keyword in keywords if keyword in vendor_text)
    return matched / len(keywords)


def check_vendor(pdf_path):
    """Review a vendor drawing against NTPC rules and return dashboard-ready analytics."""
    vendor_text = extract_text(pdf_path)
    rules = load_rules()

    buckets = {
        "engineering": [],
        "layout": [],
        "foundation": [],
        "electrical": [],
        "structural": [],
        "safety": [],
    }

    found = 0
    total = min(len(rules), 300)
    if total == 0:
        return {
            "engineering": ["No NTPC rules were loaded for review."],
            "layout": [],
            "foundation": [],
            "electrical": [],
            "structural": [],
            "safety": [],
            "score": 0,
            "found": 0,
            "total": 0,
        }

    for rule in rules[:total]:
        match_score = score_rule_against_text(rule, vendor_text)
        if match_score >= 0.22:
            found += 1
            continue

        category = classify_rule(rule)
        if category in buckets and len(buckets[category]) < 8:
            buckets[category].append(rule[:160])

    score = int((found / total) * 100)

    return {
        "engineering": buckets["engineering"][:5],
        "layout": buckets["layout"][:5],
        "foundation": buckets["foundation"][:5],
        "electrical": buckets["electrical"][:5],
        "structural": buckets["structural"][:5],
        "safety": buckets["safety"][:5],
        "score": score,
        "found": found,
        "total": total,
    }
