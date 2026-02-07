"""Pydantic models for leads, scores, and explanations."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

Industry = Literal[
    "saas", "fintech", "healthtech", "ecommerce", "manufacturing",
    "media", "education", "logistics", "government", "other",
]

Tier = Literal["hot", "warm", "cool", "cold"]


class LeadProfile(BaseModel):
    """Inbound lead information submitted by forms, APIs, or imports."""

    full_name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    title: str = Field(min_length=1, max_length=120)
    company: str = Field(min_length=1, max_length=120)
    industry: Industry = "other"
    company_size: int = Field(ge=1, le=1_000_000, description="Employee headcount")
    annual_revenue_usd: int = Field(ge=0, description="Annual revenue in USD")
    country: str = Field(default="US", max_length=2)
    source: str = Field(default="website")
    message: str = Field(default="", max_length=4000)


class Lead(LeadProfile):
    id: str
    created_at: datetime


class RuleSignal(BaseModel):
    name: str
    points: float
    detail: str


class LLMSignal(BaseModel):
    name: str
    points: float
    detail: str


class ScoreBreakdown(BaseModel):
    rules_score: float = Field(ge=0, le=100)
    llm_score: float = Field(ge=0, le=100)
    final_score: float = Field(ge=0, le=100)
    tier: Tier
    rule_signals: list[RuleSignal]
    llm_signals: list[LLMSignal]
    rules_weight: float = 0.6
    llm_weight: float = 0.4


class ScoredLead(BaseModel):
    lead: Lead
    breakdown: ScoreBreakdown


class Explanation(BaseModel):
    lead_id: str
    summary: str
    recommended_action: str
    talking_points: list[str]


class SalesforcePushResult(BaseModel):
    lead_id: str
    salesforce_id: str
    pushed_at: datetime
    fixture: bool
