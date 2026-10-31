# 🛡️ AegisAI – AI-Powered IT Incident Management System

**AegisAI** is an AI-powered IT incident management system that automates incident triage, root cause analysis, and resolution recommendations using Azure AI Foundry, LangGraph, and Retrieval-Augmented Generation (RAG).

It combines AI-driven analysis with simulated monitoring tools and human-in-the-loop approval to support structured IT incident management.

🚀 **Live Demo:** https://aegisai-4voxvhmxpysfirewv7h4dn.streamlit.app/

📂 **GitHub Repository:** https://github.com/NidhiGawde/AegisAI

---

## 🎯 Problem Statement

IT teams often spend significant time investigating incidents, identifying their root causes, assessing business impact, and determining appropriate resolutions.

AegisAI aims to streamline this process by using an LLM-powered workflow to analyze incidents, retrieve relevant troubleshooting knowledge, and generate actionable recommendations.

## ✨ Key Features

- **Automated Incident Triage:** Classifies incidents and assigns severity and priority levels.
- **Root Cause Analysis:** Identifies probable causes using incident descriptions, monitoring evidence, and retrieved knowledge.
- **RAG-Based Knowledge Retrieval:** Retrieves relevant troubleshooting information using semantic similarity.
- **Resolution Recommendations:** Generates immediate and preventive actions with associated risks and reasons.
- **Multi-Stage Agentic Workflow:** Uses LangGraph to coordinate triage, escalation, diagnosis, and resolution stages.
- **Human-in-the-Loop Approval:** Pauses the workflow when an action requires human approval and resumes based on the decision.
- **Monitoring Integration:** Uses simulated monitoring tools to provide database status, application health, and error-log information.

## 🏗️ System Architecture

```text
             Incident Description
                      |
                      v
              Incident Analyzer
                      |
          +-----------+-----------+
          |                       |
          v                       v
    RAG Knowledge Base      Monitoring Tools
    (Semantic Search)       (Simulated Data)
          |                       |
          +-----------+-----------+
                      |
                      v
                Azure AI Foundry
                  GPT-4.1-mini
                      |
                      v
             Structured AI Analysis
          (Triage, Diagnosis, Resolution)
                      |
                      v
                LangGraph Workflow
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
        Triage    Escalation  Diagnosis
                                  |
                                  v
                              Resolution
                                  |
                                  v
                         Human Approval
                                  |
                         +--------+--------+
                         |                 |
                       Approve           Reject
                         |                 |
                         +--------+--------+
                                  |
                                  v
                           Final Status
```

The incident analyzer makes a combined Azure LLM request for triage, diagnosis, and resolution analysis. LangGraph then coordinates the workflow stages and approval process.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM | GPT-4.1-mini |
| Cloud AI Platform | Microsoft Azure AI Foundry |
| Agent Workflow | LangGraph |
| RAG | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM Integration | OpenAI Python SDK |
| Frontend | Streamlit |
| Authentication | Azure API Key |
| Version Control | Git, GitHub |

## ⚙️ Project Structure

```text
Aegis-Ai/
│
├── agents/
│   ├── __init__.py
│   ├── incident_analyzer.py
│   ├── triage.py
│   ├── diagnosis.py
│   └── resolution.py
│
├── tools/
│   ├── __init__.py
│   └── monitoring.py
│
├── knowledge_base/
│   └── troubleshooting.md
│
├── tests/
│   ├── test_graph.py
│   └── test_rag.py
│
├── app.py
├── graph.py
├── llm.py
├── rag.py
├── utils.py
├── requirements.txt
├── .env.example
├── .gitignore
└── sample_incidents.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/NidhiGawde/AegisAI.git
cd AegisAI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
AZURE_AI_ENDPOINT=your_azure_ai_endpoint
AZURE_AI_DEPLOYMENT=your_model_deployment_name
AZURE_AI_API_KEY=your_azure_api_key
```

Use your own Azure AI Foundry endpoint, deployment name, and API key. Never commit your `.env` file or expose your API key.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## 🧪 Sample Incidents

The repository includes [`sample_incidents.md`](sample_incidents.md), containing example scenarios for testing AegisAI.

Examples include:

- Production database connection failures
- Database connection pool exhaustion
- Slow application response times
- API request failures
- High CPU utilization
- Network connectivity problems

## 🧠 Workflow and RAG

**Incident Analysis:** The incident analyzer combines the incident description, monitoring information, and retrieved troubleshooting knowledge to generate structured analysis.

**Knowledge Retrieval:** Sentence Transformers generate embeddings from troubleshooting knowledge. Semantic similarity is used to retrieve relevant sections for an incident.

**Workflow Orchestration:** LangGraph manages the sequence of workflow stages, conditional escalation, and human approval using workflow interrupts.

**Human Approval:** When an action requires approval, the workflow pauses until a human approves or rejects the proposed action.

## ⚠️ Current Limitations

- Monitoring tools currently return simulated, predefined infrastructure data rather than connecting to live production systems.
- The troubleshooting knowledge base is a local Markdown collection.
- The system generates recommendations but does not execute remediation on production infrastructure.
- Incident history is maintained within the application session and is not backed by persistent database storage.

## 🔮 Future Improvements

- Integrate real-time monitoring platforms and infrastructure APIs.
- Add persistent incident storage and historical analytics.
- Expand the troubleshooting knowledge base with enterprise documentation.
- Integrate automated remediation with secure approval and execution controls.
- Add authentication and role-based access control.
- Introduce additional specialized agents for deeper investigation and coordination.

## 👩‍💻 Author

**Nidhi Gawde**

[GitHub](https://github.com/NidhiGawde)

---

⭐ If you find this project interesting, feel free to explore the repository and try the live demo!
