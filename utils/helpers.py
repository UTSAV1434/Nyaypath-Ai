import json
import os
from models.schemas import Scheme

def load_scheme_by_name(name: str) -> Scheme:
    """Loads a scheme from the knowledge_base based on the display name."""
    mapping = {
        "PM-USP CSSS": "pm_usp_csss.json",
        "Top Class Education for SC Students": "top_class_sc.json"
    }
    filename = mapping.get(name)
    if not filename:
        raise ValueError(f"Unknown scheme name: {name}")
        
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "schemes", filename)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Scheme(**data)
