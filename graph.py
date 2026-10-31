
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver

from agents.incident_analyzer import analyze_incident


class IncidentState(TypedDict, total=False):
    incident: str
    combined_analysis: dict
    triage_result: dict
    diagnosis_result: dict
    resolution_result: dict
    workflow_note: str
    approval_status: str


# 1. Single Azure-powered analysis node
def analysis_node(state: IncidentState):
    result = analyze_incident(state["incident"])

    return {
        "combined_analysis": result
    }


# 2. Triage agent
def triage_node(state: IncidentState):
    return {
        "triage_result": state["combined_analysis"]["triage"]
    }


# 3. Diagnosis agent
def diagnosis_node(state: IncidentState):
    return {
        "diagnosis_result": state["combined_analysis"]["diagnosis"]
    }


# 4. Resolution agent
def resolution_node(state: IncidentState):
    return {
        "resolution_result": state["combined_analysis"]["resolution"]
    }


# 5. Escalation node
def escalation_node(state: IncidentState):
    return {
        "workflow_note": (
            "Priority escalation required. "
            "This incident needs immediate attention."
        )
    }


# 6. Route according to incident severity
def route_after_triage(state: IncidentState):
    severity = state["triage_result"]["severity"]

    if severity in ["Critical", "High"]:
        return "escalation"

    return "diagnosis"


# 7. Human approval node
def approval_node(state: IncidentState):
    resolution = state["resolution_result"]

    risky_actions = [
        action
        for action in resolution["immediate_actions"]
        if action.get("approval_required", False)
    ]

    if not risky_actions:
        return {
            "approval_status": "NOT_REQUIRED"
        }

    decision = interrupt({
        "message": "Human approval required before proceeding.",
        "actions": risky_actions
    })

    return {
        "approval_status": (
            "APPROVED" if decision is True else "REJECTED"
        )
    }


# 8. Build LangGraph workflow
builder = StateGraph(IncidentState)

builder.add_node("analyze", analysis_node)
builder.add_node("triage", triage_node)
builder.add_node("escalation", escalation_node)
builder.add_node("diagnosis", diagnosis_node)
builder.add_node("resolution", resolution_node)
builder.add_node("approval", approval_node)


builder.add_edge(START, "analyze")
builder.add_edge("analyze", "triage")

builder.add_conditional_edges(
    "triage",
    route_after_triage,
    {
        "escalation": "escalation",
        "diagnosis": "diagnosis"
    }
)

builder.add_edge("escalation", "diagnosis")
builder.add_edge("diagnosis", "resolution")
builder.add_edge("resolution", "approval")
builder.add_edge("approval", END)


# 9. Compile graph with memory checkpointing
memory = MemorySaver()

incident_graph = builder.compile(
    checkpointer=memory
)
