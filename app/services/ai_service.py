import os
import json

from google import genai


def generate_ai_response(prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Gemini API key is missing")

    client = genai.Client(api_key=api_key)

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    raw = (response.text or "").strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

    return json.loads(raw)


def generate_email(lead, service, tone, context=None):

    prompt = f"""
    You are a professional B2B sales email writer.

    Generate a personalized sales email.

    COMPANY INFORMATION:

    Company: {lead['company_name']}
    Industry: {lead['industry']}
    Contact: {lead['contact_person']}
    Website: {lead['website']}
    Technology: {lead['technology_stack']}
    Description: {lead['description']}

    OUR SERVICES:
    {service}

    ADDITIONAL CONTEXT:
    {context or "None"}

    EMAIL TONE:
    {tone}

    REQUIREMENTS:

    1. Generate a professional email.
    2. Personalize it based on the company.
    3. Explain how our services may help.
    4. Include a suitable call to action.
    5. Keep it concise.
    6. Do not invent company facts.
    7. Do not claim an unverified business requirement.

    Return ONLY JSON:

    {{
        "subject": "Email subject",
        "body": "Complete email body"
    }}
    """

    result = generate_ai_response(prompt)

    if not result.get("subject") or not result.get("body"):
        raise ValueError("Invalid email response from AI")

    return result


def generate_recommendation(
    lead,
    score,
    priority
):

    prompt = f"""
    You are an AI sales strategy assistant.

    Analyse this prospect and generate an outreach strategy.

    COMPANY:
    {lead['company_name']}

    INDUSTRY:
    {lead['industry']}

    BUSINESS DESCRIPTION:
    {lead['description']}

    LEAD SCORE:
    {score}/100

    PRIORITY:
    {priority}

    Generate:

    1. Communication channel.
    2. Suggested follow-up timing.
    3. Outreach strategy.
    4. Next recommended action.

    Do not invent previous interactions or contact history.

    Return ONLY JSON:

    {{
        "channel": "Email",
        "follow_up_timing": "Within 48 hours",
        "strategy": "Recommended strategy",
        "next_action": "Recommended next action"
    }}
    """

    result = generate_ai_response(prompt)

    required = [
        "channel",
        "follow_up_timing",
        "strategy",
        "next_action"
    ]

    if any(not result.get(key) for key in required):
        raise ValueError("Invalid recommendation response")

    return result