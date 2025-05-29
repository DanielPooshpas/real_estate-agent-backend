# dashboard.py

import os
import asyncio
import httpx
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# Stop if env vars are missing
if not SUPABASE_URL or not SUPABASE_API_KEY:
    st.error("❌ Missing SUPABASE_URL or SUPABASE_API_KEY. Please set them in your .env file or Streamlit secrets.")
    st.stop()

headers = {
    "apikey": str(SUPABASE_API_KEY),
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
}

async def fetch_leads():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SUPABASE_URL}/rest/v1/leads?select=*", headers=headers)
        response.raise_for_status()
        return response.json()

st.title("🏡 Real Estate Lead Dashboard")

try:
    raw_leads = asyncio.run(fetch_leads())
    df = pd.DataFrame(raw_leads)

    if df.empty:
        st.warning("No leads found.")
    else:
        st.dataframe(df)

except httpx.HTTPStatusError as e:
    st.error(f"HTTP error: {e.response.status_code} – {e.response.text}")
except Exception as e:
    st.error(f"Error loading leads: {e}")
