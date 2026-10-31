
import json

from llm import ask_llm
from utils import parse_json_response
from rag import retrieve_knowledge

from tools.monitoring import (
    check_database_status,
    fetch_error_logs,
    check_api_health
)


def analyze_incident(incident: str) -> dict:

    # Retrieve relevant knowledge locally
    knowledge = retrieve_knowledge(incident, top_k=1)

    knowledge_context = "\n".join(
        item["content"][:300] for item in knowledge
    )

    # Collect simulated monitoring data locally
    diagnostic_data = {
        "database": check_database_status(),
        "logs": fetch_error_logs(),
        "api": check_api_health()
    }

    system_prompt = """
You are AegisAI, an enterprise IT incident management system.

Analyze the incident and return ONLY valid JSON.

Return this structure:

{
  "triage": {
    "category": "Database/Network/Application/Security/Other",
    "severity": "Critical/High/Medium/Low",
    "priority": "P1/P2/P3/P4",
    "business_impact": "Short explanation",
    "escalation_required": true,
    "reason": "Classification reason"
  },
  "diagnosis": {
    "root_cause": "Likely cause",
    "evidence": ["Evidence"],
    "affected_service": "Service",
    "confidence": "High/Medium/Low",
    "recommended_investigation": "Next step"
  },
  "resolution": {
    "resolution_summary": "Short summary",
    "immediate_actions": [
      {
        "action": "Action",
        "reason": "Reason",
        "risk": "Low/Medium/High",
        "approval_required": true
      }
    ],
    "preventive_actions": ["Action"],
    "human_approval_required": true,
    "escalation_message": "IT team message"
  }
}

Rules:
- Critical = P1, High = P2, Medium = P3, Low = P4.
- Escalate Critical and High incidents.
- Use monitoring evidence and retrieved knowledge.
- Never invent evidence or claim an action was executed.
- Disruptive actions require human approval.
- Prefer investigation before risky remediation.
"""

    user_prompt = f"""
INCIDENT: {incident}

MONITORING: {json.dumps(diagnostic_data)}

KNOWLEDGE: {knowledge_context}
"""

    response = ask_llm(system_prompt, user_prompt)

    result = parse_json_response(response)

    # Preserve supporting information
    result["diagnosis"]["diagnostic_data"] = diagnostic_data
    result["diagnosis"]["retrieved_knowledge"] = knowledge

    return result
