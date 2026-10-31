
import json

from rag import retrieve_knowledge
from llm import ask_llm
from utils import parse_json_response

from tools.monitoring import (
    check_database_status,
    fetch_error_logs,
    check_api_health
)


def diagnose_incident(incident: str, triage_result: dict) -> dict:

    # 1. Retrieve relevant troubleshooting knowledge using RAG
    retrieved_knowledge = retrieve_knowledge(
        incident,
        top_k=1
    )

    knowledge_context = "\n\n".join(
        item["content"]
        for item in retrieved_knowledge
    )

    # 2. Execute diagnostic tools
    database_data = check_database_status()
    error_logs = fetch_error_logs()
    api_data = check_api_health()

    # 3. Collect tool outputs
    diagnostic_data = {
        "database_status": database_data,
        "error_logs": error_logs,
        "api_health": api_data
    }

    # 4. Ask the LLM to analyze the evidence and retrieved knowledge
    system_prompt = """
    You are an expert IT Diagnostic Agent.

    Analyze the incident, triage result, diagnostic data
    and retrieved troubleshooting knowledge.

    Identify the most likely root cause using the available evidence.

    Use retrieved knowledge as supporting reference material.
    Prioritize actual monitoring data and error logs when diagnosing.
    Do not assume that every possible cause in the knowledge base
    is present in this incident.
    Do not invent facts that are not present in the data.

    Return ONLY valid JSON with these fields:

    {
        "root_cause": "Most likely root cause",
        "evidence": ["Evidence 1", "Evidence 2"],
        "affected_service": "Service name",
        "confidence": "High / Medium / Low",
        "recommended_investigation": "Next investigation step"
    }
    """

    user_prompt = f"""
    INCIDENT:
    {incident}

    TRIAGE RESULT:
    {json.dumps(triage_result, indent=2)}

    DIAGNOSTIC TOOL OUTPUT:
    {json.dumps(diagnostic_data, indent=2)}

    RETRIEVED TROUBLESHOOTING KNOWLEDGE:
    {knowledge_context}

    Use this knowledge as supporting reference material.
    Base your diagnosis on the actual evidence.
    """

    result = ask_llm(system_prompt, user_prompt)

    try:
        analysis = parse_json_response(result)
    except (json.JSONDecodeError, ValueError):
        raise ValueError(f"Invalid diagnostic response: {result}")

    # 5. Preserve monitoring evidence and retrieved knowledge
    analysis["diagnostic_data"] = diagnostic_data
    analysis["retrieved_knowledge"] = retrieved_knowledge

    return analysis
