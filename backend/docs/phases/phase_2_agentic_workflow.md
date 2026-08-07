# Phase 2: Agentic Intelligence & Event-Driven Architecture (Days 8-14)

This phase transitions the system from a basic chatbot to a robust, autonomous agent capable of cyclical reasoning and handling real-world event-driven architectures via AWS.

---

## Day 8 (Sprint 8): LangGraph Setup [Completed]
* **Purpose:** Give the agent cyclical reasoning and self-correction capabilities.
* **Expected Result:** A LangGraph state machine orchestrating the agent's thought process instead of linear LLM chains.

## Day 9 (Sprint 9): Advanced Tools (The "Hands") [Completed]
* **Purpose:** Give the agent the ability to execute more than just read-only checks.
* **What we are doing:** Expanding `app/agent/tools.py` to include mock remediation tools that simulate Boto3 cloud mutations (e.g., `revoke_security_group_ingress`, `block_public_s3_access`).

## Day 10 (Sprint 10): Dynamic Code Generation & LLM Routing
* **Purpose:** Replace hardcoded scripts with actual Agentic reasoning.
* **What we are doing:** Updating the `plan_remediation` node to actively prompt the LLM to write Python Boto3 code based on the alert, utilizing syntax validation to ensure code safety.

## Day 11 (Sprint 11): Enterprise Ingestion (EventBridge + SQS)
* **Purpose:** Move from synchronous REST webhooks to asynchronous enterprise messaging.
* **What we are doing:** Defining exact JSON schemas for AWS Security Hub and architecting a background polling worker in FastAPI to consume SQS messages.

## Day 12 (Sprint 12): Least-Privilege Execution Layer
* **Purpose:** Safely execute the dynamically generated Boto3 script.
* **What we are doing:** Updating the `execute_remediation` node to safely execute the AI-generated Python code within a restricted, scoped environment.

## Day 13 (Sprint 13): Error Feedback Loop Integration
* **Purpose:** True autonomous self-correction.
* **What we are doing:** Capturing execution errors (e.g., IAM Access Denied) in the state machine and looping back to `analyze_alert` so the LLM can rewrite its code.

## Day 14 (Sprint 14): Sprint 2 Review & E2E Test
* **Purpose:** Validate the complete, autonomous LangGraph loop.
* **What we are doing:** Triggering a complex alert from the UI, forcing the agent to parse, generate code, simulate an error, self-correct, and wait for human approval.
