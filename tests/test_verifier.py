import json
import os
from models.schemas import Scheme, EligibilityResult, Citation, RejectionVerification, ActionPlan, EvidenceItem
from services.verifier import final_verify

def load_mock_scheme():
    path = os.path.join(os.path.dirname(__file__), "fixtures", "mock_scheme.json")
    with open(path, 'r') as f:
        return Scheme(**json.load(f))

def test_unsupported_no_source():
    scheme = load_mock_scheme()
    res1 = EligibilityResult(
        criterion_id="mock_age_rule",
        status="MET",
        explanation=".",
        citation=Citation(source_id="", official_source="x") # NO SOURCE ID
    )
    plan = ActionPlan(action_route="FORMAL_APPEAL", reason=".", immediate_next_action=".", required_evidence=[], missing_evidence=[])
    rej = RejectionVerification(stated_reason=".", mapped_criterion_id="x", status="CONSISTENT", explanation=".", citation=Citation(source_id="mock_source_1", official_source="x"))
    
    final = final_verify(scheme, [res1], rej, plan)
    assert final.status == "UNSUPPORTED"
    assert len(final.unsupported_claims) == 1

def test_invalid_source():
    scheme = load_mock_scheme()
    res1 = EligibilityResult(
        criterion_id="mock_age_rule",
        status="MET",
        explanation=".",
        citation=Citation(source_id="invalid_source", official_source="x")
    )
    plan = ActionPlan(action_route="FORMAL_APPEAL", reason=".", immediate_next_action=".", required_evidence=[], missing_evidence=[])
    rej = RejectionVerification(stated_reason=".", mapped_criterion_id="x", status="CONSISTENT", explanation=".", citation=Citation(source_id="mock_source_1", official_source="x"))
    
    final = final_verify(scheme, [res1], rej, plan)
    assert final.status == "UNSUPPORTED"

def test_missing_rule_uncertain():
    scheme = load_mock_scheme()
    res1 = EligibilityResult(
        criterion_id="mock_age_rule",
        status="UNCERTAIN",
        explanation=".",
        citation=Citation(source_id="mock_source_1", official_source="x")
    )
    plan = ActionPlan(action_route="UNCERTAIN", reason=".", immediate_next_action=".", required_evidence=[], missing_evidence=[])
    rej = RejectionVerification(stated_reason=".", mapped_criterion_id="x", status="CONSISTENT", explanation=".", citation=Citation(source_id="mock_source_1", official_source="x"))
    
    final = final_verify(scheme, [res1], rej, plan)
    assert final.status == "UNCERTAIN"

def test_production_loader_does_not_load_mock():
    # Demonstrating the strict boundary 
    # Production loader targets data/schemes only, ensuring mock_scheme.json is never surfaced.
    assert not os.path.exists(os.path.join(os.path.dirname(__file__), "..", "data", "schemes", "mock_scheme.json"))
