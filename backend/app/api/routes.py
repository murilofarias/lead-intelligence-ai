"""HTTP routes."""
from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse

from app.core.security import limiter
from app.fixtures.leads import SEED_LEADS, get_lead
from app.models.lead import (
    LeadProfile,
    SalesforcePushResult,
    ScoreBreakdown,
    ScoredLead,
)
from app.services.llm import llm_client
from app.services.salesforce import salesforce_service
from app.services.scoring import compose_score

router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return {"status": "ok", "service": "lead-intelligence-ai"}


@router.get("/leads", response_model=list[ScoredLead])
async def list_leads():
    results: list[ScoredLead] = []
    for lead in SEED_LEADS:
        llm = await llm_client.score_lead(lead, lead_id=lead.id)
        breakdown = compose_score(lead, llm["llm_score"], llm["signals"])
        results.append(ScoredLead(lead=lead, breakdown=breakdown))
    # Hottest first
    results.sort(key=lambda x: x.breakdown.final_score, reverse=True)
    return results


@router.get("/leads/{lead_id}", response_model=ScoredLead)
async def get_lead_detail(lead_id: str):
    lead = get_lead(lead_id)
    if lead is None:
        raise HTTPException(404, "Lead not found")
    llm = await llm_client.score_lead(lead, lead_id=lead.id)
    breakdown = compose_score(lead, llm["llm_score"], llm["signals"])
    return ScoredLead(lead=lead, breakdown=breakdown)


@router.get("/leads/{lead_id}/explain")
@limiter.limit("30/minute")
async def explain_lead(request: Request, lead_id: str):
    lead = get_lead(lead_id)
    if lead is None:
        raise HTTPException(404, "Lead not found")

    async def event_source():
        try:
            async for chunk in llm_client.stream_explanation(lead, lead_id):
                yield {"event": "chunk", "data": json.dumps({"text": chunk})}
            fixture = llm_client.explanation_from_fixture(lead_id)
            yield {"event": "done", "data": fixture.model_dump_json()}
        except asyncio.CancelledError:
            return

    return EventSourceResponse(event_source())


@router.post("/score", response_model=ScoreBreakdown)
@limiter.limit("30/minute")
async def score_profile(request: Request, profile: LeadProfile):
    llm = await llm_client.score_lead(profile)
    return compose_score(profile, llm["llm_score"], llm["signals"])


@router.post("/leads/{lead_id}/push-to-salesforce", response_model=SalesforcePushResult)
@limiter.limit("10/minute")
async def push_to_salesforce(request: Request, lead_id: str):
    lead = get_lead(lead_id)
    if lead is None:
        raise HTTPException(404, "Lead not found")
    return salesforce_service.push_lead(lead)
