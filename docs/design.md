# NyayaPath Design System

## 1. Design Philosophy
**Core design idea:** UNDERSTAND → VERIFY → ACT

The interface should make a confusing bureaucratic process feel calm, structured and understandable.
The user should always know:
- Where am I?
- What did NyayaPath understand?
- Why did it reach this result?
- What do I need to provide?
- What can I do next?

**Design priorities:**
1. Clarity
2. Trust
3. Calmness
4. Progressive disclosure
5. Actionability

Do NOT optimize for visual complexity.

## 2. Visual Character
The visual direction should be:
Premium, Editorial, Calm, Modern, Trustworthy, Civic, Human.

Avoid making it look:
- corporate SaaS
- government portal
- generic AI chatbot
- generic Streamlit app
- crypto/Web3
- overly futuristic

The product should feel sophisticated without being flashy.

## 3. Color System
Use a restrained palette.
- **Primary**: Deep ink / near-black
- **Background**: Warm off-white or very light neutral
- **Surface**: White
- **Primary accent**: Deep blue / indigo
- **Positive**: Muted green
- **Warning**: Warm amber
- **Conflict**: Muted red
- **Text**: Dark charcoal
- **Secondary text**: Neutral gray

Do not use excessive gradients. Color should communicate meaning.
For example:
- Green: verified / met
- Amber: uncertain
- Red: potential conflict / not met
- Blue: interactive / informational

Do not rely on color alone. Every trust state must also have:
- label
- icon
- text explanation

## 3.1 Visual Tokens
Background: #F7F7F4
Surface: #FFFFFF
Primary / Ink: #111111
Accent: #243B6B
Text: #181818
Muted Text: #6B6B6B
Border: #E5E5E0
Success: #2F6B4F
Warning: #9A6A18
Conflict: #A33A3A

These are starting design tokens, not hard requirements. The visual system should remain restrained and calm. Do NOT introduce excessive gradients, neon colors, or decorative color effects.

## 3.2 Responsive Behavior
Desktop:
- Desktop-first layout
- Centered content
- Approximately 1100–1200px maximum readable content width
- Multi-column layouts allowed where useful

Tablet:
- Reduce horizontal density
- Collapse secondary columns where necessary
- Maintain readable content width

Smaller screens:
- Stack major sections vertically
- Avoid two-column layouts when they become cramped
- Keep primary CTA accessible
- Never create horizontal scrolling

Do not over-engineer mobile behavior for the MVP.

## 3.3 Design Hierarchy
Every screen must have ONE primary action.
- INTAKE → Upload rejection notice
- REVIEW → Confirm information
- VERIFY → Continue verification
- EVIDENCE → Review missing evidence
- ACTION → Follow verified next step
- CASE FILE → Generate document

Secondary information must never visually compete with the primary action. The interface should answer: "What should I do next?" before: "What else can I inspect?"

## 4. Typography
Use a clean modern sans-serif.
- **Display**: Large, confident title
- **H1**: Page title
- **H2**: Section heading
- **Body**: Readable 15–17px equivalent
- **Metadata**: 12–14px
- **Status labels**: Small uppercase or compact labels

Avoid excessive font weights. Use typography to establish hierarchy instead of boxes.

## 5. Layout
Prefer:
- Centered content container
- Maximum readable width
- Generous whitespace
- Strong vertical rhythm

Use a layout roughly equivalent to:
```
┌──────────────────────────────────────┐
│ NyayaPath                  Case      │
├──────────────────────────────────────┤
│                                      │
│ Main content                         │
│                                      │
│                                      │
└──────────────────────────────────────┘
```
Avoid permanently visible sidebars unless they genuinely improve navigation.

## 6. Application Flow
The user journey should be represented as:
01 Intake → 02 Review → 03 Verify → 04 Evidence → 05 Action → 06 Case File

Use a subtle progress indicator. Do not make it look like a complicated enterprise workflow.

## 7. Intake Screen
**Purpose:** Start a case.
**Hero copy:** "Understand what happened. Find out what you can do next."
**Supporting text:** "Upload a rejection notice and NyayaPath will extract the important details, check them against published scheme criteria, and help you identify your next supported action."
**Main interaction:** Large document upload area.
**Secondary:** Text description.
**Optional:** Application/reference ID.
Keep the screen visually sparse.

## 8. Extraction Screen
Show: "Here's what we understood."
Display facts as editable structured fields. Do not overwhelm the user with raw extracted text. Important facts should be visually prioritized.
Include: Edit, Confirm & Continue.
The UI should communicate: "You are in control."

## 9. Human Confirmation
This is a critical trust interaction. Before analysis:
Show: "Review these details before we check the rules."
Explain: "NyayaPath uses these details to evaluate the case. Correct anything that looks wrong."
The user must explicitly confirm. Do not allow accidental bypass.

## 10. Eligibility Screen
Use criterion cards or a clean vertical list.
Example:
> Income requirement
> **MET**
> ₹2.1 lakh ≤ ₹4.5 lakh
> [ Show Me Why ]

Each criterion should communicate: Fact, Rule, Result, Source.
Do not create giant dashboards.

## 11. Show Me Why
This is a signature product interaction. When clicked, reveal:
WHAT WE CHECKED
WHY
RULE
SOURCE
ACADEMIC YEAR
SOURCE STATUS

If the source is historical and current-year applicability is not confirmed, display that explicitly.
Example:
**WHY**: The applicant's reported family income is within the threshold recorded in the cited scheme guidance.
**SOURCE**: PM-USP CSSS FAQ
**ACADEMIC YEAR**: 2025–26
**SOURCE STATUS**: Historical
**CURRENT-YEAR APPLICABILITY**: Uncertain

Never hide this information.

## 12. Trust State Design
- **VERIFIED**: ✓ Icon + label + explanation.
- **UNCERTAIN**: ? Icon + label + explanation.
  *(Example: "We could not confirm that this rule currently applies to the 2026–27 academic year.")*
- **POTENTIAL CONFLICT**: ⚠ Icon + label + explanation.
  *(Example: "PUBLISHED sources contain information that may not agree. We have not treated either version as definitive.")*
- **NOT MET**: ✕ Icon + label + explanation.

**DISTINCTION:**
NOT MET represents the result of evaluating the applicant's facts against a criterion.
POTENTIAL CONFLICT represents uncertainty or inconsistency in source information.
They must NOT look identical. Use both iconography and text, not color alone.

## 13. Rejection Verification
Create a visually distinct section: "Does the rejection reason match the published criteria?"
Display:
- **REJECTION NOTICE**: "The application was rejected because..."
- **MATCHED CRITERION**: Family income
- **ASSESSMENT**: CONSISTENT or POTENTIAL CONFLICT
- Then: [ Show Me Why ]

The UI should emphasize that NyayaPath is comparing—not acting as a judge.

## 14. Evidence Screen
**Title:** "What you have — and what's missing"
**Use:** ✓ Available, ○ Missing, ? Needs verification
Each item: Document, Status, Why it matters, Source.
This should feel like a checklist, not a spreadsheet.

## 15. Action Plan
This is the most actionable screen.
**Headline:** "Here's what you can do next."
**Show:**
1. Route
2. Why
3. Authority
4. Deadline if verified
5. Evidence needed
6. Immediate next step

*(Example: GRIEVANCE. Your rejection reason may be reviewable through the scheme's documented grievance mechanism. Authority: [authority]. Deadline: Not verified. Next step: Prepare the listed evidence and submit the grievance through the official route.)*

## 16. Case File
The Case File is the culmination of the experience. It should feel like a professional case summary.

**NEXT ACTION** must be visually more prominent than the other sections. The user should immediately understand:
- What route is available
- Why it is available
- What evidence is needed
- What authority is involved
- What deadline is verified, if any
- What the immediate next step is

Eligibility and rejection analysis remain important, but the Case File should ultimately be action-oriented.

Structure:
- NYAYAPATH CASE FILE / Case ID
- CASE SUMMARY (Applicant, Scheme, Application, Rejection)
- ELIGIBILITY (Criterion, Result, Source)
- REJECTION VERIFICATION (Status, Reason, Evidence)
- EVIDENCE (Available, Missing, Needs verification)
- **NEXT ACTION (Visually Prominent)** (Route, Authority, Deadline, Next step)
- SOURCES (Official references)
- DOCUMENT (Generate / Download)

## 17. Document Generation UI
**Use a clear CTA:** Generate document
**After generation:** Document ready
**Show:** Document type, Generated from verified case information, Route used, Source status.
Do not imply legal certification.

## 18. Component Style
- **Cards**: Subtle border, Small radius, Minimal shadow.
- **Buttons**:
  - Primary: Strong dark/blue button
  - Secondary: Outlined
  - Danger/conflict: Reserved for actual conflicts
- Avoid rounded-everything design.
- Avoid excessive glassmorphism.

## 19. Iconography
Use a consistent icon system. Icons should communicate: Document, Check, Warning, Conflict, Search, Evidence, Action, Source, Edit, Download.
Never use icons purely as decoration when text can communicate better.

## 20. Motion
Use subtle transitions only (e.g., Step transition, Fact confirmation, Status reveal, Expand/collapse "Show Me Why").
Do NOT add distracting animations. The experience should feel calm.

## 21. Responsive Design
Design for Desktop first, but ensure Tablet and Smaller desktop windows remain usable. Do not create horizontal scrolling.

## 22. Accessibility
Required: Keyboard-accessible interactions where possible, Clear focus states, Sufficient contrast, Status labels not dependent only on color, Readable body text, Clear error messages.

## 23. Empty / Error States
Errors should explain: What happened, Why, What the user can do.
*(Example: "NyayaPath couldn't extract readable text from this PDF. This MVP supports digital PDFs, but not scanned/image-only documents. Try uploading a text-based PDF.")*
Do not show raw stack traces.

## 24. Product Language
Use plain language.
Prefer "What's next?" instead of "Action Plan Resolution".
Prefer "What we checked" instead of "Eligibility Evaluation Results".
Prefer "Why?" instead of "Evidence provenance".
Prefer "Needs verification" instead of "Insufficient confidence".
The product is for citizens, not developers.

## 25. Design Non-Goals
Do NOT create: Generic chatbot UI, Giant analytics dashboard, Excessive glassmorphism, Neon AI aesthetic, Government-portal imitation, Dense admin panels, Decorative animations, Unnecessary navigation, Excessive cards, Fake metrics, Fake testimonials, Fake government branding.

## 26. Final Design Principle
Every screen should answer one question:
- INTAKE: "What happened?"
- REVIEW: "Did NyayaPath understand me correctly?"
- VERIFY: "Does the rejection match the rules?"
- EVIDENCE: "What do I have and what am I missing?"
- ACTION: "What can I do next?"
- CASE FILE: "What is the complete picture?"

The user should never feel lost.

## 27. UI Implementation Rule
The UI must consume the existing backend services.
Do not duplicate business logic in UI components. Do not create fake UI states that the backend cannot produce. Every visible VERIFIED, UNCERTAIN, POTENTIAL CONFLICT, MET, NOT MET state must correspond to an actual backend result.

---
*These documents are the design and architecture source of truth for NyayaPath. Any implementation change that materially affects architecture, trust behavior, or user experience should update these documents.*
