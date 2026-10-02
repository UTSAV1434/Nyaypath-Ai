import json
import os
from models.schemas import Scheme, CaseFacts, EligibilityResult, Citation, RejectionVerification, ActionPlan, EvidenceItem
from services.action_planner import plan_action

def load_mock_scheme():
    path = os.path.join(os.path.dirname(__file__), "fixtures", "mock_scheme.json")
    with open(path, 'r') as f:
        data = json.load(f)
    return Scheme(**data)

def test_unsupported_appeal_route():
    scheme = load_mock_scheme()
    # Modify the scheme to have no supported route
    scheme.appeal_process["available"] = "UNCERTAIN"
    
    eligibility = [
        EligibilityResult(criterion_id="mock_age_rule", status="MET", explanation="", citation=Citation(source_id="mock", official_source="x"))
    ]
    rejection = RejectionVerification(stated_reason="", mapped_criterion_id="mock_age_rule", status="POTENTIAL_CONFLICT", explanation="", citation=Citation(source_id="mock", official_source="x"))
    
    plan = plan_action(scheme, eligibility, rejection, [])
    assert plan.action_route == "UNCERTAIN"
    assert "unverifiable appeal process" in plan.reason

def test_uncertain_state_propagation():
    scheme = load_mock_scheme()
    
    eligibility = [
        EligibilityResult(criterion_id="mock_age_rule", status="UNCERTAIN", explanation="", citation=Citation(source_id="mock", official_source="x"))
    ]
    rejection = RejectionVerification(stated_reason="", mapped_criterion_id="mock_age_rule", status="UNABLE_TO_VERIFY", explanation="", citation=Citation(source_id="mock", official_source="x"))
    
    plan = plan_action(scheme, eligibility, rejection, [])
    assert plan.action_route == "UNCERTAIN"
    assert "Missing required rules" in plan.reason
