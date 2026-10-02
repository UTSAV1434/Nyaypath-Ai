import json
import os
from models.schemas import Scheme, CaseFacts
from services.rejection_verifier import verify_rejection

def load_mock_scheme():
    path = os.path.join(os.path.dirname(__file__), "fixtures", "mock_scheme.json")
    with open(path, 'r') as f:
        data = json.load(f)
    return Scheme(**data)

def test_consistent_rejection():
    scheme = load_mock_scheme()
    facts = CaseFacts(
        applicant_facts={"age": 20, "income": 300000, "state": "UP"},
        stated_rejection_reason="Income too high"
    )
    res = verify_rejection(facts, scheme.eligibility_criteria)
    assert res.mapped_criterion_id == "mock_income_rule"
    assert res.status == "CONSISTENT"

def test_potentially_conflicting_rejection():
    scheme = load_mock_scheme()
    facts = CaseFacts(
        applicant_facts={"age": 20, "income": 100000, "state": "UP"},
        stated_rejection_reason="Income too high"
    )
    res = verify_rejection(facts, scheme.eligibility_criteria)
    assert res.mapped_criterion_id == "mock_income_rule"
    assert res.status == "POTENTIAL_CONFLICT"

def test_unable_to_verify():
    scheme = load_mock_scheme()
    facts = CaseFacts(
        applicant_facts={"age": 20, "income": 100000, "state": "UP"},
        stated_rejection_reason="Failed randomly"
    )
    res = verify_rejection(facts, scheme.eligibility_criteria)
    assert res.status == "UNABLE_TO_VERIFY"
