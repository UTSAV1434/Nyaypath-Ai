from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class Citation(BaseModel):
    source_id: str
    official_source: str
    section: Optional[str] = None
    page: Optional[str] = None

class CaseFacts(BaseModel):
    applicant_facts: Dict[str, Any]
    stated_rejection_reason: Optional[str] = None
    application_date: Optional[str] = None
    rejection_date: Optional[str] = None
    reference_id: Optional[str] = None
    available_documents: List[str] = Field(default_factory=list)

class EvidenceItem(BaseModel):
    id: str
    name: str
    status: str # AVAILABLE, MISSING, NEEDS_VERIFICATION
    source_id: str

class SchemeRule(BaseModel):
    criterion_id: str
    name: str
    description: str
    rule_type: str
    field: str
    operator: str
    value: Any
    source_id: str
    source_section: Optional[str] = None
    source_page: Optional[str] = None
    applicable_year: Optional[str] = None

class OfficialSource(BaseModel):
    source_id: str
    title: str
    url: str
    document_type: str
    applicable_year: str
    last_verified: str
    retrieved_at: Optional[str] = None
    source_status: Optional[str] = None

class RequiredDocument(BaseModel):
    document_id: str
    name: str
    purpose: str
    mandatory: bool = True
    condition: Optional[str] = None
    source_id: str
    source_section: Optional[str] = None
    source_page: Optional[str] = None

class RejectionCondition(BaseModel):
    reason_id: str
    description: str
    related_criterion_id: str
    source_id: str
    source_section: Optional[str] = None
    source_page: Optional[str] = None

class ApplicationProcessStep(BaseModel):
    step_id: str
    description: str
    authority: str
    source_id: str
    source_section: Optional[str] = None
    source_page: Optional[str] = None

class Scheme(BaseModel):
    scheme_id: str
    scheme_name: str
    department: str
    academic_year: str
    description: str
    official_sources: List[OfficialSource]
    eligibility_criteria: List[SchemeRule]
    required_documents: List[RequiredDocument]
    application_process: List[ApplicationProcessStep]
    rejection_reasons: List[RejectionCondition]
    appeal_process: Dict[str, Any]

class EligibilityResult(BaseModel):
    criterion_id: str
    status: str  # MET, NOT_MET, UNCERTAIN
    explanation: str
    citation: Optional[Citation] = None

class RejectionVerification(BaseModel):
    stated_reason: str
    mapped_criterion_id: Optional[str]
    status: str  # CONSISTENT, POTENTIAL_CONFLICT, UNABLE_TO_VERIFY
    explanation: str
    citation: Optional[Citation] = None

class ActionPlan(BaseModel):
    action_route: str # FORMAL_APPEAL, GRIEVANCE, CORRECTION, REVIEW, NO_VERIFIED_ROUTE, UNCERTAIN
    reason: str
    authority: Optional[str] = None
    deadline: Optional[str] = None
    required_evidence: List[EvidenceItem]
    missing_evidence: List[EvidenceItem]
    immediate_next_action: str

class FinalVerification(BaseModel):
    status: str  # PASS, UNSUPPORTED, UNCERTAIN, POTENTIAL_CONFLICT
    unsupported_claims: List[str]
    explanation: str
