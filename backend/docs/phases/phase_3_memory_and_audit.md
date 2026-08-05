# Phase 3: Stateful Memory & Audit Compliance (Days 15-21)

This phase introduces database provisioning to store application state, semantic memory for the AI, and enterprise-grade audit logging to meet strict compliance standards like SOC2.

---

## Day 15 (Sprint 15): Database Provisioning (PostgreSQL)
*   **Purpose:** Establish robust, relational storage for the application state (users, alerts, remediation history).
*   **Expected Result:** A normalized PostgreSQL database schema managed via ORM.
*   **What we are doing:** 
    *   Defining SQLAlchemy models for Alerts, Remediations, and Audit Logs.
    *   Creating database migration scripts using Alembic.
    *   Designing the schema to track the full lifecycle of a security alert (Open -> Investigating -> Pending Approval -> Remediated).
*   **Nuances:** Running PostgreSQL locally via Docker for now. In Phase 4, this will be deployed via Terraform to AWS RDS.

## Day 16 (Sprint 16): Semantic Memory (pgvector)
*   **Purpose:** Give the agent historical context to improve the speed and accuracy of future fixes.
*   **Expected Result:** The agent can query past resolutions using similarity search before generating new code from scratch.
*   **What we are doing:** 
    *   Enabling the `pgvector` extension in the PostgreSQL database.
    *   Generating embeddings (using Gemini Embeddings API) for resolved alerts and storing them.
    *   Adding a `memory_retrieval` tool to the agent's LangGraph toolset.

## Day 17 (Sprint 17): Enterprise Audit Logging
*   **Purpose:** Meet enterprise compliance and security standards by maintaining an indisputable record of system actions.
*   **Expected Result:** An immutable, tamper-evident audit trail of all agent and human actions.
*   **What we are doing:** 
    *   Creating a dedicated audit logging mechanism within the backend.
    *   Logging exactly *who* approved a fix (extracting identity from the Cognito JWT), *what* the AI proposed, and the *exact* Boto3 code executed.
    *   Ensuring these database logs are append-only.

## Day 18 (Sprint 18): UI Polish & Audit Dashboard
*   **Purpose:** Provide enterprise visibility to security administrators.
*   **Expected Result:** A professional dashboard displaying active alerts, the agent's thought process, and an interactive audit history table.
*   **What we are doing:** 
    *   Enhancing the React/Angular UI.
    *   Adding paginated data tables for the audit history.
    *   Implementing summary charts (e.g., "Remediations Completed", "Time to Resolve").

## Day 19 (Sprint 19): Sprint Review (Memory & Audit)
*   **Purpose:** Validate the agent's historical recall capabilities and the integrity of the audit logs.
*   **Expected Result:** The agent correctly references past incidents to solve a new one, and the UI displays the correct audit trail.
*   **What we are doing:** 
    *   Simulating an alert identical to one resolved previously.
    *   Verifying the agent bypasses heavy LLM reasoning by citing the historical fix from `pgvector`.
    *   Verifying the audit log records both the agent's recall and the human approval accurately.

## Day 20 (Sprint 20): Refactor (Vector Optimization)
*   **Purpose:** Ensure database queries remain lightning-fast as the system scales.
*   **Expected Result:** Optimized indexing on the PostgreSQL database for both relational and vector data.
*   **What we are doing:** 
    *   Adding HNSW (Hierarchical Navigable Small World) indexes to `pgvector` columns to speed up similarity searches.
    *   Optimizing standard relational queries using EXPLAIN plans.

## Day 21 (Sprint 21): Refactor (UI Responsiveness)
*   **Purpose:** Ensure a seamless user experience under heavy data load.
*   **Expected Result:** The UI loads instantly and handles high-frequency SSE updates gracefully.
*   **What we are doing:** 
    *   Implementing strict pagination on the frontend audit tables.
    *   Debouncing state updates in the frontend to prevent re-render lag during rapid Server-Sent Events (SSE) streaming.
