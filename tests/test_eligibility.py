import json
import os
from models.schemas import Scheme, CaseFacts
from services.eligibility import evaluate_scheme

def load_mock_scheme():
    path = os.path.join(os.path.dirname(__file__), "fixtures", "mock_scheme.json")
    with open(path, 'r') as f:
        data = json.load(f)
    return Scheme(**data)

def test_eligible_case():
    scheme = load_mock_scheme()
    facts = CaseFacts(applicant_facts={"age": 20, "income": 200000, "state": "UP"})
    results = evaluate_scheme(scheme.eligibility_criteria, facts)
    
    status_map = {r.criterion_id: r.status for r in results}
    assert status_map["mock_age_rule"] == "MET"
    assert status_map["mock_income_rule"] == "MET"
    assert status_map["mock_residency_rule"] == "MET"
    # mock_malformed_rule has invalid operator
    assert status_map["mock_malformed_rule"] == "UNCERTAIN"

def test_ineligible_case():
    scheme = load_mock_scheme()
    facts = CaseFacts(applicant_facts={"age": 20, "income": 300000, "state": "UP"})
    results = evaluate_scheme(scheme.eligibility_criteria, facts)
    
    status_map = {r.criterion_id: r.status for r in results}
    assert status_map["mock_income_rule"] == "NOT_MET"

def test_missing_fact():
    scheme = load_mock_scheme()
    facts = CaseFacts(applicant_facts={"age": 20}) # Missing income and state
    results = evaluate_scheme(scheme.eligibility_criteria, facts)
    
    status_map = {r.criterion_id: r.status for r in results}
    assert status_map["mock_income_rule"] == "UNCERTAIN"
    assert status_map["mock_residency_rule"] == "UNCERTAIN"
