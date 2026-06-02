import json
import os
import re


def load_enhanced_rules(path="enhanced_rules.json"):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf8") as file:
        return json.load(file)


def search_rules(issue, limit=10, path="enhanced_rules.json"):
    words = [word for word in re.findall(r"[A-Za-z0-9_-]+", issue.lower()) if len(word) > 2]
    if not words:
        return []

    results = []
    for rule in load_enhanced_rules(path):
        rule_text = str(rule.get("rule", "")).lower()
        score = sum(1 for word in words if word in rule_text)
        if score:
            enriched = dict(rule)
            enriched["match_score"] = score
            results.append(enriched)

    return sorted(results, key=lambda item: item["match_score"], reverse=True)[:limit]


def format_rule_result(issue, rule):
    return f"""
Issue:
{issue}

Rule:
{rule.get('rule', 'N/A')}

Category:
{rule.get('category', 'N/A')}

Severity:
{rule.get('severity', 'N/A')}

Page:
{rule.get('page', 'N/A')}

Clause:
{rule.get('clause', 'N/A')}

Source:
{rule.get('source', 'N/A')}
""".strip()


if __name__ == "__main__":
    search = input("Enter issue: ")
    print("\nRESULTS\n")
    for result in search_rules(search, limit=5):
        print(format_rule_result(search, result))
        print("\n----------------------")
