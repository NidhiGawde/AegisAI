
import streamlit as st
import uuid

from graph import incident_graph
from langgraph.types import Command

st.set_page_config(
    page_title="AegisAI | Incident Management",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AegisAI")
st.subheader("Autonomous AI-Powered IT Incident Management")

st.write(
    "Multi-agent system for incident triage, diagnosis, "
    "resolution recommendations and human approval."
)

st.divider()

# Maintain a unique workflow thread for this session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "result" not in st.session_state:
    st.session_state.result = None

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# Incident submission
st.header("Submit an Incident")

incident = st.text_area(
    "Describe the incident",
    placeholder="Example: Production database is down. Users cannot access the application...",
    height=130
)

if st.button("Analyze Incident", type="primary"):

    if incident.strip():

        with st.spinner("AegisAI agents are investigating..."):

            result = incident_graph.invoke(
                {"incident": incident},
                config=config
            )

            st.session_state.result = result

    else:
        st.warning("Please enter an incident description.")


# Display workflow results
result = st.session_state.result

if result:

    st.divider()
    st.header("Incident Analysis Report")

    # TRIAGE
    if "triage_result" in result:

        triage = result["triage_result"]

        st.subheader("1. Incident Triage")

        col1, col2, col3 = st.columns(3)

        col1.metric("Category", triage["category"])
        col2.metric("Severity", triage["severity"])
        col3.metric("Priority", triage["priority"])

        st.write("**Business Impact:**", triage["business_impact"])
        st.write("**Reason:**", triage["reason"])

    # ESCALATION
    if result.get("workflow_note"):

        st.warning(result["workflow_note"])

    # DIAGNOSIS
    if "diagnosis_result" in result:

        diagnosis = result["diagnosis_result"]

        st.subheader("2. Root Cause Diagnosis")

        st.write("**Root Cause:**", diagnosis["root_cause"])
        st.write("**Affected Service:**", diagnosis["affected_service"])
        st.write("**Confidence:**", diagnosis["confidence"])

        st.write("**Supporting Evidence:**")

        for evidence in diagnosis["evidence"]:
            st.write("- ", evidence)

        with st.expander("View Monitoring Data"):
            st.json(diagnosis["diagnostic_data"])

        with st.expander("View Retrieved Knowledge Base References"):

            knowledge = diagnosis.get("retrieved_knowledge", [])

            if knowledge:
                for index, item in enumerate(knowledge, start=1):

                    st.markdown(f"**Knowledge Source {index}**")

                    st.metric("Similarity Score", item["similarity"])

                    st.markdown(item["content"])
                    st.divider()

            else:
                st.info("No relevant knowledge sources were retrieved.")

    # RESOLUTION
    if "resolution_result" in result:

        resolution = result["resolution_result"]

        st.subheader("3. Resolution Recommendations")

        st.write(resolution["resolution_summary"])

        st.write("**Immediate Actions**")

        for action in resolution["immediate_actions"]:

            st.markdown(
                f"**{action['action']}**"
            )

            st.write("Reason:", action["reason"])
            st.write("Risk:", action["risk"])

            if action["approval_required"]:
                st.warning("Human approval required")

        st.write("**Preventive Actions**")

        for action in resolution["preventive_actions"]:
            st.write("- ", action)

    # HUMAN APPROVAL
    interrupts = result.get("__interrupt__", [])

    if interrupts:

        st.divider()
        st.subheader("4. Human Approval Required")

        for item in interrupts:
            st.warning(item.value["message"])

            for action in item.value["actions"]:
                st.write("**Action:**", action["action"])
                st.write("**Risk:**", action["risk"])
                st.write("**Reason:**", action["reason"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Approve Action", type="primary"):

                with st.spinner("Resuming workflow..."):

                    updated_result = incident_graph.invoke(
                        Command(resume=True),
                        config=config
                    )

                    st.session_state.result = updated_result

                st.rerun()

        with col2:
            if st.button("Reject Action"):

                updated_result = incident_graph.invoke(
                    Command(resume=False),
                    config=config
                )

                st.session_state.result = updated_result
                st.rerun()

    elif result.get("approval_status"):

        if result["approval_status"] == "APPROVED":
            st.success("Human approval granted.")

        elif result["approval_status"] == "REJECTED":
            st.error("Human approval rejected.")

        else:
            st.info("Human approval was not required.")

    st.divider()
    st.caption("AegisAI | AI-Powered Incident Management")
