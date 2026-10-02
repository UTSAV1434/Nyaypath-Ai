# NyayaPath

NyayaPath is an AI-powered civic action copilot. It helps citizens understand rejected welfare or scholarship applications by extracting facts from rejection notices, allowing the citizen to confirm/edit those facts, and then deterministically checking those facts against a structured knowledge base to generate actionable next steps.

## How it works

1. **Intake**: You upload a text-based rejection notice PDF.
2. **Review**: The system uses a Large Language Model to extract claims from the notice, but requires you to explicitly correct and **confirm** every fact before proceeding. 
3. **Verify**: The confirmed facts are passed through a deterministic Python rule-engine mapping them against the official scheme criteria. (No LLMs are involved in this step).
4. **Evidence & Action**: NyayaPath calculates missing evidence and identifies if formal appeal or grievance routes apply.
5. **Case File & Document**: The system compiles a complete case brief and offers a controlled, professionally formatted appeal document for download.

## Supported Schemes
Currently, NyayaPath only supports structured rules for:
- PM-USP Central Sector Scheme of Scholarship for College and University Students
- Top Class Education for SC Students

## Trust & Safety Model
NyayaPath strictly adheres to a "Language for understanding, Code for deciding" philosophy:
- **No Hallucinations**: Rule evaluations and source citations are strictly pulled from local `.json` scheme data.
- **No Guessing**: Missing information naturally drops to an `UNCERTAIN` state, cascading down to block document generation safely.
- **Transparency**: Every rule features a "Show Me Why" expander to view the exact official citation.

> **Important Limitation**: NyayaPath only supports digital text-based PDFs. It does not perform OCR. It does not provide legal representation, nor does it guarantee government outcomes. Current-year applicability of historical scheme sources may be uncertain.

## Architecture
- **UI Framework**: Streamlit (`app.py` & `ui/views/`)
- **Extraction**: Google Gemini API (`services/pdf_parser.py` & `services/extraction.py`)
- **Knowledge Base**: Structured JSON schemas (`data/schemes/`)
- **Deterministic Engine**: Pure Python (`services/eligibility.py` & `services/verifier.py`)

## Setup & Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Gemini API key:
```bash
# Windows
set GEMINI_API_KEY="your-api-key"
# Mac/Linux
export GEMINI_API_KEY="your-api-key"
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```

## Demo Workflows

### 1. Happy-Path Demo
- Upload a clear rejection notice.
- Edit/confirm the facts.
- Review the deterministic Verification (Show Me Why).
- Review Evidence and Action Plan.
- Generate and download the final Appeal Document.

### 2. Safety Scenario (Insufficient Info)
- Upload a notice missing critical family income data.
- Confirm the incomplete facts.
- Observe Verification explicitly fall into `UNCERTAIN`.
- Proceed to Action Plan and observe the fallback `UNCERTAIN` safety state.
- Proceed to Case File to see the final Trust Status block Document Generation.
