# dashboard.py

import os
import asyncio
import httpx
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = "https://pnpvxufeyjqlprqzbmhv.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBucHZ4dWZleWpxbHBycXpibWh2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNjk0NzM1MiwiZXhwIjoxNzQ4NTIzMzUyfQ.m8G_l4zvPJoKi-K0uGGWI9kIOH2ZVn9EU4a4AsPbA0o"


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
