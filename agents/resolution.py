
import json
from llm import ask_llm
from utils import parse_json_response

def resolve_incident(
    incident: str,
    triage_result: dict,
    diagnosis_result: dict
) -> dict:

    system_prompt = """
    You are an expert IT Incident Resolution Agent.

    Your job is to recommend safe, practical remediation steps
    based on the incident, triage result and diagnostic evidence.

    Rules:
    - Never claim that an action has already been executed.
    - Do not invent diagnostic evidence.
    - Prioritize investigation before disruptive actions.
    - Any action that could cause downtime, data loss, or service
      disruption must require human approval.
    - Clearly distinguish immediate actions from preventive actions.

    Return ONLY valid JSON with these fields:

    {
        "resolution_summary": "Short summary",
        "immediate_actions": [
            {
                "action": "Action description",
                "reason": "Why it is needed",
                "risk": "Low / Medium / High",
                "approval_required": true
            }
        ],
        "preventive_actions": ["Action 1", "Action 2"],
        "human_approval_required": true,
        "escalation_message": "Message for the IT operations team"
    }
    """

    user_prompt = f"""
    INCIDENT:
    {incident}

    TRIAGE RESULT:
    {json.dumps(triage_result, indent=2)}

    DIAGNOSTIC RESULT:
    {json.dumps(diagnosis_result, indent=2)}
    """

    result = ask_llm(system_prompt, user_prompt)

    try:
        resolution = parse_json_response(result)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid resolution response: {result}")

    return resolution
