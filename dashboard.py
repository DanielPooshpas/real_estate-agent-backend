# dashboard.py

import os
import httpx
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

async def fetch_leads():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SUPABASE_URL}/rest/v1/leads?select=*", headers=headers)
        response.raise_for_status()
        return response.json()

st.set_page_config(page_title="🏡 Lead Dashboard", layout="wide")
st.title("🏡 Real Estate Lead Dashboard")

# Fetch data
import asyncio
raw_leads = asyncio.run(fetch_leads())

if not raw_leads:
    st.warning("No leads found.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame([
    {
        "Name": lead["name"],
        "Email": lead["email"],
        "Score": lead["urgency_score"],
        "Qualified": "✅" if lead["is_qualified"] else "❌",
        "Message": lead["message"],
        "Follow-up": lead["followup_message"],
        "Location": lead["location"],
        "Timeline": lead["timeline"]
    }
    for lead in raw_leads
])

# Sidebar Filters
st.sidebar.header("📊 Filters")

# Qualified filter
show_qualified = st.sidebar.checkbox("Show only qualified leads", value=False)
if show_qualified:
    df = df[df["Qualified"] == "✅"]

# Score filter
min_score = st.sidebar.slider("Minimum urgency score", 0, 10, 0)
df = df[df["Score"] >= min_score]

# Search
search_query = st.sidebar.text_input("Search by name, email, or message").lower()
if search_query:
    df = df[df.apply(lambda row: search_query in row["Name"].lower() 
                                      or search_query in row["Email"].lower()
                                      or search_query in row["Message"].lower(), axis=1)]

# Sort
df = df.sort_values(by="Score", ascending=False)

st.success(f"{len(df)} leads shown")

# Display
st.dataframe(df, use_container_width=True)

# Export
st.download_button(
    label="📥 Export to CSV",
    data=df.to_csv(index=False),
    file_name="leads.csv",
    mime="text/csv"
)

