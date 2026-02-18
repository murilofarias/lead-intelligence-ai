"""30+ diverse seeded leads used when FIXTURE_MODE=true."""
from __future__ import annotations

from datetime import datetime, timezone

from app.models.lead import Lead

_NOW = datetime(2026, 4, 1, 12, 0, tzinfo=timezone.utc)


def _lead(**kw) -> Lead:
    kw.setdefault("created_at", _NOW)
    return Lead(**kw)


SEED_LEADS: list[Lead] = [
    _lead(id="L-0001", full_name="Ana Ribeiro", email="ana@stripe.com", title="VP Engineering", company="Stripe", industry="fintech", company_size=8000, annual_revenue_usd=14_000_000_000, country="US", source="webinar", message="We're evaluating lead scoring platforms to replace our in-house tool. Need SOC2 and SSO. Timeline: this quarter."),
    _lead(id="L-0002", full_name="Marcus Chen", email="mchen@notion.so", title="Head of RevOps", company="Notion", industry="saas", company_size=900, annual_revenue_usd=250_000_000, country="US", source="g2", message="Interested in trialing for 50 seats. Budget approved for Q2."),
    _lead(id="L-0003", full_name="Priya Shah", email="priya@flipkart.com", title="Director of Growth", company="Flipkart", industry="ecommerce", company_size=22000, annual_revenue_usd=7_500_000_000, country="IN", source="outbound", message="Current Salesforce workflow is slow. Want to see a demo next week."),
    _lead(id="L-0004", full_name="Tomás Álvarez", email="tomas@rappi.com", title="CTO", company="Rappi", industry="logistics", company_size=5000, annual_revenue_usd=1_000_000_000, country="CO", source="referral", message="Referred by a mutual investor. Scaling our sales org from 30 to 120 reps."),
    _lead(id="L-0005", full_name="Sara Johansson", email="sara@klarna.com", title="Lead Data Scientist", company="Klarna", industry="fintech", company_size=6000, annual_revenue_usd=2_000_000_000, country="SE", source="content", message="Curious about your scoring model methodology. Academic interest mostly."),
    _lead(id="L-0006", full_name="Derek Owens", email="derek@acmesprockets.com", title="Sales Manager", company="Acme Sprockets", industry="manufacturing", company_size=45, annual_revenue_usd=6_000_000, country="US", source="website", message="Looking for something simple. Not sure if AI is overkill for us."),
    _lead(id="L-0007", full_name="Lucy Tan", email="lucy@ramp.com", title="VP Sales", company="Ramp", industry="fintech", company_size=1200, annual_revenue_usd=400_000_000, country="US", source="event", message="Met at SaaStr. Ready to pilot with our outbound team (25 reps). Need to close by end of month."),
    _lead(id="L-0008", full_name="Hiroshi Nakamura", email="hiroshi@mercari.jp", title="Product Manager", company="Mercari", industry="ecommerce", company_size=1800, annual_revenue_usd=1_100_000_000, country="JP", source="website", message="Researching options. No specific timeline yet."),
    _lead(id="L-0009", full_name="Emma Clarke", email="emma@monzo.com", title="Head of Marketing Ops", company="Monzo", industry="fintech", company_size=2500, annual_revenue_usd=500_000_000, country="GB", source="linkedin", message="Procurement process takes 6 months here — just starting discovery."),
    _lead(id="L-0010", full_name="Rafael Costa", email="rafael@nubank.com.br", title="Director of Sales Enablement", company="Nubank", industry="fintech", company_size=8000, annual_revenue_usd=5_000_000_000, country="BR", source="outbound", message="Need a demo ASAP. We're replacing 6figr next month."),
    _lead(id="L-0011", full_name="Grace Wu", email="grace@datadoghq.com", title="Senior Account Executive", company="Datadog", industry="saas", company_size=5200, annual_revenue_usd=2_100_000_000, country="US", source="partner", message="Our BDR team needs better lead prioritization. Evaluating 3 vendors."),
    _lead(id="L-0012", full_name="Jonas Weber", email="jonas@sap.com", title="Innovation Lead", company="SAP", industry="saas", company_size=110000, annual_revenue_usd=33_000_000_000, country="DE", source="event", message="Exploring partnerships and potential acquisition targets."),
    _lead(id="L-0013", full_name="Olivia Bennett", email="olivia@shopify.com", title="Growth Engineering", company="Shopify", industry="ecommerce", company_size=10000, annual_revenue_usd=7_000_000_000, country="CA", source="referral", message="Want to integrate with our Plus plan merchants. API-first evaluation."),
    _lead(id="L-0014", full_name="Ahmed Hassan", email="ahmed@careem.com", title="VP of Operations", company="Careem", industry="logistics", company_size=3500, annual_revenue_usd=800_000_000, country="AE", source="outbound", message="Looking to consolidate our MarTech stack. Budget finalized next quarter."),
    _lead(id="L-0015", full_name="Katya Volkov", email="katya@revolut.com", title="Head of Commercial", company="Revolut", industry="fintech", company_size=7000, annual_revenue_usd=1_800_000_000, country="GB", source="event", message="Pilot-ready, 40 seats, want procurement intro this week."),
    _lead(id="L-0016", full_name="Liam O'Brien", email="liam@intercom.com", title="Solutions Engineer", company="Intercom", industry="saas", company_size=900, annual_revenue_usd=300_000_000, country="IE", source="content", message="Reading your blog on hybrid scoring — really thoughtful work."),
    _lead(id="L-0017", full_name="Mei Zhang", email="mei@bytedance.com", title="AI Product Lead", company="ByteDance", industry="media", company_size=150000, annual_revenue_usd=85_000_000_000, country="CN", source="outbound", message="Investigating enterprise LLM products. Very specific compliance needs."),
    _lead(id="L-0018", full_name="Peter Hall", email="peter@smalldental.com", title="Owner", company="Hall Family Dental", industry="healthtech", company_size=6, annual_revenue_usd=900_000, country="US", source="website", message="Do you have something for small practices?"),
    _lead(id="L-0019", full_name="Jessica Park", email="jpark@salesforce.com", title="SVP Revenue", company="Salesforce", industry="saas", company_size=73000, annual_revenue_usd=34_000_000_000, country="US", source="referral", message="Exploring integration partnership for our AppExchange."),
    _lead(id="L-0020", full_name="Nikolai Ivanov", email="nik@yandex.ru", title="Analytics Engineer", company="Yandex", industry="media", company_size=20000, annual_revenue_usd=8_000_000_000, country="RU", source="website", message="Technical evaluation only. No purchasing authority."),
    _lead(id="L-0021", full_name="Chloé Martin", email="chloe@doctolib.fr", title="Director of Sales", company="Doctolib", industry="healthtech", company_size=2500, annual_revenue_usd=350_000_000, country="FR", source="event", message="Rolling out to 180 reps across EU. Need multilingual support."),
    _lead(id="L-0022", full_name="Adeola Adeyemi", email="adeola@flutterwave.com", title="Regional Head", company="Flutterwave", industry="fintech", company_size=900, annual_revenue_usd=200_000_000, country="NG", source="outbound", message="Evaluating 2 vendors. Your pricing vs competitor is our main question."),
    _lead(id="L-0023", full_name="David Kim", email="david@coupang.com", title="VP Sales Strategy", company="Coupang", industry="ecommerce", company_size=80000, annual_revenue_usd=24_000_000_000, country="KR", source="partner", message="RFP going out next month. Would like to be included."),
    _lead(id="L-0024", full_name="Helena Sørensen", email="helena@unity.com", title="Marketing Ops Lead", company="Unity", industry="media", company_size=7000, annual_revenue_usd=2_100_000_000, country="DK", source="g2", message="Team of 12 marketers — we want to self-serve initially."),
    _lead(id="L-0025", full_name="Ravi Krishnan", email="ravi@zoho.com", title="Competitive Intelligence", company="Zoho", industry="saas", company_size=15000, annual_revenue_usd=1_000_000_000, country="IN", source="website", message="Researching competitor features. Not buying."),
    _lead(id="L-0026", full_name="Sofia Greco", email="sofia@satispay.com", title="Chief of Staff", company="Satispay", industry="fintech", company_size=300, annual_revenue_usd=60_000_000, country="IT", source="referral", message="CEO wants to see a demo next week. Growing team fast."),
    _lead(id="L-0027", full_name="Brandon Miller", email="brandon@palantir.com", title="Forward Deployed Engineer", company="Palantir", industry="government", company_size=4000, annual_revenue_usd=2_200_000_000, country="US", source="outbound", message="Security review required before any trial. Air-gapped options?"),
    _lead(id="L-0028", full_name="Isabella Rossi", email="isabella@milano-edu.it", title="Program Director", company="Milano Online Academy", industry="education", company_size=85, annual_revenue_usd=12_000_000, country="IT", source="website", message="Small marketing team, want to qualify inbound faster."),
    _lead(id="L-0029", full_name="Kenji Tanaka", email="kenji@rakuten.com", title="Head of B2B", company="Rakuten", industry="ecommerce", company_size=32000, annual_revenue_usd=16_000_000_000, country="JP", source="event", message="Strategic evaluation. Multi-quarter decision cycle expected."),
    _lead(id="L-0030", full_name="Amelia Nguyen", email="amelia@canva.com", title="VP Revenue Ops", company="Canva", industry="saas", company_size=4500, annual_revenue_usd=2_000_000_000, country="AU", source="referral", message="Ready to move fast. Contract signed at competitor expires in 30 days."),
    _lead(id="L-0031", full_name="Omar Farouk", email="omar@swvl.com", title="Sales Operations Manager", company="Swvl", industry="logistics", company_size=600, annual_revenue_usd=80_000_000, country="EG", source="outbound", message="Post-restructuring, rebuilding our sales stack from scratch."),
    _lead(id="L-0032", full_name="Elena Popescu", email="elena@uipath.com", title="Senior Director, Demand Gen", company="UiPath", industry="saas", company_size=4000, annual_revenue_usd=1_300_000_000, country="RO", source="content", message="Read your case study with Ramp — very relevant to our setup."),
]


def get_lead(lead_id: str) -> Lead | None:
    return next((l for l in SEED_LEADS if l.id == lead_id), None)
