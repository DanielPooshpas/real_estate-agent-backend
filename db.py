# db.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

async def store_lead(lead, result):
    payload = {
        "name": lead.name,
        "email": lead.email,
        "message": lead.message,
        "budget": lead.budget,
        "location": lead.location,
        "timeline": lead.timeline,
        "urgency_score": result.urgency_score,
        "is_qualified": result.is_qualified,
        "followup_message": result.followup_message
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/leads",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

async def fetch_leads():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/leads?select=*",
            headers=headers
        )
        response.raise_for_status()
        return response.json()

