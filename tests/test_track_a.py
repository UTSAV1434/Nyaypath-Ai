import json
import os
import pytest
from models.schemas import Scheme, CaseFacts
from services.eligibility import evaluate_scheme
from services.rejection_verifier import verify_rejection
from services.action_planner import plan_action

def load_scheme(filename):
    path = os.path.join(os.path.dirname(__file__), "..", "data", "schemes", filename)
    with open(path, 'r') as f:
        return Scheme(**json.load(f))

def test_source_integrity():
    # Load Scheme 1
    scheme1 = load_scheme("pm_usp_csss.json")
    valid_sources_1 = {s.source_id for s in scheme1.official_sources}
    for rule in scheme1.eligibility_criteria:
        assert rule.source_id in valid_sources_1, f"Rule {rule.criterion_id} has invalid source {rule.source_id}"

    # Load Scheme 2
    scheme2 = load_scheme("top_class_sc.json")
    valid_sources_2 = {s.source_id for s in scheme2.official_sources}
    for rule in scheme2.eligibility_criteria:
        assert rule.source_id in valid_sources_2, f"Rule {rule.criterion_id} has invalid source {rule.source_id}"

def test_academic_year_preservation():
    scheme1 = load_scheme("pm_usp_csss.json")
    for rule in scheme1.eligibility_criteria:
        assert rule.applicable_year in ["2025-26", "2022-23 onwards"], "Academic year silently modified!"
        
    scheme2 = load_scheme("top_class_sc.json")
    for rule in scheme2.eligibility_criteria:
        assert rule.applicable_year == "2026-27"

def test_cross_scheme_isolation():
    scheme1 = load_scheme("pm_usp_csss.json")
    scheme2 = load_scheme("top_class_sc.json")
    
    # Ensure scheme 1 rules don't exist in scheme 2
    s1_rule_ids = {r.criterion_id for r in scheme1.eligibility_criteria}
    s2_rule_ids = {r.criterion_id for r in scheme2.eligibility_criteria}
    assert s1_rule_ids.isdisjoint(s2_rule_ids), "Rule leakage between schemes!"

def test_uncertainty_conflict():
    scheme1 = load_scheme("pm_usp_csss.json")
    
    # Test missing fact -> UNCERTAIN
    facts = CaseFacts(applicant_facts={"class_12_percentile": 85}) # Missing income, course, etc.
    res = evaluate_scheme(scheme1.eligibility_criteria, facts)
    status_map = {r.criterion_id: r.status for r in res}
    assert status_map["80th_percentile"] == "MET"
    assert status_map["family_income"] == "UNCERTAIN"

def test_end_to_end_case_A():
    # Complete info, eligible
    scheme1 = load_scheme("pm_usp_csss.json")
    facts = CaseFacts(applicant_facts={
        "class_12_percentile": 85,
        "family_income": 300000,
        "course_mode": "Regular",
        "receiving_other_scholarship": False,
        "is_diploma_student": False,
        "drop_after_12th": False
    })
    res = evaluate_scheme(scheme1.eligibility_criteria, facts)
    assert all(r.status == "MET" for r in res)

def test_end_to_end_case_B():
    # Ineligible due to income
    scheme1 = load_scheme("pm_usp_csss.json")
    facts = CaseFacts(applicant_facts={
        "class_12_percentile": 85,
        "family_income": 500000,
        "course_mode": "Regular",
        "receiving_other_scholarship": False,
        "is_diploma_student": False,
        "drop_after_12th": False
    })
    res = evaluate_scheme(scheme1.eligibility_criteria, facts)
    status_map = {r.criterion_id: r.status for r in res}
    assert status_map["family_income"] == "NOT_MET"

def test_end_to_end_case_D():
    # Rejection matches official criterion
    scheme1 = load_scheme("pm_usp_csss.json")
    facts = CaseFacts(
        applicant_facts={
            "class_12_percentile": 85,
            "family_income": 500000,
            "course_mode": "Regular",
            "receiving_other_scholarship": False,
            "is_diploma_student": False,
            "drop_after_12th": False
        },
        stated_rejection_reason="Income"
    )
    res = verify_rejection(facts, scheme1.eligibility_criteria)
    assert res.mapped_criterion_id == "mock_income_rule" # Stubbed gemini mapping
    assert res.status == "UNABLE_TO_VERIFY"

def test_nsp_date_validation():
    scheme1 = load_scheme("pm_usp_csss.json")
    app_process = scheme1.application_process[0]
    assert "31-10-2026" in app_process.description
    assert "15-11-2026" in app_process.description
    assert "30-11-2026" in app_process.description

def test_no_appeal_deadline_confusion():
    scheme1 = load_scheme("pm_usp_csss.json")
    assert scheme1.appeal_process["deadline"] == "UNCERTAIN"

def test_historical_pm_usp_rule_preservation():
    scheme1 = load_scheme("pm_usp_csss.json")
    for rule in scheme1.eligibility_criteria:
        if rule.source_id == "pmusp_csss_faq_2025_26":
            assert rule.applicable_year == "2025-26"
            
def test_source_freshness_validation():
    scheme1 = load_scheme("pm_usp_csss.json")
    for source in scheme1.official_sources:
        assert hasattr(source, "retrieved_at")
        assert source.source_status in ["CURRENT", "HISTORICAL", "UNCERTAIN", "CONFLICTING"]
        
def test_categorical_education_rule():
    scheme2 = load_scheme("top_class_sc.json")
    ed_rule = next(r for r in scheme2.eligibility_criteria if r.criterion_id == "education_level")
    assert ed_rule.rule_type == "boolean"
    assert ed_rule.operator == "=="
    assert ed_rule.value is True

def test_lower_education_level_regression():
    # Ensure that passing "10th" or false for beyond_12 does not satisfy the rule
    scheme2 = load_scheme("top_class_sc.json")
    facts = CaseFacts(
        applicant_facts={
            "caste": "SC",
            "is_beyond_class_12": False,
            "is_empanelled_institution": "True",
            "family_income": 500000
        }
    )
    from services.eligibility import evaluate_scheme
    res = evaluate_scheme(scheme2.eligibility_criteria, facts)
    status_map = {r.criterion_id: r.status for r in res}
    assert status_map["education_level"] == "NOT_MET"

def test_conditional_document_validation():
    scheme1 = load_scheme("pm_usp_csss.json")
    doc = scheme1.required_documents[0]
    assert hasattr(doc, "mandatory")
    assert hasattr(doc, "condition")
    assert doc.condition is not None

def test_rejection_condition_vs_exhaustive():
    scheme1 = load_scheme("pm_usp_csss.json")
    rej = scheme1.rejection_reasons[0]
    assert hasattr(rej, "related_criterion_id")
    assert rej.related_criterion_id == "family_income"
    assert rej.reason_id == "income_too_high"

