"""Tests for the rules engine and score composition."""
from __future__ import annotations

import pytest

from app.models.lead import LeadProfile
from app.services.scoring import (
    LLM_WEIGHT,
    RULES_WEIGHT,
    compose_score,
    run_rules_engine,
)


def make_lead(**overrides) -> LeadProfile:
    base = dict(
        full_name="Test User",
        email="test@example.com",
        title="VP Sales",
        company="Acme",
        industry="saas",
        company_size=1000,
        annual_revenue_usd=200_000_000,
        country="US",
        source="referral",
        message="Ready to buy next quarter.",
    )
    base.update(overrides)
    return LeadProfile(**base)


def test_rules_engine_enterprise_icp_hot():
    lead = make_lead(company_size=10000, annual_revenue_usd=5_000_000_000, industry="fintech")
    score, signals = run_rules_engine(lead)
    assert score >= 80
    assert len(signals) == 5


def test_rules_engine_micro_non_icp_cold():
    lead = make_lead(
        company_size=5, annual_revenue_usd=500_000, industry="other",
        country="ZW", source="website",
    )
    score, signals = run_rules_engine(lead)
    assert score < 40
    assert all(s.points >= 0 for s in signals)


def test_rules_engine_bounds():
    lead = make_lead(company_size=1_000_000, annual_revenue_usd=100_000_000_000)
    score, _ = run_rules_engine(lead)
    assert 0 <= score <= 100


@pytest.mark.parametrize(
    "size,expected_bucket",
    [(5, "Micro"), (75, "SMB"), (300, "Growth"), (2000, "Mid-market"), (9000, "Enterprise")],
)
def test_company_size_buckets(size, expected_bucket):
    lead = make_lead(company_size=size)
    _, signals = run_rules_engine(lead)
    size_signal = next(s for s in signals if s.name == "Company size")
    assert expected_bucket in size_signal.detail


def test_compose_score_weights():
    lead = make_lead()
    rules, _ = run_rules_engine(lead)
    llm_score = 50.0
    signals = [{"name": "Intent", "points": 10, "detail": "ok"}]
    br = compose_score(lead, llm_score, signals)
    expected = round(rules * RULES_WEIGHT + llm_score * LLM_WEIGHT, 1)
    assert br.final_score == expected
    assert br.rules_weight == RULES_WEIGHT
    assert br.llm_weight == LLM_WEIGHT


def test_compose_score_tier_thresholds():
    lead = make_lead(company_size=10000, annual_revenue_usd=5_000_000_000, industry="saas")
    hot = compose_score(lead, 90, [])
    assert hot.tier == "hot"

    cold_lead = make_lead(
        company_size=5, annual_revenue_usd=100_000, industry="other",
        country="ZW", source="website",
    )
    cold = compose_score(cold_lead, 10, [])
    assert cold.tier == "cold"


def test_compose_score_accepts_dict_signals():
    lead = make_lead()
    br = compose_score(lead, 60, [{"name": "x", "points": 5, "detail": "y"}])
    assert br.llm_signals[0].name == "x"
