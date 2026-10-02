from models.schemas import CaseFacts, Scheme, EvidenceItem

def check_evidence(facts: CaseFacts, scheme: Scheme) -> list[EvidenceItem]:
    """
    Checks available case facts against required scheme documents.
    """
    available_docs = facts.available_documents
    results = []
    
    for req in scheme.required_documents:
        doc_id = req.document_id
        doc_name = req.name
        source_id = getattr(req, "source_id", "UNKNOWN")
        
        if not doc_id:
            status = "NEEDS_VERIFICATION"
        elif doc_id in available_docs:
            status = "AVAILABLE"
        else:
            status = "MISSING"
            
        results.append(EvidenceItem(
            id=doc_id or "unknown",
            name=doc_name or "Unknown Document",
            status=status,
            source_id=source_id
        ))
        
    return results
