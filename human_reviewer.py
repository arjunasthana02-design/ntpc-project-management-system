def build_review_prompt(engineering, layout, foundation, electrical, structural, safety, score):
    return f"""
You are a Senior NTPC engineering reviewer.

Review the vendor drawing with practical engineering judgement. Treat missing critical
calculations, clearances, safety provisions, electrical design basis, and foundation
inputs as higher risk. Treat minor documentation gaps as comments unless they affect
constructability, safety, statutory compliance, or equipment reliability.

Vendor Drawing Accuracy: {score}%

Engineering Issues:
{engineering}

Layout Issues:
{layout}

Foundation Issues:
{foundation}

Electrical Issues:
{electrical}

Structural Issues:
{structural}

Safety Issues:
{safety}

Provide:
1. Executive summary
2. Critical findings
3. Medium findings
4. Low findings
5. Approval recommendation
6. NTPC review remarks
7. Final status: Approved / Approved with comments / Revision required
"""


def fallback_review(engineering, layout, foundation, electrical, structural, safety, score):
    issue_count = sum(len(items or []) for items in [engineering, layout, foundation, electrical, structural, safety])
    if score >= 75 and issue_count <= 8:
        status = "Approved with comments"
    elif score >= 55:
        status = "Revision required for listed comments"
    else:
        status = "Revision required"

    return f"""
Executive Summary
The drawing has been checked against NTPC rule categories and available review logic.
Calculated vendor accuracy is {score}%. {issue_count} review observations were identified.

Critical Findings
Review all safety, foundation, structural, electrical, and layout observations before approval.

Medium Findings
Resolve missing calculations, design basis references, and drawing coordination gaps.

Low Findings
Improve documentation traceability, clause references, and supporting annexures.

Approval Recommendation
{status}

NTPC Remarks
Vendor shall revise or justify all listed observations and resubmit with supporting documents
where required. Approved-style minor documentation gaps may be closed with comments only.

Final Status
{status}
""".strip()


def review(engineering, layout, foundation, electrical, structural, safety, score):
    prompt = build_review_prompt(engineering, layout, foundation, electrical, structural, safety, score)

    try:
        import ollama

        response = ollama.chat(
            model="llama3:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception:
        return fallback_review(engineering, layout, foundation, electrical, structural, safety, score)
