from pydantic import BaseModel

class LeadInput(BaseModel):
    name: str
    email: str
    message: str
    budget: str
    location: str
    timeline: str

class LeadResponse(BaseModel):
    urgency_score: int
    is_qualified: bool
    followup_message: str
    budget: str
    location: str
    timeline: str
