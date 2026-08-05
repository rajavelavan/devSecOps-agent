# Phase 4: Infrastructure as Code, CI/CD & Observability (Days 22-28)

This final phase focuses on packaging the application for production, securing the deployment pipeline, and deploying the entire stack using Infrastructure as Code (Terraform) to demonstrate enterprise DevOps maturity.

---

## Day 22 (Sprint 22): Containerization & Security Scanning
*   **Purpose:** Standardize the deployment artifact and ensure container security.
*   **Expected Result:** Dockerfiles for both the frontend and backend, successfully validated by container security scanners.
*   **What we are doing:** 
    *   Writing multi-stage Dockerfiles for the FastAPI backend and MERN/MEAN frontend.
    *   Integrating Trivy (or a similar tool) to scan the generated Docker images for vulnerabilities before they are allowed to be deployed.
*   **Nuances:** Ensuring the Docker images run as non-root users and minimize their attack surface.

## Day 23 (Sprint 23): CI/CD Pipeline (GitHub Actions)
*   **Purpose:** Automate the testing and deployment workflows to ensure code quality and security.
*   **Expected Result:** A GitHub Actions pipeline that lints, tests, and builds the application on every push.
*   **What we are doing:** 
    *   Creating `.github/workflows/main.yml`.
    *   Adding Python unit tests (using `pytest`).
    *   Adding Static Application Security Testing (SAST) tools like Bandit to scan the Python code and block merges if insecure code is detected.

## Day 24 (Sprint 24): Infrastructure as Code (Terraform)
*   **Purpose:** Define the entire cloud environment in code for repeatable, secure, and auditable deployments.
*   **Expected Result:** Terraform scripts capable of standing up the required AWS architecture.
*   **What we are doing:** 
    *   Writing HCL (HashiCorp Configuration Language) scripts to define the AWS infrastructure.
    *   Provisioning AWS ECS (Fargate) for the containers, RDS PostgreSQL, Cognito User Pools, SQS queues, and EventBridge rules.
    *   Defining the specific IAM Roles required for the backend's least-privilege AWS SDK execution.
*   **Nuances:** Designing the Terraform state to be scalable (e.g., using an S3 backend with DynamoDB locking).

## Day 25 (Sprint 25): Enterprise Observability
*   **Purpose:** Gain deep insights into application health and AI agent performance in a production environment.
*   **Expected Result:** Dashboards and alerts configured for latency, error rates, and LLM operational costs.
*   **What we are doing:** 
    *   Integrating OpenTelemetry for distributed tracing.
    *   Setting up tracing to monitor exactly how long LangGraph nodes and LLM API calls take.
    *   Implementing structured JSON logging to ensure logs are easily parsed by centralized logging solutions (e.g., Datadog, AWS CloudWatch).

## Day 26 (Sprint 26): Sprint Review (Production Readiness)
*   **Purpose:** Validate the entire system as if it were a live production environment.
*   **Expected Result:** The system handles simulated load and edge cases seamlessly.
*   **What we are doing:** 
    *   Conducting chaos engineering (e.g., simulating database downtime or IAM permission failures).
    *   Verifying that AWS alerts correctly queue in SQS and that the Dead Letter Queues (DLQs) function as intended when the agent fails.

## Day 27 (Sprint 27): Demo Prep & Presentation
*   **Purpose:** Package the project for showcasing to stakeholders or hiring managers.
*   **Expected Result:** A compelling narrative and presentation demonstrating enterprise maturity.
*   **What we are doing:** 
    *   Recording a seamless end-to-end demo video of the remediation engine in action.
    *   Highlighting the integration of AWS Cognito, Terraform, the autonomous LangGraph workflow, and the immutable audit logs.

## Day 28 (Sprint 28): Final Sign-off
*   **Purpose:** Project completion and portfolio readiness.
*   **Expected Result:** A live, secure URL (or a comprehensive code repository if waiting on a real AWS account) ready for portfolios.
*   **What we are doing:** 
    *   (Future State) Executing `terraform apply` on a real AWS account.
    *   Final verification of the live environment.
    *   Adding the project architecture and live URL/demo to your resume.
