from schema import LeadInput, LeadResponse

async def score_lead(lead: LeadInput) -> LeadResponse:
    message = lead.message.lower()
    timeline = lead.timeline.lower()

    # Basic urgency scoring
    urgency_keywords = ["asap", "urgent", "immediately", "soon", "next week", "2 weeks"]
    urgency_score = sum(1 for word in urgency_keywords if word in message or word in timeline)

    is_qualified = (
        urgency_score > 0 and
        "$" in lead.budget and
        len(lead.location.strip()) > 0
    )

    followup_message = (
        "Great! Let’s schedule a showing this week." if is_qualified
        else "Thanks for reaching out. Can you tell us more about your needs?"
    )

    return LeadResponse(
        urgency_score=urgency_score,
        is_qualified=is_qualified,
        followup_message=followup_message,
        budget=lead.budget,
        location=lead.location,
        timeline=lead.timeline
    )

