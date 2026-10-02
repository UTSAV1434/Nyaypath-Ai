from models.schemas import CaseFacts, SchemeRule, EligibilityResult, Citation

def evaluate_rule(rule: SchemeRule, facts: CaseFacts) -> EligibilityResult:
    """
    Strictly deterministic structural rule evaluator.
    NO eval() is used.
    """
    fact_val = facts.applicant_facts.get(rule.field)
    
    citation = Citation(
        source_id=rule.source_id,
        official_source="Determined by Citations Utility", 
        section=rule.source_section,
        page=rule.source_page
    )

    if fact_val is None:
        return EligibilityResult(
            criterion_id=rule.criterion_id,
            status="UNCERTAIN",
            explanation=f"Required fact '{rule.field}' is missing from applicant facts.",
            citation=citation
        )

    op = rule.operator
    rule_val = rule.value
    
    try:
        if op == "==":
            result = str(fact_val).lower() == str(rule_val).lower()
        elif op == "<=":
            result = float(fact_val) <= float(rule_val)
        elif op == ">=":
            result = float(fact_val) >= float(rule_val)
        elif op == "<":
            result = float(fact_val) < float(rule_val)
        elif op == ">":
            result = float(fact_val) > float(rule_val)
        elif op == "IN":
            result = fact_val in rule_val
        elif op == "NOT_IN":
            result = fact_val not in rule_val
        else:
            return EligibilityResult(
                criterion_id=rule.criterion_id,
                status="UNCERTAIN",
                explanation=f"Unsupported operator '{op}'. Cannot evaluate safely.",
                citation=citation
            )
            
        status = "MET" if result else "NOT_MET"
        return EligibilityResult(
            criterion_id=rule.criterion_id,
            status=status,
            explanation=f"Rule: {rule.field} {op} {rule_val}. Applicant value: {fact_val}.",
            citation=citation
        )
    except Exception as e:
        return EligibilityResult(
            criterion_id=rule.criterion_id,
            status="UNCERTAIN",
            explanation=f"Malformed rule or invalid types during evaluation: {str(e)}",
            citation=citation
        )

def evaluate_scheme(scheme_rules: list[SchemeRule], facts: CaseFacts) -> list[EligibilityResult]:
    results = []
    for rule in scheme_rules:
        results.append(evaluate_rule(rule, facts))
    return results
