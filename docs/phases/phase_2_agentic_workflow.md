# Phase 2: Agentic Intelligence & Event-Driven Architecture (Days 8-14)

This phase transitions the system from a basic chatbot to a robust, autonomous agent capable of cyclical reasoning and handling real-world event-driven architectures via AWS.

---

## Day 8 (Sprint 8): LangGraph Setup
*   **Purpose:** Give the agent cyclical reasoning and self-correction capabilities.
*   **Expected Result:** A LangGraph state machine orchestrating the agent's thought process instead of linear LLM chains.
*   **What we are doing:** 
    *   Implementing LangGraph.
    *   Defining distinct nodes for the agent's workflow: `analyze_alert`, `plan_remediation`, `execute_remediation`.
    *   Setting up state objects to pass information (like the Boto3 script and the AWS alert details) between nodes.
*   **Nuances:** Ensuring the graph can loop back on itself (e.g., if `plan_remediation` produces invalid syntax, it loops back to regenerate).

## Day 9 (Sprint 9): AWS EventBridge & Security Hub Integration
*   **Purpose:** Prepare the system for real-world cloud events originating from AWS.
*   **Expected Result:** The system is designed to ingest real AWS EventBridge payloads triggered by AWS Security Hub.
*   **What we are doing:** 
    *   Defining the exact JSON schemas for common AWS Security Hub findings (e.g., public S3 bucket, open security group ports).
    *   Creating an ingestion API endpoint that accurately parses AWS EventBridge payload structures.
*   **Nuances:** Since the real AWS account is pending, we will write a script to simulate these exact AWS EventBridge JSON payloads locally to test the ingestion logic.

## Day 10 (Sprint 10): Agentic Routing & Guardrails
*   **Purpose:** Optimize operational costs and response time while ensuring the safety of the generated code.
*   **Expected Result:** Simple tasks route to fast models; complex code generation routes to heavy reasoning models. Outputs are strictly validated.
*   **What we are doing:** 
    *   Implementing a routing layer in LangGraph.
    *   Using a smaller model (e.g., Gemini 1.5 Flash) for parsing the incoming alert and determining intent.
    *   Routing to a larger model (e.g., Gemini 1.5 Pro) strictly for writing the Boto3 remediation code.
    *   Adding syntax validators to ensure the generated code is valid Python.

## Day 11 (Sprint 11): Enterprise Messaging (SQS/SNS)
*   **Purpose:** Ensure robust, loss-less event delivery, which is critical for enterprise security tools.
*   **Expected Result:** Alerts are queued in an AWS SQS message queue rather than directly hitting the API, preventing dropped alerts during traffic spikes.
*   **What we are doing:** 
    *   Architecting the integration of Amazon SQS.
    *   Designing a background polling worker in FastAPI to consume messages from SQS.
    *   Designing a Dead Letter Queue (DLQ) for malformed alerts that cannot be parsed.
*   **Nuances:** Implementing this using `boto3` locally (or via LocalStack) so it's ready for a real AWS environment.

## Day 12 (Sprint 12): Least-Privilege Remediation via AWS SDK
*   **Purpose:** Safely execute remediations in the target environment using the AWS SDK.
*   **Expected Result:** The agent executes a generated Boto3 script to revert a misconfiguration securely.
*   **What we are doing:** 
    *   Writing the execution engine using `boto3`.
    *   Designing the system so the backend assumes a specific, scoped AWS IAM Role (least privilege) before executing any remediation scripts.
*   **Nuances:** Until the real AWS environment is ready, we will wrap the `boto3` calls in a dry-run/mock layer that validates the syntax and logs the intended action without executing a real cloud mutation.

## Day 13 (Sprint 13): Edge Cases & Error Handling
*   **Purpose:** Ensure the system gracefully handles failures without crashing.
*   **Expected Result:** The agent can self-correct if a generated script fails or escalating to a human if it gets stuck.
*   **What we are doing:** 
    *   Building an error-feedback loop in LangGraph.
    *   If the Boto3 execution simulates a failure (e.g., 'Access Denied'), the error stack trace is passed back to the LLM.
    *   The LLM is prompted to revise its code or escalate.

## Day 14 (Sprint 14): Sprint Review & Refactor
*   **Purpose:** Validate the robust agentic workflow under complex scenarios.
*   **Expected Result:** The agent handles a complex, malformed alert gracefully, and routes correctly.
*   **What we are doing:** 
    *   Conducting a full dry-run of Phase 2 using simulated SQS messages.
    *   Refactoring the SQS messaging worker and LangGraph nodes for maximum modularity.
