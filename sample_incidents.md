# AegisAI – Sample IT Incidents

Use these sample incidents to test AegisAI's incident triage, diagnosis, knowledge retrieval, resolution recommendations, and human approval workflow.

## 1. Production Database Connection Failures

**Incident:**

Production users are unable to access the application. Requests frequently fail with database connection timeouts. The issue started around 10 minutes ago and is affecting several services that depend on the production database.

## 2. Database Connection Pool Exhaustion

**Incident:**

The application has become intermittently unavailable. Database requests are timing out, and the engineering team suspects that all available database connections are in use. The issue is affecting user login and order processing.

## 3. Slow Application Response Times

**Incident:**

Users report that pages take 15–20 seconds to load. The problem is more noticeable during peak traffic. Some API requests time out, and the support team has received multiple complaints.

## 4. API Request Failures

**Incident:**

The application frontend is loading, but several users receive intermittent errors when submitting requests. API response times have increased, and some requests fail with gateway timeout errors.

## 5. High CPU Utilization

**Incident:**

The production application server is experiencing unusually high CPU utilization. Users report slow page loads, and background jobs are taking longer than normal. The issue began after a recent increase in traffic.

## 6. Network Connectivity Problems

**Incident:**

An internal service is intermittently unable to communicate with the database host. Connection attempts sometimes succeed and sometimes fail. The issue is affecting scheduled jobs and a subset of application requests.

## Suggested Demo Sequence

For a short demonstration:

1. Submit a production database connection failure.
2. Review incident severity and priority.
3. Examine root cause analysis and supporting evidence.
4. Review retrieved knowledge base references.
5. Examine immediate and preventive resolution recommendations.
6. Demonstrate human approval and rejection if requested by the workflow.

## Current Limitations

- Monitoring tools use simulated, predefined infrastructure data.
- The troubleshooting knowledge base is a local Markdown collection.
- The system generates recommendations but does not execute remediation on production infrastructure.
- Incident history is session-based and is not stored in a persistent database.
