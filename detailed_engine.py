from urllib.parse import unquote

from analysis_engine import search_rules
from remarks_engine import generate_ntpc_remark


def infer_clause_and_requirement(issue):
    matches = search_rules(issue, limit=1)
    if matches:
        rule = matches[0]
        return (
            rule.get("clause") or "NTPC Engineering Requirement",
            rule.get("rule") or "Further engineering verification required.",
            rule.get("severity") or "Medium",
            rule.get("source") or "NTPC project specification",
        )

    lower = issue.lower()
    if "wind" in lower:
        return (
            "Section VI Clause 7.3.2 + IS875 Part-3",
            "Vendor shall submit complete wind load calculations including pressure coefficient, load combinations and design basis as per IS875 Part-3.",
            "High",
            "NTPC Section VI",
        )
    if "rcdc" in lower:
        return (
            "Section VI Clause 5.2",
            "RCDC design output shall be attached for RCC verification and foundation validation.",
            "Medium",
            "NTPC Section VI",
        )
    if "cable" in lower:
        return (
            "Section VI Electrical Clause 8.4",
            "Cable sizing calculations shall include voltage drop, ampacity and load criteria.",
            "High",
            "NTPC Section VI",
        )
    if "foundation" in lower:
        return (
            "Section VI Foundation Clause 4.2",
            "Foundation calculations shall include soil data, SBC, load transfer and design basis.",
            "High",
            "NTPC Section VI",
        )

    return (
        "Section VI General Engineering",
        "Further engineering verification required.",
        "Medium",
        "NTPC Section VI",
    )


def get_detail(issue, pdf=None):
    issue = unquote(issue)
    clause, requirement, severity, source = infer_clause_and_requirement(issue)

    return {
        "issue": issue,
        "section": "NTPC Section VI",
        "clause": clause,
        "requirement": requirement,
        "finding": issue,
        "severity": severity,
        "engineering_impact": "Potential delay in approval cycle, rework at site, or non-compliance during engineering submission.",
        "root_cause": "Vendor submission appears incomplete, unclear, or not traceable to the required NTPC engineering basis.",
        "historical": "Previously approved vendor packages normally contain supporting calculations, clause references, and coordinated drawings.",
        "ai_reasoning": f"AI compared the vendor submission observation with NTPC rules, enhanced rule metadata, and approved-style drawing expectations.\n\nObservation detected:\n{issue}",
        "recommendation": generate_ntpc_remark(issue),
        "suggested_status": "Approved with comments" if severity.lower() != "high" else "Revision required",
        "source": source,
        "pdf": pdf,
    }
