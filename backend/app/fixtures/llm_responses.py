"""Pre-baked LLM responses for fixture mode.

The streaming path yields these chunks to mimic Claude's output cadence.
"""
from __future__ import annotations

GENERIC_EXPLANATION_CHUNKS: list[str] = [
    "Analyzing lead signals… ",
    "\n\n**Intent signals:** ",
    "The message explicitly references a purchase timeline and names the current vendor, ",
    "which is one of the strongest qualitative indicators of buying intent. ",
    "\n\n**Seniority:** ",
    "The title suggests budget authority and ability to champion the deal internally. ",
    "\n\n**Fit:** ",
    "Company size and industry align with our ICP; firmographic signals are green. ",
    "\n\n**Risk factors:** ",
    "Procurement cycles in this region/industry can extend timelines. ",
    "\n\n**Recommended next step:** ",
    "Route to an AE within 1 business day, include a tailored ROI deck referencing a peer customer.",
]


LLM_QUALITATIVE_FIXTURES: dict[str, dict] = {
    # Keyed by lead id; default provided below.
    "default": {
        "llm_score": 62.0,
        "signals": [
            {"name": "Intent clarity", "points": 22, "detail": "Message names a timeline or vendor comparison."},
            {"name": "Seniority", "points": 18, "detail": "Title implies budget authority."},
            {"name": "Message quality", "points": 12, "detail": "Concrete asks, specific context."},
            {"name": "Channel trust", "points": 10, "detail": "Source channel historically converts."},
        ],
        "summary": "Qualitatively strong inbound lead with clear buying signals and senior decision authority.",
        "recommended_action": "Route to AE within 24h. Prepare ROI narrative and peer case study.",
        "talking_points": [
            "Reference a peer in the same segment who adopted in <30 days.",
            "Lead with security posture (SOC2, SSO) given industry.",
            "Offer a 14-day pilot with success criteria.",
        ],
    },
    "L-0006": {
        "llm_score": 28.0,
        "signals": [
            {"name": "Intent clarity", "points": 6, "detail": "Unsure if product fits."},
            {"name": "Seniority", "points": 8, "detail": "Individual contributor sales manager."},
            {"name": "Message quality", "points": 8, "detail": "Hesitation language ('not sure', 'overkill')."},
            {"name": "Channel trust", "points": 6, "detail": "Website form, unattributed."},
        ],
        "summary": "Small prospect with hesitation — likely not a near-term deal.",
        "recommended_action": "Drop into nurture with SMB-focused content.",
        "talking_points": ["Send SMB case study", "Offer self-serve trial", "Check back in 90 days"],
    },
    "L-0020": {
        "llm_score": 18.0,
        "signals": [
            {"name": "Intent clarity", "points": 4, "detail": "Explicitly no purchasing authority."},
            {"name": "Seniority", "points": 6, "detail": "Individual contributor."},
            {"name": "Message quality", "points": 4, "detail": "Technical curiosity only."},
            {"name": "Channel trust", "points": 4, "detail": "Website, organic."},
        ],
        "summary": "Tire-kicker profile. Technical interest without commercial intent.",
        "recommended_action": "Do not route to sales. Add to developer newsletter.",
        "talking_points": ["Invite to community Slack", "Share technical docs", "Monitor for role change"],
    },
}


def get_llm_fixture(lead_id: str) -> dict:
    return LLM_QUALITATIVE_FIXTURES.get(lead_id, LLM_QUALITATIVE_FIXTURES["default"])
