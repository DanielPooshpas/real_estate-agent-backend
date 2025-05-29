# main.py

import os
from fastapi import FastAPI, HTTPException, Depends
from schema import LeadInput, LeadResponse
from llm_router import score_lead
from db import store_lead, fetch_leads
from security import verify_api_key
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.post("/leads", response_model=LeadResponse)
async def create_lead(lead: LeadInput, api_key: str = Depends(verify_api_key)):
    try:
        # Score the lead using LLM
        result = await score_lead(lead)

        # Store the lead in Supabase
        await store_lead(lead, result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads")
async def get_leads(api_key: str = Depends(verify_api_key)):
    try:
        leads = await fetch_leads()
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

