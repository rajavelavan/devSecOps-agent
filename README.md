# DevSecOps AI Engine

This repository hosts a LangGraph-powered autonomous agent for processing AWS security alerts and recommending/executing remediations.

## Project Structure

The project is structured into two main components:

- **frontend/**: A React/Vite web application that provides the user interface.
- **backend/**: A Python FastAPI server that handles webhooks and runs the LangGraph autonomous agent.

### Backend

To start the backend server:

```bash
cd backend
# Make sure your virtual environment is activated
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

To start the frontend dev server:

```bash
cd frontend
npm install
npm run dev
```

## Features
- **LangGraph State Machine**: Processes alerts, formulates remediation plans, and executes them upon human approval.
- **AWS Integration**: Receives webhooks and applies changes securely to AWS resources (e.g. revoking unauthorized security group ingress rules).
- **Web UI**: Real-time feedback and approval flows provided by the frontend.
