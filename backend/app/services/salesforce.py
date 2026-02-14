"""Salesforce integration via simple-salesforce. Fixture mode returns a fake ID."""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from app.core.config import get_settings
from app.core.logging import log
from app.models.lead import Lead, SalesforcePushResult


class SalesforceService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client = None  # lazy

    def _connect(self):
        if self._client is not None:
            return self._client
        from simple_salesforce import Salesforce  # imported lazily

        self._client = Salesforce(
            username=self.settings.salesforce_username,
            password=self.settings.salesforce_password,
            security_token=self.settings.salesforce_token,
        )
        return self._client

    def push_lead(self, lead: Lead) -> SalesforcePushResult:
        if self.settings.fixture_mode:
            fake_id = "00Q" + hashlib.sha1(lead.id.encode()).hexdigest()[:15].upper()
            log.info("salesforce.fixture_push", lead_id=lead.id, sf_id=fake_id)
            return SalesforcePushResult(
                lead_id=lead.id,
                salesforce_id=fake_id,
                pushed_at=datetime.now(timezone.utc),
                fixture=True,
            )

        sf = self._connect()
        payload = {
            "FirstName": lead.full_name.split()[0],
            "LastName": " ".join(lead.full_name.split()[1:]) or lead.full_name,
            "Email": str(lead.email),
            "Title": lead.title,
            "Company": lead.company,
            "Industry": lead.industry,
            "NumberOfEmployees": lead.company_size,
            "AnnualRevenue": lead.annual_revenue_usd,
            "Country": lead.country,
            "LeadSource": lead.source,
        }
        result = sf.Lead.create(payload)  # type: ignore[attr-defined]
        log.info("salesforce.push", lead_id=lead.id, sf_id=result.get("id"))
        return SalesforcePushResult(
            lead_id=lead.id,
            salesforce_id=result["id"],
            pushed_at=datetime.now(timezone.utc),
            fixture=False,
        )


salesforce_service = SalesforceService()
