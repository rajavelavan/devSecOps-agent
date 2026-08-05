# Phase 1: Foundation & Security (Days 1-7)

This phase establishes the foundational API, the initial integration with the LLM logic engine, and the human-in-the-loop user interface. We also introduce enterprise-grade security through Authentication and Role-Based Access Control (RBAC).

---

## Day 1 (Sprint 1): Backend Setup [Completed]
*   **Purpose:** Establish the foundational API that will act as the orchestrator for the entire DevSecOps engine.
*   **Expected Result:** A running FastAPI server capable of receiving and parsing webhook payloads representing security events.
*   **What we are doing:** 
    *   Setting up the Python virtual environment.
    *   Initializing the FastAPI application.
    *   Defining strict Pydantic models for the expected structure of incoming security alerts.
*   **Nuances:** Ensuring the API is highly extensible so that later, when we swap mock webhooks for real AWS SQS messages, the core application logic requires minimal changes.

## Day 2 (Sprint 2): AI Integration [Completed]
*   **Purpose:** Connect the logic engine (LLM) to the backend API.
*   **Expected Result:** The backend can query Gemini, parse intent, and execute a mock tool (e.g., checking an exposed port).
*   **What we are doing:** 
    *   Integrating `langchain_google_genai` to communicate with the Gemini models.
    *   Defining Python functions as tools (e.g., `check_security_group_port`) and binding them to the LLM.
*   **Nuances:** Keeping the tool logic decoupled from the LLM prompt. The tool simulates AWS environment inspection.

## Day 3 (Sprint 3): Frontend Handshake [Completed]
*   **Purpose:** Establish the user interface required for human-in-the-loop approvals.
*   **Expected Result:** A React or Angular dashboard that communicates cleanly with the FastAPI backend.
*   **What we are doing:** 
    *   Building the core UI structure.
    *   Setting up CORS policies in FastAPI.
    *   Creating the "Approve Remediation" button component that dispatches an event to the backend.

## Day 4 (Sprint 4): Streaming Text & Async Processing [Completed]
*   **Purpose:** Ensure the UI feels responsive, real-time, and doesn't suffer from HTTP timeouts during heavy LLM reasoning.
*   **Expected Result:** The dashboard streams the agent's thought process character-by-character as it evaluates a security alert.
*   **What we are doing:** 
    *   Implementing Server-Sent Events (SSE) in FastAPI.
    *   Moving LLM inference to background tasks (e.g., Python `asyncio` background tasks or a task queue) to prevent blocking the main HTTP threads.
*   **Nuances:** Handling connection drops gracefully on the frontend. Ensuring the backend cleans up SSE resources when a client disconnects.

## Day 5 (Sprint 5): Authentication & RBAC (AWS Cognito)
*   **Purpose:** Secure the application for true enterprise deployment.
*   **Expected Result:** Only authenticated administrators can access the dashboard, view sensitive alerts, and approve remediations.
*   **What we are doing:** 
    *   Integrating AWS Cognito User Pools into the frontend application.
    *   Implementing JWT validation middleware on the FastAPI backend.
    *   Adding Role-Based Access Control (RBAC) to ensure only users in an 'Admin' or 'SecurityEngineer' group can trigger the fix execution.
*   **Nuances:** Using OAuth2/OIDC standards. Since the real AWS account is pending, this will involve setting up the Cognito architecture in code (or utilizing local mock JWTs temporarily) to be fully ready for cloud deployment.

## Day 6 (Sprint 6): Sprint Review & End-to-End Test
*   **Purpose:** Validate the entire foundational flow from alert ingestion to secure, authenticated approval.
*   **Expected Result:** A successful E2E test run demonstrating alert ingestion, streaming reasoning, and authenticated human approval.
*   **What we are doing:** 
    *   Triggering a mock webhook.
    *   Watching the UI stream the agent's thought process.
    *   Logging in via AWS Cognito (or mock equivalent) to approve the remediation.
*   **Nuances:** Testing unhappy paths, such as attempting to approve a remediation without an active JWT token, to verify RBAC security.

## Day 7 (Sprint 7): Refactor & Buffer
*   **Purpose:** Consolidate code quality and address technical debt before moving to complex agentic workflows.
*   **Expected Result:** A clean, strictly typed, and well-documented codebase.
*   **What we are doing:** 
    *   Refactoring repetitive code blocks.
    *   Enforcing strict typing on all function signatures and returns.
    *   Adding comprehensive docstrings and comments.
    *   Structuring the repository directories to prepare for LangGraph integration.
