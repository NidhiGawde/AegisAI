
import json
from llm import ask_llm
from utils import parse_json_response

def triage_incident(incident: str) -> dict:
    system_prompt = """
    You are an expert IT Incident Triage Agent.

    Analyze the incident and classify it.

    Return ONLY valid JSON with these fields:
    {
        "category": "Database / Network / Application / Security / Other",
        "severity": "Critical / High / Medium / Low",
        "priority": "P1 / P2 / P3 / P4",
        "business_impact": "Short explanation",
        "escalation_required": true,
        "reason": "Explain your classification"
    }

    Severity guidelines:
    Critical: Complete production outage or major business disruption.
    High: Major functionality unavailable for many users.
    Medium: Partial functionality affected.
    Low: Minor issue with limited impact.

    Priority mapping:
    Critical = P1
    High = P2
    Medium = P3
    Low = P4

    Escalate all Critical and High incidents.
    """

    result = ask_llm(system_prompt, incident)

    try:
        return parse_json_response(result)
    except json.JSONDecodeError:
        raise ValueError(f"Agent returned invalid JSON: {result}")
