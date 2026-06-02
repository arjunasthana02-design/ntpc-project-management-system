from analysis_engine import search_rules


def generate_ntpc_remark(issue):
    matches = search_rules(issue, limit=1)
    if matches:
        rule = matches[0]
        clause = rule.get("clause", "Relevant NTPC clause")
        source = rule.get("source", "NTPC engineering specification")
    else:
        clause = "Relevant NTPC engineering requirement"
        source = "NTPC project requirements"

    return f"""
Please note that the submitted design/drawing requires review against NTPC requirements.

Issue Identified:
{issue}

Relevant Clause:
{clause}

Required Action:
Kindly review and revise the submission in line with the specified requirement. Provide
supporting calculation, drawing reference, datasheet, or compliance note as applicable.

Reference:
{source}
""".strip()


if __name__ == "__main__":
    issue = input("Enter issue: ")
    print("\nNTPC Remark:\n")
    print(generate_ntpc_remark(issue))
