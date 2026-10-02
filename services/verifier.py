from typing import Optional
from models.schemas import Scheme, EligibilityResult, RejectionVerification, ActionPlan, FinalVerification

def final_verify(scheme: Scheme, eligibility_results: list[EligibilityResult], rejection: RejectionVerification, plan: Optional[ActionPlan] = None) -> FinalVerification:
    """
    Deterministic final safety check preventing hallucinated sources.
    """
    unsupported = []
    
    valid_source_ids = {s.source_id for s in scheme.official_sources}
    
    for res in eligibility_results:
        if not res.citation or not res.citation.source_id:
            unsupported.append(f"Eligibility conclusion for {res.criterion_id} has no source_id.")
        elif res.citation.source_id not in valid_source_ids:
            unsupported.append(f"Eligibility conclusion for {res.criterion_id} cites non-existent source {res.citation.source_id}.")

    if rejection.citation:
        if not rejection.citation.source_id:
            unsupported.append("Rejection verification has no source_id.")
        elif rejection.citation.source_id not in valid_source_ids:
            unsupported.append(f"Rejection verification cites non-existent source {rejection.citation.source_id}.")

    has_uncertain_eligibility = any(r.status == "UNCERTAIN" for r in eligibility_results)

    if unsupported:
        return FinalVerification(
            status="UNSUPPORTED",
            unsupported_claims=unsupported,
            explanation="Found material conclusions without valid sources."
        )

    if has_uncertain_eligibility:
        return FinalVerification(
            status="UNCERTAIN",
            unsupported_claims=[],
            explanation="Pipeline contains uncertain facts or missing rules."
        )
        
    if plan is None:
        return FinalVerification(
            status="UNCERTAIN",
            unsupported_claims=[],
            explanation="Verification incomplete. Action Plan not yet available."
        )

    if plan.action_route == "UNCERTAIN":
        return FinalVerification(
            status="UNCERTAIN",
            unsupported_claims=[],
            explanation="Pipeline contains uncertain facts or missing rules."
        )

    return FinalVerification(
        status="PASS",
        unsupported_claims=[],
        explanation="All conclusions are source-backed and deterministic."
    )

