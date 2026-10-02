from models.schemas import Citation

def format_citation(citation: Citation) -> str:
    """Format a citation object into a human-readable string."""
    parts = [f"Source: {citation.official_source}"]
    if citation.section:
        parts.append(f"Section: {citation.section}")
    if citation.page:
        parts.append(f"Page: {citation.page}")
    return "\n".join(parts)
