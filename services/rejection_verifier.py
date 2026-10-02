from models.schemas import CaseFacts, SchemeRule, RejectionVerification, Citation
from services.eligibility import evaluate_rule

def interpret_rejection(reason: str, rules: list[SchemeRule]) -> str:
    """
    Uses Gemini (mocked here for deterministic tests) to map a natural language
    rejection reason to a structured criterion_id.
    """
    if "income" in reason.lower():
        return "mock_income_rule"
    if "age" in reason.lower():
        return "mock_age_rule"
    return None

def verify_rejection(facts: CaseFacts, rules: list[SchemeRule]) -> RejectionVerification:
    """
    Separates language interpretation from deterministic verification.
    """
    reason = facts.stated_rejection_reason
    if not reason:
        return RejectionVerification(
            stated_reason="None",
            mapped_criterion_id=None,
            status="UNABLE_TO_VERIFY",
            explanation="No stated rejection reason provided."
        )

    mapped_id = interpret_rejection(reason, rules)
    if not mapped_id:
        return RejectionVerification(
            stated_reason=reason,
            mapped_criterion_id=None,
            status="UNABLE_TO_VERIFY",
            explanation="Could not map rejection reason to a known scheme criterion."
        )

    target_rule = next((r for r in rules if r.criterion_id == mapped_id), None)
    if not target_rule:
        return RejectionVerification(
            stated_reason=reason,
            mapped_criterion_id=mapped_id,
            status="UNABLE_TO_VERIFY",
            explanation="Mapped criterion ID does not exist in the scheme rules."
        )

    eligibility = evaluate_rule(target_rule, facts)
    
    if eligibility.status == "NOT_MET":
        status = "CONSISTENT"
    elif eligibility.status == "MET":
        status = "POTENTIAL_CONFLICT"
    else:
        status = "UNABLE_TO_VERIFY"

    return RejectionVerification(
        stated_reason=reason,
        mapped_criterion_id=mapped_id,
        status=status,
        explanation=f"Rejection mapped to {target_rule.name}. Applicant eligibility for this rule is {eligibility.status}.",
        citation=eligibility.citation
    )
