from graph import incident_graph
from langgraph.types import Command


incident = """
The production database is down.
Users are unable to access the application.
Database connection timeouts are occurring.
"""

config = {
    "configurable": {
        "thread_id": "aegisai-demo-001"
    }
}

# Start workflow
result = incident_graph.invoke(
    {"incident": incident},
    config=config
)

print("\n===== AEGISAI INCIDENT REPORT =====")

print("\nTRIAGE:")
print(result["triage_result"])

print("\nDIAGNOSIS:")
print(result["diagnosis_result"])

print("\nRESOLUTION:")
print(result["resolution_result"])

# Check whether human approval is required
if "__interrupt__" in result:

    print("\n===== HUMAN APPROVAL REQUIRED =====")

    for item in result["__interrupt__"]:
        print(item.value)

    decision = input(
        "\nApprove this action? (yes/no): "
    ).strip().lower()

    approved = decision == "yes"

    # Resume workflow
    result = incident_graph.invoke(
        Command(resume=approved),
        config=config
    )

print("\n===== APPROVAL STATUS =====")
print(result.get("approval_status", "PENDING"))