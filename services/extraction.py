import os
from google import genai
from models.schemas import CaseFacts

def extract_case_facts(user_description: str, pdf_text: str) -> CaseFacts:
    """
    Uses Gemini to extract structured facts from natural language.
    Does NOT make eligibility decisions.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        # Return empty mock for testing if no key is set
        return CaseFacts(applicant_facts={})

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Extract the following information into structured facts matching this JSON schema:
    - applicant_facts: object (key value pairs)
    - stated_rejection_reason: string or null
    - application_date: string or null
    - rejection_date: string or null
    - reference_id: string or null
    - available_documents: array of strings

    User Description: {user_description}
    Notice Text: {pdf_text}
    """
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            },
        )
        import json
        data = json.loads(response.text)
        return CaseFacts(**data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Fallback safe behavior
        return CaseFacts(applicant_facts={})
