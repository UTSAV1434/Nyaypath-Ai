from models.schemas import EligibilityResult, RejectionVerification, ActionPlan, EvidenceItem, Scheme

def plan_action(scheme: Scheme, eligibility: list[EligibilityResult], rejection: RejectionVerification, evidence: list[EvidenceItem]) -> ActionPlan:
    """
    Synthesizes eligibility, verification, and appeal rules into an action state.
    Does NOT equate eligibility directly with formal appeal viability.
    """
    is_ineligible = any(r.status == "NOT_MET" for r in eligibility)
    is_uncertain = any(r.status == "UNCERTAIN" for r in eligibility)

    missing = [e for e in evidence if e.status == "MISSING"]
    
    appeal_info = scheme.appeal_process
    supported_route = appeal_info.get("available")
    
    if is_uncertain or not supported_route or supported_route == "UNCERTAIN":
        return ActionPlan(
            action_route="UNCERTAIN",
            reason="Missing required rules, facts, or unverifiable appeal process.",
            authority=appeal_info.get("authority"),
            deadline=appeal_info.get("deadline"),
            required_evidence=evidence,
            missing_evidence=missing,
            immediate_next_action="Provide missing information or consult authority."
        )

    if is_ineligible:
        return ActionPlan(
            action_route="NO_VERIFIED_ROUTE",
            reason="Applicant does not meet authoritative eligibility criteria.",
            authority=appeal_info.get("authority"),
            deadline=appeal_info.get("deadline"),
            required_evidence=evidence,
            missing_evidence=missing,
            immediate_next_action="No viable appeal available."
        )

    if rejection.status == "POTENTIAL_CONFLICT" and supported_route:
        return ActionPlan(
            action_route=supported_route,
            reason="Rejection conflicts with authoritative rules. Applicant is eligible.",
            authority=appeal_info.get("authority"),
            deadline=appeal_info.get("deadline"),
            required_evidence=evidence,
            missing_evidence=missing,
            immediate_next_action=f"Prepare {supported_route} submission."
        )

    return ActionPlan(
        action_route="UNCERTAIN",
        reason="Unable to determine viable action.",
        authority=None,
        deadline=None,
        required_evidence=[],
        missing_evidence=[],
        immediate_next_action="Review case details."
    )
