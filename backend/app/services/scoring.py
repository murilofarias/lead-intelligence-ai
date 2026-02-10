"""Hybrid lead scoring: deterministic rules engine + LLM qualitative assessment."""
from __future__ import annotations

from app.models.lead import (
    LeadProfile,
    LLMSignal,
    RuleSignal,
    ScoreBreakdown,
    Tier,
)

# --- Rules engine ------------------------------------------------------------

_ICP_INDUSTRIES = {"saas", "fintech", "ecommerce", "healthtech"}
_TIER1_COUNTRIES = {"US", "CA", "GB", "DE", "FR", "AU", "NL", "SE", "IE"}


def _score_company_size(size: int) -> RuleSignal:
    if size >= 5000:
        return RuleSignal(name="Company size", points=25, detail=f"Enterprise ({size:,} employees)")
    if size >= 1000:
        return RuleSignal(name="Company size", points=22, detail=f"Mid-market ({size:,} employees)")
    if size >= 200:
        return RuleSignal(name="Company size", points=17, detail=f"Growth ({size:,} employees)")
    if size >= 50:
        return RuleSignal(name="Company size", points=10, detail=f"SMB ({size:,} employees)")
    return RuleSignal(name="Company size", points=3, detail=f"Micro ({size:,} employees)")


def _score_industry(industry: str) -> RuleSignal:
    if industry in _ICP_INDUSTRIES:
        return RuleSignal(name="Industry fit", points=25, detail=f"{industry} is in ICP")
    if industry in {"media", "logistics", "education"}:
        return RuleSignal(name="Industry fit", points=12, detail=f"{industry} is adjacent ICP")
    return RuleSignal(name="Industry fit", points=5, detail=f"{industry} is out of ICP")


def _score_revenue(revenue_usd: int) -> RuleSignal:
    if revenue_usd >= 1_000_000_000:
        return RuleSignal(name="Revenue", points=25, detail="$1B+ annual revenue")
    if revenue_usd >= 100_000_000:
        return RuleSignal(name="Revenue", points=20, detail="$100M+ annual revenue")
    if revenue_usd >= 10_000_000:
        return RuleSignal(name="Revenue", points=14, detail="$10M+ annual revenue")
    if revenue_usd >= 1_000_000:
        return RuleSignal(name="Revenue", points=7, detail="$1M+ annual revenue")
    return RuleSignal(name="Revenue", points=2, detail="<$1M annual revenue")


def _score_geography(country: str) -> RuleSignal:
    if country in _TIER1_COUNTRIES:
        return RuleSignal(name="Geography", points=15, detail=f"{country} is tier-1 market")
    return RuleSignal(name="Geography", points=7, detail=f"{country} is tier-2 market")


def _score_source(source: str) -> RuleSignal:
    high = {"referral", "event", "partner"}
    med = {"webinar", "content", "g2"}
    if source in high:
        return RuleSignal(name="Source", points=10, detail=f"{source} converts at >3x baseline")
    if source in med:
        return RuleSignal(name="Source", points=6, detail=f"{source} converts at baseline")
    return RuleSignal(name="Source", points=3, detail=f"{source} converts below baseline")


def run_rules_engine(lead: LeadProfile) -> tuple[float, list[RuleSignal]]:
    """Apply deterministic firmographic rules. Returns (score_0_100, signals)."""
    signals = [
        _score_company_size(lead.company_size),
        _score_industry(lead.industry),
        _score_revenue(lead.annual_revenue_usd),
        _score_geography(lead.country),
        _score_source(lead.source),
    ]
    raw = sum(s.points for s in signals)  # max = 25+25+25+15+10 = 100
    return min(100.0, max(0.0, raw)), signals


# --- Composition -------------------------------------------------------------

RULES_WEIGHT = 0.6
LLM_WEIGHT = 0.4


def _tier(score: float) -> Tier:
    if score >= 80:
        return "hot"
    if score >= 60:
        return "warm"
    if score >= 40:
        return "cool"
    return "cold"


def compose_score(
    lead: LeadProfile,
    llm_score: float,
    llm_signals: list[dict] | list[LLMSignal],
) -> ScoreBreakdown:
    """Combine rules + LLM into a final weighted score with breakdown."""
    rules_score, rule_signals = run_rules_engine(lead)
    final = round(rules_score * RULES_WEIGHT + llm_score * LLM_WEIGHT, 1)

    norm_llm_signals: list[LLMSignal] = [
        s if isinstance(s, LLMSignal) else LLMSignal(**s) for s in llm_signals
    ]

    return ScoreBreakdown(
        rules_score=round(rules_score, 1),
        llm_score=round(llm_score, 1),
        final_score=final,
        tier=_tier(final),
        rule_signals=rule_signals,
        llm_signals=norm_llm_signals,
        rules_weight=RULES_WEIGHT,
        llm_weight=LLM_WEIGHT,
    )
