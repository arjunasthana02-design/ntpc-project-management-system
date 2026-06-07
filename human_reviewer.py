def build_review_prompt(engineering, layout, foundation, electrical, structural, safety, score):
    return f"""
You are a Senior NTPC engineering reviewer.

Review the vendor drawing as a professional engineering submission, not as a generic
document summary. Use practical site, design, compliance, constructability, safety,
quality, and approval-cycle judgement. Treat missing calculations, clearances, safety
provisions, electrical design basis, foundation inputs, drawing coordination gaps, and
traceability gaps as higher risk.

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
1. Executive summary with approval posture
2. Document-specific observations
3. Clause-level or requirement-level reasoning where possible
4. Engineering impact for every major observation
5. Compliance impact for every major observation
6. Risk level and reason
7. Recommended vendor action
8. Approval recommendation
9. NTPC human-review style remarks
10. Final status: Approved / Approved with comments / Revision required
"""


def fallback_review(engineering, layout, foundation, electrical, structural, safety, score):
    categories = [
        ("Engineering", engineering, "design basis, calculations, load assumptions, and interdisciplinary coordination"),
        ("Layout", layout, "access, clearances, maintainability, equipment spacing, and constructability"),
        ("Foundation", foundation, "soil basis, pile or footing design, anchor details, and load transfer"),
        ("Electrical", electrical, "earthing, cable sizing, protection, voltage-drop, and equipment interface compliance"),
        ("Structural", structural, "steel/RCC member adequacy, bracing, welding, connection, and stability checks"),
        ("Safety", safety, "fire, emergency access, PPE, hazard control, statutory safety, and operational protection"),
    ]
    issue_count = sum(len(items or []) for _, items, _ in categories)
    if score >= 75 and issue_count <= 8:
        status = "Approved with comments"
        posture = "The submission is broadly acceptable, subject to closure of listed observations."
    elif score >= 55:
        status = "Revision required for listed comments"
        posture = "The submission has usable engineering content but requires targeted revision before approval."
    else:
        status = "Revision required"
        posture = "The submission has material compliance gaps and should not be approved in its current form."

    critical_sections = []
    detailed_sections = []
    for category, observations, basis in categories:
        observations = observations or []
        if observations:
            risk = "High" if category in ["Foundation", "Electrical", "Structural", "Safety"] or score < 55 else "Medium"
            critical_sections.append(f"- {category}: {len(observations)} observation(s), risk level {risk}.")
            detailed_sections.append(f"""
{category} Review
What was found:
{chr(10).join('- ' + str(item) for item in observations[:6])}

Why it matters:
This affects {basis}. Incomplete or unclear information can cause approval delay, site rework,
non-compliance during execution, or difficulty proving design adequacy during NTPC review.

Engineering impact:
The vendor must demonstrate that the drawing package is coordinated with design calculations,
site execution constraints, and applicable NTPC/Indian Standard requirements.

Compliance impact:
The missing or weak evidence should be closed through revised drawings, calculation annexures,
datasheets, notes, references, or compliance statements traceable to the relevant requirement.

Recommended action:
Submit a revision or technical clarification addressing each observation with marked-up drawing
references and supporting calculations.
""".strip())
        else:
            detailed_sections.append(f"""
{category} Review
What was found:
- No major gap was detected by the current rule-matching engine in this category.

Recommended action:
Keep the current evidence traceable in the next submission and ensure cross-references remain
consistent with the final drawing revision.
""".strip())

    return f"""
Executive Summary
The drawing has been checked against NTPC review categories, learned project knowledge, and
available rule logic. Calculated vendor accuracy is {score}%. {issue_count} review observations
were identified. {posture}

Critical Findings
{chr(10).join(critical_sections) if critical_sections else "- No high-severity category was detected by the current review logic."}

Detailed Engineering Review
{chr(10).join(detailed_sections)}

Risk Identification
Risk level is {"High" if score < 55 else "Medium" if score < 75 or issue_count > 8 else "Low"} because the review score, number of
observations, and category exposure indicate the likely approval and execution risk.

Approval Recommendation
{status}

NTPC Remarks
Vendor shall revise or justify all listed observations and resubmit with supporting documents
where required. Each closure shall identify the drawing sheet, revision number, calculation or
document reference, and the exact response to the NTPC observation.

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
